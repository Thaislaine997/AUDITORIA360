// supabase/functions/processar-pdf/index.ts

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// Esta é uma implementação básica de processamento de PDF
// Em produção, você pode usar bibliotraries como pdf-parse ou similares
async function extrairTextoPDF(fileBuffer: Uint8Array): Promise<string> {
  // Placeholder para extração real de texto do PDF
  // Para implementação completa, use uma biblioteca como pdf2pic + OCR ou pdf-parse

  // Por enquanto, retornamos um texto de exemplo para demonstração
  const textoExemplo = `
    PORTARIA Nº 123/2024
    
    Art. 1º Fica estabelecido o valor do salário mínimo nacional em R$ 1.550,00 (um mil, quinhentos e cinquenta reais), 
    vigente a partir de 1º de janeiro de 2024.
    
    Art. 2º As alíquotas de contribuição para o INSS ficam estabelecidas da seguinte forma:
    I - 7,5% (sete vírgula cinco por cento) para salários de até R$ 1.412,00;
    II - 9% (nove por cento) para salários de R$ 1.412,01 até R$ 2.666,68;
    III - 12% (doze por cento) para salários de R$ 2.666,69 até R$ 4.000,03;
    IV - 14% (quatorze por cento) para salários acima de R$ 4.000,03.
    
    Art. 3º O valor do salário família fica estabelecido em R$ 59,82 (cinquenta e nove reais e oitenta e dois centavos) 
    para dependentes de segurados com remuneração mensal de até R$ 1.819,26.
  `;

  console.log(
    "AVISO: Usando texto de exemplo para demonstração. Em produção, implemente extração real de PDF."
  );
  return textoExemplo.trim();
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

    // Processar multipart/form-data para arquivos
    const formData = await req.formData();
    const file = formData.get("file") as File;

    if (!file) {
      throw new Error("Nenhum arquivo PDF foi fornecido");
    }

    console.log(`Processando arquivo: ${file.name} (${file.size} bytes)`);

    // 1. Validar se é um PDF
    if (
      !file.type.includes("pdf") &&
      !file.name.toLowerCase().endsWith(".pdf")
    ) {
      throw new Error("O arquivo deve ser um PDF");
    }

    // 2. Ler o arquivo
    const fileBuffer = new Uint8Array(await file.arrayBuffer());

    // 3. Extrair texto do PDF
    console.log("Extraindo texto do PDF...");
    const textoExtraido = await extrairTextoPDF(fileBuffer);

    if (!textoExtraido || textoExtraido.trim().length === 0) {
      throw new Error("Não foi possível extrair texto do PDF");
    }

    // 4. Criar registro na tabela Documentos
    console.log("Criando registro na base de dados...");
    const { data: docRecord, error: insertError } = await supabaseAdmin
      .from("Documentos")
      .insert({
        nome: file.name,
        texto_extraido: textoExtraido,
        status: "PROCESSANDO",
      })
      .select()
      .single();

    if (insertError) {
      console.error("Erro ao criar documento:", insertError);
      throw new Error(`Erro ao salvar documento: ${insertError.message}`);
    }

    console.log(`Documento criado com ID: ${docRecord.id}`);

    // 5. Atualizar status para CONCLUIDO
    const { error: updateError } = await supabaseAdmin
      .from("Documentos")
      .update({ status: "CONCLUIDO" })
      .eq("id", docRecord.id);

    if (updateError) {
      console.error("Erro ao atualizar status:", updateError);
      throw updateError;
    }

    // 6. NOVO: Chamar a próxima função na nossa linha de montagem
    console.log("Enviando para análise de IA...");
    const { data: invokeData, error: invokeError } =
      await supabaseAdmin.functions.invoke("analisar-texto-com-ia", {
        body: { record: docRecord },
      });

    if (invokeError) {
      console.error("Erro ao chamar função de IA:", invokeError);
      // Não falha completamente - o PDF foi processado, apenas a IA falhou
      console.warn("Documento processado mas análise de IA falhou");
    } else {
      console.log("Análise de IA executada com sucesso:", invokeData);
    }

    // 7. Retornar sucesso
    return new Response(
      JSON.stringify({
        message: `Documento ${file.name} processado e enviado para análise de IA.`,
        documentoId: docRecord.id,
        textoExtraido: textoExtraido.substring(0, 200) + "...", // Apenas preview
      }),
      {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
        status: 200,
      }
    );
  } catch (err) {
    console.error("Erro na função processar-pdf:", err);
    return new Response(
      JSON.stringify({
        error: String(err?.message ?? err),
        message: "Falha no processamento do PDF",
      }),
      {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  }
});
