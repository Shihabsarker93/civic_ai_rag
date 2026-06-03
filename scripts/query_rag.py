from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline import CivicRAGPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the Civic.ai passport RAG baseline.")
    parser.add_argument("query")
    parser.add_argument("--config", default="domains/passport/config.json")
    parser.add_argument("--model", default=None, help="Ollama model, e.g. llama3.2, llama3, qwen2.5:7b")
    parser.add_argument("--method", choices=["simple", "civic"], default="civic")
    parser.add_argument("--no-generate", action="store_true", help="Only show retrieved evidence.")
    args = parser.parse_args()

    pipeline = CivicRAGPipeline(PROJECT_ROOT, PROJECT_ROOT / args.config)
    response = pipeline.ask(args.query, model=args.model, generate=not args.no_generate, method=args.method)
    results = response["sources"]

    print("\nRetrieved evidence")
    print("=" * 80)
    for rank, result in enumerate(results, start=1):
        metadata = result["metadata"]
        print(f"{rank}. {result['id']} score={result['score']:.5f} via={','.join(result['retrievers'])}")
        print(f"   category={metadata.get('category')} subcategory={metadata.get('subcategory')}")

    if args.no_generate:
        return

    print("\nAnswer")
    print("=" * 80)
    print(response["answer"])


if __name__ == "__main__":
    main()
