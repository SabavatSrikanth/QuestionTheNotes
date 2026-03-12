# 📘 QuestionTheNotes

**QuestionTheNotes** is an AI-powered notes assistant built with Streamlit and LangChain. It allows users to upload their study materials or documents (PDF, DOCX, TXT) and instantly ask questions about the content. 

Under the hood, it uses **Retrieval-Augmented Generation (RAG)** powered by Google's Gemini AI and FAISS vector stores to ensure that every answer is strictly sourced from your uploaded materials—eliminating hallucinations.

## ✨ Features

* **Multi-Format Support:** Upload `.pdf`, `.docx`, or `.txt` files easily.
* **Context-Aware AI:** Powered by Google's `gemini-1.5-flash` model for fast, accurate answers.
* **Strict Sourcing:** The AI is prompted to reply *only* using the provided context. If the answer isn't in your notes, it will honestly tell you.
* **Fast Retrieval:** Utilizes local FAISS vector search and `embedding-001` to instantly find the most relevant chunks of your text.
* **Modern UI:** Features a custom CSS chat interface and animated Lottie graphics for a polished user experience.

## 🛠️ Tech Stack

* **Frontend UI:** Streamlit, Streamlit-Lottie
* **LLM & Embeddings:** Google Generative AI (Gemini API)
* **Orchestration:** LangChain
* **Vector Store:** FAISS (CPU)
* **Document Parsers:** PyPDF, python-docx

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/SabavatSrikanth/QuestionTheNotes.git
cd QuestionTheNotes
```