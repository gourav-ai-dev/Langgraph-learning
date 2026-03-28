from typing import TypedDict
from langgraph.graph import StateGraph, END


class MyState(TypedDict):
    number: int

def intial_node(state: MyState):
    print("initial node")
    return state

def small_node(state: MyState):
    print("small node")
    return {"number": state["number"]}

def medium_node(state: MyState):
    print("medium node")
    return {"number": state["number"]}
 
def large_node(state: MyState):
    print("large node")
    return {"number": state["number"]}

def check_number(state: MyState):
    print("check number")
    if state["number"] < 10:
        return "small"
    elif state["number"] < 20:
        return "medium"
    else:
        return "large"

def main():
    builder = StateGraph(MyState)
    
    builder.add_node("initial_node", intial_node)
    builder.add_node("small_node", small_node)
    builder.add_node("medium_node", medium_node)
    builder.add_node("large_node", large_node)
    
    builder.set_entry_point("initial_node")
    builder.add_conditional_edges("initial_node", check_number,
                                  {
                                      "small": "small_node",
                                      "medium": "medium_node",
                                      "large": "large_node"
                                  })
    
    builder.add_edge("small_node", END)
    builder.add_edge("medium_node", END)
    builder.add_edge("large_node", END)
    
    graph = builder.compile()
    print(graph.get_graph().draw_ascii())
    result = graph.invoke({"number": 15})
    print("Final result ", result)
    
if __name__ == "__main__":    main()