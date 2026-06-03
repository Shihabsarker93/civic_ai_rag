from __future__ import annotations

from typing import Any

from langchain_ollama import ChatOllama


SYSTEM_INSTRUCTIONS = """You are Civic.ai, a government service guidance assistant for Bangladesh.
Answer only using the retrieved evidence.
The retrieved sources are ranked by relevance. Source 1 is the strongest evidence.
If Source 1 directly answers the user's question, answer from Source 1.
If another retrieved source directly answers the question better than Source 1, use that source.
Only say the available dataset does not contain enough information when none of the retrieved sources answer the question.
Keep the answer factual, concise, and citizen-friendly.
Preserve the user's language when possible.
Include source ids at the end."""


def build_prompt(query: str, contexts: list[dict[str, Any]]) -> str:
    evidence_blocks = []
    for index, context in enumerate(contexts, start=1):
        evidence_blocks.append(
            "\n".join(
                [
                    f"[Source {index}] id={context['id']}",
                    context["content"],
                ]
            )
        )

    evidence = "\n\n".join(evidence_blocks)
    return f"""{SYSTEM_INSTRUCTIONS}

Question:
{query}

Retrieved evidence:
{evidence}

Before answering, silently identify the single best source. Do not mention unrelated source variants unless they are needed.

Answer:"""


class OllamaAnswerGenerator:
    def __init__(
        self,
        *,
        model: str,
        base_url: str,
        temperature: float,
        top_p: float,
        num_predict: int,
    ) -> None:
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=temperature,
            top_p=top_p,
            num_predict=num_predict,
        )

    def answer(self, query: str, contexts: list[dict[str, Any]]) -> str:
        response = self.llm.invoke(build_prompt(query, contexts))
        return str(response.content)
