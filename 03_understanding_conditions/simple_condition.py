from typing import TypedDict
from langgraph.graph import StateGraph, END

class MyState(TypedDict):
    number: int
    
def check_number(state: MyState):
    print("check_number")
    return state

def even_node(state: MyState):
    print("Even node")
    return {"Even": state["number"] * 2}

def odd_node(state: MyState):
    print("Odd node")
    return {"Odd": state["number"] + 1}

def decide_next(state: MyState):
    if(state["number"] % 2 ==0):
        return "even"
    else:
        return "odd"
def main():
    builder = StateGraph(MyState)
    builder.add_node("check_number",check_number)
    builder.add_node("even_node",even_node)
    builder.add_node("odd_node",odd_node)
    builder.set_entry_point("check_number")
    builder.add_conditional_edges("check_number",decide_next,
                                  {
                                      "even":"even_node",
                                      "odd":"odd_node"
                                  })
    builder.add_edge("even_node",END)
    builder.add_edge("odd_node",END)
    
    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())
    
    result = graph.invoke({"number":8})
    print("Final result ", result)
    
if __name__ == "__main__":    main()