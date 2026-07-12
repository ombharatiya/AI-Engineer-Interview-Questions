# ⌨️ Cursor (Anysphere) - AI Engineer Interview Guide

> **Last reviewed: July 2026.** Based only on public information - official pages, engineering blogs, and publicly shared candidate reports. Processes change and vary by team; treat this as a map, not a contract. No confidential or leaked material.

## TL;DR

- The centrepiece is famous and publicly confirmed by the CEO: **every engineer and designer goes through an on-site work trial** - reported as up to two days - with a desk, a laptop, and a frozen snapshot of the real codebase. You build something real instead of whiteboarding. This is the decision round.
- Earlier stages are lighter: a recruiter/manager screen plus one or more 60-minute technical screens with **practical problems** (file-system dedup, hash trees, editor/streaming primitives) - not LeetCode-puzzle grinding.
- **AI tools are often permitted in coding rounds** (reported), but with scoped-query expectations - pasting whole problems into a model reads as a negative. Judgment about model output is itself the signal.
- **Authentic product usage is close to a hard requirement.** Multiple public reports say interviewers can tell within minutes whether you actually work in Cursor daily. Come with real opinions about tab, agent mode, and what's broken.
- The work trial doubles as a **mutual cultural interview**: meals with the team, informal conversations, founder-level chats for many roles. They're a small, talent-obsessed team screening for self-motivated ICs who go end-to-end.

## Company context

Anysphere builds Cursor, the AI code editor - tab (next-edit prediction), inline edits, codebase-aware chat, agent mode, and background agents - used by millions of developers, plus their own custom models for completion and fast code application. It's one of the fastest-growing software products ever (publicly reported to have hit $100M ARR roughly 20 months after launch), built by a deliberately small team, which is exactly the draw: enormous surface area per engineer. "AI engineer" at Cursor means shipping the full stack around models - retrieval/indexing over huge codebases, low-latency inference, agent harnesses, evals, and editor UX - often training or fine-tuning their own models rather than only wrapping frontier APIs.

## Roles & titles they hire

From their careers page (July 2026):

- **Software Engineer** - with many specialisations posted: Agent Evaluation, Infrastructure, ML, Bugbot, Security, Storage, Billing
- **Research Scientist** (RL / mid-training research, owning ambiguous research problems end-to-end)
- **Design Engineer**
- **Data Platform Engineer**
- **Field Engineer / Forward Deployed Engineer** and **Solutions Architect** (enterprise-facing)
- **Technical Support Engineer**
- **Engineering Manager** (Core Services, Desktop, Infrastructure, ML)

Their careers page is explicit about culture: they "obsess over talent to an unusual degree" and are building "a haven for self-motivated individual contributors."

## The interview loop

The work-trial onsite is unusually well documented - CEO Michael Truell has described it on the a16z and Lenny's podcasts, and Business Insider covered it. Earlier-stage details come from third-party guides and candidate reports, so treat those rows as directionally right, not gospel.

| Stage | Format | What's evaluated |
|---|---|---|
| Recruiter/manager screen | 30-45 min call | Why Cursor specifically, genuine interest in the problem space, product usage. (reported, varies) |
| Technical phone screen(s) | 1-3 rounds, ~60 min live coding | Practical problems: file-system/dedup tasks, hash trees over repo data, streaming/editor primitives. Clean working code, communication. AI tools reportedly allowed for scoped queries. (reported, varies) |
| Take-home | Some senior/staff loops | A project of similar weight to the onsite, done async. (reported, varies) |
| **On-site work trial** | Reported as up to two days in SF; desk, laptop, frozen codebase snapshot; some reports describe an ~8-hour project variant, sometimes remote | Can you go end-to-end in an unfamiliar real codebase? What do you build when left alone without direction? Raw technical skill, autonomy, product taste. **This is the decision round.** |
| Culture / team fit | Meals and informal conversations woven through the trial; founder-level conversation for many roles | Passion for the problem space vs. job-shopping; mutual fit. (publicly described by CEO) |

Two caveats worth knowing. First, logistics vary by role and seniority - public reports describe both a two-day in-office trial and a one-day (~8-hour) project, sometimes remote. Second, **payment for the trial is disputed in public reports**: some third-party guides describe it as paid, while at least one public candidate post described a two-day unpaid trial with IP-assignment language in the agreement. Ask your recruiter directly about compensation and IP terms before the trial - that's a normal, professional question.

