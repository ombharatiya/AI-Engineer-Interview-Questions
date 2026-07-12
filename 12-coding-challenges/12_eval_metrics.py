"""Challenge 12 - Eval Metrics: pass@k, QA F1, Model-Graded Harness (Medium)

PROBLEM
-------
Implement three evaluation building blocks:

1. pass_at_k(n, c, k) -> float
   Unbiased estimator of pass@k for code generation (Chen et al., 2021,
   "Evaluating Large Language Models Trained on Code"): given n samples of
   which c passed, estimate P(at least one of k random samples passes):
       pass@k = 1 - C(n-c, k) / C(n, k)
   Compute it in the numerically stable product form
       1 - prod_{i=n-c+1..n} (1 - k/i)
   never materializing huge binomial coefficients.

2. SQuAD-style QA metrics:
       normalize_answer(s) - lowercase, strip punctuation, drop articles
                              (a/an/the), collapse whitespace
       exact_match(pred, gold) -> float   (0.0 or 1.0, on normalized text)
       token_f1(pred, gold) -> float      (multiset token overlap F1;
                              if either normalized side is empty, EM instead)

3. A minimal model-graded (LLM-as-judge) pairwise harness:
       pairwise_eval(judge, examples, rubric) -> EvalReport
   - judge is an injected callable: judge(prompt: str) -> str
   - for each example, build a judge prompt from the rubric and BOTH answer
     orders (position swap), parse the two verdicts, and score:
     consistent winner -> win; both TIE -> tie; disagreement -> inconsistent
   - report wins_a, wins_b, ties, inconsistent, and win_rate_a
     (ties and inconsistent count 0.5).

INTERVIEW NOTES
---------------
A strong solution demonstrates:
- WHY the naive estimator (fraction of tasks where any of the first k samples
  pass) is biased for k < n, and why the combinatorial form fixes it.
- Numerical maturity: C(200, 100) ~ 9e58 still fits in float64, but
  C(2000, 1000) ~ 2e600 overflows it (float64 max ~1.8e308); the product form
  never leaves [0, 1].
- Knowing the official SQuAD normalization steps by heart - most homegrown
  F1 implementations forget article stripping and get systematically lower
  scores than reported baselines.
- Position bias is THE failure mode of pairwise LLM judges; swapping answer
  order and requiring agreement is the standard mitigation.
Common mistakes: pass@k returning >1 or negative for edge cases (c=0, c=n,
n-c<k); F1 using set intersection instead of multiset (double-counted tokens);
judge harness trusting a single ordering; parsing judge output with equality
instead of tolerant matching.
Follow-ups: confidence intervals on pass@k via bootstrap; length-bias
controls for judges; Elo aggregation across many model pairs; agreement
metrics (Cohen's kappa) between judge and humans.
"""

import math
import re
import string
from collections import Counter
from dataclasses import dataclass
from typing import Callable

# ------------------------------------------------------------------ pass@k


def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased pass@k estimate from n samples with c successes."""
    if not 0 <= c <= n or not 1 <= k <= n:
        raise ValueError("require 0 <= c <= n and 1 <= k <= n")
    if n - c < k:
        return 1.0  # every size-k draw must contain a passing sample
    prob_all_fail = 1.0
    for i in range(n - c + 1, n + 1):  # stable: product of factors in (0, 1)
        prob_all_fail *= 1.0 - k / i
    return 1.0 - prob_all_fail


# ------------------------------------------------------------------ QA metrics

_ARTICLES = re.compile(r"\b(a|an|the)\b")
_PUNCT = set(string.punctuation)


def normalize_answer(s: str) -> str:
    s = s.lower()
    s = "".join(ch for ch in s if ch not in _PUNCT)
    s = _ARTICLES.sub(" ", s)
    return " ".join(s.split())


def exact_match(pred: str, gold: str) -> float:
    return float(normalize_answer(pred) == normalize_answer(gold))


def token_f1(pred: str, gold: str) -> float:
    p_tokens = normalize_answer(pred).split()
    g_tokens = normalize_answer(gold).split()
    if not p_tokens or not g_tokens:
        return float(p_tokens == g_tokens)  # SQuAD convention for empty sides
    overlap = sum((Counter(p_tokens) & Counter(g_tokens)).values())  # multiset
    if overlap == 0:
        return 0.0
    precision = overlap / len(p_tokens)
    recall = overlap / len(g_tokens)
    return 2 * precision * recall / (precision + recall)


# ------------------------------------------------------------------ judge harness

JUDGE_TEMPLATE = """You are an impartial grader. Rubric: {rubric}

Question: {question}

FIRST answer: {first}

SECOND answer: {second}

