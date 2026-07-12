"""Challenge 04 - Positional encodings: sinusoidal + RoPE (Medium).

PROBLEM
-------
Numpy only:

1. sinusoidal_encoding(n_positions: int, d_model: int) -> np.ndarray
   The "Attention Is All You Need" table, shape (n_positions, d_model):
       PE[pos, 2i]   = sin(pos / 10000^(2i / d_model))
       PE[pos, 2i+1] = cos(pos / 10000^(2i / d_model))
   d_model is even. Build it vectorized (no double loop).

2. apply_rope(x, positions=None, base=10000.0) -> np.ndarray
   Rotary Position Embedding, half-split ("rotate half") convention as used
   by Llama / GPT-NeoX. x has shape (..., T, d) with d even; dimension pair
   (j, j + d/2) is rotated by angle pos * theta_j, theta_j = base^(-2j/d).
   `positions` is an optional (T,) int array (defaults to 0..T-1) - needed
   for KV-cache decode, where the new token's position is not 0.

INTERVIEW NOTES
---------------
A strong solution: knows RoPE rotates Q and K *inside* attention (it is not
added to embeddings like sinusoidal PE); can state the key property - the
rotation makes q_m . k_n depend only on the offset m - n, giving relative
position from an absolute encoding; mentions that rotations preserve norms
so attention logit scale is unchanged; accepts explicit positions (cache-
aware) rather than assuming 0..T-1.

Common mistakes: mixing the interleaved (original paper, pairs (2i, 2i+1))
and half-split (pairs (i, i + d/2)) conventions - both are valid but
incompatible, a classic source of broken checkpoint conversions; wrong
frequency exponent (theta_j must span 1 down to ~1/base across dims);
adding RoPE to V (it belongs on Q and K only).

Follow-up variations: why low dims rotate fast and high dims slow
(multi-scale positional resolution); context extension - position
interpolation and NTK-aware / YaRN scaling of theta; ALiBi as a bias-based
alternative; why learned absolute embeddings fail to extrapolate.
"""
from __future__ import annotations

import numpy as np


def sinusoidal_encoding(n_positions: int, d_model: int) -> np.ndarray:
    assert d_model % 2 == 0
    pos = np.arange(n_positions)[:, None]            # (T, 1)
    i = np.arange(d_model // 2)[None, :]             # (1, d/2)
    angles = pos / (10000.0 ** (2 * i / d_model))    # (T, d/2)
    pe = np.empty((n_positions, d_model))
    pe[:, 0::2] = np.sin(angles)
    pe[:, 1::2] = np.cos(angles)
    return pe


def apply_rope(
    x: np.ndarray,
    positions: np.ndarray | None = None,
    base: float = 10000.0,
) -> np.ndarray:
    t, d = x.shape[-2], x.shape[-1]
    assert d % 2 == 0
    if positions is None:
        positions = np.arange(t)
    theta = base ** (-np.arange(0, d, 2) / d)        # (d/2,) frequencies
    angles = positions[:, None] * theta[None, :]     # (T, d/2)
    cos, sin = np.cos(angles), np.sin(angles)
    x1, x2 = x[..., : d // 2], x[..., d // 2:]
    # 2-D rotation of each (x1_j, x2_j) pair by its angle
    return np.concatenate([x1 * cos - x2 * sin, x1 * sin + x2 * cos], axis=-1)


if __name__ == "__main__":
    rng = np.random.default_rng(0)

    # --- sinusoidal: hand-computed values, d_model=4 ---
    # theta for dim pairs: [1, 1/100] since 10000^(2*1/4) = 100.
    pe = sinusoidal_encoding(8, 4)
    assert pe.shape == (8, 4)
    assert np.allclose(pe[0], [0.0, 1.0, 0.0, 1.0])          # pos 0: sin=0, cos=1
    assert np.allclose(pe[1], [np.sin(1), np.cos(1), np.sin(0.01), np.cos(0.01)])
    assert np.allclose(pe[5, 2], np.sin(5 / 100.0))

    # --- each (sin, cos) pair lies on the unit circle ---
    pe = sinusoidal_encoding(50, 64)
    assert np.allclose(pe[:, 0::2] ** 2 + pe[:, 1::2] ** 2, 1.0)
    # values bounded (unlike learned embeddings, no growth with position)
    assert np.all(np.abs(pe) <= 1.0)

    # --- RoPE: position 0 is the identity rotation ---
    d = 16
    q = rng.normal(size=(1, d))
    assert np.allclose(apply_rope(q, positions=np.array([0])), q)

    # --- RoPE preserves norms (pure rotation) ---
    x = rng.normal(size=(7, d))
    rx = apply_rope(x)
    assert np.allclose(np.linalg.norm(rx, axis=-1), np.linalg.norm(x, axis=-1))

    # --- THE property: q_m . k_n depends only on the offset m - n ---
    qv = rng.normal(size=(1, d))
    kv = rng.normal(size=(1, d))

    def rot_dot(m: int, n: int) -> float:
        qm = apply_rope(qv, positions=np.array([m]))
        kn = apply_rope(kv, positions=np.array([n]))
        return float((qm @ kn.T).item())

    assert np.isclose(rot_dot(3, 7), rot_dot(10, 14), atol=1e-9)     # offset -4
    assert np.isclose(rot_dot(0, 5), rot_dot(100, 105), atol=1e-9)   # offset -5
    assert not np.isclose(rot_dot(3, 7), rot_dot(3, 8), atol=1e-6)   # offset matters

    # --- explicit positions match the default range (KV-cache decode) ---
    full = apply_rope(x)
    last = apply_rope(x[-1:], positions=np.array([6]))
    assert np.allclose(full[-1:], last), "cached decode must pass true position"

    # --- batched input: leading axes broadcast (e.g. heads) ---
    xb = rng.normal(size=(2, 4, 7, d))  # (batch, heads, T, d)
    rb = apply_rope(xb)
    assert rb.shape == xb.shape
    assert np.allclose(rb[1, 2], apply_rope(xb[1, 2]))

    # --- rotation is linear: rope(a+b) == rope(a) + rope(b) ---
    a, b = rng.normal(size=(5, d)), rng.normal(size=(5, d))
    assert np.allclose(apply_rope(a + b), apply_rope(a) + apply_rope(b))

    print("All tests passed.")
