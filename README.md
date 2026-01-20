📚 Chat with Multiple PDFs

An AI-powered RAG (Retrieval-Augmented Generation) application that lets you upload multiple PDF documents and ask questions about their content using natural language.

The app retrieves relevant document chunks and generates accurate answers using a fast LLM.

✨ Features

📄 Upload multiple PDF files

🤖 Ask questions in natural language

🔍 Answers grounded only in uploaded documents

📌 View source document chunks for transparency

⚡ Fast responses powered by Groq

🧠 How It Works (High Level)

PDFs are uploaded and parsed

Text is split into chunks

Chunks are embedded using Sentence Transformers

Embeddings are stored in ChromaDB

Relevant chunks are retrieved for each query

Groq LLM generates answers using retrieved context

🛠 Tech Stack

Streamlit – Web UI

LangChain – RAG orchestration

Groq – Fast LLM inference

ChromaDB – Vector database (cloud-safe)

Sentence Transformers – Text embeddings

PyPDF – PDF parsing

⚠️ FAISS was intentionally removed to ensure Streamlit Cloud compatibility.

🚀 Local Setup
1️⃣ Clone the repository
git clone https://github.com/aswinalakkad/Chat_with_multiple_PDFs.git
cd Chat_with_multiple_PDFs

2️⃣ Create & activate environment (recommended)
conda create -n chatpdf python=3.10 -y
conda activate chatpdf

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add Groq API Key

Create .streamlit/secrets.toml:

GROQ_API_KEY = "your_groq_api_key_here"


OR set it as an environment variable:

export GROQ_API_KEY="your_groq_api_key_here"

5️⃣ Run the app
streamlit run app.py

☁️ Deployment

This application is deployed using Streamlit Community Cloud and is fully compatible with CPU-only environments.

📌 Notes

Answers are generated only from document context

If the answer is not found, the model clearly states so

No hallucinated or external information is used

📄 License

MIT License
