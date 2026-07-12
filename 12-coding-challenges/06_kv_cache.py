"""Challenge 06 - Autoregressive decoding with vs. without a KV cache (Medium).

PROBLEM
-------
Given a toy single-layer causal-attention language model (provided: embedding
matrix, Wq/Wk/Wv/Wo, unembedding matrix), implement greedy decoding two ways
and prove they are equivalent:

1. generate_no_cache(model, prompt_ids, n_new) -> list[int]
   Every step re-runs the FULL forward pass over the whole sequence and takes
   the last position's logits. Per-step attention cost: O(T^2).

2. generate_with_cache(model, prompt_ids, n_new) -> list[int]
   Keep K and V for every processed position. Each step embeds ONE token,
   computes its q/k/v, appends k/v to the cache, and attends the single query
   over all cached keys. Per-step attention cost: O(T). No causal mask needed
 - the cache only contains the past.

Both must produce byte-identical token sequences and (near-)identical logits.
Instrument the model to count q.k score dot-products as a FLOP proxy and show
the cached path does asymptotically less work.

INTERVIEW NOTES
---------------
A strong solution: explains WHY caching is exact (causal attention means
k/v at past positions never change when a token is appended; only the new
query is needed); attends the new query over ALL cached positions including
itself; notes the memory bill - per token the cache stores
2 * n_layers * n_kv_heads * d_head values, which is why long contexts are
memory-bound and why GQA/MQA shrink n_kv_heads.

Common mistakes: applying a causal mask in the cached path and accidentally
masking valid past positions; recomputing k/v for the whole prefix each step
(cache exists but saves nothing); forgetting positional information - with
RoPE the new token must be rotated by its TRUE absolute position, not 0
(this toy model omits positions to keep the diff focused on caching).

Follow-up variations: prefill vs decode phases (compute-bound vs memory-
bandwidth-bound); continuous batching; PagedAttention (vLLM) for cache
fragmentation; cache quantization (fp8 KV); sliding-window attention and
attention sinks as cache-eviction strategies; speculative decoding.
"""
from __future__ import annotations

import numpy as np


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / np.sum(e, axis=axis, keepdims=True)


class TinyDecoder:
    """One causal self-attention layer + residual + unembedding."""

    def __init__(self, vocab_size: int, d_model: int, seed: int = 0) -> None:
        rng = np.random.default_rng(seed)
        s = 1.0 / np.sqrt(d_model)
        self.emb = rng.normal(0.0, s, (vocab_size, d_model))
        self.w_q = rng.normal(0.0, s, (d_model, d_model))
        self.w_k = rng.normal(0.0, s, (d_model, d_model))
        self.w_v = rng.normal(0.0, s, (d_model, d_model))
        self.w_o = rng.normal(0.0, s, (d_model, d_model))
        self.w_u = rng.normal(0.0, s, (d_model, vocab_size))  # unembedding
        self.d_model = d_model
        self.score_dots = 0  # number of q.k dot products computed (FLOP proxy)

    def forward_full(self, token_ids: list[int]) -> np.ndarray:
        """Recompute everything. Returns logits for every position: (T, V)."""
        x = self.emb[np.asarray(token_ids)]                      # (T, d)
        q, k, v = x @ self.w_q, x @ self.w_k, x @ self.w_v
        t = len(token_ids)
        self.score_dots += t * t
        scores = q @ k.T / np.sqrt(self.d_model)                 # (T, T)
        scores = np.where(np.tril(np.ones((t, t), dtype=bool)), scores, -np.inf)
        h = x + softmax(scores) @ v @ self.w_o                   # residual
        return h @ self.w_u                                      # (T, V)

    def forward_step(
        self, token_id: int, cache: dict[str, list[np.ndarray]]
    ) -> np.ndarray:
        """Process ONE new token using the KV cache. Returns logits: (V,)."""
        x = self.emb[token_id]                                   # (d,)
        q = x @ self.w_q
        cache["k"].append(x @ self.w_k)
        cache["v"].append(x @ self.w_v)
        k = np.stack(cache["k"])                                 # (T_past+1, d)
        v = np.stack(cache["v"])
        self.score_dots += k.shape[0]
        scores = k @ q / np.sqrt(self.d_model)                   # (T_past+1,)
        h = x + softmax(scores) @ v @ self.w_o
        return h @ self.w_u                                      # (V,)


def generate_no_cache(
    model: TinyDecoder, prompt_ids: list[int], n_new: int
) -> list[int]:
    ids = list(prompt_ids)
    for _ in range(n_new):
        logits = model.forward_full(ids)          # O(T^2) attention, every step
        ids.append(int(np.argmax(logits[-1])))
    return ids


def generate_with_cache(
    model: TinyDecoder, prompt_ids: list[int], n_new: int
) -> list[int]:
    ids = list(prompt_ids)
    cache: dict[str, list[np.ndarray]] = {"k": [], "v": []}
    logits = None
    for tok in prompt_ids:                        # prefill (token by token here)
        logits = model.forward_step(tok, cache)
    for _ in range(n_new):                        # decode: O(T) per step
        nxt = int(np.argmax(logits))
        ids.append(nxt)
        logits = model.forward_step(nxt, cache)
    return ids


if __name__ == "__main__":
    vocab, d_model, n_new = 50, 16, 20
    prompt = [1, 7, 42]

    # --- exactness: the two decoding paths agree token for token ---
    m1 = TinyDecoder(vocab, d_model)
    out_full = generate_no_cache(m1, prompt, n_new)
    ops_full = m1.score_dots

    m2 = TinyDecoder(vocab, d_model)  # same seed -> identical weights
    out_cache = generate_with_cache(m2, prompt, n_new)
    ops_cache = m2.score_dots

    assert out_full == out_cache, f"{out_full} != {out_cache}"
    assert len(out_full) == len(prompt) + n_new
    assert len(set(out_full[len(prompt):])) >= 4, \
        "degenerate generation; equivalence test would prove little"

    # --- per-step logits agree numerically, not just argmax ---
    m3 = TinyDecoder(vocab, d_model)
    cache: dict[str, list[np.ndarray]] = {"k": [], "v": []}
    for i, tok in enumerate(out_full):
        step_logits = m3.forward_step(tok, cache)
        full_logits = m3.forward_full(out_full[: i + 1])[-1]
        assert np.allclose(step_logits, full_logits, atol=1e-10)

    # --- the cache state has one k and one v per processed token ---
    assert len(cache["k"]) == len(cache["v"]) == len(out_full)
    assert cache["k"][0].shape == (d_model,)

    # --- work: cached decoding does asymptotically less ---
    # no-cache: sum of T^2 over steps; cache: sum of T (here T runs 3..22).
    t0, T = len(prompt), len(prompt) + n_new
    assert ops_full == sum(t * t for t in range(t0, T))
    assert ops_cache == sum(range(1, T + 1))
    assert ops_cache < ops_full / 10, (ops_cache, ops_full)

    # --- prompt is preserved verbatim ---
    assert out_full[: len(prompt)] == prompt

    print(f"score dot-products  no cache: {ops_full}   with cache: {ops_cache}")
    print("All tests passed.")
