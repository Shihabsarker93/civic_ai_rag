from __future__ import annotations

import json
import os
import re
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import parse_qs, urlparse

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from src.pipeline import CivicRAGPipeline


BANGLA_QUERY_PATTERN = re.compile(r"[\u0980-\u09FF]")


HTML = """<!doctype html>
<html lang="bn">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Civic.ai Government Service RAG</title>
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
      grid-template-columns: 1fr auto auto;
      gap: 10px;
      align-items: end;
      position: sticky;
      bottom: 0;
      background: rgba(247,249,252,.92);
      padding: 12px 0 4px;
      backdrop-filter: blur(10px);
    }
    #domain {
      min-width: 178px;
      padding: 12px 10px;
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
        <h1>Civic.ai Government Service RAG</h1>
        <div class="sub" id="domain-note">বাংলা প্রশ্ন করুন এবং সঠিক সেবা ডোমেইন নির্বাচন করুন। BRTA ও Passport ডেটাসেট পরীক্ষামূলক।</div>
      </div>
      <div class="controls">
        <a id="register-link" href="/data-register" target="_blank">Data register</a>
        <select id="method" aria-label="RAG method">
          <option value="civic">CivicRAG (ours)</option>
          <option value="simple">Simple RAG</option>
        </select>
        <select id="model" aria-label="Model">
          <option value="llama3.2">llama3.2</option>
          <option value="llama3">llama3</option>
          <option value="qwen2.5:7b">qwen2.5:7b</option>
          <option value="qwen3:8b">qwen3:8b</option>
        </select>
      </div>
    </header>
    <main>
      <section id="chat"></section>
      <div>
        <div id="status" class="status">Ready</div>
        <form id="form">
          <textarea id="query" placeholder="নির্বাচিত সেবা সম্পর্কে বাংলায় প্রশ্ন লিখুন..." required></textarea>
          <select id="domain" aria-label="Service domain"></select>
          <button id="send" type="submit">প্রশ্ন করুন</button>
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
    const domain = document.getElementById("domain");
    const domainNote = document.getElementById("domain-note");
    const registerLink = document.getElementById("register-link");
    const status = document.getElementById("status");
    const send = document.getElementById("send");
    const banglaPattern = /[\u0980-\u09FF]/;

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
        const route = run.answer_route === "controlled" ? "Controlled answer (LLM bypassed)" : `${run.model} (${run.answer_route || "LLM"})`;
        generation.textContent = `${run.domain} | ${methodLabel(run.method)} | ${route}`;
        node.appendChild(generation);
      }
      if (sources.length) {
        const box = document.createElement("div");
        box.className = "sources";
        const title = document.createElement("div");
        title.className = "links-title";
        title.textContent = "Retrieved candidate chunks for debugging";
        box.appendChild(title);
        sources.forEach((source, index) => {
          const item = document.createElement("div");
          item.className = "source";
          const metadata = source.metadata || {};
          item.textContent = `${index + 1}. ${source.id} | ${metadata.document_type || "unknown"} | ${metadata.section_title || metadata.category || "source"} | score ${Number(source.score || 0).toFixed(4)}`;
          if (metadata.experimental) {
            item.textContent += ` | File: ${metadata.source_relative_path} | Document date: ${metadata.document_date || "unknown"} | Audit: ${metadata.audit_flags || "not independently verified"}`;
          }
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
      if (!banglaPattern.test(text)) {
        addMessage("এই সংস্করণে অনুগ্রহ করে বাংলায় প্রশ্ন করুন।", "bot");
        status.textContent = "বাংলা প্রশ্ন প্রয়োজন";
        return;
      }
      addMessage(text, "user");
      query.value = "";
      send.disabled = true;
      const selectedDomain = domain.value;
      const methodLabel = method.options[method.selectedIndex].text;
      status.textContent = `Thinking with ${methodLabel} + ${model.value}...`;
      try {
        const response = await fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: text, model: model.value, method: method.value, domain: selectedDomain })
        });
        const payload = await response.json();
        if (!response.ok) throw new Error(payload.error || "Request failed");
        addMessage(payload.answer, "bot", payload.sources || [], {
          method: payload.method || method.value,
          model: payload.model || model.value,
          domain: payload.domain || selectedDomain,
          answer_route: payload.answer_route
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

    domain.addEventListener("change", () => {
      registerLink.href = `/data-register?domain=${encodeURIComponent(domain.value)}`;
      domainNote.textContent = domain.value === "birth_death_registration" ? "জন্ম ও মৃত্যু নিবন্ধন: বাংলায় প্রশ্ন করুন।" : "পরীক্ষামূলক ডেটাসেট: বাংলায় প্রশ্ন করুন এবং উৎস ও ডেটা রেজিস্টার দেখুন।";
    });
    send.disabled = true;
    fetch("/domains").then(r => r.json()).then(payload => {
      payload.domains.forEach(item => {
        const option = document.createElement("option");
        option.value = item.id;
        option.textContent = item.name + (item.experimental ? " (experimental)" : "");
        domain.appendChild(option);
      });
      domain.value = payload.default_domain;
      domain.dispatchEvent(new Event("change"));
      send.disabled = false;
    }).catch(() => { status.textContent = "Unable to load service domains"; });
    addMessage("সেবা ডোমেইন ও মডেল নির্বাচন করে বাংলায় প্রশ্ন করুন। উত্তরের সঙ্গে ব্যবহৃত উৎস দেখানো হবে।", "bot");
  </script>
</body>
</html>
"""


