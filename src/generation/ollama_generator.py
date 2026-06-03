from __future__ import annotations

import re
from typing import Any

from langchain_ollama import ChatOllama


SYSTEM_INSTRUCTIONS = """You are Civic.ai, a government service guidance assistant for Bangladesh.
Answer only using the retrieved evidence.
The retrieved sources are ranked by relevance. Source 1 is the strongest evidence.
If Source 1 directly answers the user's question, answer from Source 1.
If another retrieved source directly answers the question better than Source 1, use that source.
Only say the available dataset does not contain enough information when none of the retrieved sources answer the question.
Keep the answer factual, concise, and citizen-friendly.
The requested answer language is mandatory. Do not switch languages unless the user asks for translation.
If the requested answer language is English and the evidence is Bangla, translate the evidence into English instead of replying in Bangla.
If the requested answer language is Bangla, answer fully in natural Bangla and do not write the main answer in English.
Retrieval aliases are search hints only; do not treat them as factual evidence.
Write a real answer first; never answer with only a source id.
For how-to questions, give direct step-by-step instructions only; avoid legal background unless it is necessary.
Use at most 6 short bullets and avoid repeating the same point.
End with a Sources line containing the source ids you used."""


BANGLA_PATTERN = re.compile(r"[\u0980-\u09FF]")
ASCII_LETTER_PATTERN = re.compile(r"[A-Za-z]")


def detect_answer_language(query: str) -> str:
    bangla_chars = len(BANGLA_PATTERN.findall(query))
    ascii_letters = len(ASCII_LETTER_PATTERN.findall(query))
    if ascii_letters > bangla_chars:
        return "English"
    if bangla_chars:
        return "Bangla"
    return "the user's language"


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

Answer language:
{detect_answer_language(query)}

Retrieved evidence:
{evidence}

Before answering, silently identify the best supporting sources. Do not mention unrelated source variants unless they are needed.
If the question is broad, summarize the core facts from the most relevant retrieved sources.

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
        answer = str(response.content).strip()
        source_ids = [str(context["id"]) for context in contexts[:3]]
        if source_ids and not any(source_id in answer for source_id in source_ids):
            answer = f"{answer}\n\nSources: {', '.join(source_ids)}"
        return answer
