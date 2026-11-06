# Build log

This document records the major stages and troubleshooting themes from the development process. Add exact dates, commands, error messages, and test outcomes from your notes where available; do not invent timestamps or claim a test passed unless you personally verified it.

## Project objective

Build a basic AI Data Agent for free and run the application and database locally. The project uses a free-tier Gemini API for cloud inference, rather than a paid hosted application or a fully local/offline LLM.

## Development stages

### 1. Python environment
- Created a Python virtual environment (`myvenv`) in VS Code.
- Installed the Python packages required for LLM integration, database access, and data handling.
- Worked through Windows environment and dependency issues.

### 2. Gemini API integration
- Connected Gemini to Python through `langchain-google-genai`.
- Loaded configuration with `python-dotenv`.
- Tested model responses using `model.invoke()`.
- Experimented with multiple Gemini models to learn their behaviour and find workable options within free-tier constraints.

### 3. Free-tier model and quota experimentation
- Checked usage and rate-limit information in Google AI Studio after iterations/API calls.
- Switched between model options when encountering availability or usage constraints.
- Treated model selection as an ongoing experiment rather than assuming every model would remain available or within quota.
- Free-tier quotas and model availability can change over time.

### 4. Interactive command-line workflow
- Added an input loop so questions could be entered repeatedly.
- Added exit commands such as `quit` and `exit`.
- Tested conversation-message handling during development.

### 5. SQL Server connectivity
- Connected Python to SQL Server Express using SQLAlchemy and `pyodbc`.
- Used Windows Authentication in the development environment.
- Connected to the `Tourism_India_Analysis_pyt` database.

### 6. Dynamic schema discovery
- Queried `INFORMATION_SCHEMA.COLUMNS` to retrieve table names, column names, and data types.
- Expanded schema retrieval from an individual table to all relevant tables in the `dbo` schema.
- Used schema metadata in the SQL-generation prompt.

### 7. Text-to-SQL and analytical interpretation
- Designed prompts for SQL Server-compatible SELECT query generation.
- Executed generated SQL and returned results as Pandas DataFrames.
- Added a second LLM call to interpret query results in relation to the original question.
- Refined analytical instructions to reduce selective reporting and unsupported conclusions.

### 8. LangChain tool-calling experiment
- Wrapped database functions using the `@tool` decorator.
- Registered tools with LangChain's `create_agent()`.
- Tested a separate CLI tool-calling workflow.
- Kept this approach distinct from the manually orchestrated `main.py` pipeline.

### 9. Streamlit interface
- Developed a Streamlit chat interface around the tool-calling implementation.
- Worked on chat history and tool-call visibility.
- Tested local execution and addressed configuration/model availability issues.

## Troubleshooting

| Area | What happened | What I did |
|---|---|---|
| Windows security | Running `python tools.py` for the first time was blocked by Windows Smart App Control | Turned Smart App Control off on my development machine so the Python/ODBC process could run. Note that this lowers a Windows protection and is hard to undo, so consider other options on a machine you care about |
| Python packages | Dependency and import compatibility while setting up LangChain and the agent | Installed everything from `requirements.txt` inside the virtual environment |
| Database | Needed a working SQL Server / ODBC connection | Used SQLAlchemy with `pyodbc`, ODBC Driver 17 and Windows Authentication; verified with a test query in `tools.py` |
| Schema | Hardcoding one table would break when tables change | Queried `INFORMATION_SCHEMA.COLUMNS` for all `dbo` tables and kept only table, column and data type |
| Gemini API: 503 | `gemini-3.1-flash-lite` returned `503 UNAVAILABLE` (high demand) during a Streamlit test | Retried later and switched to another model; `max_retries` handles short spikes |
| Gemini API: 404 | `gemini-2.5-flash` returned `404 NOT_FOUND` ("no longer available to new users") | Switched to a currently available model |
| Model choice | Models went unavailable or rate-limited at different times | Made the model name a setting (`GEMINI_MODEL` in `.env`) so it can be changed without editing code |
| Analytical output | Incomplete or selective interpretation of query results | Tightened the analysis prompt rules |

## What I learned

- An LLM response, a SQL query, and a verified analytical conclusion are three different things.
- Prompt instructions do not replace application-level validation.
- A fixed Python workflow and an agent that chooses tools are different architectures.
- Free-tier API usage requires attention to model availability and rate limits.
- A working local demo still needs careful configuration before it can be shared publicly.

## Before publishing

- [ ] Replace machine-specific database connection strings with environment variables.
- [ ] Verify that `.env` and `_env` are not committed.
- [ ] Check the Git staging area for secrets and personal paths.
- [ ] Verify the actual model names used in each entry point.
- [ ] Verify that the documented Streamlit command matches the filename.
- [ ] Run the public setup instructions from a fresh virtual environment if possible.
- [ ] Add genuine screenshots and a short demo.
