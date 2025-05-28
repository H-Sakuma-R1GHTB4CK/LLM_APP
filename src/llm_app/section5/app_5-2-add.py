import traceback
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# models
from langchain_openai import ChatOpenAI

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Youtubeの動画を要約するためのプロンプト
from langchain_community.document_loaders import YoutubeLoader
from langchain_core.documents import Document

SUMMARIZE_PROMPT:str = """以下のコンテンツについて、内容を300字程度でわかりやすく要約してください
========
{content}
========
日本語で書いてください。
"""

SUPER_SUMMARIZE_PROMPT:str = """以下のコンテンツについて、内容を100字程度でわかりやすく関西弁で要約してください
========
{content}
========
日本語で書いてください。
"""

def init_page():
    st.set_page_config(
        page_title="YouTube要約アプリ",
        page_icon="🎥",
    )
    st.header("YouTUbe🎥要約アプリ📄")
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


def init_chain():
    llm = select_model()
    prompt = ChatPromptTemplate.from_messages([
        ("user", "{summarize_prompt}"),
    ])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain


def validate_url(url: str) -> bool:
    """URLの形式を検証する"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    

def get_content(url: str) -> str | None:
    """Document:
         - page_content: str
         - metadata: dict

            - source: str
            - title: str
            - description: Option[str]
            - view_count: int
            - thumbnail_url: Option[str]
            - publish_date: str
            - length: int
            - author: str
    """
    # Debug
    # last_err = None
    # lang_order=("en", "ja")
    # for lang in lang_order:
    #     st.write(f"[DEBUG]▶ Using language: {lang}")
    #     try:
    #         loader_dbg = YoutubeLoader.from_youtube_url(url,language=[lang])
    #         docs = loader_dbg.load()
    #         # 成功したらforループを抜ける
    #         break
    #     except Exception as e:
    #         last_err = e
    #     st.error(f"字幕が取得できませんでした: {lang}")
    # st.write(traceback.format_exc())
    # st.write(docs[0].page_content)  # 最初の Document の内容を表示


    # Youtubeの場合は、字幕(transcript)を取得して、要約に利用する
    with st.spinner("Fetching Content... / コンテンツを取得中..."):
            lang_order = ("en", "ja")  # 英語→日本語の優先順位で字幕を取得
            for lang in lang_order:
                st.write(f"[DEBUG]▶ Using language: {lang}")
                try:
                    loader = YoutubeLoader.from_youtube_url(
                        url,
                        language=[lang],  # 英語→日本語の優先順位で字幕を取得
                        # add_video_info=False # タイトルや再生数などのメタデータも取得するオプション。バージョンのせいかエラーになるのでコメントアウト
                        )
                    res = loader.load()
                    break  # 成功したらforループを抜ける
                except Exception as e:
                    last_err = e
                    st.caption("日本語または英語の字幕が取得できませんでした。URLが正しいか確認してください。")
                    # st.write(traceback.format_exc())  # エラーの詳細を表示

            # res は Document型 のリスト
            # res[0] は最初の Document で、page_content と metadata を持つ
            print(res)
            try:
                if res:
                    content = res[0].page_content
                    title = res[0].metadata.get("title", "No Title")
                    return f"Title: {title}\n\n{content}"
                else:
                    st.error("No content found in the provided URL.")
                    return None
            except Exception as e:
                st.error(f"Error fetching content: {e}")
                st.write(traceback.format_exc())  # エラーの詳細を表示
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
                 # コンテンツをテンプレートに埋め込んでおく
                prompt_text = SUMMARIZE_PROMPT.format(content=content)
                super_prompt_text = SUPER_SUMMARIZE_PROMPT.format(content=content)
                st.markdown("### 要約(300字程度)")
                # その完成形をプレースホルダー summarize_prompt に渡す
                summary_text: str = st.write_stream(chain.stream({"summarize_prompt": prompt_text}))
                num_chars = len(summary_text.replace("\n", ""))
                st.markdown(f"_（{num_chars} 文字）_")
                st.markdown("---")
                st.markdown("### 超要約(100字程度)")
                summary_text: str = st.write_stream(chain.stream({"summarize_prompt": super_prompt_text}))
                num_chars = len(summary_text.replace("\n", ""))
                st.markdown(f"_（{num_chars} 文字）_")
                st.markdown("---")
                st.markdown("### 元のコンテンツ")
                st.text(content)

    # コストを表示する場合は第3章と同様に実装
    # calc_and_display_costs()


if __name__ == "__main__":
    main()