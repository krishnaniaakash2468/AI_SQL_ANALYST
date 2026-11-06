import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from agent_tools import execute_query, get_schema
from langchain.agents import create_agent

load_dotenv()

model = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
    timeout=60,
    max_retries=1
)

agent = create_agent(model = model,
                      tools=[execute_query, get_schema],
                      system_prompt="You are Sql server expert,use tools if required")

while True:
    user_input = input("\nEnter your question (or 'quit' to exit): ")

    if user_input.lower() in ["quit", "exit"]:
        break
    response = agent.invoke({'messages':[user_input]})
    print(response['messages'][-1].text)