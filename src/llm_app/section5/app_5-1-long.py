import traceback
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain.text_splitter import RecursiveCharacterTextSplitter
# models
from langchain_openai import ChatOpenAI
import tiktoken

import requests
from bs4 import BeautifulSoup
from typing import cast
from urllib.parse import urlparse


SUMMARIZE_PROMPT:str = """以下のコンテンツについて、内容を300字程度でわかりやすく要約してください
========
{content}
========
日本語で書いてください。
"""


def init_page():
    st.set_page_config(
        page_title="Web要約アプリ",
        page_icon="📄",
    )
    st.header("Web要約アプリ📄")
    st.sidebar.title("設定")


def select_model(temperature:float=0) -> ChatOpenAI:
    models = ("gpt-4.1-nano", "gpt-4.1-mini", "o4-mini")
    model = st.sidebar.radio("Choose a model:", models)
    if model is None:
        model = "gpt-4.1-nano" # デフォルトモデルを設定
    
    if model == "o4-mini":
        st.sidebar.write("このモデルでは temperature は 1.0 固定です")
        temperature = 1.0
    else:
        temperature = st.sidebar.slider(
            "Temperature:", min_value=0.0, max_value=2.0, step=0.1 
        )
    
    llm = ChatOpenAI(temperature=temperature, model=model)
    st.session_state.model_name = model  # session_stateに保存
    st.sidebar.write(f"[DEBUG]▶ Using LLM: {model}, temperature={getattr(llm, 'temperature', 'N/A')}")
    return llm


def init_summarize_chain():
    llm = select_model()
    prompt = ChatPromptTemplate.from_messages([
        ("user", SUMMARIZE_PROMPT),
    ])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain

def init_chain():
    summarize_chain = init_summarize_chain()

    text_splitter = \
        RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            # モデルによりトークン数カウント方法が違うため、model_nameを指定する
            model_name = "gpt-4",
            # チャンクサイズはトークン数でカウント
            chunk_size = 16000,
            chunk_overlap = 0,
            # 日本語文書の処理でセパレータを変更するのなら以下の文のコメントアウトを外す
            # separators=["\n\n", "\n", "。", "、", " ", ""]
            )
    text_split = RunnableLambda(
        lambda x: [
        {"content": doc}
        for doc in text_splitter.split_text(
            cast(dict[str, str], x)["content"]
        )
    ]
    )
    text_concat = RunnableLambda(
        lambda x: {"content": "\n".join(cast(list[str], x))}
    )
    map_reduce_chain = (
        text_split | summarize_chain.map() | text_concat | summarize_chain
    )

    def route(x):
        encoding = tiktoken.encoding_for_model("gpt-4")
        token_count = len(encoding.encode(x['content']))
        if token_count > 16000:
            return map_reduce_chain
        else:
            return summarize_chain
    chain = RunnableLambda(route)
    return chain




def validate_url(url: str) -> bool:
    """URLの形式を検証する"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    

def get_content(url: str) -> str | None:
    """指定されたURLからコンテンツを取得する"""
    try:
        with st.spinner("Fetching Content... / コンテンツを取得中..."):
            response = requests.get(url)
            response.raise_for_status()  # HTTPエラーをチェック
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # なるべく本文である可能性が高い要素を抽出
            if soup.main:
                return soup.main.get_text()
            elif soup.article:
                return soup.article.get_text()
            elif soup.body:
                return soup.body.get_text()
            else:
                return soup.get_text()
    except Exception as e:
        st.error(f"Error fetching content: {e}")
        return None


def main():
    init_page()
    chain = init_chain()

    # ユーザーの入力を監視
    if url := st.text_input("URL: ", key="input"):
        is_valid_url = validate_url(url)
        if not is_valid_url:
            st.error("無効なURLです。正しいURLを入力してください。")
        else:
            if content := get_content(url):
                st.markdown("### 要約")
                st.write_stream(chain.stream({"content": content}))
                st.markdown("---")
                st.markdown("### 元のコンテンツ")
                st.text(content)

    # コストを表示する場合は第3章と同様に実装
    # calc_and_display_costs()


if __name__ == "__main__":
    main()