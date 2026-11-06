
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from tools import execute_query, get_schema

load_dotenv()

model = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
    timeout=60,
    max_retries=3
)

schema = get_schema()

SQL_PROMPT = """
You are an AI SQL Analyst connected to a SQL Server database.

Your task is to generate SQL Server compatible SELECT queries.

RULES:
1. Understand the user's question before selecting tables.
2. Use only tables and columns present in the schema.
3. Retrieve all relevant records for comparisons.
4. Use SQL aggregations for rankings and calculations.
5. Never invent tables, columns or values.
6. Exclude aggregate rows such as 'Total' when calculating
   averages or rankings unless explicitly requested.
7. Exclude aggregate rows from final results unless requested.
8. Generate SELECT queries only.
9. Return only SQL without explanation or markdown.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}
"""

ANALYSIS_PROMPT = """
You are an analytical assistant.

Answer the user's question using ONLY the SQL query
results provided below.

RULES:
1. Base every factual statement on retrieved data.
2. Include all relevant entities in comparisons.
3. Do not selectively exclude relevant records.
4. Use comparison tables when appropriate.
5. Explain the metrics used to support conclusions.
6. Clearly distinguish observations from assumptions.
7. Never claim infrastructure is underdeveloped
   without sufficient supporting indicators.
8. Do not invent missing statistics.
9. If the available data is insufficient, state the limitation.
10. Keep the response clear and understandable.

USER QUESTION:
{question}

SQL QUERY RESULTS:
{results}

Provide an evidence-based answer.
"""

while True:
    user_input = input("\nEnter your question (or 'quit' to exit): ")

    if user_input.lower() in ["quit", "exit"]:
        break

    try:
        # STEP 1: Generate SQL
        prompt = SQL_PROMPT.format(
            schema=schema,
            question=user_input
        )

        response = model.invoke(prompt)

        query = response.content.strip()
        query = query.replace("```sql", "").replace("```", "").strip()

        print("\nGenerated SQL:", query)

        # STEP 2: Execute SQL
        result = execute_query(query)

        print("\nQuery Result:")
        print(result.to_string(index=False))

        # STEP 3: Analytical interpretation
        analysis_prompt = ANALYSIS_PROMPT.format(
            question=user_input,
            results=result.to_string(index=False)
        )

        analysis = model.invoke(analysis_prompt)

        print("\nAnalytical Response:")
        print(analysis.content)

    except Exception as e:
        print(f"\nError: {e}")
