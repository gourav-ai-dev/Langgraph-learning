from typing import TypedDict, Optional
from langchain_community.llms import Ollama
from langgraph.graph import StateGraph, END

llm = Ollama(model="phi3")

class AgentState(TypedDict):
    question: str
    answer: Optional[str]
    tool_result: Optional[str]
    next: Optional[str]

def calculator_tool(query: str):
    try:
        result = eval(query)
        return str(result)
    except:
        return "Error in calculation"

def decide_node(state: AgentState):
    question = state["question"]

    prompt = f"""
    
    You are an AI agent.

    Decide whether the question requires a calculator.

    Rules:
    - If it involves math/calculation → respond ONLY: use_tool
    - Otherwise → respond ONLY: llm

    Do NOT explain.

    Question: {question}

    """

    decision = llm.invoke(prompt).strip().lower()

    print("🧠 Decision:", decision)

    next_step = "tool" if "use_tool" in decision else "llm"

    return {
        "question": question,
        "next": next_step
    }

def tool_node(state: AgentState):
    print(" Using calculator tool")

    result = calculator_tool(state["question"])

    return {
    "question": state["question"],
    "tool_result": result
    }


def llm_node(state: AgentState):
    print("Generating answer")

    if state.get("tool_result"):
        prompt = f"""
        Use this result to answer:
        Result: {state['tool_result']}
        Question: {state['question']}
    """
    else:
        prompt = state["question"]

    answer = llm.invoke(prompt)

    return {
    "question": state["question"],
    "answer": answer
    }

def route_decision(state: AgentState):
    return state.get("next", "llm")

def main():

    builder = StateGraph(AgentState)

    builder.add_node("decide", decide_node)
    builder.add_node("tool", tool_node)
    builder.add_node("llm", llm_node)
    
    builder.set_entry_point("decide")

    builder.add_conditional_edges(
        "decide",
        route_decision,
        {
            "tool": "tool",
            "llm": "llm"
        }
    )

    builder.add_edge("tool", "llm")
    builder.add_edge("llm", END)

    graph = builder.compile()
    print(graph.get_graph().draw_ascii())
    
    question = input("Ask: ")

    result = graph.invoke({
        "question": question
    })

    print("\n✅ Final Answer:")
    print(result["answer"])


if __name__ == "__main__" : main()