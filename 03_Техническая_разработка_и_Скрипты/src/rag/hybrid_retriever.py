# -*- coding: utf-8 -*-
from typing import List, Dict, Any
import numpy as np

class HybridRetriever:
    def __init__(self, dense_weight: float = 0.6):
        self.dense_weight = dense_weight
        self.sparse_weight = 1.0 - dense_weight
        self.documents: List[Dict[str, Any]] = []

    def add_documents(self, docs: List[Dict[str, Any]]):
        self.documents.extend(docs)

    def reciprocal_rank_fusion(self, dense_ranks: Dict[int, int], sparse_ranks: Dict[int, int], k: int = 60) -> List[int]:
        rrf_scores = {}
        all_doc_ids = set(dense_ranks.keys()).union(set(sparse_ranks.keys()))
        for doc_id in all_doc_ids:
            score = 0.0
            if doc_id in dense_ranks:
                score += self.dense_weight * (1.0 / (k + dense_ranks[doc_id]))
            if doc_id in sparse_ranks:
                score += self.sparse_weight * (1.0 / (k + sparse_ranks[doc_id]))
            rrf_scores[doc_id] = score
        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        return [doc_id for doc_id, _ in sorted_docs]

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.documents:
            return []
        dense_mock = {i: i + 1 for i in range(min(15, len(self.documents)))}
        sparse_mock = {i: len(self.documents) - i for i in range(min(15, len(self.documents)))}
        fused_ids = self.reciprocal_rank_fusion(dense_mock, sparse_mock)
        return [self.documents[idx] for idx in fused_ids[:top_k] if idx < len(self.documents)]
