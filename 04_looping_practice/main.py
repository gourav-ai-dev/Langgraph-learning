from typing import TypedDict
from langgraph.graph import StateGraph, END

class MyState(TypedDict):
    number: int


def increment_node(state: MyState):
    print("increment state", state["number"])
    return {"number": state["number"] + 1}


def should_continue(state: MyState):
    print("should continue state")
    if state["number"] > 10:
        return "end"
    else:
       return "continue"


def main():
    builder = StateGraph(MyState)

    builder.add_node("increment", increment_node)

    builder.set_entry_point("increment")

    builder.add_conditional_edges(
        "increment",
        should_continue,
        {
            "continue":"increment",
            "end":END
        }
    )

    graph = builder.compile()

    graph_obj = graph.get_graph()
    
    with open("graph.dot", "w") as f:
         f.write("digraph G {\n")
         
         # Add nodes
         for node_id in graph_obj.nodes:
             f.write(f'  "{node_id}";\n')
         
         # Add edges
         for edge in graph_obj.edges:
             label = f' [label="{edge.data}"]' if edge.data else ""
             f.write(f'  "{edge.source}" -> "{edge.target}"{label};\n')

         f.write("}")
    
    result = graph.invoke({"number": 7})

    print("final Result", result)


if __name__ == "__main__":    main()