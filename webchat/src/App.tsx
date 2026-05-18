import { FormEvent, useMemo, useRef, useState } from "react";

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

function createStarterMessages(): ChatMessage[] {
  return [{
    id: crypto.randomUUID(),
    role: "assistant",
    content: "你好，我是这个 demo 的聊天助手。发一句话试试。"
  }];
}

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>(createStarterMessages);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);

  const canSend = useMemo(() => input.trim().length > 0 && !isSending, [input, isSending]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const text = input.trim();
    if (!text || isSending) {
      return;
    }

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: text
    };

    const nextMessages = [...messages, userMessage];
    setMessages(nextMessages);
    setInput("");
    setError(null);
    setIsSending(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: nextMessages.map(({ role, content }) => ({ role, content }))
        })
      });

      const data = (await response.json()) as { reply?: string; error?: string };
      if (!response.ok) {
        throw new Error(data.error ?? "Chat request failed");
      }

      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: data.reply?.trim() || "我没有生成有效回复。"
        }
      ]);
    } catch (caught) {
      const message = caught instanceof Error ? caught.message : "Unknown error";
      setError(message);
    } finally {
      setIsSending(false);
      inputRef.current?.focus();
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">WebChat</div>
        <button className="new-chat" type="button" onClick={() => setMessages(createStarterMessages())}>
          New chat
        </button>
      </aside>

      <section className="chat-panel" aria-label="Chat">
        <header className="chat-header">
          <div>
            <h1>Chatbot Demo</h1>
            <p>Gemini text chat through a local Node.js API</p>
          </div>
          <span className="status">Local</span>
        </header>

        <div className="message-list">
          {messages.map((message) => (
            <article className={`message ${message.role}`} key={message.id}>
              <div className="avatar">{message.role === "user" ? "U" : "AI"}</div>
              <p>{message.content}</p>
            </article>
          ))}

          {isSending && (
            <article className="message assistant">
              <div className="avatar">AI</div>
              <p className="typing">Thinking...</p>
            </article>
          )}
        </div>

        <form className="composer" onSubmit={handleSubmit}>
          {error && <div className="error">{error}</div>}
          <textarea
            ref={inputRef}
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Message WebChat"
            rows={1}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                event.currentTarget.form?.requestSubmit();
              }
            }}
          />
          <button type="submit" disabled={!canSend} aria-label="Send message">
            Send
          </button>
        </form>
      </section>
    </main>
  );
}
