from langchain_community.llms import Ollama
from langgraph.graph import StateGraph, END
from typing import TypedDict

class MyStateGraph(TypedDict):
    number: str

def node_1(state: MyStateGraph):
    print("Node 1")
    new_number  = state["number"] + 1
    return {"number": new_number}


    
    

def main():
    builder =  StateGraph(MyStateGraph)
    builder.add_node("node 1",node_1)
    builder.set_entry_point("node 1")
    builder.add_edge("node 1", END)
    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())    
    result = graph.invoke({"number": 5})
    
    print("Final result ", result)
    
    
if __name__ == "__main__":    
    main()