"""Challenge 13 - Streaming SSE Parser + Tool-Call Assembler (Hard)

PROBLEM
-------
LLM APIs stream responses as Server-Sent Events over HTTP. The network hands
you raw byte chunks split at ARBITRARY boundaries - mid-line, even mid-way
through a multi-byte UTF-8 character. Implement:

1. SSEParser - incremental push parser.

       feed(chunk: bytes) -> list[SSEEvent]   # complete events only

   Requirements:
   - byte chunks may split anywhere; buffer partial lines AND partial UTF-8
     sequences (an emoji is 4 bytes and can straddle chunks)
   - `data:` field lines; multiple data lines in one event join with "\n"
   - `event:` field sets the event type (default "message")
   - comment lines starting with ":" are ignored (keep-alive pings)
   - events are dispatched on a blank line; `data: [DONE]` marks the sentinel
     (SSEEvent.done == True)
   - handles both "\n" and "\r\n" line endings
   - feeding the same byte stream in different chunkings must yield the
     IDENTICAL sequence of events.

2. ToolCallAssembler - reassembles streamed tool calls. Providers stream a
   tool call as deltas: the name/id arrive first, then the JSON `arguments`
   string arrives in fragments (which are NOT individually valid JSON).

       add_delta(index, *, id=None, name=None, arguments=None) -> None
       is_complete(index) -> bool     # accumulated args parse as JSON?
       finish() -> list[ToolCall]     # all calls, ordered by index

INTERVIEW NOTES
---------------
A strong solution demonstrates:
- Two distinct buffering layers: bytes -> text (incremental UTF-8 decoder)
  and text -> lines (find "\n" in a buffer). Decoding each chunk with
  bytes.decode() crashes on a split code point - the #1 mistake.
- Push-parser design: feed() returns only COMPLETE events and keeps partial
  state; no assumption that one chunk == one event (or even one line).
- Knowing the SSE grammar details: value may have one optional leading space
  ("data: x" and "data:x" are both "x"); a lone "data" line means empty data;
  comments keep connections alive through proxies.
- For tool calls: argument fragments are meaningless until concatenated, so
  completion == "accumulated string parses as JSON", checked incrementally.
Common mistakes: bytes.decode() per chunk (UnicodeDecodeError on split
emoji); str(chunk) instead of decoding; discarding "data:" lines that follow
another (multi-line data is legal); treating [DONE] as JSON; json.loads on
each argument fragment.
Follow-ups: support the `id:` field and Last-Event-ID reconnection; lone-\r
line endings from the SSE spec; backpressure via a generator API; parallel
tool calls interleaved by index (already supported here - discuss why the
index, not order of arrival, keys the accumulator).
"""

import codecs
import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SSEEvent:
    data: str
    event: str = "message"
    done: bool = False


class SSEParser:
    DONE_SENTINEL = "[DONE]"

    def __init__(self) -> None:
        self._decoder = codecs.getincrementaldecoder("utf-8")()  # buffers partial code points
        self._text = ""                 # decoded text not yet split into lines
        self._data_lines: list[str] = []
        self._event_type: str | None = None

    def feed(self, chunk: bytes) -> list[SSEEvent]:
        self._text += self._decoder.decode(chunk)
        events: list[SSEEvent] = []
        while (nl := self._text.find("\n")) != -1:
            line = self._text[:nl]
            if line.endswith("\r"):     # tolerate \r\n
                line = line[:-1]
            self._text = self._text[nl + 1:]
            ev = self._process_line(line)
            if ev is not None:
                events.append(ev)
        return events

    def _process_line(self, line: str) -> SSEEvent | None:
        if line == "":                  # blank line dispatches the pending event
            if not self._data_lines:
                self._event_type = None  # event with no data is dropped per spec
                return None
            data = "\n".join(self._data_lines)
            ev = SSEEvent(data=data, event=self._event_type or "message",
                          done=(data == self.DONE_SENTINEL))
            self._data_lines = []
            self._event_type = None
            return ev
        if line.startswith(":"):        # comment / keep-alive
            return None
        f, _, value = line.partition(":")
        if value.startswith(" "):       # spec: strip ONE leading space only
            value = value[1:]
        if f == "data":
            self._data_lines.append(value)
        elif f == "event":
            self._event_type = value
        # id:/retry:/unknown fields ignored in this challenge
        return None


@dataclass
class ToolCall:
    index: int
    id: str | None
    name: str
    arguments: dict[str, Any]


