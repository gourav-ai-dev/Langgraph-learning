from typing import TypedDict
from langgraph.graph import StateGraph, END
from execute import execute_branching

class MyState(TypedDict):
    number: int
    target: int

def intial_node(state: MyState):
    print("initial node")
    return state

def small_node(state: MyState):
    print("small node")
    return {"number": state["number"] + 1}

def medium_node(state: MyState):
    print("medium node")
    return {"number": state["number"]}

def large_node(state: MyState):
    print("large node")
    return {"number": state["number"] - 1}

def check_number(state: MyState):
    print("check number")
    if state["number"] <  state["target"]:
        
        return "small"
    elif state["number"] >  state["target"]:
        return "large"
    else:
        return "medium"
    
def main():
    builder = StateGraph(MyState)
    target = int(input("set the Target"))
    number = int(input("set the initial number"))
    state: MyState = {"number": number, "target": target}
    builder.add_node("initial_node", intial_node)
    builder.add_node("small_node", small_node)
    builder.add_node("medium_node", medium_node)
    builder.add_node("large_node", large_node)
    
    builder.set_entry_point("initial_node")
    builder.add_conditional_edges("initial_node", 
                                  check_number,
                                  {
                                      "small": "small_node",
                                      "medium": "medium_node",
                                      "large": "large_node"
                                  })
    
    builder.add_edge("small_node", "initial_node")
    builder.add_edge("large_node", "initial_node")
    builder.add_edge("medium_node", END)
    
    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())
    
    result = graph.invoke(state, config={"recursion_limit":200})
    print("Final result ", result)
    
    execute_branching(graph)
    
if __name__ == "__main__":    main()