## What they emphasise

- **End-to-end ability in a real codebase.** Truell has said the trial tests what a traditional coding interview can't: whether you can navigate an unfamiliar, large codebase and ship a working feature - design, implementation, and polish - with minimal hand-holding.
- **What you build "in a vacuum."** The trial is deliberately under-specified. Product judgment - choosing something valuable and scoping it to fit the time - is evaluated as much as code quality.
- **Authentic daily use of Cursor.** Repeated across public reports: candidates who clearly live in the editor, know its failure modes, and have compared it honestly against competitors do disproportionately well. Skimming the changelog the night before is a known failure mode.
- **Latency and cost obsession.** Their differentiation is a sub-100ms-feeling tab model and fast-apply edits at massive scale. Design conversations reward concrete latency budgets, caching strategy, and cost-per-request reasoning over generic architecture talk.
- **Working with AI, with judgment.** Where AI tools are allowed, they expect you to use them the way a strong engineer does - targeted queries, sceptical review, fast rejection of bad suggestions - not delegation of the whole problem.
- **Self-motivated ICs at high intensity.** A small team shipping at unusual speed; the culture conversation probes comfort with ambiguity, pace, and ownership without process scaffolding.

## Representative questions

*Representative questions synthesised from this company's publicly known focus areas and role descriptions - not leaked questions.*

### 1. Design Cursor's tab (next-edit prediction) system: it must feel instant - sub-100ms perceived latency - for millions of daily users. Walk me through the stack.

<details><summary><b>Answer</b></summary>

Start with the latency budget, because it drives everything: ~100ms perceived leaves maybe 50-70ms for inference after network and client overhead. That immediately rules out frontier-API calls and forces a **small custom model** (low single-digit billions of parameters or less), served on dedicated GPUs, likely with quantization (INT8/FP8) and aggressive batching tuned for latency, not throughput.

Key components: (1) **Client-side context assembly** - recent edits, cursor position, visible file region, and a small set of related snippets, prepacked so the request is one shot. (2) **Prefix/KV caching** - consecutive keystrokes share almost all context; caching the prompt prefix across requests within a session is the single biggest win. (3) **Debounce + speculative requests** - fire on pause heuristics, cancel stale requests when the user keeps typing; most requests die before completion, so cheap cancellation matters. (4) **Streaming + early rendering** - show the first tokens of the prediction while the rest streams. (5) **Regional serving** - RTT to a single US region blows the budget from Europe/Asia.

Quality loop: log accept/reject/partial-accept per suggestion; acceptance rate and retained-characters-after-N-seconds are the north-star offline/online metrics; train on accepted-edit data. Cost: at millions of DAU and dozens of requests per user per minute, unit economics dominate - smaller model + cache hit rate is the lever, not GPU count.

**Follow-ups:** How do you cancel in-flight GPU work cheaply? What breaks in your KV-cache scheme when the user edits the middle of a file rather than appending?

</details>

### 2. How would you index a 100k-file monorepo so an AI editor can retrieve relevant context - and keep the index fresh as the user edits?

<details><summary><b>Answer</b></summary>

Two-layer design: a **sync layer** that detects what changed cheaply, and a **retrieval layer** over chunks.

Sync: hash every file, build a **Merkle tree** over the directory structure (Cursor has publicly described using Merkle trees for codebase indexing). Comparing root hashes tells you in O(1) whether anything changed; walking mismatched subtrees finds exactly which files changed in O(changed × depth) instead of rescanning 100k files. This makes continuous re-sync viable on every save.

Chunking: split by code structure (tree-sitter functions/classes), not fixed windows - a function is the natural retrieval unit. Store embeddings in a vector index keyed by chunk hash so unchanged chunks are never re-embedded; an edit to one function re-embeds only that chunk.

Retrieval: hybrid. Embeddings for semantic queries ("where do we handle auth retries"), plus exact-match/symbol search (grep, LSP definitions/references) for identifiers - embeddings are notoriously weak on exact symbol lookup. Re-rank the union, then pack into the context budget with file paths and line numbers so the model can cite and edit precisely.

