# AI Data Agent

A free-tier, locally hosted AI Data Agent that lets users ask questions about a SQL Server database in natural language. The application uses Gemini through its API, LangChain tool-calling, Python, SQLAlchemy, and Streamlit to retrieve database information and present responses in conversational form.

> **Deployment note:** The application and SQL Server database are intended to run locally. Gemini inference is performed through Google's cloud API. This is a locally hosted application with free-tier cloud inference, not a fully offline or on-device LLM.

## Project objective

Build an AI-powered data assistant while keeping development and usage within free-tier resources and using a local database. The project was also an opportunity to learn LLM integration, prompt engineering, database connectivity, schema discovery, tool calling, and application development by implementing and troubleshooting each component.

## What it does

- Accepts natural-language questions about the database.
- Retrieves database schema information.
- Uses an LLM to help translate questions into SQL.
- Executes database queries through Python and SQLAlchemy.
- Presents retrieved results and an LLM-generated explanation.
- Includes a Streamlit interface for conversational interaction.
- Includes a separate CLI experiment using LangChain's `create_agent()` tool-calling workflow.

The exact capabilities depend on which entry point is run. See [Architecture](ARCHITECTURE.md).

## Technology stack

- Python
- Google Gemini API (free-tier usage, subject to Google's quotas and availability)
- LangChain / LangGraph
- SQL Server Express
- SQLAlchemy and pyodbc
- Pandas
- Streamlit
- python-dotenv

## Repository structure

```text
AI-Data-Agent/
├── main.py                 # Manually orchestrated SQL + analysis workflow
├── data_agent.py           # LangChain tool-calling CLI experiment
├── streamlitapp.py         # Streamlit tool-calling interface
├── tools.py                # Plain Python database functions
├── agent_tools.py          # LangChain-decorated database tools
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── BUILD_LOG.md
├── ARCHITECTURE.md
└── screenshots/
```

Only include files that are actually part of the version you intend to publish. Remove unused experiments if you prefer a smaller repository, or keep them and label them clearly.

## Getting started

### 1. Prerequisites

- Windows (the current SQL Server connection setup was developed on Windows)
- Python installed
- SQL Server Express or another compatible SQL Server instance
- SQL Server ODBC driver installed (the current connection string uses ODBC Driver 17)
- A database containing the expected tourism tables
- A Google AI Studio API key

### 2. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/AI-Data-Agent.git
cd AI-Data-Agent
```

### 3. Create and activate a virtual environment

```powershell
python -m venv myvenv
.\myvenv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the appropriate execution-policy setting for your machine or activate the environment through your IDE. Do not disable security controls unnecessarily.

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure environment variables

Copy `.env.example` to `.env` and fill in your own values:

```env
GOOGLE_API_KEY=replace_with_your_own_key
GEMINI_MODEL=gemini-3.5-flash-lite
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=your_database_name
DB_DRIVER=ODBC Driver 17 for SQL Server
```

`GEMINI_MODEL` can be changed whenever a model is unavailable or rate-limited. Never commit `.env`. Do not paste API keys, server names or credentials into source code, screenshots, README files, issues, or commit history.

### 6. Configure SQL Server

The original development setup used SQL Server Express with Windows Authentication and a local database named `Tourism_India_Analysis_pyt`. Set `DB_SERVER`, `DB_NAME` and `DB_DRIVER` in `.env` for your own machine. No code changes are needed.

### 7. Run the application

For the Streamlit interface:

```powershell
streamlit run streamlitapp.py
```

For the separate CLI tool-calling experiment:

```powershell
python data_agent.py
```

For the manually orchestrated SQL-generation and analysis workflow:

```powershell
python main.py
```

The `main.py`, `data_agent.py`, and `streamlitapp.py` entry points represent different workflows. They are not interchangeable; read [ARCHITECTURE.md](ARCHITECTURE.md) before describing the project.

## Database used during development

The development database was named `Tourism_India_Analysis_pyt` and included these tables:

- `tourism_attractions_state_2023`
- `tourism_infrastructure_state_2023`
- `tourism_visits_state_2023`

The repository should not contain a private or copyrighted database dump unless you have permission to redistribute it. A reader will need to create or configure a compatible database to reproduce the demo.

## Screenshots and demo

Add your own screenshots to `screenshots/` and embed them here. Do not include API keys, server names, personal paths, or sensitive query results in screenshots.

Example:

```markdown
![Streamlit application](screenshots/app-interface.png)
![Sample analytical response](screenshots/sample-analysis.png)
```

A short screen-recording demo can also be linked here after uploading it to a platform such as YouTube or LinkedIn.

## Current limitations and responsible use

This is a learning project and a basic AI-powered data-querying application, not a production-ready autonomous analytics platform.

- Complex analytical questions may produce incomplete or shallow reasoning.
- An LLM-generated explanation can omit relevant records or misinterpret query results.
- Prompt instructions alone do not enforce read-only SQL execution. The current query execution functions should not be treated as a security boundary.
- SQL validation, parameterization, query timeouts, row limits, and least-privilege database permissions need stronger implementation and testing before use with sensitive or important data.
- The manually orchestrated `main.py` workflow follows a fixed Python-controlled sequence; it is not the same as the separate LangChain tool-calling workflow.
- Gemini API availability, model names, free-tier quotas, and rate limits can change. Free access is not guaranteed indefinitely.
- Large result sets and advanced statistical analysis are not comprehensively handled.

**Do not connect this project to a production or sensitive database without implementing and testing appropriate security controls.**

## Learning outcomes

This project involved practical work with:

- Calling LLMs from Python.
- Prompt design for SQL generation and result interpretation.
- SQL Server connectivity using SQLAlchemy and ODBC.
- Dynamic schema discovery using `INFORMATION_SCHEMA.COLUMNS`.
- Wrapping Python functions as LangChain tools.
- Experimenting with LangChain's `create_agent()` workflow.
- Building a Streamlit chat interface.
- Managing environment variables and API usage limits.
- Debugging model availability, rate-limit, dependency, and Windows environment issues.

See [BUILD_LOG.md](BUILD_LOG.md) for the development journey and [ARCHITECTURE.md](ARCHITECTURE.md) for the different execution paths.

## Future improvements

- Deterministic SQL validation and read-only enforcement.
- Least-privilege database access.
- Better handling of SQL errors and controlled retries.
- Result verification for totals, averages, rankings, and comparisons.
- More reliable reasoning over complex analytical questions.
- Query result limits and pagination.
- Optional charts and statistical analysis using Python.
- Configurable model selection and clearer quota/error handling.

## License

Released under the MIT License. See [LICENSE](LICENSE).
