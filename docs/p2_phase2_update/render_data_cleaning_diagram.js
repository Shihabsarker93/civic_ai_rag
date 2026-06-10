const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const root = __dirname;
  const htmlPath = path.join(root, "data_cleaning_diagram.html");
  const pdfPath = path.join(root, "data_cleaning_diagram.pdf");
  const pngPath = path.join(root, "data_cleaning_diagram.png");

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
