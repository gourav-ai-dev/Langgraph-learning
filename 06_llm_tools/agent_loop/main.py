from typing import TypedDict, Optional
from langchain_community.llms import Ollama
from langgraph.graph import StateGraph, END

llm = Ollama(model="phi3")

class AgentState(TypedDict):
    question: str
    thought: Optional[str]
    action: Optional[str]
    observation: Optional[str]
    answer: Optional[str]

def calculator_tool(query: str):
    try:
        return str(eval(query))
    except:
        return "error"
    
def think_node(state: AgentState):
    print("Thinking...")

    prompt = f"""
    You are an AI agent.

    You can:
    1. Use a calculator
    2. Answer directly

    if you already has this result dont do again observe the old result first {state.get('observation')}

    If math needed:
    Respond:
    ACTION: calculate

    If final answer:
    Respond:
    ACTION: final
    ANSWER: <your answer>

    Question: {state['question']}
    """

    response = llm.invoke(prompt)

    return {"thought": response}


def act_node(state: AgentState):
    print("Deciding action...")

    thought = state["thought"].lower()

    print("\nthought ", thought)
    
    if "calculate" in thought:
        return {"action": "tool"}
    elif "final" in thought:
        return {"action": "final"}
    
    return {"action": "final"}

def tool_node(state: AgentState):
    print("Using tool...")

    result = calculator_tool(state["question"])

    return {
        "observation": result
    }


def final_node(state: AgentState):
    print("Generating final answer...")

    prompt = f"""
    Based on tool result:

    Result: {state.get("observation")}

    Answer the question:
    
    {state['question']}
    
    """

    answer = llm.invoke(prompt)

    return {"answer": answer}

def route_action(state: AgentState):
    return state["action"]


def main():
    builder = StateGraph(AgentState)

    builder.add_node("think", think_node)
    builder.add_node("act", act_node)
    builder.add_node("tool", tool_node)
    builder.add_node("final", final_node)

    builder.set_entry_point("think")

    builder.add_edge("think", "act")
    builder.add_conditional_edges(
        "act",
        route_action,
        {
            "tool": "tool",
            "final": "final"
        }
    )

    # LOOP HERE 🔥
    builder.add_edge("tool", "think")
    builder.add_edge("final", END)

    graph = builder.compile()

    print(graph.get_graph().draw_ascii())

    question = input("Ask: ")

    result = graph.invoke(
        {"question": question},
        config={"recursion_limit": 10}
    )

    print("\n✅ Final Answer:")
    print(result["answer"])


if __name__ == "__main__" : main()