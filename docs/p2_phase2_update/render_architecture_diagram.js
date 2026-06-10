const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

(async () => {
  const root = __dirname;
  const sourceHtml = fs.readFileSync(path.join(root, "p2_phase2_update.html"), "utf8");
  const svgMatch = sourceHtml.match(/<svg class="architecture-svg"[\s\S]*?<\/svg>/);
  if (!svgMatch) {
    throw new Error("Architecture SVG not found in p2_phase2_update.html");
  }

  const standalone = `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>CivicRAG Architecture Diagram</title>
  <style>
    @page { size: A4 landscape; margin: 8mm; }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: #f7fbff;
      font-family: "Noto Sans Bengali", "Noto Sans", Arial, sans-serif;
      color: #132033;
    }
    .sheet {
      width: 100%;
      min-height: 100vh;
      padding: 7mm;
      background:
        radial-gradient(circle at 8% 8%, rgba(15,118,110,0.10), transparent 24%),
        linear-gradient(135deg, #ffffff, #eef8f4);
      border: 1px solid #cbd8e8;
      border-radius: 18px;
    }
    .title {
      display: flex;
      justify-content: space-between;
      align-items: end;
      margin-bottom: 4mm;
      border-bottom: 2px solid #d7e1ed;
      padding-bottom: 3mm;
    }
    h1 {
      margin: 0;
      font-size: 28px;
      letter-spacing: -0.02em;
    }
    .subtitle {
      color: #5d6a7f;
      font-size: 13px;
      text-align: right;
      max-width: 360px;
    }
    svg {
      width: 100%;
      height: auto;
      background: #ffffff;
      border: 1px solid #cbd8e8;
      border-radius: 14px;
      box-shadow: 0 14px 35px rgba(15, 35, 55, 0.10);
    }
    svg text {
      font-family: "Noto Sans Bengali", "Noto Sans", Arial, sans-serif;
    }
    .footer {
      display: flex;
      justify-content: space-between;
      margin-top: 3mm;
      color: #526277;
      font-size: 12px;
    }
    code {
      color: #0f5132;
      background: #e9f8f2;
      padding: 1px 5px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <main class="sheet">
    <div class="title">
      <div>
        <h1>CivicRAG System Architecture</h1>
        <div>Birth and death registration domain | Bangla-first grounded RAG pipeline</div>
      </div>
      <div class="subtitle">Offline indexing is separated from online answering so retrieval quality, evidence grounding, and generation can be evaluated independently.</div>
    </div>
    ${svgMatch[0]}
    <div class="footer">
      <span>Key design: aliases are used in <code>retrieval_text</code>; original Bangla source content is used as <code>answer_evidence</code>.</span>
      <span>Embedding: BGE-M3 | Retrieval: Dense + BM25 + RRF | Local LLMs: llama3.2, llama3, qwen2.5:7b</span>
    </div>
  </main>
</body>
</html>`;

  const htmlPath = path.join(root, "civicrag_architecture_diagram.html");
  const pdfPath = path.join(root, "civicrag_architecture_diagram.pdf");
  const pngPath = path.join(root, "civicrag_architecture_diagram.png");
  fs.writeFileSync(htmlPath, standalone, "utf8");

  const browser = await chromium.launch({
    headless: true,
    executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  });
  const page = await browser.newPage({ viewport: { width: 1754, height: 1240 }, deviceScaleFactor: 2 });
  await page.goto(`file://${htmlPath}`, { waitUntil: "networkidle" });
  await page.pdf({
    path: pdfPath,
    format: "A4",
    landscape: true,
    printBackground: true,
    margin: { top: "8mm", right: "8mm", bottom: "8mm", left: "8mm" },
  });
  await page.screenshot({ path: pngPath, fullPage: true });
  await browser.close();
  console.log(pdfPath);
  console.log(pngPath);
})();
