"""Challenge 02 - Byte-level BPE tokenizer: train, encode, decode (Medium).

PROBLEM
-------
Implement a byte-level Byte Pair Encoding tokenizer (stdlib only):

class BPETokenizer:
    def train(self, text: str, vocab_size: int) -> None
        Start from the 256 raw bytes. Repeatedly find the most frequent
        adjacent token pair in the corpus and merge it into a new token,
        until the vocab reaches `vocab_size` (or no pairs remain).
        Break frequency ties deterministically.

    def encode(self, text: str) -> list[int]
        Apply the learned merges to arbitrary text. Merges must be applied
        in the ORDER they were learned (lowest merge rank first), not
        greedily left-to-right.

    def decode(self, ids: list[int]) -> str
        Invert encode. decode(encode(s)) == s for ANY string s, including
        text never seen in training (byte-level means no <unk>).

INTERVIEW NOTES
---------------
A strong solution: works on raw UTF-8 bytes so any unicode round-trips;
applies merges by training rank at encode time (the classic GPT-2 approach:
repeatedly merge the pair with the lowest rank present); keeps train() and
encode() logic consistent so encoding the training text reproduces the
final training state.

Common mistakes: operating on Python chars instead of bytes (then decode
crashes on unseen characters); merging greedily left-to-right at encode
time (produces different tokens than training did); nondeterministic
tie-breaking (dict order) so two training runs disagree; O(n^2) scans that
time out on a big corpus - fine here, but say how you'd fix it (pair-count
deltas / priority queue, as in the original Sennrich-style implementations).

Follow-up variations: why byte-level vs char-level (no OOV, 256-symbol
base alphabet); pre-tokenization with a regex (GPT-2 splits on words so
merges never cross spaces - why?); special tokens and why they're inserted
outside BPE; how tokenizer choice affects arithmetic/code performance.
"""
from __future__ import annotations


def _pair_counts(ids: list[int]) -> dict[tuple[int, int], int]:
    counts: dict[tuple[int, int], int] = {}
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    return counts


def _merge(ids: list[int], pair: tuple[int, int], new_id: int) -> list[int]:
    """Replace every non-overlapping occurrence of `pair` with `new_id`."""
    out: list[int] = []
    i = 0
    while i < len(ids):
        if i + 1 < len(ids) and (ids[i], ids[i + 1]) == pair:
            out.append(new_id)
            i += 2
        else:
            out.append(ids[i])
            i += 1
    return out


class BPETokenizer:
    def __init__(self) -> None:
        self.merges: dict[tuple[int, int], int] = {}  # pair -> new token id
        self.vocab: dict[int, bytes] = {i: bytes([i]) for i in range(256)}

    def train(self, text: str, vocab_size: int) -> None:
        assert vocab_size >= 256, "byte-level BPE needs at least 256 tokens"
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}
        ids = list(text.encode("utf-8"))
        while len(self.vocab) < vocab_size:
            counts = _pair_counts(ids)
            if not counts:
                break
            # Highest count wins; ties broken by smallest pair -> deterministic.
            pair = min(counts, key=lambda p: (-counts[p], p))
            new_id = len(self.vocab)
            self.merges[pair] = new_id
            self.vocab[new_id] = self.vocab[pair[0]] + self.vocab[pair[1]]
            ids = _merge(ids, pair, new_id)

    def encode(self, text: str) -> list[int]:
        ids = list(text.encode("utf-8"))
        while len(ids) >= 2:
            # Merge the pair that was learned EARLIEST among pairs present.
            # Token ids double as merge ranks (lower id == learned earlier).
            pairs = set(zip(ids, ids[1:]))
            best = min(pairs, key=lambda p: self.merges.get(p, float("inf")))
            if best not in self.merges:
                break  # nothing left to merge
            ids = _merge(ids, best, self.merges[best])
        return ids

    def decode(self, ids: list[int]) -> str:
        data = b"".join(self.vocab[i] for i in ids)
        # errors="replace": a token sequence sliced mid-codepoint shouldn't crash
        return data.decode("utf-8", errors="replace")


if __name__ == "__main__":
    corpus = (
        "the quick brown fox jumps over the lazy dog. "
        "the quicker brown foxes jump over the lazier dogs. "
        "tokenizers turn text into tokens; the best tokenizers are boring. "
    ) * 20

    tok = BPETokenizer()
    tok.train(corpus, vocab_size=300)

    # --- vocab size and merge bookkeeping ---
    assert len(tok.vocab) == 300
    assert len(tok.merges) == 44  # 300 - 256
    assert all(len(tok.vocab[i]) >= 2 for i in range(256, 300))

    # --- round-trip on training text ---
    assert tok.decode(tok.encode(corpus)) == corpus

    # --- round-trip on UNSEEN text, including multibyte unicode ---
    unseen = "Héllo, 世界! Zebras quiz vexed jockeys - 🚀 naïve café №42"
    assert tok.decode(tok.encode(unseen)) == unseen

    # --- compression: trained text uses fewer tokens than raw bytes ---
    n_bytes = len(corpus.encode("utf-8"))
    n_tokens = len(tok.encode(corpus))
    assert n_tokens < 0.6 * n_bytes, f"weak compression: {n_tokens}/{n_bytes}"

    # --- frequent word compresses; encode matches training-time merges ---
    # Note: without pre-tokenization, merges cross word boundaries, so the
    # learned token is " the " (spaces included) - exactly why GPT-2 style
    # tokenizers regex-split into words BEFORE running BPE.
    the_ids = tok.encode(" the ")
    assert len(the_ids) == 1 and tok.vocab[the_ids[0]] == b" the "
    assert tok.decode(the_ids) == " the "

    # --- determinism: retraining gives identical merges ---
    tok2 = BPETokenizer()
    tok2.train(corpus, vocab_size=300)
    assert tok2.merges == tok.merges
    assert tok2.encode(unseen) == tok.encode(unseen)

    # --- edge cases ---
    assert tok.encode("") == []
    assert tok.decode([]) == ""
    single = "\x00"  # raw byte outside any merge
    assert tok.decode(tok.encode(single)) == single

    # --- untrained tokenizer degrades to plain UTF-8 bytes ---
    fresh = BPETokenizer()
    assert fresh.encode("ab") == [97, 98]
    assert fresh.decode([97, 98]) == "ab"

    print("All tests passed.")
