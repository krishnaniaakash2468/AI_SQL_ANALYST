# Architecture and execution paths

This repository contains more than one implementation approach developed during the project. Keep the distinctions clear when demonstrating or explaining it.

## 1. Manually orchestrated workflow: `main.py` + `tools.py`

```text
User question
     |
     v
Python formats SQL-generation prompt + database schema
     |
     v
Gemini generates SQL
     |
     v
Python calls execute_query()
     |
     v
SQL Server returns rows / Pandas DataFrame
     |
     v
Python formats results into analysis prompt
     |
     v
Gemini interprets retrieved results
     |
     v
Analytical response
```

Python controls the sequence. The LLM generates SQL and then interprets the result in a second model call. This is an LLM-powered text-to-SQL and analysis pipeline, but it is not an autonomous tool-calling agent.

`tools.py` contains ordinary Python database functions:
- `get_schema()` reads table, column, and data-type metadata from `INFORMATION_SCHEMA.COLUMNS`.
- `execute_query(query)` executes the supplied SQL and returns a Pandas DataFrame.

## 2. LangChain tool-calling CLI: `data_agent.py` + `agent_tools.py`

```text
User question
     |
     v
LangChain create_agent()
     |
     +---- model decides whether / how to use tools
     |
     +---- get_schema()
     |
     +---- execute_query(query)
     |
     v
Final model response
```

`agent_tools.py` wraps database functions with LangChain's `@tool` decorator. `data_agent.py` registers those tools with `create_agent()`. This is the tool-calling experiment and is architecturally different from the fixed sequence in `main.py`.

## 3. Streamlit interface: `streamlitapp.py` + `agent_tools.py`

The Streamlit application provides a chat-based interface around the LangChain tool-calling workflow. The supplied development version includes chat-history handling and an option to inspect tool calls. Review the current source before claiming every UI feature is present in the public version.

Run it with:

```powershell
streamlit run streamlitapp.py
```

If the file is renamed to `app.py`, update the command accordingly.

## File responsibilities

| File | Responsibility |
|---|---|
| `main.py` | Fixed, Python-orchestrated SQL generation, execution, and result interpretation |
| `tools.py` | Plain Python database access and schema discovery |
| `data_agent.py` | CLI entry point for LangChain tool-calling |
| `agent_tools.py` | Database functions exposed as LangChain tools |
| `streamlitapp.py` | Streamlit chat interface using the tool-calling workflow |
| `requirements.txt` | Python dependencies |

## Important implementation boundaries

- The current `main.py` fetches the schema at startup. A schema change during a running process may not be reflected until restart.
- Prompt instructions requesting SELECT-only SQL are not equivalent to deterministic SQL validation.
- Do not claim automatic SQL repair, guaranteed analytical accuracy, production-grade safety, or fully autonomous planning unless those capabilities are implemented and tested in the code being published.
- Database connection settings and the Gemini model name are read from environment variables (`.env`) rather than hardcoded.
- The current tool functions return Pandas DataFrames. Check compatibility with the LangChain version used and consider returning a serializable representation.

## Local application vs. local inference

The application and SQL Server database run on the user's local machine. Gemini is called through Google's API, so model inference requires internet connectivity and is performed by Google's service. The project is not fully offline.
