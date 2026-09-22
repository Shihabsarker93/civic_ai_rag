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
      --ink: #11221f;
      --muted: #60716c;
      --line: #d7e4df;
      --surface: #f4f8f5;
      --panel: #ffffff;
      --teal: #087c6d;
      --teal-deep: #075b52;
      --saffron: #f4b942;
      --navy: #143a52;
      --answer: #fbfdfc;
      --user: #e5f4ef;
      --shadow: 0 18px 45px rgba(16, 55, 48, .10);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Anek Bangla", "Noto Sans Bengali", "Hind Siliguri", ui-sans-serif, sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at 8% -8%, rgba(244, 185, 66, .24), transparent 29rem),
        radial-gradient(circle at 94% 3%, rgba(8, 124, 109, .16), transparent 28rem),
        linear-gradient(160deg, #eff7f4 0%, #f9fbf9 43%, #eef4f1 100%);
    }
    .shell {
      min-height: 100vh;
    }
    header {
      width: min(1220px, calc(100% - 32px));
      margin: 18px auto 0;
      border: 1px solid rgba(211, 229, 222, .9);
      border-radius: 20px;
      background: rgba(255,255,255,.78);
      backdrop-filter: blur(14px);
      box-shadow: 0 8px 25px rgba(18, 58, 48, .06);
      padding: 14px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }
    .brand { display: flex; align-items: center; gap: 12px; }
    .brand-mark {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border-radius: 14px;
      color: white;
      font-family: Georgia, serif;
      font-size: 21px;
      font-weight: 700;
      background: linear-gradient(145deg, var(--teal), var(--navy));
      box-shadow: 0 8px 17px rgba(8, 124, 109, .23);
    }
    .eyebrow {
      color: var(--teal);
      font-size: 10px;
      font-weight: 800;
      letter-spacing: .12em;
      text-transform: uppercase;
    }
    .controls {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: flex-end;
    }
    h1 { margin: 1px 0 0; font-family: Georgia, "Noto Serif Bengali", serif; font-size: 21px; line-height: 1.15; letter-spacing: -.02em; }
    .sub { color: var(--muted); font-size: 12px; margin-top: 4px; }
    select, button, textarea {
      font: inherit;
      border: 1px solid var(--line);
      border-radius: 11px;
      background: var(--panel);
      color: var(--ink);
    }
    .controls select { padding: 8px 9px; min-width: 120px; color: #38514a; font-size: 12px; }
    #register-link {
      color: var(--teal-deep);
      font-size: 12px;
      font-weight: 700;
      text-decoration: none;
      padding: 8px 9px;
    }
    #register-link:hover { color: var(--teal); }
    main {
      width: min(1120px, 100%);
      margin: 0 auto;
      padding: 28px clamp(16px, 4vw, 30px) 34px;
      display: grid;
      grid-template-rows: 1fr auto;
      gap: 18px;
    }
    #chat {
      min-height: 54vh;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .welcome {
      min-height: 420px;
      display: grid;
      align-content: center;
      justify-items: center;
      text-align: center;
      padding: 42px 22px;
      border: 1px solid rgba(215, 229, 223, .92);
      border-radius: 28px;
      background: rgba(255,255,255,.68);
      box-shadow: var(--shadow);
    }
    .welcome-badge {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 7px 11px;
      border-radius: 999px;
      background: #e4f3ed;
      color: var(--teal-deep);
      font-size: 12px;
      font-weight: 750;
    }
    .welcome-badge::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: var(--saffron); box-shadow: 0 0 0 3px rgba(244,185,66,.18); }
    .welcome h2 { max-width: 680px; margin: 16px 0 9px; font-family: Georgia, "Noto Serif Bengali", serif; font-size: clamp(27px, 4vw, 42px); line-height: 1.13; letter-spacing: -.035em; }
    .welcome p { max-width: 590px; margin: 0; color: var(--muted); font-size: 15px; line-height: 1.65; }
    .service-cards { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-top: 25px; }
    .service-card {
      border: 1px solid #d8e8e1;
      border-radius: 14px;
      padding: 11px 14px;
      color: #254940;
      background: #fff;
      font-size: 13px;
      font-weight: 700;
    }
    .service-card span { color: var(--muted); font-size: 11px; font-weight: 500; }
    .example-row { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; max-width: 790px; margin-top: 23px; }
    .example-chip {
      border: 1px solid #c9ddd5;
      border-radius: 999px;
      padding: 8px 12px;
      color: var(--teal-deep);
      background: #f8fcfa;
      font-size: 12px;
      cursor: pointer;
    }
    .example-chip:hover { background: #e7f5ef; border-color: #80b9aa; }
    .message {
      width: fit-content;
      max-width: min(850px, 92%);
      padding: 16px 17px;
      border: 1px solid #d7e4df;
      border-radius: 18px;
      line-height: 1.65;
      white-space: pre-wrap;
      box-shadow: 0 8px 20px rgba(18, 58, 48, .055);
    }
    .message.user { align-self: flex-end; color: #073b34; background: linear-gradient(145deg, #ddf2eb, #eef8f4); border-bottom-right-radius: 5px; }
    .message.bot { align-self: flex-start; background: var(--answer); border-bottom-left-radius: 5px; }
    .sources {
      margin-top: 12px;
      display: grid;
      gap: 8px;
      color: var(--muted);
      font-size: 13px;
      white-space: normal;
    }
    .source {
      border-left: 3px solid var(--teal);
      padding-left: 8px;
    }
    details.evidence-details { margin-top: 13px; border-top: 1px solid #e0ebe6; padding-top: 11px; white-space: normal; }
    details.evidence-details summary { color: var(--teal-deep); cursor: pointer; font-size: 12px; font-weight: 750; }
    .generation {
      margin-top: 12px;
      display: inline-flex;
      width: fit-content;
      max-width: 100%;
      padding: 5px 8px;
      border: 1px solid #cce3da;
      border-radius: 999px;
      background: #eff8f4;
      color: #416259;
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
      color: var(--teal);
      overflow-wrap: anywhere;
      text-decoration: none;
      border-bottom: 1px solid rgba(8, 124, 109, .32);
    }
    .link-item a:hover {
      border-bottom-color: var(--teal);
    }
    form {
      display: grid;
      grid-template-columns: 1fr auto auto;
      gap: 9px;
      align-items: end;
      padding: 10px;
      border: 1px solid #d4e3dd;
      border-radius: 19px;
      background: rgba(255,255,255,.88);
      box-shadow: var(--shadow);
      backdrop-filter: blur(12px);
    }
    #domain {
      min-width: 178px;
      padding: 12px 10px;
      background: #f4f9f6;
    }
    textarea {
      width: 100%;
      min-height: 56px;
      max-height: 170px;
      resize: vertical;
      padding: 12px 13px;
      line-height: 1.45;
      border-color: transparent;
      background: transparent;
      outline: none;
    }
    textarea:focus { box-shadow: inset 0 0 0 2px rgba(8,124,109,.2); }
    button {
      padding: 12px 17px;
      background: linear-gradient(145deg, var(--teal), var(--teal-deep));
      color: white;
      border-color: var(--teal-deep);
      font-weight: 650;
      cursor: pointer;
      box-shadow: 0 7px 13px rgba(8,124,109,.2);
    }
    button:hover:not(:disabled) { transform: translateY(-1px); filter: brightness(1.03); }
    button:disabled {
      opacity: .58;
      cursor: wait;
    }
    .status { color: var(--muted); font-size: 12px; padding: 0 3px 8px; }
    .status::before { content: ""; display: inline-block; width: 7px; height: 7px; margin-right: 6px; border-radius: 50%; background: #55af86; }
    @media (max-width: 760px) {
      header { width: calc(100% - 22px); align-items: flex-start; flex-direction: column; margin-top: 11px; }
      .controls { justify-content: flex-start; }
      #register-link { padding-left: 0; }
      form { grid-template-columns: 1fr; }
      button { width: 100%; }
      #domain { width: 100%; }
      .welcome { min-height: 390px; padding: 30px 16px; }
      .welcome h2 { font-size: 30px; }
      .message { max-width: 96%; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div class="brand">
        <div class="brand-mark">সি</div>
        <div>
          <div class="eyebrow">Bangladesh public service assistant</div>
          <h1>Civic.ai</h1>
          <div class="sub" id="domain-note">বাংলা প্রশ্ন করুন এবং সঠিক সেবা ডোমেইন নির্বাচন করুন।</div>
        </div>
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
      <section id="chat">
        <div id="welcome" class="welcome">
          <div class="welcome-badge">সোর্স-ভিত্তিক নাগরিক সেবা সহায়তা</div>
          <h2>সরকারি সেবা সম্পর্কে পরিষ্কার উত্তর, বাংলায়।</h2>
          <p>প্রশ্নের ধরন অনুযায়ী যাচাইকৃত উৎস থেকে তথ্য আনা হয়। একটি সেবা ডোমেইন নির্বাচন করে সরাসরি, নিজের ভাষায় বা পরিস্থিতি ব্যাখ্যা করে প্রশ্ন করুন।</p>
          <div class="service-cards">
            <div class="service-card">জন্ম ও মৃত্যু নিবন্ধন<br><span>Birth &amp; death registration</span></div>
            <div class="service-card">পাসপোর্ট<br><span>Passport services</span></div>
            <div class="service-card">বিআরটিএ<br><span>Vehicle &amp; licence services</span></div>
          </div>
          <div class="example-row">
            <button class="example-chip" type="button" data-domain="birth_death_registration" data-query="জন্ম নিবন্ধনের জন্য কী কী কাগজপত্র লাগবে?">জন্ম নিবন্ধনের কাগজপত্র</button>
            <button class="example-chip" type="button" data-domain="passport" data-query="পাসপোর্ট করতে কত টাকা লাগে?">পাসপোর্টের ফি</button>
            <button class="example-chip" type="button" data-domain="brta" data-query="ড্রাইভিং লাইসেন্স নবায়ন কীভাবে করব?">লাইসেন্স নবায়ন</button>
          </div>
        </div>
      </section>
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
    const welcome = document.getElementById("welcome");
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
      if (welcome) welcome.remove();
      const node = document.createElement("div");
      node.className = `message ${role}`;
      node.textContent = text;
      if (role === "bot" && run) {
        const generation = document.createElement("div");
        generation.className = "generation";
        const controlledRoutes = ["controlled", "controlled_evidence"];
        const route = controlledRoutes.includes(run.answer_route)
          ? (run.answer_route === "controlled_evidence" ? "Evidence-first answer" : "Controlled answer (LLM bypassed)")
          : `${run.model} (${run.answer_route || "LLM"})`;
        generation.textContent = `${run.domain} | ${methodLabel(run.method)} | ${route}`;
        node.appendChild(generation);
      }
      if (sources.length) {
        const details = document.createElement("details");
        details.className = "evidence-details";
        const summary = document.createElement("summary");
        summary.textContent = "প্রমাণ ও রিট্রিভাল বিস্তারিত দেখুন";
        details.appendChild(summary);
        const box = document.createElement("div");
        box.className = "sources";
        const title = document.createElement("div");
        title.className = "links-title";
        title.textContent = "Retrieved candidate chunks";
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
        details.appendChild(box);
        node.appendChild(details);
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
          const target = node.querySelector(".evidence-details");
          (target || node).appendChild(linksBox);
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
    document.querySelectorAll(".example-chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        domain.value = chip.dataset.domain;
        domain.dispatchEvent(new Event("change"));
        query.value = chip.dataset.query;
        query.focus();
      });
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
