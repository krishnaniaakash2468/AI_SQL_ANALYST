"""
SQL Agent - Streamlit UI built on data_agent.py

Place this file next to agent_tools.py and run:
    pip install streamlit
    streamlit run streamlitapp.py

Features
- Same model / tools / system prompt as data_agent.py (existing files untouched)
- Chat history in the left sidebar (new chat, switch, delete), saved to chats_history.json
- "Show tool calls" toggle: when ON, every tool call is shown with its arguments
  and result; when OFF, tool calls are hidden.
"""
import json
import os
import time
import uuid

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from agent_tools import execute_query, get_schema

HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, "chats_history.json")
load_dotenv()
load_dotenv(os.path.join(HERE, "_env"))  # your env file is named "_env"

st.set_page_config(page_title="SQL Agent", page_icon="🗄️", layout="wide")

MAX_RESULT_CHARS = 4000  # truncate very long tool results in the UI only


# ------------------------------------------------------------------ storage
def load_store():
    try:
        with open(STORE, encoding="utf-8") as f:
            d = json.load(f)
        return d["chats"], d["order"]
    except Exception:
        return {}, []


def save_store():
    try:
        with open(STORE, "w", encoding="utf-8") as f:
            json.dump(
                {"chats": st.session_state.chats, "order": st.session_state.order},
                f,
                ensure_ascii=False,
            )
    except Exception:
        pass


if "chats" not in st.session_state:
    st.session_state.chats, st.session_state.order = load_store()
    st.session_state.current = None


# ------------------------------------------------------------------ agent
@st.cache_resource(show_spinner=False)
def build_agent():
    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        timeout=60,
        max_retries=1,
    )
    return create_agent(
        model=model,
        tools=[execute_query, get_schema],
        system_prompt="You are Sql server expert,use tools if required",
    )


def _text(msg) -> str:
    """Get plain text from a LangChain message (handles str / block-list content)."""
    t = getattr(msg, "text", None)
    if callable(t):
        t = t()
    if isinstance(t, str) and t:
        return t
    c = msg.content
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "".join(
            b.get("text", "") if isinstance(b, dict) else str(b) for b in c
        )
    return str(c)


def ask_agent(question: str, turns: list):
    """Run the agent with prior turns as context. Returns (answer, tool_calls)."""
    msgs = []
    for t in turns:
        msgs.append({"role": "user", "content": t["question"]})
        msgs.append({"role": "assistant", "content": t["answer"]})
    msgs.append({"role": "user", "content": question})

    result = build_agent().invoke({"messages": msgs})
    new_msgs = result["messages"][len(msgs):]  # only messages from this run

    calls, by_id = [], {}
    for m in new_msgs:
        if m.type == "ai" and getattr(m, "tool_calls", None):
            for tc in m.tool_calls:
                entry = {"name": tc["name"], "args": tc["args"], "result": None}
                calls.append(entry)
                by_id[tc["id"]] = entry
        elif m.type == "tool":
            entry = by_id.get(m.tool_call_id)
            if entry is not None:
                entry["result"] = _text(m)

    return _text(result["messages"][-1]), calls


# ------------------------------------------------------------------ render
def render_tool_calls(calls):
    for i, c in enumerate(calls, 1):
        with st.expander(f"🔧 Tool call {i}: {c['name']}", expanded=False):
            st.markdown("**Arguments**")
            st.json(c["args"])
            st.markdown("**Result**")
            res = c["result"] if c["result"] is not None else "(no result)"
            if len(res) > MAX_RESULT_CHARS:
                res = res[:MAX_RESULT_CHARS] + "\n... (truncated)"
            st.code(res, language="text")


def render_turn(t, show_tools):
    with st.chat_message("user"):
        st.write(t["question"])
    with st.chat_message("assistant"):
        if show_tools and t["tool_calls"]:
            render_tool_calls(t["tool_calls"])
        st.write(t["answer"])
        st.caption(f"{t['secs']:.1f}s")


# ------------------------------------------------------------------ sidebar
with st.sidebar:
    st.title("🗄️ SQL Agent")
    if st.button("＋ New chat", use_container_width=True, type="primary"):
        st.session_state.current = None
        st.rerun()

    show_tools = st.toggle(
        "Show tool calls",
        value=False,
        help="Show each tool call with its arguments and result.",
    )

    st.divider()
    st.subheader("Chat history")
    if not st.session_state.order:
        st.caption("Your chats will appear here.")

    for cid in st.session_state.order:
        title = st.session_state.chats[cid]["title"]
        label = title if len(title) <= 32 else title[:29] + "..."
        active = cid == st.session_state.current
        if st.button(
            label,
            key=f"chat_{cid}",
            help=title,
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state.current = cid
            st.rerun()

    if st.session_state.current:
        st.divider()
        if st.button("🗑️ Delete this chat", use_container_width=True):
            cid = st.session_state.current
            st.session_state.chats.pop(cid, None)
            if cid in st.session_state.order:
                st.session_state.order.remove(cid)
            st.session_state.current = None
            save_store()
            st.rerun()

# ------------------------------------------------------------------ main
st.header("Ask your database anything")
st.caption("Powered by a Gemini agent with SQL Server tools.")

chat = st.session_state.chats.get(st.session_state.current)
turns = chat["turns"] if chat else []

for t in turns:
    render_turn(t, show_tools)

question = st.chat_input("Ask a question about your data")

if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        try:
            start = time.time()
            with st.spinner("Thinking..."):
                answer, calls = ask_agent(question, turns)
            turn = {
                "question": question,
                "answer": answer,
                "tool_calls": calls,
                "secs": time.time() - start,
            }
            if chat is None:
                cid = uuid.uuid4().hex[:8]
                st.session_state.chats[cid] = {"title": question, "turns": []}
                st.session_state.order.insert(0, cid)
                st.session_state.current = cid
                chat = st.session_state.chats[cid]
            chat["turns"].append(turn)
            save_store()
            st.rerun()
        except Exception as e:
            st.error(f"The agent could not finish: {e}")
