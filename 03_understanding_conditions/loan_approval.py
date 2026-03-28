from typing import TypedDict
from langgraph.graph import StateGraph,END
from execute import execute_branching

class LoanState(TypedDict):
    credit_score: int
    income: int
    
def user_details(state: LoanState):
    print(f"User details: Credit Score: {state['credit_score']}, Income: {state['income']}")
    return {"credit_score": state['credit_score'], "income": state['income']}

def manual_review(state: LoanState):
    print(f"Manual review required for Credit Score: {state['credit_score']}, Income: {state['income']}")
    return {"credit_score": state['credit_score'], "income": state['income']}

def reject(state: LoanState):
    print(f"Loan rejected for Credit Score: {state['credit_score']}, Income: {state['income']}")
    return {"credit_score": state['credit_score'], "income": state['income']}

def approved(state: LoanState):
    print(f"Loan approved for Credit Score: {state['credit_score']}, Income: {state['income']}")
    return {"credit_score": state['credit_score'], "income": state['income']}


def check_loan_eligibility(state: LoanState):
    if state['credit_score'] >= 600 and state['income'] >= 20000:
        return "approved"
    elif state["credit_score"] >= 600 and state["income"] < 20000:
        return "manual_review"
    else:
        return "reject"

def main():
    builder = StateGraph(LoanState)
    
    builder.add_node("user_details", user_details)
    builder.add_node("manual_review", manual_review)
    builder.add_node("reject", reject)
    builder.add_node("approved", approved)
    
    builder.set_entry_point("user_details")
    
    builder.add_edge("approved", END)
    builder.add_edge("reject", END)
    builder.add_edge("manual_review", END)


    builder.add_conditional_edges("user_details", check_loan_eligibility, {
        "approved": "approved",
        "manual_review": "manual_review",
        "reject": "reject"
    })
    
    
    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())
    execute_branching(graph)
    result = graph.invoke({"credit_score": 700, "income": 50000})
    print(result)
    

if __name__ == "__main__":    main()