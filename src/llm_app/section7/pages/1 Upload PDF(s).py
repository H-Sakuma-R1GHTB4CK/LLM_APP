import fitz # PyMuPDF
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def init_page():
    st.set_page_config(
        page_title="Upload PDF(s)",
        page_icon="📄"
    )
    st.sidebar.title("Options")


def init_messages():
    clear_button = st.sidebar.button("Clear DB", key="clear")
    if clear_button and "vectorstore" in st.session_state:
        del st.session_state["vectorstore"]
        

def get_pdf_text():
    pdf_file = st.file_uploader(
        label="Upload your PDF file(s) 📄",
        type=["pdf"]
    )

    if pdf_file:
        pdf_text = ""
        with st.spinner("PDFを読み込んでいます..."):
            pdf_doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            for page in pdf_doc:
                pdf_text += page.get_text()
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="text_embedding-3-small",
            # 適切なチャンクサイズは質問対象のPDFの内容によるため、調整が必要
            chunk_size=500,
            chunk_overlap=10,
        )
        return text_splitter.split_text(pdf_text)
    else:
        st.warning("PDFファイルをアップロードしてください。")
        return None
    