Which answer better satisfies the rubric? Reply with exactly one word:
FIRST, SECOND, or TIE."""


@dataclass
class Example:
    question: str
    answer_a: str
    answer_b: str


@dataclass
class EvalReport:
    wins_a: int
    wins_b: int
    ties: int
    inconsistent: int
    verdicts: list[str]

    @property
    def win_rate_a(self) -> float:
        n = len(self.verdicts)
        return (self.wins_a + 0.5 * (self.ties + self.inconsistent)) / n if n else 0.0


def _parse_verdict(raw: str) -> str:
    word = raw.strip().upper().split()[0].strip(".,!") if raw.strip() else ""
    if word in ("FIRST", "SECOND", "TIE"):
        return word.lower()
    raise ValueError(f"unparseable judge output: {raw!r}")


def pairwise_eval(judge: Callable[[str], str], examples: list[Example],
                  rubric: str) -> EvalReport:
    wins_a = wins_b = ties = inconsistent = 0
    verdicts: list[str] = []
    for ex in examples:
        # Run both orderings to control for position bias.
        v_ab = _parse_verdict(judge(JUDGE_TEMPLATE.format(
            rubric=rubric, question=ex.question, first=ex.answer_a, second=ex.answer_b)))
        v_ba = _parse_verdict(judge(JUDGE_TEMPLATE.format(
            rubric=rubric, question=ex.question, first=ex.answer_b, second=ex.answer_a)))
        pick_1 = {"first": "A", "second": "B", "tie": "tie"}[v_ab]
        pick_2 = {"first": "B", "second": "A", "tie": "tie"}[v_ba]  # swapped order
        if pick_1 == pick_2 == "A":
            wins_a += 1; verdicts.append("A")
        elif pick_1 == pick_2 == "B":
            wins_b += 1; verdicts.append("B")
        elif pick_1 == pick_2 == "tie":
            ties += 1; verdicts.append("tie")
        else:  # orderings disagree -> judge is position-sensitive here
            inconsistent += 1; verdicts.append("inconsistent")
    return EvalReport(wins_a, wins_b, ties, inconsistent, verdicts)


if __name__ == "__main__":
    # 1. pass@k against hand-computed values.
    assert abs(pass_at_k(5, 2, 2) - 0.7) < 1e-12          # 1 - C(3,2)/C(5,2) = 7/10
    assert pass_at_k(10, 0, 5) == 0.0
    assert pass_at_k(10, 10, 1) == 1.0
    assert pass_at_k(5, 4, 2) == 1.0                       # n-c=1 < k=2
    assert abs(pass_at_k(4, 1, 1) - 0.25) < 1e-12
    for n, c, k in [(20, 7, 5), (100, 13, 10), (50, 50, 25), (30, 1, 30)]:
        exact = 1.0 - math.comb(n - c, k) / math.comb(n, k)
        assert abs(pass_at_k(n, c, k) - exact) < 1e-12     # matches comb form
    assert 0.0 <= pass_at_k(2000, 3, 100) <= 1.0           # stable at scale
    try:
        pass_at_k(5, 6, 1); assert False
    except ValueError:
        pass

    # 2. EM + F1 edge cases.
    assert exact_match("The Eiffel Tower.", "eiffel tower") == 1.0  # articles/punct
    assert exact_match("Paris", "London") == 0.0
    assert token_f1("same answer", "same answer") == 1.0
    assert token_f1("", "nonempty") == 0.0
    assert token_f1("nonempty", "") == 0.0
    assert token_f1("", "") == 1.0
    assert token_f1("the a an", "") == 1.0                 # normalizes to empty
    assert abs(token_f1("The cat sat", "cat sat down") - 0.8) < 1e-12
    assert token_f1("completely wrong", "right answer") == 0.0
    assert abs(token_f1("cat cat cat", "cat") - 0.5) < 1e-12  # multiset, not set

    # 3. Judge harness with a deterministic mock judge.
    def mock_judge(prompt: str) -> str:
        """Prefers whichever answer contains '42' - position-consistent."""
        first = re.search(r"FIRST answer: (.*)\n", prompt).group(1)
        second = re.search(r"SECOND answer: (.*)\n", prompt).group(1)
        if ("42" in first) == ("42" in second):
            return "TIE"
        return "FIRST" if "42" in first else "second."     # parser must cope

    examples = [
        Example("Meaning of life?", "It is 42.", "Unknowable."),   # A wins
        Example("Meaning of life?", "No idea.", "Clearly 42."),    # B wins
        Example("Meaning of life?", "42", "It is 42."),            # tie
    ]
    report = pairwise_eval(mock_judge, examples, rubric="Factual accuracy.")
    assert (report.wins_a, report.wins_b, report.ties, report.inconsistent) == (1, 1, 1, 0)
    assert abs(report.win_rate_a - (1 + 0.5) / 3) < 1e-12
    assert report.verdicts == ["A", "B", "tie"]

    # 4. Position-biased judge (always says FIRST) -> flagged inconsistent.
    biased = pairwise_eval(lambda prompt: "FIRST", examples, rubric="anything")
    assert biased.inconsistent == 3 and biased.wins_a == 0
    assert abs(biased.win_rate_a - 0.5) < 1e-12            # bias doesn't inflate A

    print("All tests passed.")
