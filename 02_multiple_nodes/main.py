from typing import TypedDict
from langgraph.graph import StateGraph, END


class MyState(TypedDict):
    number: str
    
def node_1(state: MyState):
    print("Node 1")
    new_number =state["number"] + 1
    return{"number": new_number}

def node_2(state: MyState):
    print("Node 2")
    new_number =state["number"] + 1
    return{"number": new_number}

def main():
    builder = StateGraph(MyState)
    
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    
    builder.set_entry_point("node_1")
    
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_2", END)
    
    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())    
    result = graph.invoke({"number": 5})
    
    print("Final result ", result)
    
    
if __name__ == "__main__":    
    main()