"""Challenge 03 - Sampling strategies: temperature, top-k, top-p, min-p, repetition penalty (Easy).

PROBLEM
-------
Implement the standard LLM decoding toolbox over a 1-D logits vector
(shape (vocab_size,)), numpy only:

1. apply_temperature(logits, temperature) -> logits / T          (T > 0)
2. apply_repetition_penalty(logits, generated_ids, penalty)
   CTRL-style: for every token already generated, divide its logit by
   `penalty` if positive, multiply if negative (penalty > 1 discourages).
3. top_k_filter(logits, k)   -> keep the k highest logits, others -> -inf
4. top_p_filter(logits, p)   -> nucleus: keep the smallest set of tokens
   (by descending probability) whose cumulative probability >= p
5. min_p_filter(logits, min_p) -> keep tokens with prob >= min_p * max_prob
6. sample(logits, *, temperature=1.0, top_k=None, top_p=None, min_p=None,
          repetition_penalty=1.0, generated_ids=(), rng=None) -> int
   Pipeline: penalty -> temperature -> top_k -> top_p -> min_p -> softmax
   -> draw. Filters mark dropped tokens as -inf; softmax renormalizes.

INTERVIEW NOTES
---------------
A strong solution: filters by setting -inf and renormalizing via softmax
(never zeroing probabilities without renormalizing); applies temperature
BEFORE the filters (order changes which tokens survive top-p); always keeps
at least the top token in top-p (p smaller than the max prob must not
produce an empty set).

Common mistakes: dividing probabilities instead of logits by T; top-p on
unsorted cumulative sums; off-by-one at the nucleus boundary (the token that
crosses p is INCLUDED); repetition penalty that multiplies negative logits
by 1/penalty, which *encourages* repeats; forgetting penalty is applied per
unique token, not per occurrence.

Follow-up variations: why min-p adapts better than top-p when the
distribution is flat vs peaked; greedy vs T->0 equivalence; frequency and
presence penalties (additive, per the OpenAI API) vs multiplicative CTRL
penalty; beam search and why it's rare for open-ended chat generation.
"""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x))
    return e / e.sum()


def apply_temperature(logits: np.ndarray, temperature: float) -> np.ndarray:
    assert temperature > 0, "T=0 is greedy decoding; handle it as argmax"
    return logits / temperature


def apply_repetition_penalty(
    logits: np.ndarray, generated_ids: Sequence[int], penalty: float
) -> np.ndarray:
    out = logits.astype(float).copy()
    for i in set(generated_ids):  # per unique token, not per occurrence
        out[i] = out[i] / penalty if out[i] > 0 else out[i] * penalty
    return out


def top_k_filter(logits: np.ndarray, k: int) -> np.ndarray:
    assert 1 <= k <= logits.size
    kth = np.sort(logits)[-k]  # value of the k-th largest logit
    return np.where(logits >= kth, logits, -np.inf)


def top_p_filter(logits: np.ndarray, p: float) -> np.ndarray:
    assert 0 < p <= 1
    probs = softmax(logits)
    order = np.argsort(-probs)  # descending
    csum = np.cumsum(probs[order])
    # First index where cumulative mass reaches p; that token is included,
    # so even p < max_prob keeps the top token.
    cutoff = int(np.searchsorted(csum, p))
    keep = order[: cutoff + 1]
    out = np.full(logits.shape, -np.inf)
    out[keep] = logits[keep]
    return out


def min_p_filter(logits: np.ndarray, min_p: float) -> np.ndarray:
    assert 0 < min_p <= 1
    probs = softmax(logits)
    return np.where(probs >= min_p * probs.max(), logits, -np.inf)


def sample(
    logits: np.ndarray,
    *,
    temperature: float = 1.0,
    top_k: int | None = None,
    top_p: float | None = None,
    min_p: float | None = None,
    repetition_penalty: float = 1.0,
    generated_ids: Sequence[int] = (),
    rng: np.random.Generator | None = None,
) -> int:
    rng = rng or np.random.default_rng()
    x = logits.astype(float)
    if repetition_penalty != 1.0:
        x = apply_repetition_penalty(x, generated_ids, repetition_penalty)
    x = apply_temperature(x, temperature)
    if top_k is not None:
        x = top_k_filter(x, top_k)
    if top_p is not None:
        x = top_p_filter(x, top_p)
    if min_p is not None:
        x = min_p_filter(x, min_p)
    return int(rng.choice(x.size, p=softmax(x)))


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    # Logits chosen so softmax(logits) is exactly [0.5, 0.3, 0.15, 0.05].
    probs = np.array([0.5, 0.3, 0.15, 0.05])
    logits = np.log(probs)
    assert np.allclose(softmax(logits), probs)

    # --- temperature: <1 sharpens, >1 flattens ---
    assert softmax(apply_temperature(logits, 0.5)).max() > probs.max()
    assert softmax(apply_temperature(logits, 2.0)).max() < probs.max()
    hot = softmax(apply_temperature(logits, 100.0))
    assert np.allclose(hot, 0.25, atol=1e-2)  # -> uniform

    # --- top-k keeps exactly k tokens, and the right ones ---
    f = top_k_filter(logits, 2)
    assert np.isfinite(f).sum() == 2 and np.all(np.isinf(f[[2, 3]]))
    assert np.isfinite(top_k_filter(logits, 1)).sum() == 1

    # --- top-p: minimal nucleus, crossing token included ---
    f = top_p_filter(logits, 0.75)  # 0.5 < 0.75, 0.5+0.3 >= 0.75 -> keep {0,1}
    assert np.isfinite(f[[0, 1]]).all() and np.isinf(f[[2, 3]]).all()
    f = top_p_filter(logits, 0.3)  # smaller than max prob: still keeps top token
    assert np.isfinite(f).sum() == 1 and np.isfinite(f[0])
    assert np.isfinite(top_p_filter(logits, 1.0)).sum() == 4  # p=1 keeps all
    renorm = softmax(top_p_filter(logits, 0.75))
    assert np.allclose(renorm[[0, 1]], [0.5 / 0.8, 0.3 / 0.8])  # renormalized

    # --- min-p: threshold is relative to the max probability ---
    f = min_p_filter(logits, 0.2)  # cutoff = 0.2 * 0.5 = 0.1 -> keep {0,1,2}
    assert np.isfinite(f[[0, 1, 2]]).all() and np.isinf(f[3])

    # --- repetition penalty: divide positive, multiply negative ---
    pen = apply_repetition_penalty(np.array([2.0, -2.0, 0.5]), [0, 1, 1], 2.0)
    assert np.allclose(pen, [1.0, -4.0, 0.5])
    # penalised-away token loses probability mass
    p_before = softmax(np.array([2.0, -2.0, 0.5]))
    p_after = softmax(pen)
    assert p_after[0] < p_before[0] and p_after[2] > p_before[2]

    # --- sample(): top_k=1 is greedy regardless of randomness ---
    big = rng.normal(size=1000)
    for _ in range(10):
        assert sample(big, top_k=1, rng=rng) == int(np.argmax(big))

    # --- sample(): empirical frequencies track the distribution ---
    draws = np.array([sample(logits, rng=rng) for _ in range(4000)])
    freq0 = float(np.mean(draws == 0))
    assert 0.45 < freq0 < 0.55, f"token 0 frequency {freq0} far from 0.5"
    # filters actually constrain the support
    draws = {sample(logits, top_p=0.75, rng=rng) for _ in range(500)}
    assert draws <= {0, 1}

    print("All tests passed.")
