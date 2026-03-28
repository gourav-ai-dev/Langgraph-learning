from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_community.llms import Ollama

from rag import create_retriever
from tools import calculator_tool, text_tool, rag_tool

llm = Ollama(model="phi3")

retriever = create_retriever()

class AgentState(TypedDict):
    question: str
    thought: Optional[str]
    action: Optional[str]
    observation: Optional[str]
    answer: Optional[str]


def think_node(state: AgentState):
    print("THINK")

    prompt = f"""

    You are an AI agent.

    Available tools:
    - calculator → math
    - text → uppercase text
    - rag → answer from documents

    Previous observation:
    {state.get("observation")}

    Question:
    {state["question"]}

    Decide next step:

    - ACTION: calculator
    - ACTION: text
    - ACTION: rag
    - ACTION: final
      ANSWER: <your answer>
      
      Respond ONLY in this format.
    """

    response = llm.invoke(prompt).strip()

    print("Thought:", response)

    return {"thought": response}


def act_node(state: AgentState):
    print("ACT")

    thought = state["thought"].lower()

    if "calculator" in thought:
        return {"action": "calculator"}
    elif "text" in thought:
        return {"action": "text"}
    elif "rag" in thought:
        return {"action": "rag"}
    elif "final" in thought:
        return {"action": "final"}

    return {"action": "final"}


def calculator_node(state: AgentState):
    print("Calculator Tool")

    result = calculator_tool(state["question"])

    return {
        "observation": result,
        "question": f"Result is {result}. Now answer."
    }


def text_node(state: AgentState):
    print("Text Tool")

    result = text_tool(state["question"])

    return {
        "observation": result,
        "question": f"Text result is {result}. Now answer."
    }


def rag_node(state: AgentState):
    print("RAG Tool")

    context = rag_tool(state["question"], retriever)

    return {
        "observation": context,
        "question": f"Context:\n{context}\n\nAnswer the question."
    }


def final_node(state: AgentState):
    print("FINAL")

    prompt = f"""
    
    Use this information:

    {state.get("observation")}

    Answer:

    {state["question"]}
    """

    answer = llm.invoke(prompt)

    return {"answer": answer}


def route_action(state: AgentState):
    return state["action"]


def main():
    builder = StateGraph(AgentState)

    builder.add_node("think", think_node)
    builder.add_node("act", act_node)
    builder.add_node("calculator", calculator_node)
    builder.add_node("text", text_node)
    builder.add_node("rag", rag_node)
    builder.add_node("final", final_node)

    builder.set_entry_point("think")

    builder.add_edge("think", "act")

    builder.add_conditional_edges(
        "act",
        route_action,
        {
            "calculator": "calculator",
            "text": "text",
            "rag": "rag",
            "final": "final"
        }
    )

    builder.add_edge("calculator", "think")
    builder.add_edge("text", "think")
    builder.add_edge("rag", "think")

    builder.add_edge("final", END)

    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())

    question = input("\nAsk: ")

    result = graph.invoke(
        {"question": question},
        config={"recursion_limit": 10}
    )

    print("\n Final Answer:")
    print(result["answer"])


if __name__ == "__main__":   main()

    
