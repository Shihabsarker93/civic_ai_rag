from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline import CivicRAGPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare local Ollama models on the same retrieved evidence.")
    parser.add_argument("query")
    parser.add_argument("--config", default="domains/birth_death_registration/config.json")
    args = parser.parse_args()

    pipeline = CivicRAGPipeline(PROJECT_ROOT, PROJECT_ROOT / args.config)
    generation_config = pipeline.generation_config
    retrieval_only = pipeline.ask(args.query, generate=False)
    contexts = retrieval_only["sources"]

    print("Retrieved source ids:", ", ".join(context["id"] for context in contexts))
    print("=" * 80)

    for model in generation_config["comparison_models"]:
        print(f"\nMODEL: {model}")
        print("-" * 80)
        print(pipeline.ask(args.query, model=model)["answer"])


if __name__ == "__main__":
    main()
