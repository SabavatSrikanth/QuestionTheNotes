import os
import warnings
import requests
import streamlit as st
from dotenv import load_dotenv
from docx import Document
from pypdf import PdfReader
from streamlit_lottie import st_lottie

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

warnings.filterwarnings("ignore")

# =========================
# Load API Key
# =========================
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Add it to your .env file.")
    st.stop()

# =========================
# Lottie Animation Loader
# =========================
def load_lottie_url(url: str):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# =========================
# Custom CSS (HTML Styling)
# =========================
st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
font-family:Segoe UI;
}

.title{
text-align:center;
font-size:42px;
font-weight:700;
margin-bottom:5px;
}

.subtitle{
text-align:center;
opacity:0.8;
margin-bottom:30px;
}

.chat-bubble{
padding:14px;
margin:10px 0;
border-radius:14px;
max-width:80%;
font-size:15px;
line-height:1.6;
}

.user-bubble{
background:linear-gradient(135deg,#4CAF50,#2e7d32);
margin-left:auto;
text-align:right;
}

.bot-bubble{
background:#1f2933;
border:1px solid #334155;
margin-right:auto;
}

.footer{
text-align:center;
margin-top:40px;
opacity:0.6;
font-size:13px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================

st.markdown('<div class="title">📘 QuestionTheNotes</div>', unsafe_allow_html=True)
st.markdown(
'<div class="subtitle">Upload your notes and ask questions instantly using AI</div>',
unsafe_allow_html=True
)

col1, col2 = st.columns([1,4])

with col1:
    lottie = load_lottie_url(
        "https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json"
    )
    if lottie:
        st_lottie(lottie, height=110)

with col2:
    st.markdown("""
**How it works**

1️⃣ Upload notes  
2️⃣ Ask a question  
3️⃣ Get answers from your content only  
""")

st.markdown("---")

# =========================
# Upload Section
# =========================

st.subheader("📂 Upload your notes")

file = st.file_uploader(
"Supported formats: PDF, DOCX, TXT",
type=["pdf","docx","txt"]
)

# =========================
# File Processing
# =========================

if file is not None:

    with st.status("📄 Processing your file...", expanded=True) as status:

        try:

            text = ""
            status.update(label="Reading file...")

            if file.type == "application/pdf":
                pdf = PdfReader(file)
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted

            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = Document(file)
                for para in doc.paragraphs:
                    text += para.text + "\n"

            elif file.type == "text/plain":
                text = file.read().decode("utf-8")

            if not text.strip():
                status.update(label="No readable text found ❌", state="error")
                st.stop()

            status.update(label="Splitting text...")

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=400,
                chunk_overlap=80
            )

            chunks = splitter.split_text(text)

            status.update(label="Creating embeddings...")

            embeddings = GoogleGenerativeAIEmbeddings(
                model="embedding-001",
                google_api_key=GOOGLE_API_KEY
            )

            vector_store = FAISS.from_texts(chunks, embeddings)

            status.update(label="File processed successfully ✅", state="complete")

        except Exception as e:
            status.update(label="Processing error ❌", state="error")
            st.error(e)
            st.stop()

# =========================
# Question Section
# =========================

    st.subheader("💬 Ask a question")

    user_query = st.text_input(
        "Ask something about your notes",
        placeholder="Example: Explain this topic simply"
    )

    if user_query:

        with st.status("🤔 Generating answer...", expanded=True) as q_status:

            try:

                q_status.update(label="Searching notes...")

                docs = vector_store.similarity_search(user_query, k=3)

                context = "\n\n".join([doc.page_content for doc in docs])

                q_status.update(label="Generating AI answer...")

                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    temperature=0.3,
                    google_api_key=GOOGLE_API_KEY
                )

                prompt = ChatPromptTemplate.from_template("""

Answer the question using ONLY the context below.

<context>
{context}
</context>

Question: {input}

If the answer is not in the context, say:
"I couldn't find that in the uploaded notes."

""")

                chain = prompt | llm | StrOutputParser()

                output = chain.invoke({
                    "context": context,
                    "input": user_query
                })

                q_status.update(label="Answer ready ✅", state="complete")

                st.markdown(
                    f'<div class="chat-bubble user-bubble">{user_query}</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="chat-bubble bot-bubble">{output}</div>',
                    unsafe_allow_html=True
                )

            except Exception as e:

                q_status.update(label="Error generating answer ❌", state="error")
                st.error(e)

# =========================
# Footer
# =========================

st.markdown(
'<div class="footer">⚡ QuestionTheNotes • AI Notes Assistant</div>',
unsafe_allow_html=True
)