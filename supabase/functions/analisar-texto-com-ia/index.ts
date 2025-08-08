// supabase/functions/analisar-texto-com-ia/index.ts

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// Função para comunicar com a API da IA (ex: Google Gemini, OpenAI GPT)
// NOTA: Precisará de uma chave de API para o serviço de IA escolhido.
async function chamarModeloIA(texto: string): Promise<any> {
  // Placeholder para a chamada à API de IA.
  // Substitua pela implementação real do seu modelo de preferência (Gemini, etc.)
  const GEMINI_API_KEY = Deno.env.get("GEMINI_API_KEY")!;

  if (!GEMINI_API_KEY) {
    throw new Error("GEMINI_API_KEY não configurada nos segredos do projeto");
  }

  const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${GEMINI_API_KEY}`;

  const prompt = `
    Você é um assistente de contabilidade especialista em legislação trabalhista do Brasil.
    Analise o seguinte texto de um documento oficial e extraia TODOS os parâmetros quantificáveis relevantes para a folha de pagamento.
    Os parâmetros incluem, mas não se limitam a: alíquotas de INSS, faixas de IRRF, valor do salário mínimo, valor do salário família, limites, etc.
    Sua resposta DEVE ser um objeto JSON válido, contendo uma única chave "parametros", que é uma lista de objetos.
    Cada objeto na lista deve ter EXATAMENTE as seguintes chaves: "nome_parametro", "valor_parametro", "tipo_valor", "contexto_original".

    Exemplo de formato de resposta:
    {
      "parametros": [
        {
          "nome_parametro": "aliquota_inss_faixa_1",
          "valor_parametro": "7.5",
          "tipo_valor": "percentual",
          "contexto_original": "A alíquota para a primeira faixa salarial é de 7,5%."
        },
        {
          "nome_parametro": "valor_salario_minimo_nacional",
          "valor_parametro": "1550.00",
          "tipo_valor": "moeda",
          "contexto_original": "Fica estabelecido o salário mínimo de R$ 1.550,00 a partir de Janeiro."
        }
      ]
    }

    Texto para análise:
    ---
    ${texto}
    ---
  `;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
    });

    if (!response.ok) {
      throw new Error(`Erro na API de IA: ${response.statusText}`);
    }

    const data = await response.json();

    // O texto da resposta da IA está dentro de uma estrutura complexa
    if (
      !data.candidates ||
      !data.candidates[0] ||
      !data.candidates[0].content
    ) {
      throw new Error("Resposta da API de IA em formato inesperado");
    }

    const jsonText = data.candidates[0].content.parts[0].text
      .replace(/```json|```/g, "")
      .trim();
    return JSON.parse(jsonText);
  } catch (error) {
    console.error("Erro ao processar resposta da IA:", error);
    throw new Error(`Falha na análise de IA: ${error.message}`);
  }
}

serve(async req => {
  const corsHeaders = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers":
      "authorization, x-client-info, apikey, content-type",
  };

  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabaseAdmin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

    const { record: documento } = await req.json();

    if (!documento || !documento.texto_extraido) {
      throw new Error("Documento ou texto extraído não fornecido");
    }

    console.log(`Iniciando análise de IA para documento ID: ${documento.id}`);

    // 1. Chamar a IA com o texto extraído
    const respostaIA = await chamarModeloIA(documento.texto_extraido);
    const parametrosExtraidos = respostaIA.parametros;

    if (!parametrosExtraidos || parametrosExtraidos.length === 0) {
      console.log("IA não encontrou parâmetros para extrair.");
      return new Response(
        JSON.stringify({
          message: "IA não encontrou parâmetros para extrair.",
        }),
        {
          status: 200,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    console.log(`IA extraiu ${parametrosExtraidos.length} parâmetros`);

    // 2. Preparar os dados para inserção na tabela ParametrosLegais
    const dadosParaInserir = parametrosExtraidos.map((p: any) => ({
      documento_id: documento.id,
      nome_parametro: p.nome_parametro,
      valor_parametro: p.valor_parametro,
      tipo_valor: p.tipo_valor,
      contexto_original: p.contexto_original,
      // TODO: A IA também poderia extrair a data de vigência
    }));

    // 3. Inserir os parâmetros extraídos na base de dados
    const { error: insertError } = await supabaseAdmin
      .from("ParametrosLegais")
      .insert(dadosParaInserir);

    if (insertError) {
      console.error("Erro ao inserir parâmetros:", insertError);
      throw insertError;
    }

    console.log(
      `${parametrosExtraidos.length} parâmetros inseridos com sucesso`
    );

    return new Response(
      JSON.stringify({
        message: `${parametrosExtraidos.length} parâmetros extraídos e guardados.`,
        parametros: parametrosExtraidos.map(p => p.nome_parametro),
      }),
      {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
        status: 200,
      }
    );
  } catch (err) {
    console.error("Erro na função analisar-texto-com-ia:", err);
    return new Response(
      JSON.stringify({
        error: String(err?.message ?? err),
        message: "Falha na análise de texto com IA",
      }),
      {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  }
});