Practical constraints worth raising: privacy (embed server-side but store only hashes/vectors, not plaintext, as Cursor describes publicly), embedding cost at fleet scale (dedupe identical chunks across users - vendored dependencies are shared), and cold-start latency for a fresh clone (prioritise open files and imports first, backfill the rest).

**Follow-ups:** When does retrieval lose to just stuffing a long-context model? How do you evaluate retrieval quality for code specifically?

</details>

### 3. The model is streaming a multi-file edit while the user keeps typing in one of those files. How do you apply the edits without corrupting the buffer?

<details><summary><b>Answer</b></summary>

The core problem is that the model's edits are anchored to a **stale snapshot** of the buffer. Naive line-number application corrupts the file the moment the user inserts a line above the edit site.

The standard solution is snapshot + rebase. Record the document version the model saw. Represent model output as a diff against that snapshot (ranges, not line numbers alone - include surrounding text for verification). As user keystrokes arrive, they generate operations against the live buffer. Before applying a model edit, **transform its ranges through every user operation since the snapshot** - the same operational-transform bookkeeping collaborative editors use, but you only need one-directional transformation (model edits rebased onto user edits; the user always wins conflicts).

Concrete failure handling: if the user edited *inside* a region the model is rewriting, the rebase is ambiguous - don't guess. Mark that hunk conflicted, drop or re-request it, and apply the clean hunks. Verify anchors before applying: check the context lines still match; if not, fall back to a fuzzy re-anchor (search nearby for the expected text) with a strict threshold.

Streaming adds one more wrinkle: don't apply token-by-token into the real buffer. Accumulate into a shadow copy and apply per-hunk atomic edits with undo-stack integration, so one Ctrl+Z reverts one logical AI edit, not 400 micro-inserts. Multi-file edits should commit as a single workspace transaction with a preview/diff state, so the user can reject file 3 without unwinding files 1-2.

**Follow-ups:** How does your design change for two users plus an agent (three writers)? How do you make the whole multi-file apply atomically undoable?

</details>

### 4. Implement the core of a text buffer for an editor: efficient insert/delete at arbitrary positions and fast line lookup. What structure do you pick?

<details><summary><b>Answer</b></summary>

A flat string is O(n) per edit - fine until files hit megabytes and an agent makes thousands of edits. The two serious candidates are a **rope** (balanced tree of string chunks) and a **piece table** (original buffer + append-only add buffer + a list of pieces referencing them). VS Code famously uses a piece tree - a piece table indexed by a balanced tree - which is the right default answer for an editor with undo and large files.

Minimal piece-table sketch:

```python
from dataclasses import dataclass

@dataclass
class Piece:
    source: str   # "orig" or "add"
    start: int
    length: int

class PieceTable:
    def __init__(self, text: str):
        self.orig, self.add = text, ""
        self.pieces = [Piece("orig", 0, len(text))] if text else []

    def insert(self, pos: int, text: str) -> None:
        start = len(self.add)
        self.add += text
        new = Piece("add", start, len(text))
        i, offset = self._locate(pos)
        p = self.pieces[i]
        left = Piece(p.source, p.start, offset)
        right = Piece(p.source, p.start + offset, p.length - offset)
        self.pieces[i:i+1] = [pc for pc in (left, new, right) if pc.length]
```

With a plain list, `_locate` is O(pieces); production versions put pieces in a balanced tree with subtree character counts and **line-break counts** cached per node, making position→line and line→position O(log n). Piece tables also give near-free undo (pieces are immutable references) and cheap snapshots - which matters when an AI is diffing against a snapshot while the user types (see Q3).

**Follow-ups:** Where does a piece table degrade (long editing sessions fragmenting pieces)? How would you store line-start offsets to keep line lookup O(log n) after edits?

</details>

### 5. Your agent model outputs an edited version of a 500-line file. Applying it verbatim is slow and error-prone. How do you make "apply" fast and reliable?

<details><summary><b>Answer</b></summary>

Three broad strategies, in ascending sophistication:

1. **Ask the model for a diff** (search/replace blocks or unified diff). Cheap in tokens, but models are unreliable diff emitters - line numbers drift, context lines get paraphrased, and malformed hunks need fuzzy matching and repair heuristics. Workable, fragile at the tail.

