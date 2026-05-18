import path from "node:path";
import { fileURLToPath } from "node:url";
import cors from "cors";
import dotenv from "dotenv";
import express from "express";
import { GoogleGenAI } from "@google/genai";

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.resolve(__dirname, "../../.env") });
dotenv.config({ path: path.resolve(__dirname, "../.env") });

const app = express();
const port = Number(process.env.PORT ?? 8787);
const model = process.env.GEMINI_MODEL ?? "gemini-3-flash-preview";
const useVertexAi = parseBoolean(process.env.GOOGLE_GENAI_USE_VERTEXAI);
const project = process.env.GOOGLE_CLOUD_PROJECT;
const location = process.env.GOOGLE_CLOUD_LOCATION;

app.use(cors({ origin: true }));
app.use(express.json({ limit: "1mb" }));

const apiKey = process.env.GEMINI_API_KEY;
const ai = createGenAiClient();

app.get("/api/health", (_req, res) => {
  res.json({
    ok: Boolean(ai),
    model,
    authMode: useVertexAi ? "vertexai" : "gemini-api-key",
    project: project ? maskValue(project) : null,
    location: location ?? null,
    hasGeminiApiKey: Boolean(apiKey)
  });
});

app.post("/api/chat", async (req, res) => {
  const messages = normalizeMessages(req.body?.messages);

  if (!messages.length) {
    return res.status(400).json({ error: "messages is required" });
  }

  if (!ai) {
    return res.status(500).json({
      error:
        "No GenAI auth configured. Set GOOGLE_GENAI_USE_VERTEXAI=True with Google Cloud credentials, or set GEMINI_API_KEY."
    });
  }

  try {
    const contents = messages
      .map((message) => `${message.role === "user" ? "User" : "Assistant"}: ${message.content}`)
      .join("\n\n");

    const response = await ai.models.generateContent({
      model,
      contents: [
        "You are a helpful, concise chatbot. Reply in the same language as the user when appropriate.",
        contents
      ].join("\n\n")
    });

    res.json({ reply: response.text ?? "" });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    res.status(500).json({ error: message });
  }
});

app.listen(port, "127.0.0.1", () => {
  console.log(`WebChat API listening on http://127.0.0.1:${port}`);
});

function normalizeMessages(value: unknown): ChatMessage[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value
    .filter((item): item is ChatMessage => {
      return (
        typeof item === "object" &&
        item !== null &&
        ((item as ChatMessage).role === "user" || (item as ChatMessage).role === "assistant") &&
        typeof (item as ChatMessage).content === "string"
      );
    })
    .map((item) => ({
      role: item.role,
      content: item.content.trim()
    }))
    .filter((item) => item.content.length > 0)
    .slice(-20);
}

function createGenAiClient(): GoogleGenAI | null {
  if (useVertexAi) {
    return new GoogleGenAI({
      vertexai: true,
      project,
      location
    });
  }

  if (apiKey) {
    return new GoogleGenAI({ apiKey });
  }

  return null;
}

function parseBoolean(value: string | undefined): boolean {
  return ["1", "true", "yes", "on"].includes((value ?? "").trim().toLowerCase());
}

function maskValue(value: string): string {
  if (value.length <= 8) {
    return "configured";
  }

  return `${value.slice(0, 6)}...${value.slice(-4)}`;
}
