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
Do not write meta commentary such as "based on the retrieved evidence" or "the correct answer is".
Do not repeat headings, paragraphs, or bullet groups.
End after the final useful instruction."""


BANGLA_PATTERN = re.compile(r"[\u0980-\u09FF]")
ASCII_LETTER_PATTERN = re.compile(r"[A-Za-z]")
SOURCE_LINE_PATTERN = re.compile(
    r"(?im)^\s*(?:sources?|source ids?|সোর্সেস|সোুর্সেস|উৎস)\s*:.*(?:\n\s*(?:id=)?[A-Za-z0-9_\-\u0980-\u09FF, ]+.*)*"
)


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

Before answering, silently identify the best supporting sources.
Write one concise answer. For procedural questions, include only the steps supported by the evidence.
Do not include verification, correction, appeal, or legal-background details unless the user asks for them.

Answer:"""


def remove_repeated_blocks(answer: str) -> str:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", answer.strip()) if block.strip()]
    cleaned: list[str] = []
    seen: set[str] = set()
    for block in blocks:
        normalized = re.sub(r"\W+", "", block.lower())
        if normalized in seen:
            continue
        seen.add(normalized)
        cleaned.append(block)
    return "\n\n".join(cleaned).strip()


def canonicalize_answer(answer: str, source_ids: list[str]) -> str:
    answer = SOURCE_LINE_PATTERN.sub("", answer).strip()
    answer = remove_repeated_blocks(answer)
    if source_ids:
        answer = f"{answer}\n\nSources: {', '.join(source_ids)}"
    return answer.strip()


class OllamaAnswerGenerator:
    def __init__(
        self,
        *,
        model: str,
        base_url: str,
        temperature: float,
        top_p: float,
        num_predict: int,
        repeat_last_n: int | None = None,
        repeat_penalty: float | None = None,
    ) -> None:
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=temperature,
            top_p=top_p,
            num_predict=num_predict,
            repeat_last_n=repeat_last_n,
            repeat_penalty=repeat_penalty,
        )

    def answer(self, query: str, contexts: list[dict[str, Any]]) -> str:
        response = self.llm.invoke(build_prompt(query, contexts))
        answer = str(response.content).strip()
        source_ids = [str(context["id"]) for context in contexts[:3]]
        return canonicalize_answer(answer, source_ids)
