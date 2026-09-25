"""Generate editable draw.io pages and matching SVGs; no runtime code changes."""
from pathlib import Path
from xml.etree import ElementTree as ET
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/architecture/final_2026_09_25"
COLORS = {"teal": ("#e6f5f1", "#238578"), "blue": ("#eaf1fb", "#5276a6"),
          "amber": ("#fff4dd", "#b88426"), "red": ("#fcece9", "#ba6152"),
          "gray": ("#f0f3f6", "#7b8b9b"), "white": ("#ffffff", "#b9c8d4")}


class Page:
    def __init__(self, title, subtitle, width=1800, height=1450):
        self.title, self.subtitle, self.width, self.height = title, subtitle, width, height
        self.nodes, self.edges, self.panels, self.notes = {}, [], [], []

    def panel(self, x, y, w, h, title):
        self.panels.append((x, y, w, h, title))

    def node(self, id, x, y, w, h, text, color="teal", diamond=False):
        self.nodes[id] = (x, y, w, h, text, color, diamond)

    def edge(self, source, target, points, label="", dashed=False, label_xy=None):
        self.edges.append((source, target, points, label, dashed, label_xy))

    def note(self, x, y, w, h, text):
        self.notes.append((x, y, w, h, text))

    def export(self, book, name):
        diagram = ET.SubElement(book, "diagram", {"id": name, "name": self.title})
        model = ET.SubElement(diagram, "mxGraphModel", {"dx": "1800", "dy": "1450", "grid": "1", "gridSize": "10", "page": "1", "pageScale": "1", "pageWidth": str(self.width), "pageHeight": str(self.height), "math": "0", "shadow": "0"})
        root = ET.SubElement(model, "root")
        ET.SubElement(root, "mxCell", {"id": "0"})
        ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">',
               '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="#526578"/></marker></defs>',
               f'<rect width="{self.width}" height="{self.height}" fill="white"/>']

        def cell(id, x, y, w, h, value, style):
            c = ET.SubElement(root, "mxCell", {"id": id, "parent": "1", "vertex": "1", "value": value, "style": style})
            ET.SubElement(c, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})

        def text(x, y, w, h, value, size=19, bold_first=True, align="middle"):
            lines = value.split("\n")
            center = x + w / 2 if align == "middle" else x
            first_y = y + h / 2 - (len(lines) - 1) * (size + 6) / 2 + size * .34
            for i, line in enumerate(lines):
                weight = "600" if i == 0 and bold_first else "400"
                svg.append(f'<text x="{center}" y="{first_y + i*(size+6)}" text-anchor="{align}" font-family="Helvetica,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="#203448">{escape(line)}</text>')

        cell("title", 45, 25, 1700, 45, self.title, "text;html=0;align=left;fontSize=34;fontStyle=1;fontColor=#203448;")
        cell("subtitle", 45, 78, 1710, 40, self.subtitle, "text;html=0;align=left;fontSize=18;fontColor=#526578;")
        text(45, 25, 1700, 45, self.title, 34, True, "start")
        text(45, 78, 1710, 40, self.subtitle, 18, False, "start")
        for i, (x, y, w, h, title) in enumerate(self.panels):
            cell(f"panel{i}", x, y, w, h, "", "rounded=1;arcSize=4;fillColor=#fafcfd;strokeColor=#d6e1e8;strokeWidth=1;container=0;")
            cell(f"panelTitle{i}", x+20, y+12, w-40, 28, title, "text;html=0;align=left;fontSize=20;fontStyle=1;fontColor=#238578;")
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#fafcfd" stroke="#d6e1e8"/>')
            text(x+20, y+12, w-40, 28, title, 20, True, "start")
        # Explicit elbow points keep the preview and editable connector routes identical.
        for i, (source, target, points, label, dashed, label_xy) in enumerate(self.edges):
            sx, sy, sw, sh, *_ = self.nodes[source]
            tx, ty, tw, th, *_ = self.nodes[target]
            start, end = points[0], points[-1]
            style = f"edgeStyle=none;rounded=0;html=0;endArrow=block;endFill=1;strokeColor=#526578;strokeWidth=2;exitX={(start[0]-sx)/sw};exitY={(start[1]-sy)/sh};exitPerimeter=0;entryX={(end[0]-tx)/tw};entryY={(end[1]-ty)/th};entryPerimeter=0;"
            if dashed:
                style += "dashed=1;dashPattern=6 4;"
            c = ET.SubElement(root, "mxCell", {"id": f"edge{i}", "parent": "1", "edge": "1", "source": source, "target": target, "style": style})
            geom = ET.SubElement(c, "mxGeometry", {"relative": "1", "as": "geometry"})
            if len(points) > 2:
                arr = ET.SubElement(geom, "Array", {"as": "points"})
                for px, py in points[1:-1]:
                    ET.SubElement(arr, "mxPoint", {"x": str(px), "y": str(py)})
            dash = ' stroke-dasharray="8 5"' if dashed else ""
            coordinates = " ".join(f"{px},{py}" for px, py in points)
            svg.append(f'<polyline points="{coordinates}" fill="none" stroke="#526578" stroke-width="2" marker-end="url(#arrow)"{dash}/>')
            if label:
                lx, ly = label_xy
                cell(f"edgeLabel{i}", lx-75, ly-13, 150, 26, label, "text;html=0;fontSize=16;fillColor=#ffffff;align=center;")
                svg.append(f'<rect x="{lx-75}" y="{ly-13}" width="150" height="26" fill="white"/>')
                text(lx-75, ly-13, 150, 26, label, 16, False)
        for id, (x, y, w, h, value, color, diamond) in self.nodes.items():
            fill, stroke = COLORS[color]
            shape = "rhombus;" if diamond else "rounded=1;arcSize=12;"
            lines = value.split("\n")
            font_size = min(18, (w-24) / (max(map(len, lines)) * .56), (h-18) / len(lines)-6)
            font_size = round(font_size, 1)
            cell(id, x, y, w, h, value, shape+f"whiteSpace=wrap;html=0;fillColor={fill};strokeColor={stroke};strokeWidth=1.8;fontColor=#203448;fontSize={font_size};spacing=10;")
            if diamond:
                svg.append(f'<polygon points="{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
            else:
                svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>')
            text(x, y, w, h, value, font_size)
        for i, (x, y, w, h, value) in enumerate(self.notes):
            cell(f"note{i}", x, y, w, h, value, "text;html=0;align=left;fontSize=17;fontColor=#526578;whiteSpace=wrap;")
            text(x, y, w, h, value, 17, False, "start")
        svg.append("</svg>")
        (OUT / f"{name}.svg").write_text("\n".join(svg))


def architecture():
    p = Page("CivicRAG | Final evaluated architecture", "Bangla civic-service QA | Birth/death registration, Passport and BRTA | Selected-evidence path")
    p.panel(35, 135, 1730, 365, "01  OFFLINE DATA PREPARATION AND INDEXING")
    p.node("raw", 65, 235, 195, 120, "Source documents\nPDF / DOCX / HTML\nPrepared MD / JSON", "gray")
    p.node("clean", 300, 235, 215, 120, "Data preparation\nManual / scripted cleanup\nText normalization\nSource tracking")
    p.node("chunks", 555, 220, 215, 145, "Per-domain chunks\nStructure-aware splitting\nTypes where available\nIDs + metadata + URLs\nLocal JSONL corpus")
    p.node("searchtext", 810, 200, 205, 85, "retrieval_text\nContent + search aliases", "blue")
    p.node("evidence", 810, 365, 205, 85, "content\nOriginal source evidence\nNot a generated answer", "amber")
    p.node("bge", 1060, 200, 200, 85, "BAAI/bge-m3\nDense text embeddings", "blue")
    p.node("bmindex", 1060, 325, 200, 95, "BM25 index\nTokenized retrieval_text\nBuilt at retriever load", "blue")
    p.node("chroma", 1320, 205, 405, 110, "ChromaDB: per-domain collection\nChunk ID + vector + source content\n+ metadata (URLs when available)")
    p.edge("raw", "clean", [(260,295),(300,295)])
    p.edge("clean", "chunks", [(515,295),(555,295)])
    p.edge("chunks", "searchtext", [(770,250),(790,250),(790,242),(810,242)])
    p.edge("chunks", "evidence", [(770,335),(790,335),(790,407),(810,407)])
    p.edge("searchtext", "bge", [(1015,242),(1060,242)])
    p.edge("searchtext", "bmindex", [(912,285),(912,310),(1040,310),(1040,372),(1060,372)])
    p.edge("bge", "chroma", [(1260,242),(1320,242)])
    p.edge("evidence", "chroma", [(1015,435),(1295,435),(1295,285),(1320,285)], "store text by ID", label_xy=(1160,450))
    p.note(65,175,1250,25,"Only retrieval_text is embedded; source content stays linked by chunk ID. Index construction is not model training.")

    p.panel(35, 535, 1730, 360, "02  ONLINE DOMAIN-SCOPED RETRIEVAL")
    p.node("query", 65, 645, 195, 105, "User query\nBangla + selected domain\nDirect / paraphrase /\nscenario questions")
    p.node("checks", 305, 645, 205, 105, "Input / scope checks\nBangla input check\nCross-domain aggregate\nclarification guard", "amber")
    p.node("normalize", 550, 645, 205, 105, "Normalize query\nUnicode / wording\nUse selected domain")
    p.node("qembed", 795, 585, 205, 80, "BAAI/bge-m3\nEncode query", "blue")
    p.node("dense", 1040, 585, 215, 80, "Dense search\nChroma similarity\nTop 20 chunk IDs", "blue")
    p.node("bmsearch", 1040, 760, 215, 80, "BM25 search\nKeyword scoring\nTop 20 chunk IDs", "blue")
    p.node("rrf", 1295, 665, 195, 100, "Weighted RRF\nk = 50\nDense .55 / BM25 .45\nKeep top 15", "teal")
    p.node("rerank", 1530, 610, 205, 115, "Rerank candidates\nBGE cross-encoder OR\nlexical-overlap fallback\nBirth/death boosts only", "teal")
    p.node("resolve", 1530, 765, 205, 100, "Resolve source content\nChunk IDs -> local JSONL\nBirth/death fee-context\naugmentation if triggered", "amber")
    p.node("reject", 305, 795, 205, 65, "Clarification response\nUnsupported input / scope", "red")
    p.edge("query", "checks", [(260,697),(305,697)])
    p.edge("checks", "normalize", [(510,697),(550,697)])
    p.edge("checks", "reject", [(407,750),(407,795)])
    p.edge("normalize", "qembed", [(755,675),(775,675),(775,625),(795,625)])
    p.edge("qembed", "dense", [(1000,625),(1040,625)])
    p.edge("normalize", "bmsearch", [(755,722),(775,722),(775,800),(1040,800)])
    p.edge("chroma", "dense", [(1450,315),(1450,515),(1147,515),(1147,585)], dashed=True)
    p.edge("bmindex", "bmsearch", [(1260,372),(1750,372),(1750,870),(1275,870),(1275,800),(1255,800)], dashed=True)
    p.edge("dense", "rrf", [(1255,625),(1275,625),(1275,690),(1295,690)])
    p.edge("bmsearch", "rrf", [(1255,810),(1285,810),(1285,740),(1295,740)])
    p.edge("rrf", "rerank", [(1490,695),(1510,695),(1510,667),(1530,667)])
    p.edge("rerank", "resolve", [(1632,725),(1632,765)])
    p.note(65,795,200,70,"Solid: processing flow\nDashed: index access")

    p.panel(35, 930, 1730, 380, "03  APPLICABLE EVIDENCE AND ANSWER GENERATION  (FLOW RIGHT TO LEFT)")
    p.node("select", 1450, 1000, 280, 155, "Automatic evidence selector\nService / action / scope checks\nCompatible section expansion\nGroup continuations first\nWhole-chunk budget:\n6 passages / 14,000 chars max", "amber")
    p.node("enough", 1210, 1020, 170, 105, "Any selected\nevidence?", "amber", True)
    p.node("prompt", 945, 1020, 220, 105, "Evidence-only prompt\nQuestion + selected content\nPreserve source conditions\nRequest Bangla answer")
    p.node("llm", 680, 1020, 220, 105, "Local LLM via Ollama\nQwen3:8b in comparison\nGenerate from supplied text", "blue")
    p.node("guard", 415, 1020, 220, 105, "Output checks\nLanguage rejection fallback\nTruncation warning\nCanonicalize source IDs", "amber")
    p.node("answer", 65, 1020, 280, 105, "Final response\nBangla answer or clarification\nSource IDs + available links\nScores / evidence in debug view")
    p.node("noevidence", 1185, 1190, 220, 65, "No applicable evidence\nAsk for clarification", "red")
    p.edge("resolve", "select", [(1632,865),(1632,1000)])
    p.edge("select", "enough", [(1450,1072),(1380,1072)])
    p.edge("enough", "prompt", [(1210,1072),(1165,1072)], "Yes", label_xy=(1187,995))
    p.edge("enough", "noevidence", [(1295,1125),(1295,1190)], "No", label_xy=(1295,1165))
    p.edge("prompt", "llm", [(945,1072),(900,1072)])
    p.edge("llm", "guard", [(680,1072),(635,1072)])
    p.edge("guard", "answer", [(415,1072),(345,1072)])
    p.edge("noevidence", "answer", [(1185,1222),(205,1222),(205,1125)])
    p.note(65,1335,1680,90,"Current default: CIVIC_EVIDENCE_SELECTION=1. Legacy controlled-answer paths remain in code but are bypassed on this CivicRAG route.\nThe selector is rule-based, not an LLM judge; applicability and language checks do not guarantee factual correctness.\nSource IDs identify supplied passages, not verified claim-level citations. Baselines and evaluation boundaries are on page 2.")
    return p


def evaluation():
    p = Page("CivicRAG | Comparison and evaluation boundaries", "Keep answer-pipeline comparison separate from retrieval-only ablations and legacy P2 evaluation.", height=1260)
    p.panel(35,145,1730,485,"A  MATCHED ANSWER-PIPELINE COMPARISON: EXISTING 30 QUESTIONS / THREE DOMAINS")
    p.node("shared",65,260,270,165,"Shared experimental inputs\nSame 30 Bangla questions\nSame domain-scoped corpus\nSame BGE-M3 embeddings\nSame Qwen3:8b generator\nSame selected-evidence prompt")
    p.node("simple",400,225,355,120,"Matched Simple RAG\nDense top 6\nWhole-chunk context budget\nNo RRF / reranker / selector", "blue")
    p.node("civic",400,410,355,140,"CivicRAG\nDense + BM25 -> RRF -> reranking\nDomain-specific processing if triggered\nAutomatic evidence selection\nand compatible-section expansion", "teal")
    p.node("gen",840,285,300,185,"Matched generation settings\nQwen3:8b through Ollama\nUp to 6 passages / 14,000 chars\nSame prompt and output checks\nSaved answers + actual contexts\nNo regenerated answers for scoring", "blue")
    p.node("ragas",1230,225,470,145,"Automatic answer/context evaluation\nRAGAS faithfulness + answer relevancy\nCustom binary context relevance (separate metric)\nQwen3 self-judge: exploratory, not gold accuracy", "amber")
    p.node("desc",1230,435,470,100,"Descriptive reporting\nSaved latency, context size, language fraction\nNot proof of factual correctness", "gray")
    p.edge("shared","simple",[(335,300),(365,300),(365,285),(400,285)])
    p.edge("shared","civic",[(335,380),(365,380),(365,480),(400,480)])
    p.edge("simple","gen",[(755,285),(790,285),(790,330),(840,330)])
    p.edge("civic","gen",[(755,480),(790,480),(790,425),(840,425)])
    p.edge("gen","ragas",[(1140,330),(1185,330),(1185,297),(1230,297)])
    p.edge("gen","desc",[(1140,425),(1185,425),(1185,485),(1230,485)])
    p.note(65,570,1640,40,"This baseline is scripts/run_simple_matched.py, not necessarily every legacy branch of the live Simple RAG option.")
    p.panel(35,675,1730,410,"B  RETRIEVAL-ONLY ABLATION: NO ANSWER GENERATION, RERANKING OR EVIDENCE SELECTION")
    p.node("q",65,805,250,110,"Current 30 questions\n10 per domain\nDomain-scoped indices")
    p.node("methods",385,780,350,165,"Three retrieval variants\nBM25-only\nBGE-M3 dense-only\nWeighted Hybrid RRF\nTop 20 -> evaluate top 5", "blue")
    p.node("labels",805,780,360,165,"Pooled relevance labels\nUnion of each variant's top 5\nAssistant-reviewed, not human gold\nUncertain questions excluded\n26/30 provisionally scorable", "amber")
    p.node("metrics",1235,780,470,165,"Per-domain and overall retrieval metrics\nHit@1 / Hit@5 / Precision@5 / MRR@5\nPooled Recall@5 / pooled nDCG@5\nRecall/nDCG: 25 nonempty eligible pools\nNot end-to-end chatbot correctness")
    p.edge("q","methods",[(315,860),(385,860)])
    p.edge("methods","labels",[(735,860),(805,860)])
    p.edge("labels","metrics",[(1165,860),(1235,860)])
    p.note(65,990,1630,65,"Separate historical check: the current birth/death index was also tested on 58 existing P2-labelled questions (19 paraphrase groups).\nDo not merge those scores with the current 30-question results or interpret pooled recall as exhaustive corpus recall.")
    p.note(65,1120,1650,85,"The overnight Qwen draft-labeling experiment is a separate exploratory artifact with unresolved judgments, not final ground truth.\nEvaluation is outside the online chatbot path. No RAGAS judge or relevance-review process runs when a citizen submits a normal query.\nThese diagrams describe implemented paths, not a novel-model-training claim or proof that one method is universally superior.")
    return p


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    book = ET.Element("mxfile", {"host": "app.diagrams.net", "type": "device", "version": "24.7.17"})
    architecture().export(book, "civicrag_final_architecture")
    evaluation().export(book, "evaluation_boundaries")
    path = OUT / "civicrag_final_architecture.drawio"
    ET.indent(book)
    ET.ElementTree(book).write(path, encoding="utf-8", xml_declaration=True)
    for diagram in ET.parse(path).getroot().findall("diagram"):
        cells = diagram.findall("./mxGraphModel/root/mxCell")
        ids = {c.get("id") for c in cells}
        assert len(ids) == len(cells)
        for c in cells:
            if c.get("edge"):
                assert c.get("source") in ids and c.get("target") in ids
    print(path)


if __name__ == "__main__":
    main()
