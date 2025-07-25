from typing import TypedDict, List
from langgraph.graph import StateGraph
from .planner_agent import planner, generate_plan
from .executor_agent import executor
from .reflector_agent import reflector, vector_db

class WorkflowState(TypedDict):
    goals: List[str]
    profile: dict
    plan: dict
    results: dict
    insights: dict

def create_workflow():
    workflow = StateGraph(WorkflowState)
    
    workflow.add_node("planner", lambda state: {"plan": generate_plan(state)})
    workflow.add_node("executor", lambda state: {"results": executor.invoke(state["plan"])})
    workflow.add_node("reflector", lambda state: {"insights": reflector.invoke(state["results"])})
    
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", "reflector")
    workflow.add_edge("reflector", END)
    
    return workflow.compile()

financial_workflow = create_workflow()