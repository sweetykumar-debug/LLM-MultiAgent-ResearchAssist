# 📚 RAG-Based Academic Research Assistant

A Retrieval-Augmented Generation (RAG) powered academic research assistant built using Streamlit, Ollama, and ChromaDB.

This system retrieves relevant research papers from an ArXiv dataset using semantic similarity search and generates structured, context-grounded academic responses using a locally hosted Large Language Model (LLM).

---

## 🚀 Project Overview

This project implements a modular RAG pipeline that:

- Performs semantic retrieval over research abstracts
- Generates structured academic responses
- Reduces hallucination through retrieval grounding
- Runs fully locally using Ollama
- Provides measurable evaluation metrics

The system achieved an evaluated **67% overall accuracy** based on structured testing.

---

## 🧠 System Architecture

User Query  
↓  
Streamlit Interface  
↓  
Embedding Model  
↓  
ChromaDB Vector Store  
↓  
Top-K Retrieval (k = 3)  
↓  
Ollama LLM  
↓  
Structured Academic Response  

---

## 🛠 Tech Stack

- **Frontend:** Streamlit  
- **LLM Engine:** Ollama (Mistral / LLaMA-based models)  
- **Vector Database:** ChromaDB  
- **Embeddings:** Sentence Transformers  
- **Dataset:** ArXiv Metadata Dataset  
- **Programming Language:** Python  

---

## 📂 Dataset Details

- Processed first 300 rows from ArXiv dataset  
- Embedded first 50 research abstracts  
- Implemented similarity-based retrieval  
- Built abstract-driven semantic search pipeline  

---

## 📊 Evaluation Framework

The system was evaluated using 10 structured research prompts across four performance metrics:

| Metric                          | Score |
|----------------------------------|--------|
| Conceptual Correctness           | 78%    |
| Retrieval Grounding              | 60%    |
| Hallucination Control            | 55%    |
| Question Coverage & Structure    | 75%    |

### 🎯 Overall Evaluated Accuracy: **67%**

**Classification:** Moderate Academic-Grade RAG System

---

## ✨ Core Features

- Retrieval-Augmented Generation (RAG) pipeline
- Context-grounded LLM responses
- Structured academic formatting
- Lightweight and extensible architecture
- Fully local execution (no external API dependency)

---

## ⚙️ Installation

Clone the repository:
git clone https://github.com/yourusername/rag-academic-research-assistant.git

cd rag-academic-research-assistant


Install dependencies:


pip install -r requirements.txt


---

## ▶️ Running the Application

Ensure Ollama is installed and running locally:


ollama run mistral


Then launch the Streamlit application:


streamlit run app.py


---

## 📁 Project Structure


├── app.py
├── embeddings.py
├── vector_store/
├── arxiv_data.csv
├── requirements.txt
└── README.md


---

## 📈 Future Improvements

- Embed full dataset instead of limited subset
- Add metadata-aware retrieval (title, authors, year)
- Implement strict grounding enforcement
- Improve hallucination mitigation strategies
- Increase retrieval diversity (dynamic top-k tuning)
- Add automated evaluation benchmarking

---

## 🎓 Learning Outcomes

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation architecture
- Vector similarity search
- LLM grounding techniques
- Prompt engineering for structured outputs
- Evaluation methodology for LLM systems
- Local LLM deployment workflows

---

## 📜 License

This project is intended for academic and educational purposes.
