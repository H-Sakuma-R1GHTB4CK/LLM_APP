import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    st.set_page_config(
        page_title = "関西弁AIアシスタント",
        page_icon = "🤖",
    )
    st.header("my関西弁AI🤖")

    # チャット履歴の初期化 message_historyがなければ作成
    if "message_history" not in st.session_state:
        st.session_state.message_history = [
            # System Promptを設定("system"はSystem Promptを意味する)
            ("system", "あなたは優秀なAIアシスタントです。絶対に関西弁で返答してください。"),
        ]

    # ChatGPTに質問を与えて回答を取り出す（パースする）処理を作成(1.-4.の処理)
    # 1. ChatGPTのモデルを指定
    # デフォルトではgpt-3.5-turboが指定されている
    # アカウント設定で"gpt-4.1-nano"のみ許可しているので、それを設定する
    llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)

    # 2. ユーザーの質問を受け取り、ChatGPTに渡すためのテンプレートを作成
    # 　テンプレートには過去のチャット履歴を含めるように設定
    prompt = ChatPromptTemplate.from_messages([
        *st.session_state.message_history,
        ("user", "{user_input}"), #ここにあとでユーザーの入力が入る
    ])

    # 3. ChatGPTの返答(=出力)をパースするための処理を呼び出し
    output_parser = StrOutputParser()

    # 4. ユーザーの質問をChatGPTに渡し、返答を取り出す連続的な処理(chain)を作成
    #   各要素を|(パイプ)でつなげることで、連続的な処理を作成するのがLCELの特徴
    chain = prompt | llm | output_parser

    # ユーザーの入力を監視
    if user_input := st.chat_input("聞きたいことを入力してな！"):
        with st.spinner("ChatGPTに聞いてるで..."):
            response = chain.invoke({"user_input": user_input})

        # ユーザーの質問とChatGPTの返答を履歴に追加
        st.session_state.message_history.append(("user", user_input))
        st.session_state.message_history.append(("assistant", response))

    # チャット履歴を表示
    for role, message in st.session_state.get("message_history", []):
        # # roleが"system"の場合は表示しない
        # if role == "system":
        #     continue
        st.chat_message(role).markdown(message)


if __name__ == "__main__":
    main()