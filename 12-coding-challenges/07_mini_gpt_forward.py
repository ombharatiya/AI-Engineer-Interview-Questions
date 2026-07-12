"""Challenge 07 - Mini GPT Forward Pass (Hard)

PROBLEM
-------
Implement the full forward pass of a decoder-only transformer (GPT-style) in
pure numpy. No autograd, no training - just inference-time math.

Architecture (GPT-2 style, pre-norm):

    token embeddings + learned position embeddings
    -> N x [ LayerNorm -> causal multi-head self-attention -> residual add
             LayerNorm -> MLP (4x expansion, GELU)         -> residual add ]
    -> final LayerNorm
    -> logits via tied embedding matrix (x @ W_emb.T)

Required signatures:

    init_params(cfg: GPTConfig, seed: int = 0) -> dict
    gpt_forward(params: dict, cfg: GPTConfig, token_ids, return_attn=False)
        token_ids: int array of shape (batch, seq_len)
        returns logits of shape (batch, seq_len, vocab_size)
        (and, if return_attn, a list of per-layer attention weight tensors
        of shape (batch, n_heads, seq_len, seq_len))

Constraints:
- Tiny config: vocab 64, d_model 32, 2 layers, 4 heads, max_seq_len 16.
- Attention must be causal: position i may attend only to positions <= i.
- Softmax must be numerically stable (subtract the row max).

INTERVIEW NOTES
---------------
A strong solution demonstrates:
- Correct pre-norm residual wiring (norm INSIDE the residual branch; post-norm
  is the original 2017 layout and a common mix-up).
- Head split/merge done with reshape+transpose, not Python loops over heads.
- Scaling scores by 1/sqrt(head_dim), not 1/sqrt(d_model).
- The causality argument: masking scores (not weights) before softmax so each
  row renormalizes over the visible prefix only.
Common mistakes: forgetting the mask entirely (tests below catch it), masking
with 0 instead of -inf/-1e9, applying LayerNorm over the sequence axis instead
of the feature axis, and unstable softmax overflowing in float32.
Follow-up variations: add a KV cache and show decode is O(T) per step; swap
learned positions for RoPE; make attention weights optional to save memory;
implement grouped-query attention (fewer K/V heads than Q heads).
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class GPTConfig:
    vocab_size: int = 64
    d_model: int = 32
    n_layers: int = 2
    n_heads: int = 4
    max_seq_len: int = 16


def layer_norm(x: np.ndarray, g: np.ndarray, b: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    mu = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def gelu(x: np.ndarray) -> np.ndarray:
    # tanh approximation, as used in GPT-2.
    return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * x**3)))


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - x.max(axis=axis, keepdims=True)  # stability: exp of <=0 only
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)


def init_params(cfg: GPTConfig, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)

    def w(*shape: int) -> np.ndarray:
        return rng.standard_normal(shape) * 0.02

    def ln() -> dict:
        return {"g": np.ones(cfg.d_model), "b": np.zeros(cfg.d_model)}

    blocks = []
    for _ in range(cfg.n_layers):
        blocks.append({
            "ln1": ln(),
            "attn": {
                "w_qkv": w(cfg.d_model, 3 * cfg.d_model),
                "b_qkv": np.zeros(3 * cfg.d_model),
                "w_o": w(cfg.d_model, cfg.d_model),
                "b_o": np.zeros(cfg.d_model),
            },
            "ln2": ln(),
            "mlp": {
                "w1": w(cfg.d_model, 4 * cfg.d_model),
                "b1": np.zeros(4 * cfg.d_model),
                "w2": w(4 * cfg.d_model, cfg.d_model),
                "b2": np.zeros(cfg.d_model),
            },
        })
    return {"wte": w(cfg.vocab_size, cfg.d_model), "wpe": w(cfg.max_seq_len, cfg.d_model),
            "blocks": blocks, "ln_f": ln()}


def causal_self_attention(x: np.ndarray, p: dict, n_heads: int) -> tuple[np.ndarray, np.ndarray]:
    """Returns (output, attention_weights). x: (B, T, D)."""
    B, T, D = x.shape
    head_dim = D // n_heads

    qkv = x @ p["w_qkv"] + p["b_qkv"]              # (B, T, 3D)
    q, k, v = np.split(qkv, 3, axis=-1)

    def split_heads(t: np.ndarray) -> np.ndarray:  # (B, T, D) -> (B, H, T, hd)
        return t.reshape(B, T, n_heads, head_dim).transpose(0, 2, 1, 3)

    q, k, v = split_heads(q), split_heads(k), split_heads(v)

    scores = q @ k.transpose(0, 1, 3, 2) / np.sqrt(head_dim)   # (B, H, T, T)
    future = np.triu(np.ones((T, T), dtype=bool), k=1)         # True above diagonal
    scores = np.where(future, -1e9, scores)                    # mask BEFORE softmax
    weights = softmax(scores, axis=-1)

    out = weights @ v                                          # (B, H, T, hd)
    out = out.transpose(0, 2, 1, 3).reshape(B, T, D)           # merge heads
    return out @ p["w_o"] + p["b_o"], weights


def gpt_forward(params: dict, cfg: GPTConfig, token_ids, return_attn: bool = False):
    ids = np.asarray(token_ids)
    B, T = ids.shape
    assert T <= cfg.max_seq_len, "sequence longer than max_seq_len"

    x = params["wte"][ids] + params["wpe"][:T]     # (B, T, D)
    attn_maps = []
    for blk in params["blocks"]:
        a, w = causal_self_attention(layer_norm(x, **blk["ln1"]), blk["attn"], cfg.n_heads)
        x = x + a                                  # pre-norm residual
        h = layer_norm(x, **blk["ln2"])
        m = blk["mlp"]
        x = x + gelu(h @ m["w1"] + m["b1"]) @ m["w2"] + m["b2"]
        attn_maps.append(w)

    x = layer_norm(x, **params["ln_f"])
    logits = x @ params["wte"].T                   # weight tying
    return (logits, attn_maps) if return_attn else logits


if __name__ == "__main__":
    cfg = GPTConfig()
    params = init_params(cfg, seed=0)
    rng = np.random.default_rng(42)
    B, T = 2, 10
    ids = rng.integers(0, cfg.vocab_size, size=(B, T))

    # 1. Output shape.
    logits, attn_maps = gpt_forward(params, cfg, ids, return_attn=True)
    assert logits.shape == (B, T, cfg.vocab_size)
    assert len(attn_maps) == cfg.n_layers
    assert attn_maps[0].shape == (B, cfg.n_heads, T, T)

    # 2. Attention softmax rows sum to 1, and future positions get zero weight.
    for w in attn_maps:
        assert np.allclose(w.sum(axis=-1), 1.0)
        assert np.allclose(w[..., np.triu_indices(T, k=1)[0], np.triu_indices(T, k=1)[1]], 0.0)

    # 3. Causality: changing a FUTURE token must not change past logits.
    t = 6
    ids2 = ids.copy()
    ids2[:, t] = (ids2[:, t] + 1) % cfg.vocab_size
    logits2 = gpt_forward(params, cfg, ids2)
    assert np.allclose(logits[:, :t], logits2[:, :t], rtol=0.0, atol=1e-12), \
        "past logits changed when a future token changed - attention is not causal"
    # ...and the changed position itself SHOULD produce different logits.
    assert not np.allclose(logits[:, t], logits2[:, t])

    # 4. Next-token distribution is a valid probability distribution.
    probs = softmax(logits, axis=-1)
    assert np.allclose(probs.sum(axis=-1), 1.0)
    assert (probs >= 0).all()

    # 5. Works at max context length.
    ids_full = rng.integers(0, cfg.vocab_size, size=(1, cfg.max_seq_len))
    assert gpt_forward(params, cfg, ids_full).shape == (1, cfg.max_seq_len, cfg.vocab_size)

    print("All tests passed.")