2. **Full-file rewrite** by the frontier model. Most reliable output format, but slow and expensive: 500 lines is thousands of output tokens at frontier-model decode speeds - many seconds of user-visible latency.

3. **A dedicated fast-apply model with speculative decoding** - the approach Cursor has publicly written about. The insight: most of the output file is *identical to the input*. Use the original file as the speculation source: feed chunks of the current file as draft tokens, and the model only "takes over" generation where the edit actually diverges, then re-syncs. Because verification of draft tokens is parallel while generation is serial, unchanged regions fly through at very high token rates. Cursor has described this as speculative edits, reaching effective speeds around 1000 tokens/sec - turning a many-second apply into sub-second.

Whatever the mechanism, wrap it in verification: the applied result should parse (run tree-sitter/syntax check), the diff shown to the user should be computed from actual before/after buffers (never trust the model's own claimed diff), and failures should degrade to strategy 2 rather than corrupting the file.

**Follow-ups:** Why does speculative decoding preserve exactness of the target model's distribution? When does the plan-with-frontier-model, apply-with-small-model split break down?

</details>

### 6. How do you evaluate a code-editing model before shipping it? Design the offline and online eval story for tab or agent edits.

<details><summary><b>Answer</b></summary>

Separate three layers, because they fail independently.

**Offline, automatic:** a benchmark of real editing tasks - (repo state, instruction/edit-context, held-out ground truth). Metrics: exact/AST-level match for small edits; for larger tasks, **execution-based** checks - does the repo still build, do hidden tests pass? Execution beats string similarity: there are many correct edits that don't match the reference. Guard against contamination (the model may have trained on the repos) by mining fresh commits from after the training cutoff.

**Offline, judged:** for agentic multi-step tasks, use an LLM judge with a rubric (correctness, scope discipline - did it touch files it shouldn't?, style consistency). Calibrate the judge against a few hundred human-labelled examples and report agreement; an uncalibrated judge is a random-number generator with confidence.

**Online:** the metrics that actually decide launches. For tab: suggestion acceptance rate, and - more robust - **retained characters after N seconds/minutes**, because users accept bad suggestions and then delete them. For agent edits: fraction of applied diffs surviving to commit, follow-up-fix rate, task abandonment. Ship via interleaved A/B on a small traffic slice; completion models are cheap enough to run shadow inference (new model predicts, old model serves) to compare offline metrics on live traffic before any user sees it.

The meta-point interviewers want: offline evals gate iteration speed, online metrics gate launch, and the two disagree often enough that you need both.

**Follow-ups:** Acceptance rate went up 2% but retained-characters went down - what happened? How do you eval retrieval (Q2) separately from generation?

</details>

### 7. An agent needs to iterate on code - run builds, tests, lints - without disturbing what the user sees in their editor. How do you architect that?

<details><summary><b>Answer</b></summary>

This is the problem Cursor publicly described as the "shadow workspace": give the AI its own working copy plus real feedback signals (LSP diagnostics, build errors, test results) while guaranteeing the user's session is untouched.

Design axes:

**Isolation level.** Options in ascending cost: (a) in-memory overlay - agent edits live only in a virtual file system layered over the real one, and language servers are asked to diagnose against overlay contents; (b) a hidden second editor/LSP instance running against the overlay, so the agent gets full go-to-definition/diagnostics without touching disk; (c) full copy - git worktree or container - required the moment the agent must *execute* code, because builds and tests read from disk and running arbitrary code demands sandboxing (resource limits, no network by default, no access to user credentials).

**Feedback loop.** The agent's edit-check-revise loop is only as good as its signals: surface compiler/LSP errors verbatim, test failures with stack traces, and diff-scoped lint results. Structured errors beat raw stdout for model consumption.

**Reconciliation.** The user kept editing while the agent worked, so merging back is a rebase problem (same machinery as Q3): present the agent's work as a reviewable diff against current state, flag conflicts, never auto-apply to dirty files.

**Cost control.** Duplicate LSP instances and containers per agent run are expensive; pool them, hibernate idle ones, and cap concurrent agent sessions per machine.

**Follow-ups:** What syscall/network policy do you set for the test-execution sandbox? How does this extend to background agents running remotely on a repo the user doesn't have checked out?

</details>

### 8. Coding: given a repository snapshot (path → content), build a Merkle tree and write the function that returns which files changed between two snapshots without comparing every file's content.

<details><summary><b>Answer</b></summary>

Hash leaves (files), then hash children's hashes upward through directories. Diffing two trees: if root hashes match, done; otherwise recurse only into children whose hashes differ.

```python
import hashlib
from dataclasses import dataclass, field

def h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

@dataclass
class Node:
    hash: str
    children: dict = field(default_factory=dict)  # name -> Node; empty = file

def build(paths: dict[str, str]) -> Node:
    root = Node("", {})
    for path, content in sorted(paths.items()):
        parts, cur = path.split("/"), root
        for p in parts[:-1]:
            cur = cur.children.setdefault(p, Node("", {}))
        cur.children[parts[-1]] = Node(h(content.encode()))
    def finalize(node: Node) -> str:
        if node.children:
            combined = "".join(
                name + finalize(c) for name, c in sorted(node.children.items()))
            node.hash = h(combined.encode())
        return node.hash
    finalize(root)
    return root

def diff(a: Node | None, b: Node | None, prefix="") -> list[str]:
    if a and b and a.hash == b.hash:
        return []                      # identical subtree: skip entirely
    if not (a and a.children) and not (b and b.children):
        return [prefix.rstrip("/")]    # file added/removed/modified
    changed, names = [], set((a.children if a else {}) | (b.children if b else {}))
    for n in sorted(names):
        changed += diff(a.children.get(n) if a else None,
                        b.children.get(n) if b else None, prefix + n + "/")
    return changed
```

Points to narrate: sorting children makes hashes deterministic; cost is O(changed files × depth), which is why this pattern powers incremental codebase indexing (Q2); include file mode/name in the leaf hash in production; and note the empty-`children` ambiguity between files and empty dirs - state your convention.

**Follow-ups:** How do you handle renames (content hash matches at a new path)? Where would you persist the tree so a restart doesn't rescan the repo?

</details>

### 9. Long context windows keep getting cheaper. Why not drop retrieval and stuff the whole repo into context for every request?

<details><summary><b>Answer</b></summary>

Because the three costs - latency, dollars, and attention quality - all scale with context length, and an editor's request volume is extreme.

**Latency:** prefill cost grows roughly linearly (attention worse) with prompt length. A 500k-token prompt can add many seconds of time-to-first-token - fatal for interactive editing where the budget is sub-second, absurd for tab where it's sub-100ms. Prefix caching helps only if the long prefix is stable across requests; real editing mutates files constantly, invalidating cached prefixes mid-file.

**Dollars:** editors generate orders of magnitude more requests than chat apps. Paying for 100-500k input tokens per request, dozens of times per session, versus 5-20k retrieved tokens is a 10-50x unit-cost difference at fleet scale.

**Quality:** long-context models still exhibit position-dependent degradation ("lost in the middle") and distraction from irrelevant code; a request about auth handling doesn't benefit from 80k tokens of vendored CSS. Focused, well-ranked context frequently *beats* full-repo stuffing on answer quality, not just cost.

The honest synthesis: it's a spectrum, and the right point moves with model economics. Long context is winning for medium scopes - whole files plus their import neighbourhood, agent sessions that need cross-file state. Retrieval remains the outer loop that selects *which* megabyte of a multi-gigabyte monorepo deserves the window. Design the system so the context budget is a tunable parameter, and re-evaluate quarterly as prices drop - an answer that acknowledges the trend reads better than a dogmatic defence of RAG.

**Follow-ups:** How does prompt caching change this math for agent loops specifically? What repo size makes full stuffing physically impossible today?

</details>

### 10. Design the harness for an agent that makes multi-file changes from a natural-language task. How do you keep it from wrecking a codebase?

<details><summary><b>Answer</b></summary>

Structure it as a loop with hard guardrails rather than trusting model judgment.

**Loop:** gather context (retrieval + LSP over the repo, Q2) → plan (explicit step list, especially for multi-file tasks) → act via a small tool set (read file, search, edit, run command) → observe structured feedback (diagnostics, test output) → revise. Cap iterations and tokens; agents that loop are burning money and usually stuck - surface "I'm stuck because X" over silent retries.

**Damage control is the actual question:**
- **Checkpointing:** snapshot before every edit batch (shadow git commits or piece-table snapshots), so any state is one-click restorable. Users forgive wrong edits they can revert instantly; they don't forgive lost work.
- **Scope discipline:** track files-touched against task scope; an agent asked to fix a test that starts editing CI configs should trip a wire and ask.
- **Review as the default gate:** the agent's output is a proposed diff, reviewed hunk-by-hunk - not applied changes. Auto-apply is an opt-in for low-risk operations.
- **Sandboxed execution** for anything it runs (Q7): no credentials, no network by default, resource limits.
- **Verification before hand-off:** parse edited files, run the narrowest relevant tests, and report results honestly - "edits applied, 2 of 3 tests pass" beats fake confidence.

Evaluate the harness separately from the model (Q6): same model with a better harness routinely doubles task success rates, which is why harness engineering is a first-class job at an AI editor company.

**Follow-ups:** How do you decide when the agent should ask a clarifying question versus proceed? What telemetry tells you the harness, not the model, is the bottleneck?

</details>

### 11. You have two days in our codebase and no assigned task. What do you build, and how do you spend the time? (The work-trial meta-question.)

<details><summary><b>Answer</b></summary>

The trap is treating it as a coding test. It's a judgment test: what do you choose, how do you scope it, and does it ship.

A strong plan for a two-day trial: spend the first 2-3 hours **reading, not writing** - build a map of the architecture, run the product from source, skim recent commits to learn conventions and where activity is. Choose a project that is (a) genuinely useful - ideally a paper cut you've personally hit as a daily user of the product, which is why authentic usage matters so much here; (b) **completable to a demo in the time box**, with a core you can finish by mid-day-two and stretch goals you explicitly label as stretch; (c) touching enough of the stack to show range - some UI, some backend, ideally something model-adjacent - without requiring you to understand everything.

Then work like a teammate, not a candidate: commit in coherent increments with real messages, follow the codebase's existing patterns rather than imposing your own, ask a few sharp questions (asking good questions is signal; asking none is a red flag), and cut scope early and visibly when something takes longer than expected. Reserve the last hours for polish and a demo: a working, honest demo of a small thing beats a broken ambitious one, every time. Public accounts of Cursor's trial say the evaluation is exactly this - end-to-end ability and what you build without direction.

**Follow-ups:** How do you pick between a flashy feature and an unglamorous fix? What would you do if your chosen project turned out to be blocked at hour six?

</details>

### 12. Serving a custom completion model to millions of DAU: walk me through the inference-cost model and your top three levers.

<details><summary><b>Answer</b></summary>

Build the napkin math first. Cost per request ≈ (prefill tokens × cost/token-prefill) + (decode tokens × cost/token-decode), where the underlying unit is GPU-seconds. For a completion model: prompts of a few thousand tokens, outputs of tens of tokens - so **prefill dominates compute** and decode dominates wall-clock per token. Multiply by request rate: millions of DAU × O(10-100) requests/user/day means billions of requests/day; at even a hundredth of a cent each, that's real money, so tenths of milliseconds and cache points matter.

Top levers, in rough order of impact:

1. **Prefix/KV caching.** Consecutive requests in an editing session share almost all their prompt. A high cache-hit rate converts most prefill from compute into memory lookup - plausibly a several-fold cost reduction alone. Design prompts cache-first: stable context (file prefix, retrieved snippets) before volatile context (cursor-local edits).
2. **Model size and quantization.** The smallest model that clears your quality bar (measured by the Q6 eval suite, especially online retained-characters), quantized to INT8/FP8. Halving model size roughly halves both cost and latency - it's the rare lever that improves both.
3. **Batching policy.** Continuous batching raises GPU utilisation; the tension is tail latency. For interactive completion, cap batch delay aggressively (single-digit ms) and absorb the utilisation loss - then reclaim it by cancelling the large fraction of requests the user's next keystroke invalidates before they finish.

Also worth naming: request dedupe/debounce at the client, regional capacity planning against diurnal peaks, and watching P99 - averages hide the experience that makes users disable the feature.

**Follow-ups:** GPU utilisation is 35% but P99 is fine - do you chase it? How does speculative decoding interact with continuous batching?

</details>

## How to prepare

**Repo topics to go deep on, in priority order:**

- **[12-coding-challenges](../12-coding-challenges/)** - every technical stage is build-something-practical: streaming handlers, file-system tasks, hash trees, editor primitives. Practise writing clean, working Python fast, narrating as you go.
- **[11-ai-system-design](../11-ai-system-design/)** - and specifically the **[AI code assistant case study](../11-ai-system-design/case-studies/02-ai-code-assistant.md)**, which is essentially Cursor's product. Do that one until you can whiteboard the tab-latency budget and the indexing pipeline cold.
- **[04-rag-and-retrieval](../04-rag-and-retrieval/)** - codebase context retrieval (chunking by AST, hybrid search, incremental indexing) is core product tech and prime interview material.
- **[08-inference-and-production](../08-inference-and-production/)** - KV/prefix caching, quantization, speculative decoding, batching-vs-latency. They train and serve their own models; cost/latency fluency is a differentiator.
- **[06-agents-and-tool-use](../06-agents-and-tool-use/)** - agent mode, background agents, and Bugbot are where they're hiring; harness design (checkpoints, sandboxing, feedback loops) maps directly.
- **[07-evaluation-and-observability](../07-evaluation-and-observability/)** - they post roles specifically in Agent Evaluation; know acceptance-rate-style online metrics and execution-based offline evals for code.
- **[13-interview-process-and-behavioral](../13-interview-process-and-behavioral/)** - the trial is a two-day behavioural interview disguised as work; scoping, communication, and demo skills decide it.

**Company-specific prep moves:**

1. **Use Cursor seriously for at least a few weeks** - daily, on real projects, including tab, inline edit, agent mode, and Bugbot. Multiple public reports say inauthentic usage is detectable within minutes and is the most common failure mode. Keep a running list of three things you'd fix and one feature you'd build; that list is your product-round answer and your work-trial project shortlist.
2. **Read their engineering blog** (cursor.com/blog) - they've published unusually technical posts on their tab model, fast-apply/speculative edits, and background-agent infrastructure. Interview problems rhyme with what they write about.
3. **Rehearse the work trial format:** pick a large unfamiliar open-source codebase, give yourself one day, and ship a small end-to-end feature with a demo. The skill of ramping into strange code fast is trainable and is exactly what the trial measures.
4. **Prepare latency-budget fluency:** be able to decompose "100ms perceived" into network, queueing, prefill, and decode, with realistic numbers. Their design rounds reportedly reward this specificity.
5. **Clarify trial logistics up front** - duration, payment, and IP terms have varied across public reports; asking directly is professional and protects you.

## Sources

- [Cursor careers page](https://cursor.com/careers) - role titles, culture statements (consulted July 2026)
- [Business Insider coverage (AOL syndication): Cursor's recruiting and two-day work trial, quoting CEO Michael Truell on the a16z podcast](https://www.aol.com/news/cursor-courted-top-engineers-flying-070128578.html)
- [Lenny's Podcast: "The rise of Cursor" - Michael Truell on hiring and the work trial](https://www.lennysnewsletter.com/p/the-rise-of-cursor-michael-truell)
- [a16z on X, summarising Truell on the two-day onsite ("Can they go end-to-end in the codebase?")](https://x.com/a16z/status/1987963295446475108)
- [Exponent: Cursor Software Engineer interview guide](https://www.tryexponent.com/guides/cursor-software-engineer-interview) - third-party; screen formats, AI-tool policy reports
- [techinterview.org: Cursor interview guide](https://www.techinterview.org/companies/cursor/) - third-party; round themes and emphasis reports
- [Interview Coder: Cursor Software Engineer interview](https://www.interviewcoder.co/blog/cursor-software-engineer-interview) - third-party; loop structure reports
- [Blind thread: candidate report of an unpaid two-day work trial](https://www.teamblind.com/post/exploitative-unpaid-work-trials-in-tech-my-experience-interviewing-at-cursor-2k265lxy) - single unverified candidate account; included only as the basis for the payment/IP caveat
