import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# models
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from llm_app.config import (
    GPT_4_1_NANO, GPT_4_1_MINI, O4_MINI
)

def init_page():
    st.set_page_config(
        page_title="Ask My PDF(s)",
        page_icon="❓"
    )
    st.sidebar.title("Options")


def select_model(temperature: float = 0.0) -> BaseChatModel:
    models = (GPT_4_1_NANO, GPT_4_1_MINI, O4_MINI)
    model = st.sidebar.radio("Choose a model:", models)
    if model in (GPT_4_1_NANO, GPT_4_1_MINI, O4_MINI):
        # OpenAI以外のモデルに対応するためのif文
        # 今はOpenAIのみなので意味はない
        return ChatOpenAI(
            temperature=temperature,
            model=model
        )
    else:
        return ChatOpenAI(
            temperature=temperature,
            model="gpt-4.1-nano"  # デフォルトモデルを設定
        )

def init_qa_chain():
    llm = select_model()
    prompt = ChatPromptTemplate.from_template(
        """
        あなたは親切なアシスタントです。以下の前提知識を用いて、ユーザーからの質問に答えてください
        
        ========
        前提知識
        {context}
        
        ========
        ユーザーからの質問
        {question}
        """
        )
    retriever = st.session_state.vectorstore.as_retriever(
        # "mmr", "similarity_score_threshold" などもある
        serch_type = "similarity",
        #文書を何個取得するか(defaulte: 4)
        search_kwargs={"k":5}
        )
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def page_ask_my_pdf():
    chain = init_qa_chain()

    if query := st.text_input("PDFへの質問を書いてね: ", key="input"):
        st.markdown("## Answer")
        st.write_stream(chain.stream(query))


def main():
    init_page()
    st.title("PDF QA ❓")
    if "vectorstore" not in st.session_state:
        st.warning("まずはPDFをアップロードしてください。")
    else:
        page_ask_my_pdf()


if __name__ == "__main__":
    main()
