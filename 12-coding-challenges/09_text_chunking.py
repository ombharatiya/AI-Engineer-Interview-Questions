"""Challenge 09 - Text Chunking Strategies (Easy)

PROBLEM
-------
Implement four chunkers used in RAG ingestion pipelines:

    chunk_fixed(text, size) -> list[str]
        Non-overlapping fixed-size chunks. Concatenating the chunks must
        reconstruct the original text exactly.

    chunk_sliding(text, size, overlap) -> list[str]
        Sliding window: each chunk is at most `size` chars and consecutive
        chunks share exactly `overlap` chars (step = size - overlap).
        Every character of the text must be covered. overlap < size required.

    chunk_sentences(text, max_size) -> list[str]
        Split into sentences (on ., !, ? followed by whitespace), then greedily
        pack whole sentences into chunks of at most `max_size` chars. A single
        sentence longer than max_size is hard-split so the invariant holds.

    chunk_recursive(text, max_size, separators=("\n\n", "\n", ". ", "")) -> list[str]
        Recursive splitter (LangChain-style): try the coarsest separator first;
        pieces still over max_size fall through to finer separators, ending
        with a raw character split. Separators stay attached to the preceding
        piece so that "".join(chunks) == text.

All chunkers must return only non-empty chunks and respect their size bound.

INTERVIEW NOTES
---------------
A strong solution demonstrates:
- Treating chunker properties as invariants (coverage, max size, overlap)
  and testing the invariants rather than hard-coding expected chunk lists.
- Correct sliding-window arithmetic: step = size - overlap, and the guard
  overlap < size (step <= 0 loops forever - a classic bug).
- In the recursive splitter, keeping separators attached so no characters are
  silently dropped; naive str.split() loses them and corrupts offsets.
- Knowing WHY each strategy exists: fixed is simple but cuts mid-sentence;
  overlap protects boundary context at the cost of index bloat (size 512 /
  overlap 128 stores ~1.33x the text); sentence/recursive respect semantics.
Common mistakes: dropping the tail chunk, empty-string chunks, off-by-one at
the last window, and recursion that never terminates on separator-free text.
Follow-ups: return (chunk, start_offset) pairs for citation highlighting;
token-based sizes with a real tokenizer; semantic chunking via embedding
similarity between adjacent sentences.
"""

import re


def chunk_fixed(text: str, size: int) -> list[str]:
    if size <= 0:
        raise ValueError("size must be positive")
    return [text[i:i + size] for i in range(0, len(text), size)]


def chunk_sliding(text: str, size: int, overlap: int) -> list[str]:
    if not 0 <= overlap < size:
        raise ValueError("require 0 <= overlap < size")
    if not text:
        return []
    step = size - overlap
    chunks = []
    for start in range(0, len(text), step):
        chunks.append(text[start:start + size])
        if start + size >= len(text):  # this window reached the end
            break
    return chunks


_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def split_sentences(text: str) -> list[str]:
    return [s for s in _SENTENCE_END.split(text) if s]


def chunk_sentences(text: str, max_size: int) -> list[str]:
    if max_size <= 0:
        raise ValueError("max_size must be positive")
    chunks: list[str] = []
    buf = ""
    for sent in split_sentences(text):
        if len(sent) > max_size:            # oversized sentence: flush + hard split
            if buf:
                chunks.append(buf)
                buf = ""
            chunks.extend(chunk_fixed(sent, max_size))
            continue
        candidate = f"{buf} {sent}" if buf else sent
        if len(candidate) <= max_size:
            buf = candidate
        else:
            chunks.append(buf)
            buf = sent
    if buf:
        chunks.append(buf)
    return chunks


def _split_keep_sep(text: str, sep: str) -> list[str]:
    """Split on sep, keeping sep attached to the preceding piece."""
    parts = text.split(sep)
    return [p + sep for p in parts[:-1]] + ([parts[-1]] if parts[-1] else [])


def chunk_recursive(text: str, max_size: int,
                    separators: tuple[str, ...] = ("\n\n", "\n", ". ", "")) -> list[str]:
    if max_size <= 0:
        raise ValueError("max_size must be positive")
    if len(text) <= max_size:
        return [text] if text else []
    sep, rest = separators[0], separators[1:]
    if sep == "":                            # base case: raw character split
        return chunk_fixed(text, max_size)
    if sep not in text:
        return chunk_recursive(text, max_size, rest)

    chunks: list[str] = []
    buf = ""
    for part in _split_keep_sep(text, sep):
        if len(buf) + len(part) <= max_size:
            buf += part                      # greedy merge of small pieces
        else:
            if buf:
                chunks.append(buf)
            if len(part) > max_size:         # still too big: finer separator
                chunks.extend(chunk_recursive(part, max_size, rest))
                buf = ""
            else:
                buf = part
    if buf:
        chunks.append(buf)
    return chunks


if __name__ == "__main__":
    text = (
        "Retrieval quality gates RAG quality. Chunking is the first lever.\n\n"
        "Fixed windows are simple but cut sentences in half. Overlap keeps "
        "boundary context. Sentence packing respects meaning!\n"
        "Recursive splitting tries paragraphs, then lines, then sentences. "
        "Does it terminate? Yes, the character fallback guarantees it."
    )

    # 1. Fixed: exact coverage, max size respected, no empty chunks.
    for size in (7, 50, 1000):
        chunks = chunk_fixed(text, size)
        assert "".join(chunks) == text
        assert all(0 < len(c) <= size for c in chunks)

    # 2. Sliding: full coverage, size bound, exact overlap between neighbours.
    size, overlap = 40, 10
    chunks = chunk_sliding(text, size, overlap)
    step = size - overlap
    covered = set()
    for i, c in enumerate(chunks):
        assert len(c) <= size
        covered.update(range(i * step, i * step + len(c)))
    assert covered == set(range(len(text))), "sliding chunks must cover every char"
    for a, b in zip(chunks, chunks[1:]):
        assert len(a) == size, "only the final chunk may be short"
        assert a[-overlap:] == b[:overlap], "adjacent chunks must share `overlap` chars"
    assert chunk_sliding("", 10, 3) == []
    try:
        chunk_sliding(text, 10, 10)
        assert False, "overlap == size must raise"
    except ValueError:
        pass

    # 3. Sentences: size bound; every sentence's content survives, in order.
    max_size = 80
    schunks = chunk_sentences(text, max_size)
    assert all(0 < len(c) <= max_size for c in schunks)
    joined = " ".join(schunks)
    for sent in split_sentences(text):
        if len(sent) <= max_size:
            assert sent in joined
    long_sent = "x" * 205
    assert chunk_sentences(long_sent, 100) == ["x" * 100, "x" * 100, "x" * 5]

    # 4. Recursive: lossless (separators kept), size bound, prefers coarse cuts.
    for max_size in (30, 60, 120):
        rchunks = chunk_recursive(text, max_size)
        assert "".join(rchunks) == text, "recursive chunking must be lossless"
        assert all(0 < len(c) <= max_size for c in rchunks)
    para_chunks = chunk_recursive(text, 200)
    assert para_chunks[0].endswith("\n\n"), "should split at paragraph boundary first"
    assert chunk_recursive("abcdefgh", 3) == ["abc", "def", "gh"]  # char fallback
    assert chunk_recursive("", 10) == []

    print("All tests passed.")
