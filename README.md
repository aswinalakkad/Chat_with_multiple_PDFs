# 📚 Chat with Multiple PDFs

An AI-powered application that allows you to upload PDF documents and ask questions about their content using natural language.

## Features

- 📄 Upload multiple PDF files
- 🤖 Ask questions in natural language
- 💡 Get accurate answers based on document content
- 🔍 View source chunks for transparency

## Tech Stack

- **Streamlit** - Web interface
- **LangChain** - LLM orchestration
- **Groq** - Fast LLM inference
- **FAISS** - Vector similarity search
- **Sentence Transformers** - Text embeddings

## Local Setup

1. Clone the repository
```bash
git clone https://github.com/your-username/pdf-chat-app.git
cd pdf-chat-app
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.streamlit/secrets.toml` and add your Groq API key
```toml
GROQ_API_KEY = "your-api-key-here"
```

4. Run the app
```bash
streamlit run app.py
```

## Deployment

This app is deployed on Streamlit Community Cloud.

## License

MIT License