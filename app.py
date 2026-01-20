import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
import os
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma



# Load environment variables (works locally with .env)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Page configuration
st.set_page_config(
    page_title="Chat with PDF",
    page_icon="📚",
    layout="wide"
)

def get_pdf_texts(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                page_text = page_text.replace('\x00', '')
                text += page_text + "\n"
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    
    unique_chunks = list(set(chunks))
    print(f"Total chunks: {len(chunks)}, Unique chunks: {len(unique_chunks)}")
    
    return unique_chunks


def get_vector_store(text_chunks):
    # Force-load model (important for Streamlit Cloud)
    _ = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    vectordb = Chroma.from_texts(
        texts=text_chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )

    return vectordb

    

def get_conversational_chain():
    # Embeddings (CPU-safe for Streamlit Cloud)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    # 🔴 FAISS REMOVED → ✅ ChromaDB used
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    prompt_template = """You are a helpful assistant that answers questions based on the provided context from PDF documents.

Instructions:
- Use ONLY the information from the context below to answer the question
- Provide a clear, concise, and well-structured answer
- If the context doesn't contain enough information to answer the question, say "I don't have enough information in the provided documents to answer this question."
- Do NOT repeat the same information multiple times
- Do NOT make up information that's not in the context

Context:
{context}

Question: {question}

Answer (be specific and concise):"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    # Get API key from Streamlit secrets or environment variable
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        st.error("⚠️ GROQ_API_KEY not found! Please add it to Streamlit secrets or .env file")
        st.stop()

    model = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        max_tokens=500,
        api_key=api_key
    )

    chain = RetrievalQA.from_chain_type(
        llm=model,
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        ),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    return chain



def user_input(user_question):
    try:
        chain = get_conversational_chain()
        
        response = chain.invoke({"query": user_question})
        
        st.write("### 💬 Answer:")
        st.write(response["result"])
        
        if "source_documents" in response:
            with st.expander("📄 View Source Chunks"):
                for i, doc in enumerate(response["source_documents"]):
                    st.write(f"**Chunk {i+1}:**")
                    st.write(doc.page_content[:300] + "...")
                    st.write("---")
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def main():
    st.title("📚 Chat with Multiple PDFs")
    st.markdown("Upload your PDF files and ask questions about their content!")

    with st.sidebar:
        st.header("📁 Upload Documents")
        pdf_docs = st.file_uploader(
            "Choose PDF files & Click 'Process PDFs'",
            accept_multiple_files=True,
            type=['pdf']
        )
        
        if st.button("🚀 Process PDFs", type="primary"):
            if pdf_docs:
                with st.spinner("Processing your PDFs..."):
                    raw_text = get_pdf_texts(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.session_state.processed = True
                st.success("✅ PDFs processed successfully!")
            else:
                st.warning("⚠️ Please upload at least one PDF file.")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("This app uses AI to answer questions from your PDF documents.")
        st.markdown("**Powered by:** LangChain + Groq + ChromaDB")

    if 'processed' not in st.session_state:
        st.info("👈 Upload PDFs from the sidebar to get started!")
    else:
        user_question = st.text_input("❓ Ask a question about your documents:")
        
        if user_question:
            user_input(user_question)


if __name__ == "__main__":
    main()
