import * as fs from "fs/promises";
import { createClient } from "@supabase/supabase-js";
import { chatComplete } from "../services/ai/ghmodels_client";
import * as puppeteer from "puppeteer";

const SUPABASE_URL = process.env.SUPABASE_URL!;
const SUPABASE_SERVICE_ROLE = process.env.SUPABASE_SERVICE_ROLE!;
const MODEL = process.env.AUDITORIA_MODEL ?? "openai/gpt-4.1";

// 1) Busca os dados dos Workspaces no Supabase
async function fetchWorkspaces() {
  const sb = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE, {
    auth: { persistSession: false },
  });

  // CORRIGIDO: Busca da tabela "workspaces"
  const { data, error } = await sb.from("workspaces").select("*").limit(50);
  if (error) throw error;
  return data ?? [];
}

// 2) Gera o conteúdo do relatório com a IA
async function gerarSumario(dados: any) {
  const input = JSON.stringify(dados, null, 2);
  const resp = await chatComplete({
    model: MODEL,
    messages: [
      {
        role: "system",
        content:
          "Você é um auditor sênior. Responda em português de forma objetiva, criando um relatório em Markdown.",
      },
      {
        role: "user",
        content: `Gere um sumário executivo e um plano de ação para o workspace com os seguintes dados:\n${input}`,
      },
    ],
    max_tokens: 4000,
  });
  return resp.choices?.[0]?.message?.content ?? "Nenhuma resposta gerada.";
}

// 3) Monta um HTML e renderiza o PDF
async function salvarPdf(
  workspaceTitle: string,
  createdAt: string,
  conteudo: string
) {
  const dataFormatada = new Date(createdAt).toLocaleDateString("pt-BR");
  const html = `<!doctype html><html><head><meta charset="utf-8"><title>Relatório</title>
  <style>body{font-family:Arial,sans-serif;line-height:1.4;padding:24px} h1,h2{margin:0 0 8px}
  .tag{display:inline-block;padding:4px 8px;border-radius:8px;border:1px solid #ddd}</style></head>
  <body><h1>Relatório de Auditoria</h1>
  <div class="tag">${workspaceTitle} • Criado em: ${dataFormatada}</div><hr/>
  <pre style="white-space: pre-wrap; word-wrap: break-word;">${conteudo.replace(/</g, "&lt;")}</pre></body></html>`;

  const outDir = "artifacts/relatorios";
  await fs.mkdir(outDir, { recursive: true });
  const safeTitle = workspaceTitle.replace(/[^a-z0-9]/gi, "_").toLowerCase();
  const tmpHtmlPath = `/tmp/${safeTitle}.html`;
  const pdfPath = `${outDir}/${safeTitle}.pdf`;
  await fs.writeFile(tmpHtmlPath, html, "utf8");

  const browser = await puppeteer.launch({ args: ["--no-sandbox"] });
  const page = await browser.newPage();
  await page.goto("file://" + tmpHtmlPath, { waitUntil: "networkidle0" });
  await page.pdf({ path: pdfPath, format: "A4", printBackground: true });
  await browser.close();
}

async function main() {
  const workspaces = await fetchWorkspaces();
  for (const ws of workspaces) {
    // CORRIGIDO: Usa ws.title e ws.created_at, que existem na sua tabela
    const texto = await gerarSumario(ws);
    await salvarPdf(ws.title, ws.created_at, texto);
    console.log(`Relatório gerado para o workspace: ${ws.title}`);
  }
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
