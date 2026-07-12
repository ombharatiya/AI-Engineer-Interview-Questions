"""Challenge 01 - Attention from scratch (Medium).

PROBLEM
-------
Using only numpy, implement:

1. softmax(x: np.ndarray, axis: int = -1) -> np.ndarray
   Numerically stable softmax along `axis`.

2. causal_mask(t: int) -> np.ndarray
   Boolean (t, t) mask where entry [i, j] is True iff position i may attend
   to position j (i.e. j <= i).

3. scaled_dot_product_attention(q, k, v, mask=None) -> (output, weights)
   q: (..., T_q, d_k), k: (..., T_k, d_k), v: (..., T_k, d_v).
   mask: optional bool array broadcastable to (..., T_q, T_k); True = keep,
   False = block. Returns output (..., T_q, d_v) and weights (..., T_q, T_k)
   whose rows sum to 1.

4. multi_head_attention(x, w_q, w_k, w_v, w_o, n_heads, causal=True) -> np.ndarray
   x: (T, d_model); each weight: (d_model, d_model); d_model % n_heads == 0.
   Split heads, attend per head, concatenate, project. Returns (T, d_model).

Constraint: no Python loops over sequence positions or heads - use
reshape/transpose/broadcasting.

INTERVIEW NOTES
---------------
A strong solution: subtracts the row max before exp; scales scores by
1/sqrt(d_k) BEFORE softmax; applies the mask as -inf on the scores (masking
weights after softmax leaves rows that don't sum to 1); splits heads with a
(T, H, d_h) -> (H, T, d_h) transpose.

Common mistakes: scaling by d_k instead of sqrt(d_k); using np.triu when you
mean np.tril; a wrong transpose when splitting heads (shapes check out,
values are silently wrong); forgetting the output projection w_o.

Follow-up variations: why sqrt(d_k)? (dot-product variance grows with d_k,
saturating softmax and killing gradients); grouped-query / multi-query
attention (share K/V across heads to shrink the KV cache); FlashAttention
(tiling + online softmax so the (T, T) matrix never materialises in HBM);
cross-attention (K/V come from a different sequence than Q).
"""
from __future__ import annotations

import numpy as np


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x_max = np.max(x, axis=axis, keepdims=True)
    e = np.exp(x - x_max)
    return e / np.sum(e, axis=axis, keepdims=True)


def causal_mask(t: int) -> np.ndarray:
    return np.tril(np.ones((t, t), dtype=bool))


def scaled_dot_product_attention(
    q: np.ndarray,
    k: np.ndarray,
    v: np.ndarray,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    d_k = q.shape[-1]
    scores = q @ np.swapaxes(k, -1, -2) / np.sqrt(d_k)  # (..., T_q, T_k)
    if mask is not None:
        # -inf, not 0: after softmax the blocked positions get exactly 0 weight
        # and each row still sums to 1.
        scores = np.where(mask, scores, -np.inf)
    weights = softmax(scores, axis=-1)
    return weights @ v, weights


def multi_head_attention(
    x: np.ndarray,
    w_q: np.ndarray,
    w_k: np.ndarray,
    w_v: np.ndarray,
    w_o: np.ndarray,
    n_heads: int,
    causal: bool = True,
) -> np.ndarray:
    t, d_model = x.shape
    assert d_model % n_heads == 0, "d_model must be divisible by n_heads"
    d_head = d_model // n_heads

    def split(m: np.ndarray) -> np.ndarray:
        # (T, d_model) -> (H, T, d_head); transpose, don't reshape directly to
        # (H, T, d_head) - that would interleave positions across heads.
        return m.reshape(t, n_heads, d_head).transpose(1, 0, 2)

    q, k, v = split(x @ w_q), split(x @ w_k), split(x @ w_v)
    mask = causal_mask(t) if causal else None  # broadcasts over the head axis
    out, _ = scaled_dot_product_attention(q, k, v, mask)  # (H, T, d_head)
    out = out.transpose(1, 0, 2).reshape(t, d_model)  # concat heads
    return out @ w_o


if __name__ == "__main__":
    rng = np.random.default_rng(0)

    # --- softmax: stability and correctness ---
    s = softmax(np.array([1e4, 1e4 + 1.0, 1e4 + 2.0]))
    assert np.all(np.isfinite(s)) and np.isclose(s.sum(), 1.0)
    assert np.allclose(s, softmax(np.array([0.0, 1.0, 2.0])))  # shift invariant

    # --- scaled dot-product attention vs hand-computed values ---
    # d_k = 1 so the scale is 1. scores = [[1, 0], [0, 0]].
    q = k = np.array([[1.0], [0.0]])
    v = np.array([[1.0], [2.0]])
    out, w = scaled_dot_product_attention(q, k, v)
    e = np.e
    assert np.allclose(w[0], [e / (e + 1), 1 / (e + 1)])
    assert np.allclose(w[1], [0.5, 0.5])
    assert np.allclose(out, [[(e + 2) / (e + 1)], [1.5]])

    # --- causal masking: zero weight on the future, rows still sum to 1 ---
    t, d = 5, 8
    x = rng.normal(size=(t, d))
    _, w = scaled_dot_product_attention(x, x, x, mask=causal_mask(t))
    assert np.allclose(w.sum(axis=-1), 1.0)
    assert np.all(w[np.triu_indices(t, k=1)] == 0.0)

    # --- batched shapes broadcast correctly ---
    qb = rng.normal(size=(2, 4, 7, 8))  # (batch, heads, T, d_k)
    kb = rng.normal(size=(2, 4, 7, 8))
    vb = rng.normal(size=(2, 4, 7, 16))
    ob, wb = scaled_dot_product_attention(qb, kb, vb, mask=causal_mask(7))
    assert ob.shape == (2, 4, 7, 16) and wb.shape == (2, 4, 7, 7)

    # --- multi-head with 1 head and identity w_o == single-head attention ---
    d_model = 8
    x = rng.normal(size=(6, d_model))
    w_q, w_k, w_v = (rng.normal(size=(d_model, d_model)) for _ in range(3))
    mha_out = multi_head_attention(x, w_q, w_k, w_v, np.eye(d_model), n_heads=1)
    ref, _ = scaled_dot_product_attention(x @ w_q, x @ w_k, x @ w_v, causal_mask(6))
    assert np.allclose(mha_out, ref)

    # --- multi-head: shape, and causality end to end ---
    w_o = rng.normal(size=(d_model, d_model))
    out1 = multi_head_attention(x, w_q, w_k, w_v, w_o, n_heads=4)
    assert out1.shape == (6, d_model)
    x2 = x.copy()
    x2[-1] += 10.0  # perturb only the last token
    out2 = multi_head_attention(x2, w_q, w_k, w_v, w_o, n_heads=4)
    assert np.allclose(out1[:-1], out2[:-1]), "earlier positions saw the future"
    assert not np.allclose(out1[-1], out2[-1])

    print("All tests passed.")
