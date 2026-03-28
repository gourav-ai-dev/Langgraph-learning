import math

def calculator_tool(query: str):
    try:
        return str(eval(query, {"__builtins__": {}}, {"math": math}))
    except:
        return "Error in calculation"


def text_tool(query: str):
    return query.upper()


def rag_tool(query: str, retriever):
    docs = retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in docs])
    return context