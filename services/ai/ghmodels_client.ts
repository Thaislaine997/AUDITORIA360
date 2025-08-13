import { Readable } from "stream";

const MODELS_URL = process.env.GH_MODELS_BASE ?? "https://models.github.ai";
const ORG = process.env.GH_MODELS_ORG; // Opcional: envia para /orgs/{org}

type Msg = { role: "system" | "user" | "assistant"; content: string };

export async function chatComplete(opts: {
  messages: Msg[];
  model: string;
  max_tokens?: number;
  temperature?: number;
  stream?: boolean;
}) {
  const token = process.env.GITHUB_TOKEN;
  if (!token)
    throw new Error(
      "GITHUB_TOKEN ausente (fornecido automaticamente no Actions)"
    );

  const path = ORG
    ? `/orgs/${ORG}/inference/chat/completions`
    : `/inference/chat/completions`;

  const res = await fetch(`${MODELS_URL}${path}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
    },
    body: JSON.stringify({
      model: opts.model,
      messages: opts.messages,
      max_tokens: opts.max_tokens,
      temperature: opts.temperature ?? 0.2,
      stream: !!opts.stream,
    }),
  });

  if (!res.ok)
    throw new Error(`GH Models erro: ${res.status} ${await res.text()}`);
  return await res.json();
}
