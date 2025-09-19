
# app.py
# Minimal LangGraph example application that defines a compiled graph object.
# The langgraph CLI/server may load this module to discover an 'app' object.
# This script also works as a standalone runner for local testing.

from typing import TypedDict, Optional, List, Dict, Any
from langgraph.graph import StateGraph
from langgraph.checkpoint import MemorySaver
try:
    from langchain_openai import ChatOpenAI
except Exception:
    ChatOpenAI = None  # optional; LLM calls will be mocked if not available

# --- State definition ---
class State(TypedDict, total=False):
    text: str
    history: List[Dict[str, Any]]
    summary: str
    approved: bool

# --- Reducer ---
def append_history(existing: Optional[List[Dict[str, Any]]], new: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    if existing is None:
        existing = []
    if new is None:
        return existing
    return existing + new

# --- Nodes ---
def summarize_node(state: State) -> Dict[str, Any]:
    text = state.get("text", "")
    # If ChatOpenAI available, call real LLM; otherwise mock
    if ChatOpenAI is not None:
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        resp = llm.invoke("Summarize in 2 sentences:\n\n" + text)
        summary = resp.content
    else:
        # Mock summarization
        summary = "MOCK_SUMMARY: " + (text[:120] + ("..." if len(text) > 120 else ""))
    return {"summary": summary}

def add_history_node(state: State) -> Dict[str, Any]:
    h = state.get("history") or []
    h.append({"summary": state.get("summary", ""), "meta": {"source": "summarizer"}})
    return {"history": h}

def approval_node(state: State) -> Dict[str, Any]:
    # For CLI/local run, we ask for approval; in Studio you could use interactive HITL.
    print("\\n=== Human Approval Required ===")
    print("Summary:")
    print(state.get("summary"))
    print("History length:", len(state.get("history") or []))
    ans = input("Approve summary? (y/N): ").strip().lower()
    return {"approved": ans == "y"}

# --- Build Graph ---
graph = StateGraph(State)
graph.add_node("summarize", summarize_node)
graph.add_node("add_history", add_history_node)
graph.add_node("approval", approval_node)
graph.add_edge("summarize", "add_history")
graph.add_edge("add_history", "approval")
graph.set_entry_point("summarize")

# Use MemorySaver for dev persistence
checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer, reducers={"history": append_history})

# Standalone run helper
def run_local(text: str, thread_id: str = "local-thread-1"):
    cfg = {"configurable": {"thread_id": thread_id}}
    out = app.invoke({"text": text}, config=cfg)
    print("\\n=== run_local output ===")
    print(out)
    return out

if __name__ == "__main__":
    # Quick test run
    sample = "LangGraph allows building stateful flows and connecting multiple agents."
    run_local(sample)
