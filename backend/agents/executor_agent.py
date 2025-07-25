from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.llms import Ollama
from typing import Annotated

@tool
def calculate_sip(
    principal: Annotated[float, "Monthly investment"],
    years: Annotated[int, "Duration"],
    rate: Annotated[float, "Expected return %"]
) -> dict:
    """Calculate SIP returns using compound interest"""
    months = years * 12
    monthly_rate = rate / 12 / 100
    future_value = principal * (((1 + monthly_rate)**months - 1) / monthly_rate)
    return {
        "total_invested": principal * months,
        "estimated_value": future_value
    }

def create_executor():
    tools = [calculate_sip]
    llm = Ollama(model="llama3")
    prompt = ChatPromptTemplate.from_template(
        "Execute this financial task: {input}\n\nUse tools if needed."
    )
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools)

executor = create_executor()