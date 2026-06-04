from __future__ import annotations

import json
import os
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from src.pipeline import CivicRAGPipeline


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Civic.ai Birth/Death Registration RAG</title>
  <style>
    :root {
      --ink: #172033;
      --muted: #667085;
      --line: #d7dee8;
      --surface: #f7f9fc;
      --panel: #ffffff;
      --accent: #116a5c;
      --accent-2: #c76b2a;
      --answer: #eef7f4;
      --user: #f1f4f9;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: linear-gradient(180deg, #eef3f8 0%, #fbfcfe 42%, #f5f8fb 100%);
    }
    .shell {
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr auto;
    }
    header {
      border-bottom: 1px solid var(--line);
      background: rgba(255,255,255,.86);
      backdrop-filter: blur(14px);
      padding: 16px clamp(16px, 4vw, 42px);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }
    .controls {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }
    h1 { margin: 0; font-size: 20px; line-height: 1.2; }
    .sub { color: var(--muted); font-size: 13px; margin-top: 3px; }
    select, button, textarea {
      font: inherit;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--ink);
    }
    select { padding: 9px 10px; min-width: 135px; }
    main {
      width: min(980px, 100%);
      margin: 0 auto;
      padding: 22px clamp(14px, 4vw, 30px);
      display: grid;
      grid-template-rows: 1fr auto;
      gap: 16px;
    }
    #chat {
      min-height: 55vh;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .message {
      max-width: 820px;
      padding: 14px 15px;
      border: 1px solid var(--line);
      border-radius: 8px;
      line-height: 1.52;
      white-space: pre-wrap;
    }
    .message.user { align-self: flex-end; background: var(--user); }
    .message.bot { align-self: flex-start; background: var(--answer); }
    .sources {
      margin-top: 12px;
      display: grid;
      gap: 8px;
      color: var(--muted);
      font-size: 13px;
      white-space: normal;
    }
    .source {
      border-left: 3px solid var(--accent);
      padding-left: 8px;
    }
    .generation {
      margin-top: 12px;
      display: inline-flex;
      width: fit-content;
      max-width: 100%;
      padding: 5px 8px;
      border: 1px solid #c8d6e3;
      border-radius: 999px;
      background: rgba(255,255,255,.72);
      color: #475467;
      font-size: 12px;
      font-weight: 650;
      white-space: normal;
    }
    .links {
      margin-top: 12px;
      display: grid;
      gap: 7px;
      color: var(--muted);
      font-size: 13px;
      white-space: normal;
    }
    .links-title {
      color: var(--ink);
      font-weight: 700;
    }
    .link-item a {
      color: var(--accent);
      overflow-wrap: anywhere;
      text-decoration: none;
      border-bottom: 1px solid rgba(17, 106, 92, .32);
    }
    .link-item a:hover {
      border-bottom-color: var(--accent);
    }
    form {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      align-items: end;
      position: sticky;
      bottom: 0;
      background: rgba(247,249,252,.92);
      padding: 12px 0 4px;
      backdrop-filter: blur(10px);
    }
    textarea {
      width: 100%;
      min-height: 58px;
      max-height: 170px;
      resize: vertical;
      padding: 12px 13px;
      line-height: 1.45;
    }
    button {
      padding: 12px 17px;
      background: var(--accent);
      color: white;
      border-color: var(--accent);
      font-weight: 650;
      cursor: pointer;
    }
    button:disabled {
      opacity: .58;
      cursor: wait;
    }
    .status { color: var(--muted); font-size: 13px; padding: 0 2px; }
    @media (max-width: 640px) {
      header { align-items: flex-start; flex-direction: column; }
      form { grid-template-columns: 1fr; }
      button { width: 100%; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div>
        <h1>Civic.ai Birth/Death Registration RAG</h1>
        <div class="sub">Local NextRAG-style chatbot over Bangladeshi birth and death registration documents</div>
      </div>
      <div class="controls">
        <select id="method" aria-label="RAG method">
          <option value="civic">CivicRAG (ours)</option>
          <option value="simple">Simple RAG</option>
        </select>
        <select id="model" aria-label="Model">
          <option value="llama3.2">llama3.2</option>
          <option value="llama3">llama3</option>
          <option value="qwen2.5:7b">qwen2.5:7b</option>
        </select>
      </div>
    </header>
    <main>
      <section id="chat"></section>
      <div>
        <div id="status" class="status">Ready</div>
        <form id="form">
          <textarea id="query" placeholder="Ask about birth registration, death registration, correction, fees, BDRIS, documents..." required></textarea>
          <button id="send" type="submit">Ask</button>
        </form>
      </div>
    </main>
  </div>
  <script>
    const chat = document.getElementById("chat");
    const form = document.getElementById("form");
    const query = document.getElementById("query");
    const model = document.getElementById("model");
    const method = document.getElementById("method");
    const status = document.getElementById("status");
    const send = document.getElementById("send");

    function methodLabel(value) {
      return value === "simple" ? "Simple RAG" : "CivicRAG (ours)";
    }

    function uniqueLinksFromSources(sources = []) {
      const seen = new Set();
      const links = [];
      const urlPattern = /https?:\\/\\/[^\\s`"'<>),।]+/g;
      sources.forEach((source) => {
        const metadata = source.metadata || {};
        const candidates = [];
        if (metadata.source_url) candidates.push({ url: metadata.source_url, label: metadata.source_url });
        const content = source.content || "";
        for (const match of content.matchAll(urlPattern)) {
          candidates.push({ url: match[0], label: match[0] });
        }
        candidates.forEach((candidate) => {
          const cleanUrl = candidate.url.replace(/[.,;:]+$/, "");
          if (!cleanUrl || seen.has(cleanUrl)) return;
          seen.add(cleanUrl);
          links.push({
            url: cleanUrl,
            label: candidate.label,
            sourceId: source.id
          });
        });
      });
      return links;
    }

    function addMessage(text, role, sources = [], run = null) {
      const node = document.createElement("div");
      node.className = `message ${role}`;
      node.textContent = text;
      if (role === "bot" && run) {
        const generation = document.createElement("div");
        generation.className = "generation";
        generation.textContent = `Generated by: ${methodLabel(run.method)} + ${run.model}`;
        node.appendChild(generation);
      }
      if (sources.length) {
        const box = document.createElement("div");
        box.className = "sources";
        sources.forEach((source, index) => {
          const item = document.createElement("div");
          item.className = "source";
          const metadata = source.metadata || {};
          item.textContent = `${index + 1}. ${source.id} | ${metadata.document_type || "unknown"} | ${metadata.section_title || metadata.category || "source"} | score ${Number(source.score || 0).toFixed(4)}`;
          box.appendChild(item);
        });
        node.appendChild(box);
      }
      if (role === "bot" && sources.length) {
        const links = uniqueLinksFromSources(sources);
        if (links.length) {
          const linksBox = document.createElement("div");
          linksBox.className = "links";
          const title = document.createElement("div");
          title.className = "links-title";
          title.textContent = "Relevant official/source links";
          linksBox.appendChild(title);
          links.slice(0, 5).forEach((link, index) => {
            const item = document.createElement("div");
            item.className = "link-item";
            const anchor = document.createElement("a");
            anchor.href = link.url;
            anchor.target = "_blank";
            anchor.rel = "noopener noreferrer";
            anchor.textContent = `${index + 1}. ${link.url}`;
            item.appendChild(anchor);
            const sourceText = document.createElement("span");
            sourceText.textContent = ` (${link.sourceId})`;
            item.appendChild(sourceText);
            linksBox.appendChild(item);
          });
          node.appendChild(linksBox);
        }
      }
      chat.appendChild(node);
      node.scrollIntoView({ behavior: "smooth", block: "end" });
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const text = query.value.trim();
      if (!text) return;
      addMessage(text, "user");
      query.value = "";
      send.disabled = true;
      const methodLabel = method.options[method.selectedIndex].text;
      status.textContent = `Thinking with ${methodLabel} + ${model.value}...`;
      try {
        const response = await fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: text, model: model.value, method: method.value })
        });
        const payload = await response.json();
        if (!response.ok) throw new Error(payload.error || "Request failed");
        addMessage(payload.answer, "bot", payload.sources || [], {
          method: payload.method || method.value,
          model: payload.model || model.value
        });
        status.textContent = "Ready";
      } catch (error) {
        addMessage(`Error: ${error.message}`, "bot");
        status.textContent = "Error";
      } finally {
        send.disabled = false;
        query.focus();
      }
    });

    addMessage("Ask a birth/death registration question and choose Simple RAG or CivicRAG (ours). The answer will show source IDs so you can compare retrieval behavior.", "bot");
  </script>
</body>
</html>
"""


class ChatHandler(BaseHTTPRequestHandler):
    pipeline: CivicRAGPipeline | None = None

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/":
            self._send_text(HTML, "text/html; charset=utf-8")
            return
        if path == "/health":
            self._send_json({"status": "ok"})
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/chat":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            query = str(payload.get("query", "")).strip()
            model = str(payload.get("model", "llama3.2")).strip()
            method = str(payload.get("method", "civic")).strip()
            if not query:
                raise ValueError("Query is required")
            if self.pipeline is None:
                raise RuntimeError("Pipeline is not initialized")
            response = self.pipeline.ask(query, model=model, method=method)
            self._send_json(response)
        except Exception as exc:
            self._send_json({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_text(self, body: str, content_type: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        self._send_text(json.dumps(payload, ensure_ascii=False), "application/json; charset=utf-8", status)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run the Civic.ai local birth/death registration RAG chatbot.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--config", default="domains/birth_death_registration/config.json")
    args = parser.parse_args()

    ChatHandler.pipeline = CivicRAGPipeline(PROJECT_ROOT, PROJECT_ROOT / args.config)
    server = ThreadingHTTPServer((args.host, args.port), ChatHandler)
    print(f"Civic.ai chatbot running at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
