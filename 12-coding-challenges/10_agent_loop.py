"""Challenge 10 - Minimal Agent Loop with Tool Use (Medium)

PROBLEM
-------
Implement the core loop of a tool-using agent, with the LLM mocked out so the
loop's control flow can be tested deterministically.

Model protocol - the "LLM" is any callable `llm(history) -> dict` returning:
    {"tool": "<name>", "args": {...}}   # tool call request
    {"final": "<text>"}                 # finished, return this answer

Implement:

    run_agent(llm, tools, task, max_iterations=8) -> AgentResult
        - history starts as [{"role": "user", "content": task}]
        - each model action is appended as {"role": "assistant", "content": action}
        - tool output (or an error string) is appended as
          {"role": "tool", "content": <observation>} and the loop continues
        - unknown tool or a tool raising -> feed the error text back to the
          model as the observation; do NOT crash the loop
        - stop when the model returns "final", or after max_iterations model
          calls (AgentResult.stopped_at_limit = True, output = None)

Tools to provide:
    calculator(expression) - safe arithmetic via the `ast` module (no eval()!)
    convert(value, from_unit, to_unit) - km/m/mi and kg/lb via base units
    lookup(key) - small in-memory fact table

INTERVIEW NOTES
---------------
A strong solution demonstrates:
- The agent loop is just: model -> action -> execute -> observe -> repeat.
  Everything else (planning, reflection) layers on top of this skeleton.
- Errors are observations, not exceptions: feeding "unknown tool" back lets
  the model self-correct - exactly how production agents recover.
- A safe calculator: walking the AST whitelist (constants, + - * / ** %),
  never eval()/exec() on model output. Injecting `llm` and the tool registry
  makes the loop unit-testable without network calls.
Common mistakes: eval() on model-generated strings; no iteration cap
(runaway loops burn tokens/money); swallowing tool errors instead of
returning them to the model; mutating a shared history list across runs.
Follow-ups: parallel tool calls in one turn; token budgets in addition to
iteration caps; structured tool schemas + argument validation (the essence
of MCP tool definitions); persisting history for resumability.
"""

import ast
import operator
from dataclasses import dataclass, field
from typing import Any, Callable


# --------------------------------------------------------------------------- tools

_ALLOWED_BINOPS: dict[type, Callable] = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
}
_ALLOWED_UNARY: dict[type, Callable] = {ast.USub: operator.neg, ast.UAdd: operator.pos}