class ToolCallAssembler:
    """Accumulates streamed tool-call deltas keyed by call index."""

    def __init__(self) -> None:
        self._calls: dict[int, dict] = {}

    def add_delta(self, index: int, *, id: str | None = None,
                  name: str | None = None, arguments: str | None = None) -> None:
        slot = self._calls.setdefault(index, {"id": None, "name": [], "args": []})
        if id is not None:
            slot["id"] = id
        if name is not None:
            slot["name"].append(name)       # names can also stream in pieces
        if arguments is not None:
            slot["args"].append(arguments)  # fragments are NOT valid JSON alone

    def raw_arguments(self, index: int) -> str:
        return "".join(self._calls[index]["args"])

    def is_complete(self, index: int) -> bool:
        if index not in self._calls or not self._calls[index]["name"]:
            return False
        try:
            json.loads(self.raw_arguments(index) or "{}")
            return True
        except json.JSONDecodeError:
            return False

    def finish(self) -> list[ToolCall]:
        calls = []
        for index in sorted(self._calls):
            slot = self._calls[index]
            raw = self.raw_arguments(index)
            try:
                args = json.loads(raw) if raw else {}
            except json.JSONDecodeError as e:
                raise ValueError(f"tool call {index} has incomplete arguments: {raw!r}") from e
            calls.append(ToolCall(index=index, id=slot["id"],
                                  name="".join(slot["name"]), arguments=args))
        return calls


if __name__ == "__main__":
    stream = (
        b": keep-alive ping\n"
        + 'data: {"delta": "Hel"}\n\n'.encode()
        + 'data: {"delta": "lo \U0001f680"}\n\n'.encode()     # rocket emoji: 4 UTF-8 bytes
        + b"event: usage\r\ndata: line one\r\ndata: line two\r\n\r\n"
        + b"data: [DONE]\n\n"
    )

    def run(chunks: list[bytes]) -> list[SSEEvent]:
        parser = SSEParser()
        out: list[SSEEvent] = []
        for c in chunks:
            out.extend(parser.feed(c))
        return out

    # 1. Same stream, three chunkings: whole, every 3 bytes, every 1 byte.
    whole = run([stream])
    by_3 = run([stream[i:i + 3] for i in range(0, len(stream), 3)])
    by_1 = run([stream[i:i + 1] for i in range(0, len(stream), 1)])
    assert whole == by_3 == by_1, "chunking must not change parsed events"

    # 2. Event contents: comment dropped, emoji intact, multi-line data joined.
    assert len(whole) == 4
    assert whole[0] == SSEEvent(data='{"delta": "Hel"}')
    assert json.loads(whole[1].data)["delta"] == "lo \U0001f680"  # survived byte splits
    assert whole[2] == SSEEvent(data="line one\nline two", event="usage")
    assert whole[3].done and whole[3].data == "[DONE]"
    assert not whole[0].done

    # 3. Deliberate split INSIDE the emoji's 4-byte sequence.
    emoji_pos = stream.find("\U0001f680".encode())
    parts = [stream[:emoji_pos + 2], stream[emoji_pos + 2:]]   # cut after 2 of 4 bytes
    assert run(parts) == whole

    # 4. Partial trailing event is never emitted early.
    parser = SSEParser()
    assert parser.feed(b"data: incomplete") == []
    assert parser.feed(b" tail\n") == []                       # still no blank line
    assert parser.feed(b"\n") == [SSEEvent(data="incomplete tail")]

    # 5. "data:x" (no space) and bare "data" lines follow the spec.
    parser = SSEParser()
    assert parser.feed(b"data:x\n\n") == [SSEEvent(data="x")]
    assert parser.feed(b"data\n\n") == [SSEEvent(data="")]

    # 6. Tool-call assembler reconstructs fragmented JSON arguments.
    asm = ToolCallAssembler()
    asm.add_delta(0, id="call_1", name="get_", arguments="")
    asm.add_delta(0, name="weather")
    assert asm.is_complete(0)                    # no args streamed yet == {} (valid)
    asm.add_delta(0, arguments='{"loc')
    assert not asm.is_complete(0)                # fragment is not valid JSON
    asm.add_delta(0, arguments='ation": "Par')
    asm.add_delta(1, id="call_2", name="get_time", arguments='{"tz": "UTC"}')
    assert asm.is_complete(1) and not asm.is_complete(0)
    asm.add_delta(0, arguments='is", "unit": "c"}')
    assert asm.is_complete(0)
    calls = asm.finish()
    assert [c.name for c in calls] == ["get_weather", "get_time"]
    assert calls[0].arguments == {"location": "Paris", "unit": "c"}
    assert calls[0].id == "call_1" and calls[0].index == 0

    # 7. finish() on incomplete arguments fails loudly.
    bad = ToolCallAssembler()
    bad.add_delta(0, name="f", arguments='{"x": ')
    try:
        bad.finish()
        assert False, "must reject unparseable arguments"
    except ValueError:
        pass

    print("All tests passed.")
