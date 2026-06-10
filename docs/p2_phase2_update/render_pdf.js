const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const root = __dirname;
  const htmlPath = path.join(root, "p2_phase2_update.html");
  const pdfPath = path.join(root, "p2_phase2_update.pdf");

  const browser = await chromium.launch({
    headless: true,
    executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  });
  const page = await browser.newPage({ viewport: { width: 1240, height: 1754 } });
  await page.goto(`file://${htmlPath}`, { waitUntil: "networkidle" });
  await page.pdf({
    path: pdfPath,
    format: "A4",
    printBackground: true,
    margin: { top: "18mm", right: "16mm", bottom: "18mm", left: "16mm" },
  });
  await browser.close();
  console.log(pdfPath);
})();