def calculator(expression: str) -> float:
    """Safely evaluate an arithmetic expression by walking its AST."""
    def ev(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
            return _ALLOWED_BINOPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[type(node.op)](ev(node.operand))
        raise ValueError(f"disallowed syntax: {type(node).__name__}")
    return float(ev(ast.parse(expression, mode="eval")))


# unit -> (dimension, factor to base unit)
_UNITS = {"m": ("length", 1.0), "km": ("length", 1000.0), "mi": ("length", 1609.344),
          "kg": ("mass", 1.0), "lb": ("mass", 0.45359237)}


def convert(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in _UNITS or to_unit not in _UNITS:
        raise ValueError(f"unknown unit; supported: {sorted(_UNITS)}")
    (dim_f, f), (dim_t, t) = _UNITS[from_unit], _UNITS[to_unit]
    if dim_f != dim_t:
        raise ValueError(f"cannot convert {dim_f} to {dim_t}")
    return value * f / t


_FACTS = {"speed_of_light_kmps": 299792.458, "boiling_point_c": 100,
          "marathon_km": 42.195}


def lookup(key: str) -> Any:
    if key not in _FACTS:
        raise KeyError(f"no fact for {key!r}; known keys: {sorted(_FACTS)}")
    return _FACTS[key]


TOOLS: dict[str, Callable] = {"calculator": calculator, "convert": convert, "lookup": lookup}


# --------------------------------------------------------------------------- loop

@dataclass
class AgentResult:
    output: str | None
    history: list[dict]
    stopped_at_limit: bool = False


class MockLLM:
    """Plays back a scripted list of actions; records every history it saw."""

    def __init__(self, script: list[dict]):
        self.script = list(script)
        self.seen_histories: list[list[dict]] = []

    def __call__(self, history: list[dict]) -> dict:
        self.seen_histories.append([dict(m) for m in history])
        if not self.script:
            raise RuntimeError("MockLLM script exhausted")
        return self.script.pop(0)


def run_agent(llm: Callable[[list[dict]], dict], tools: dict[str, Callable],
              task: str, max_iterations: int = 8) -> AgentResult:
    history: list[dict] = [{"role": "user", "content": task}]
    for _ in range(max_iterations):
        action = llm(history)
        history.append({"role": "assistant", "content": action})

        if "final" in action:
            return AgentResult(output=action["final"], history=history)

        name = action.get("tool")
        if name not in tools:
            observation = f"Error: unknown tool {name!r}. Available tools: {sorted(tools)}"
        else:
            try:
                observation = repr(tools[name](**action.get("args", {})))
            except Exception as e:  # tool failure is an observation, not a crash
                observation = f"Error: {type(e).__name__}: {e}"
        history.append({"role": "tool", "content": observation})

    return AgentResult(output=None, history=history, stopped_at_limit=True)


if __name__ == "__main__":
    # 1. Scripted multi-step task: compute, convert, answer.
    llm = MockLLM([
        {"tool": "calculator", "args": {"expression": "(3 + 4) * 2"}},
        {"tool": "convert", "args": {"value": 14.0, "from_unit": "km", "to_unit": "mi"}},
        {"final": "That distance is about 8.70 miles."},
    ])
    result = run_agent(llm, TOOLS, "How many miles is (3+4)*2 km?")
    assert result.output == "That distance is about 8.70 miles."
    assert not result.stopped_at_limit
    tool_msgs = [m for m in result.history if m["role"] == "tool"]
    assert tool_msgs[0]["content"] == "14.0"
    assert tool_msgs[1]["content"].startswith("8.699")
    # The model saw the calculator result before its second action.
    assert any(m["role"] == "tool" for m in llm.seen_histories[1])

    # 2. Unknown tool: error is fed back, model corrects itself and recovers.
    llm = MockLLM([
        {"tool": "calculater", "args": {"expression": "6 * 7"}},   # typo'd tool
        {"tool": "calculator", "args": {"expression": "6 * 7"}},
        {"final": "42"},
    ])
    result = run_agent(llm, TOOLS, "What is 6*7?")
    assert result.output == "42"
    errors = [m for m in result.history if m["role"] == "tool"
              and m["content"].startswith("Error: unknown tool")]
    assert len(errors) == 1 and "calculator" in errors[0]["content"]

    # 3. Tool raising an exception is also recoverable.
    llm = MockLLM([
        {"tool": "lookup", "args": {"key": "speed_of_sound"}},     # missing key
        {"tool": "lookup", "args": {"key": "marathon_km"}},
        {"final": "42.195 km"},
    ])
    result = run_agent(llm, TOOLS, "How long is a marathon?")
    assert result.output == "42.195 km"
    assert any("KeyError" in m["content"] for m in result.history if m["role"] == "tool")

    # 4. Loop terminates at max_iterations when the model never finishes.
    llm = MockLLM([{"tool": "calculator", "args": {"expression": "1 + 1"}}] * 10)
    result = run_agent(llm, TOOLS, "Loop forever", max_iterations=3)
    assert result.stopped_at_limit and result.output is None
    assert sum(1 for m in result.history if m["role"] == "assistant") == 3

    # 5. Calculator refuses non-arithmetic payloads.
    for evil in ("__import__('os').system('rm -rf /')", "open('x')", "[1]*9**9"):
        try:
            calculator(evil)
            assert False, f"should have rejected: {evil}"
        except (ValueError, SyntaxError):
            pass
    assert calculator("-(2 ** 3) % 5") == 2.0

    print("All tests passed.")
