import fitz # PyMuPDF
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from llm_app.config import EMBEDDING_3_SMALL
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
                pdf_text += page.get_text() # type: ignore
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name=EMBEDDING_3_SMALL,
            # 適切なチャンクサイズは質問対象のPDFの内容によるため、調整が必要
            chunk_size=500,
            chunk_overlap=10,
        )
        return text_splitter.split_text(pdf_text)
    else:
        st.warning("PDFファイルをアップロードしてください。")
        return None
    

def build_vector_store(pdf_text: list[str]) -> None:
    with st.spinner("Saving to vector store ..."):
        if 'vectorstore' in st.session_state:
            st.session_state.vectorstore.add_texts(pdf_text)
        else:
            # ベクトルDBの初期化と文書の追加を同時に行う
            # Langchain の Document Loader を利用した場合は`from_documents`にする
            st.session_state.vectorstore = FAISS.from_texts(
                pdf_text,
                OpenAIEmbeddings(model=EMBEDDING_3_SMALL)
            )
            
            # FAISSのデフォルト設定はL2距離となっている
            # コサイン距離にしたい場合は以下のようにする
            # from langchain_community.vectorstores.utils import DistanceStrategy
            # st.session_state.vectorstore = FAISS.from_texts(
            #    pdf_text,
            #    embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
            #    distance_strategy=DistanceStrategy.COSINE
            # )


def page_pdf_upload_and_build_vector_store():
    st.title("PDF Upload📄")
    pdf_text = get_pdf_text()
    if pdf_text:
        build_vector_store(pdf_text)


def main():
    init_page()
    init_messages()
    page_pdf_upload_and_build_vector_store()


if __name__ == "__main__":
    main()