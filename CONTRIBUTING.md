# Contributing

Contributions are welcome - this repo gets better with every question, correction, and case study the community adds. The bar is simple: **would this help someone pass an AI Engineer interview in the next 12 months?**

## What to contribute

- **New questions** you were actually asked (anonymise the company if needed) - these are the most valuable contributions.
- **Better answers** - tighter, more accurate, more current.
- **Corrections** - wrong formulas, outdated claims, dead links. Open an issue or PR directly.
- **New coding challenges** - must be self-contained, numpy/stdlib-only, with assert-based tests.
- **New system design case studies** - follow the template in [11-ai-system-design](11-ai-system-design/).

## Question format

Every question in a `questions.md` file follows this exact structure:

```markdown
### N. <Question as an interviewer would phrase it>

<details><summary><b>Answer</b></summary>

<150-400 words. Direct answer first, then depth: tradeoffs, concrete numbers, examples.>

**Follow-ups:** <1-3 probing follow-up questions an interviewer might ask next.>

</details>
```

Rules:

- The blank lines after `<summary>` and before `</details>` are **required** - GitHub won't render Markdown inside `<details>` without them.
- Number questions sequentially across the whole file (1..N, never reset per section).
- Place the question under the right difficulty header: `## Basic`, `## Intermediate`, or `## Advanced`.
- Python for code samples, mermaid for diagrams.

## Style rules

- **Direct answer in the first sentence.** Write the answer a strong candidate would give, not an essay about the topic.
- **No hype, no filler.** Delete every sentence that starts with "In today's rapidly evolving...".
- **Accuracy over coverage.** Never invent paper titles, benchmark numbers, or URLs. Label approximate figures with `~`.
- **Vendor-neutral.** Draw examples across OpenAI, Anthropic, Google, and open-source ecosystems.
- **House style.** International English spelling, straight quotes, plain hyphens rather than em dashes.

## Coding challenge rules

- One file per challenge in [12-coding-challenges](12-coding-challenges/).
- Module docstring with the **problem statement** (function signatures, constraints) and **interview notes** (what a strong solution demonstrates).
- Reference solution with type hints.
- `if __name__ == "__main__":` block with real assert-based tests, ending with `print("All tests passed.")`.
- Dependencies: numpy and the standard library only. The file must run with `python3 <file>`.

## PR checklist

- [ ] Follows the format above (collapsible answers render correctly - check the *Preview* tab).
- [ ] Question numbering in touched files is still sequential with no gaps.
- [ ] Any Python file you touched runs clean: `python3 <file>` prints `All tests passed.`
- [ ] Links point to canonical sources (arXiv abstract pages, official docs) and actually resolve.
- [ ] No copyrighted content pasted from books or paywalled courses.

## Reporting problems

Open an issue with the file path and, for technical errors, a source supporting the correction. "This answer is wrong because X, see Y" gets merged fast.
