"""Challenge 08 - Semantic Search + RAG Pipeline (Medium)

PROBLEM
-------
Build the retrieval core of a RAG system, end to end, with no external
services. Implement:

1. HashedNGramEmbedder - a deterministic mock embedder. Extract character
   n-grams (default n=3) from normalized text, hash each into one of `dim`
   buckets with a sign (the "hashing trick"), and L2-normalize the result.
   Same text must always produce the same unit vector.

       embed(text: str) -> np.ndarray            # shape (dim,), ||v|| == 1
       embed_batch(texts: list[str]) -> np.ndarray  # shape (len(texts), dim)

2. VectorIndex - cosine top-k retrieval over an in-memory corpus.

       add(docs: list[str]) -> None
       search(query: str, k: int = 3) -> list[tuple[int, float]]
           # [(doc_id, score), ...] sorted by score descending

3. build_prompt(query, docs) - assemble a grounded prompt with numbered
   citations [1], [2], ... so the model can cite sources.

4. recall_at_k(retrieved, relevant, k) - retrieval eval against a golden set:
   mean over queries of |top-k ∩ relevant| / |relevant|.

INTERVIEW NOTES
---------------
A strong solution demonstrates:
- Knowing that cosine similarity over L2-normalized vectors is just a dot
  product, so search is a single matrix-vector multiply.
- Determinism awareness: Python's built-in hash() is salted per process
  (PYTHONHASHSEED), so a stable hash (crc32/md5) is required.
- top-k via argpartition (O(n)) before sorting only the k winners, rather
  than a full O(n log n) argsort - the habit matters at 10M vectors.
- Clean separation of embed / index / prompt / eval, which mirrors how real
  RAG stacks are tested (retrieval metrics independent of generation).
Common mistakes: normalizing after batching but not in embed(), recall@k
computed per-doc instead of per-query, prompts that dump documents with no
citation anchors, and dividing by zero when a query has no relevant docs.
Follow-ups: add MMR re-ranking for diversity; swap recall@k for MRR/nDCG;
add a keyword (BM25-ish) scorer and reciprocal-rank-fusion hybrid search.
"""

import zlib

import numpy as np


class HashedNGramEmbedder:
    """Deterministic mock embedding: hashed character n-grams, L2-normalized."""

    def __init__(self, dim: int = 256, n: int = 3):
        self.dim = dim
        self.n = n

    def _ngrams(self, text: str) -> list[str]:
        text = " ".join(text.lower().split())  # normalize case + whitespace
        text = f" {text} "                     # mark word boundaries
        return [text[i:i + self.n] for i in range(max(len(text) - self.n + 1, 0))]

    def embed(self, text: str) -> np.ndarray:
        vec = np.zeros(self.dim)
        for gram in self._ngrams(text):
            h = zlib.crc32(gram.encode("utf-8"))   # stable across processes
            sign = 1.0 if (h >> 31) & 1 else -1.0  # signed hashing trick
            vec[h % self.dim] += sign
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        return np.stack([self.embed(t) for t in texts])


class VectorIndex:
    """In-memory cosine-similarity index."""

    def __init__(self, embedder: HashedNGramEmbedder):
        self.embedder = embedder
        self.docs: list[str] = []
        self._matrix: np.ndarray | None = None  # (n_docs, dim), rows unit-norm

    def add(self, docs: list[str]) -> None:
        self.docs.extend(docs)
        new = self.embedder.embed_batch(docs)
        self._matrix = new if self._matrix is None else np.vstack([self._matrix, new])

    def search(self, query: str, k: int = 3) -> list[tuple[int, float]]:
        if self._matrix is None:
            return []
        k = min(k, len(self.docs))
        scores = self._matrix @ self.embedder.embed(query)  # cosine == dot (unit norm)
        top = np.argpartition(-scores, k - 1)[:k]           # O(n) select, then sort k
        top = top[np.argsort(-scores[top])]
        return [(int(i), float(scores[i])) for i in top]


def build_prompt(query: str, docs: list[str]) -> str:
    sources = "\n".join(f"[{i}] {doc}" for i, doc in enumerate(docs, start=1))
    return (
        "Answer the question using ONLY the sources below. "
        "Cite sources inline like [1]. If the sources are insufficient, say so.\n\n"
        f"Sources:\n{sources}\n\n"
        f"Question: {query}\n"
        "Answer:"
    )


def recall_at_k(retrieved: list[list[int]], relevant: list[set[int]], k: int) -> float:
    """Mean over queries of |top-k retrieved ∩ relevant| / |relevant|."""
    if len(retrieved) != len(relevant):
        raise ValueError("retrieved and relevant must have one entry per query")
    scores = []
    for got, want in zip(retrieved, relevant):
        if not want:
            raise ValueError("each query needs at least one relevant doc")
        scores.append(len(set(got[:k]) & want) / len(want))
    return float(sum(scores) / len(scores))


CORPUS = [
    "Transformers use self-attention to weigh the relevance of every token to every other token.",
    "Photosynthesis converts sunlight, water, and carbon dioxide into glucose and oxygen.",
    "The token bucket algorithm enforces API rate limits by refilling tokens at a fixed rate.",
    "Retrieval-augmented generation grounds model answers in documents fetched at query time.",
    "Gradient descent updates model weights in the direction that reduces the loss.",
]


if __name__ == "__main__":
    embedder = HashedNGramEmbedder(dim=256, n=3)

    # 1. Embedder is deterministic, unit-norm, and case/whitespace-insensitive.
    v1, v2 = embedder.embed("hello world"), embedder.embed("hello world")
    assert np.array_equal(v1, v2)
    assert abs(np.linalg.norm(v1) - 1.0) < 1e-9
    assert np.allclose(embedder.embed("Hello   WORLD"), v1)
    assert not np.allclose(embedder.embed("goodbye moon"), v1)

    # 2. Known queries retrieve the right doc at rank 1.
    index = VectorIndex(embedder)
    index.add(CORPUS)
    results = index.search("how does self-attention work in transformers", k=3)
    assert results[0][0] == 0, f"expected doc 0 first, got {results}"
    assert results[0][1] > results[1][1]  # scores sorted descending
    assert index.search("what is retrieval augmented generation", k=2)[0][0] == 3
    assert index.search("rate limiting with token buckets", k=1)[0][0] == 2

    # 3. Prompt assembly carries numbered citations and the query.
    top_docs = [CORPUS[i] for i, _ in results[:2]]
    prompt = build_prompt("How does attention work?", top_docs)
    assert "[1] " + CORPUS[0] in prompt
    assert "[2]" in prompt and "How does attention work?" in prompt

    # 4. recall@k against hand-computed values.
    retrieved = [[0, 2, 1], [3, 1, 0]]
    relevant = [{0}, {1, 4}]
    assert recall_at_k(retrieved, relevant, k=2) == (1.0 + 0.5) / 2   # 0.75
    assert recall_at_k(retrieved, relevant, k=1) == (1.0 + 0.0) / 2   # 0.5
    assert recall_at_k([[1], [1]], [{1}, {1}], k=1) == 1.0

    # 5. End-to-end eval on the live index: golden set is fully recovered.
    golden = {"self-attention in transformers": {0},
              "grounding answers with retrieval": {3},
              "api rate limiting": {2}}
    got = [[i for i, _ in index.search(q, k=2)] for q in golden]
    assert recall_at_k(got, list(golden.values()), k=2) == 1.0

    print("All tests passed.")
