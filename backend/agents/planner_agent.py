from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from typing import TypedDict, List
import json

class PlannerState(TypedDict):
    goals: List[str]
    profile: dict

def initialize_planner():
    prompt = ChatPromptTemplate.from_template("""
    Analyze this financial profile:
    {profile}
    
    Generate a plan with:
    1. 3 short-term (1y) goals
    2. 2 long-term (5y) goals
    3. Recommended asset allocation
    
    Format as JSON with: short_term_goals, long_term_goals, allocation
    """)
    return prompt | Ollama(model="mistral")

planner = initialize_planner()

def generate_plan(state: PlannerState):
    response = planner.invoke({"profile": state["profile"]})
    try:
        return json.loads(response)
    except:
        return {"error": "Failed to parse plan"}