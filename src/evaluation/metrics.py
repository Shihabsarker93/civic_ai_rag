from __future__ import annotations

from collections import Counter
from math import log2

import numpy as np

from src.retrieval.hybrid_retriever import tokenize


def recall_at_k(retrieved_ids: list[str], expected_ids: set[str], k: int) -> float:
    return float(any(chunk_id in expected_ids for chunk_id in retrieved_ids[:k]))


def precision_at_k(retrieved_ids: list[str], expected_ids: set[str], k: int) -> float:
    if k <= 0:
        return 0.0
    hits = sum(1 for chunk_id in retrieved_ids[:k] if chunk_id in expected_ids)
    return hits / k


def reciprocal_rank(retrieved_ids: list[str], expected_ids: set[str]) -> float:
    for index, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in expected_ids:
            return 1 / index
    return 0.0


def ndcg_at_k(retrieved_ids: list[str], expected_ids: set[str], k: int) -> float:
    dcg = 0.0
    for index, chunk_id in enumerate(retrieved_ids[:k], start=1):
        if chunk_id in expected_ids:
            dcg += 1 / log2(index + 1)

    ideal_hits = min(len(expected_ids), k)
    idcg = sum(1 / log2(index + 1) for index in range(1, ideal_hits + 1))
    if idcg == 0:
        return 0.0
    return dcg / idcg


def token_f1(prediction: str, reference: str) -> float:
    pred_tokens = tokenize(prediction)
    ref_tokens = tokenize(reference)
    if not pred_tokens or not ref_tokens:
        return 0.0

    pred_counts = Counter(pred_tokens)
    ref_counts = Counter(ref_tokens)
    overlap = sum((pred_counts & ref_counts).values())
    if overlap == 0:
        return 0.0

    precision = overlap / len(pred_tokens)
    recall = overlap / len(ref_tokens)
    return 2 * precision * recall / (precision + recall)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        return 0.0
    return float(np.dot(a, b) / denominator)
