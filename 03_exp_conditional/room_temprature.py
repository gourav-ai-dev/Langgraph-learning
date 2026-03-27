from typing import TypedDict
from langgraph.graph import StateGraph,END
from execute import execute_branching

class RoomState(TypedDict):
    temperature: int

def current_temperature(state: RoomState):
    print(f"Current temperature: {state['temperature']}°C")
    return {"temperature": state['temperature']} 

def stable_temperature(state: RoomState):
    print(f"Current temperature: {state['temperature']}°C")
    return {"temperature": state['temperature']}        

def increase_temperature(state: RoomState):
    print(f"Current temperature: {state['temperature']}°C")
    return {"temperature": state['temperature'] + 1 }

def decrease_temperature(state: RoomState):
    print(f"Current temperature: {state['temperature']}°C")
    return {"temperature": state['temperature'] - 1 }

def check_temperature(state: RoomState):
    if state['temperature'] < 18:
        return "too_cold"
    elif state['temperature'] > 26:
        return "too_hot"
    else:
        return "comfortable"

def main():
    builder = StateGraph(RoomState)
    builder.add_node("current_temperature", current_temperature)
    builder.add_node("increase_temperature", increase_temperature)
    builder.add_node("decrease_temperature", decrease_temperature)
    builder.add_node("stable_temperature", stable_temperature)
    
    builder.set_entry_point("current_temperature")
    
    builder.add_conditional_edges("current_temperature", check_temperature,{
        "too_cold": "increase_temperature",
        "too_hot": "decrease_temperature",
        "comfortable": "stable_temperature"
    })
    
    builder.add_edge("increase_temperature", "current_temperature")
    builder.add_edge("decrease_temperature", "current_temperature")
    builder.add_edge("stable_temperature", END)    
    
    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())
    execute_branching(graph)
    
    result  = graph.invoke({"temperature": 15})
    
    print(result)
    
if __name__ == "__main__":    main()    
        