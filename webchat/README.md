# WebChat Demo

A minimal ChatGPT-style text chat demo built with Node.js, TypeScript, Express, Vite, and React.

## Setup

Install dependencies:

```bash
npm install
```

For Vertex AI, put these values in the repository root `.env` file:

```env
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=global
GEMINI_MODEL=gemini-3-flash-preview
```

Make sure local Google Cloud application credentials are available, for example through `gcloud auth application-default login`.

For Gemini API key mode instead, set `GOOGLE_GENAI_USE_VERTEXAI=False` and provide `GEMINI_API_KEY`.

Run frontend and backend together:

```bash
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

The browser calls Vite at port `5173`, and Vite proxies `/api/chat` to the local Express backend at `http://127.0.0.1:8787`.
