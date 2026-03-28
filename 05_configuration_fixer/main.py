from typing import TypedDict, Optional
from langchain_community.llms import Ollama
from langgraph.graph import StateGraph, END
from execute import execute_branching
import os

llm = Ollama(model="llama3")

class GraphState(TypedDict):
    file_path: str
    config: str
    is_valid: bool
    tech_stack: str
    validation_reason: Optional[str]
    final_output: str
    output_path: str
    
    
def read_file_node(state: GraphState):
    try:
        with open(state["file_path"], "r") as f:
            content = f.read()

        return {
            "config": content,
        }

    except Exception as e:
        return {
            "config": "",
            "is_valid": False,
            "validation_reason": f"Error reading file: {str(e)}",
            "final_output": f"Error reading file: {str(e)}"
        }
        
def verify_node(state: GraphState):
    config = state["config"]

    prompt = f"""
    You are a strict Docker Compose validator.

    Check if the following config is valid.

    Rules:
    - Must be valid YAML
    - Must follow Docker Compose structure
    - Must not have missing required fields

    Respond ONLY in this format:
    VALID: true/false
    REASON: short explanation

    Config:
    {config}
    """

    response = llm.invoke(prompt)

    # simple parsing
    is_valid = "valid: true" in response.lower()

    return {
        "is_valid": is_valid,
        "validation_reason": response
    }


def correct_node(state: GraphState):
    prompt = f"""
    The following Docker config is invalid.

    Issues found:
    {state.get("validation_reason")}

    Fix it properly.

    Config:
    {state["config"]}

    Return ONLY corrected config.
    """

    fixed = llm.invoke(prompt)

    return {
        "config": fixed,
    }
    
def beautify_node(state: GraphState):
    prompt = f"""
    You are a DevOps assistant.

    Given a Docker configuration and validation feedback:

    VALIDATION ISSUES:
    {state.get("validation_reason")}

    FINAL CONFIG:
    {state["config"]}

    Create a clean report with:

    1. Corrected Docker Compose file
    2. List of issues found
    3. What was fixed

    Format clearly.
    """

    output = llm.invoke(prompt)

    return {"final_output": output}

def route_after_verify(state: GraphState):
    if state["is_valid"]:
        return "beautify_node"
    else:
        return "correct_node"

def write_file_node(state: GraphState):
    input_path = state["file_path"]

    # create output file name
    base, ext = os.path.splitext(input_path)
    output_path = base + "_fixed_report.md"

    with open(output_path, "w") as f:
        f.write(state["final_output"])

    return {
        "output_path": output_path
    }
    
def main():
    builder = StateGraph(GraphState)
    
    builder.add_node("read_file_node", read_file_node)
    builder.add_node("verify_node", verify_node)
    builder.add_node("correct_node", correct_node)
    builder.add_node("beautify_node", beautify_node)
    builder.add_node("write_file_node", write_file_node)
    

    builder.set_entry_point("read_file_node")

    builder.add_edge("read_file_node", "verify_node")

    builder.add_conditional_edges(
        "verify_node",
        route_after_verify,
        {
            "correct_node": "correct_node",
            "beautify_node": "beautify_node"
        }
        )

    builder.add_edge("correct_node", "verify_node")
    builder.add_edge("beautify_node", "write_file_node")
    builder.add_edge("write_file_node", END)

    graph = builder.compile()
    
    result = graph.invoke({"file_path": "docker-compose.yml", "tech_stack": "docker"}, config={"recursion_limit":100})
    execute_branching(graph)

    print("Saved at:", result["output_path"])
    
if __name__ == "__main__":    main()
