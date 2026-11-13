# Architecture and execution paths

The project is a LangChain tool-calling agent with two entry points: a command-line version and a Streamlit chat interface. Both share the same database tools.

## 1. LangChain tool-calling CLI: `data_agent.py` + `agent_tools.py`

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

`agent_tools.py` wraps database functions with LangChain's `@tool` decorator. `data_agent.py` registers those tools with `create_agent()`. Here the model decides whether and how to use the tools, rather than Python following a fixed sequence.

## 2. Streamlit interface: `streamlitapp.py` + `agent_tools.py`

The Streamlit application provides a chat-based interface around the LangChain tool-calling workflow. The supplied development version includes chat-history handling and an option to inspect tool calls. Review the current source before claiming every UI feature is present in the public version.

Run it with:

```powershell
streamlit run streamlitapp.py
```

If the file is renamed to `app.py`, update the command accordingly.

## File responsibilities

| File | Responsibility |
|---|---|
| `data_agent.py` | CLI entry point for LangChain tool-calling |
| `agent_tools.py` | Database functions exposed as LangChain tools |
| `streamlitapp.py` | Streamlit chat interface using the tool-calling workflow |
| `requirements.txt` | Python dependencies |

## Important implementation boundaries

- Read-only SQL is not enforced in code: `execute_query` runs whatever SQL the model passes to it. Use a read-only database login.
- Do not claim automatic SQL repair, guaranteed analytical accuracy, production-grade safety, or fully autonomous planning unless those capabilities are implemented and tested in the code being published.
- Database connection settings and the Gemini model name are read from environment variables (`.env`) rather than hardcoded.
- The current tool functions return Pandas DataFrames. Check compatibility with the LangChain version used and consider returning a serializable representation.

## Local application vs. local inference

The application and SQL Server database run on the user's local machine. Gemini is called through Google's API, so model inference requires internet connectivity and is performed by Google's service. The project is not fully offline.
