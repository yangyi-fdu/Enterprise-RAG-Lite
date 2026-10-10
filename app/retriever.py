import logging
from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np

from app.chunking import chunk_document
from app.config import Config

logger = logging.getLogger(__name__)


@dataclass
class Hit:
    chunk_id: int
    text: str
    score: float  # cosine similarity, higher is more relevant


class Retriever:
    """FAISS index over sentence embeddings with a relevance threshold.

    Embeddings are L2-normalised, so the inner product equals cosine
    similarity (and ranking by it is the same as ranking by L2 distance).
    """

    def __init__(self, chunks: list[str], model):
        if not chunks:
            raise ValueError("knowledge base is empty")
        self.chunks = chunks
        self.model = model
        embeddings = self._embed(chunks)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)
        logger.info("Indexed %d chunks (dim=%d)", len(chunks), embeddings.shape[1])

    @classmethod
    def from_file(cls, path: str, model, chunk_size: int = Config.CHUNK_SIZE,
                  overlap: int = Config.CHUNK_OVERLAP) -> "Retriever":
        text = Path(path).read_text(encoding="utf-8")
        return cls(chunk_document(text, chunk_size, overlap), model)

    def _embed(self, texts: list[str]) -> np.ndarray:
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return np.asarray(vectors, dtype="float32")

    def search(self, query: str, top_k: int = Config.DEFAULT_TOP_K) -> list[Hit]:
        """Return the top_k chunks by similarity, without filtering."""
        scores, ids = self.index.search(self._embed([query]), min(top_k, len(self.chunks)))
        return [Hit(int(i), self.chunks[i], float(s))
                for s, i in zip(scores[0], ids[0]) if i != -1]

    def retrieve(self, query: str, top_k: int = Config.DEFAULT_TOP_K,
                 min_similarity: float = Config.MIN_SIMILARITY) -> list[Hit]:
        """Return only the hits that clear the relevance threshold.

        An empty list means the question is outside the knowledge base, and
        the caller should fall back instead of letting the LLM guess.
        """
        hits = self.search(query, top_k)
        kept = [h for h in hits if h.score >= min_similarity]
        if not kept:
            best = hits[0].score if hits else float("nan")
            logger.info("No chunk above %.2f (best %.3f): fallback", min_similarity, best)
        return kept


def load_embedding_model(name: str = Config.EMBEDDING_MODEL):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(name)
