# 🚀 Agentic RAG System (LangGraph + LangChain)

## 📌 Overview

This project demonstrates an **Agentic RAG (Retrieval-Augmented Generation) system** built using LangGraph.

The system can:

* Answer general questions
* Perform calculations
* Transform text
* Retrieve knowledge from documents

---

## 🧠 Key Concepts

### 🔹 Agent

An AI system that can:

* Think
* Decide actions
* Use tools
* Iterate until final answer

### 🔹 RAG (Retrieval-Augmented Generation)

Enhances LLM by fetching real data from documents.

---

## ⚙️ Architecture

User Question
→ Think Node (LLM decides)
→ Act Node (select tool)
→ Tool Execution
→ Observation
→ Loop until final

---

## 🛠 Tools Used

* Calculator Tool → math operations
* Text Tool → uppercase transformation
* RAG Tool → document retrieval

---

## 🔁 Agent Loop

Think → Act → Tool → Observe → Think → ... → Final Answer

---

## 📂 Project Structure

* `main.py` → Agent logic (LangGraph)
* `rag.py` → RAG setup (FAISS + embeddings)
* `tools.py` → Tools implementation
* `data/` → Knowledge base

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python main.py
```

---

## 🧪 Example Queries

* "What is LangGraph?"
* "25 * 4"
* "Explain RAG and convert to uppercase"

---

## 🚀 What You Learn

* LangGraph fundamentals
* Agent design pattern
* Tool-based reasoning
* RAG integration
* Multi-step AI workflows

---

## 🔥 Future Improvements

* Add memory
* Add API tools
* Improve prompts
* UI integration (React)

---

## 🧠 Final Insight

LLM = Brain
Tools = Execution

Together → Intelligent AI System 🚀