class ChatHandler(BaseHTTPRequestHandler):
    pipeline: CivicRAGPipeline | None = None
    pipelines: dict[str, CivicRAGPipeline] = {}
    domain_configs: dict[str, Path] = {}
    inference_lock = Lock()

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/":
            self._send_text(HTML, "text/html; charset=utf-8")
            return
        if path == "/health":
            self._send_json({"status": "ok"})
            return
        if path == "/domains":
            domains = []
            for domain_id, config_path in self.domain_configs.items():
                info = json.loads(config_path.read_text())["domain"]
                domains.append({"id": domain_id, "name": info["display_name"], "experimental": info.get("experimental", False)})
            self._send_json({"domains": domains, "default_domain": self.pipeline.domain_id})
            return
        if path == "/data-register":
            domain_id = parse_qs(urlparse(self.path).query).get("domain", [self.pipeline.domain_id])[0]
            if domain_id not in self.domain_configs:
                self._send_json({"error": "Unknown domain"}, status=HTTPStatus.BAD_REQUEST)
                return
            config = json.loads(self.domain_configs[domain_id].read_text())
            register = config["data"].get("register_path")
            result = json.loads((PROJECT_ROOT / register).read_text()) if register else {"domain": domain_id, "note": "Existing birth/death dataset; experimental register applies to new domains only."}
            loaded = self.pipelines.get(domain_id)
            result["published_collection"] = config["data"]["collection_name"]
            result["loaded_collection"] = loaded.data_config["collection_name"] if loaded else None
            result["restart_required"] = loaded is not None and loaded.data_config["collection_name"] != config["data"]["collection_name"]
            self._send_json(result)
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
            if not BANGLA_QUERY_PATTERN.search(query):
                raise ValueError("এই সংস্করণে অনুগ্রহ করে বাংলায় প্রশ্ন করুন।")
            if self.pipeline is None:
                raise RuntimeError("Pipeline is not initialized")
            domain_id = str(payload.get("domain", self.pipeline.domain_id))
            if domain_id not in self.domain_configs:
                raise ValueError("Unknown domain")
            with self.inference_lock:
                if domain_id not in self.pipelines:
                    self.pipelines[domain_id] = CivicRAGPipeline(PROJECT_ROOT, self.domain_configs[domain_id], shared_pipeline=self.pipeline)
                response = self.pipelines[domain_id].ask(query, model=model, method=method)
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

    parser = argparse.ArgumentParser(description="Run the Civic.ai local government-service RAG chatbot.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--config", default="domains/birth_death_registration/config.json")
    args = parser.parse_args()

    ChatHandler.pipeline = CivicRAGPipeline(PROJECT_ROOT, PROJECT_ROOT / args.config)
    ChatHandler.pipelines = {ChatHandler.pipeline.domain_id: ChatHandler.pipeline}
    ChatHandler.domain_configs = {ChatHandler.pipeline.domain_id: PROJECT_ROOT / args.config}
    for domain in ("birth_death_registration", "brta", "passport"):
        config_path = PROJECT_ROOT / "domains" / domain / "config.json"
        if config_path.exists() and domain not in ChatHandler.domain_configs:
            ChatHandler.domain_configs[domain] = config_path
    server = ThreadingHTTPServer((args.host, args.port), ChatHandler)
    print(f"Civic.ai chatbot running at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
