import tiktoken
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# models
from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
# from langchain_google import ChatGoogleGenerativeAI

MODEL_PRICES = {
    "Input" : {
        "gpt-4.1-nano": 0.1/ 1_000_000,
        "gpt-4.1-mini": 0.4 / 1_000_000,
        "o4-mini": 0.15 / 1_000_000,
    },
    "Output" : {
        "gpt-4.1-nano": 0.4 / 1_000_000,
        "gpt-4.1-mini": 1.6 / 1_000_000,
        "o4-mini": 0.6 / 1_000_000,
    }
}


def init_page():
    st.set_page_config(
        page_title="My関西弁ChatGPT",
        page_icon="🐙",)
    st.header("My関西弁🐙ChatGPT🤖")
    st.sidebar.title("設定")

def init_messages():
    clear_botton = st.sidebar.button("Clear Chat", key="clear")
    # clear_botton が押された場合や、message_history がまだ存在しない場合に初期化
    if clear_botton or "message_history" not in st.session_state:
        st.session_state.message_history = [
            ("system", "あなたは親切なアシスタントです。関西弁で質問に答えてください。"),
            ]

def select_model():
    # スライダーを追加し、temperatureを0から2までの範囲で設定可能する
    # 初期値は0.0, 刻み幅は0.1

    
    models = ["gpt-4.1-nano", "gpt-4.1-mini", "o4-mini"]
    model = st.sidebar.radio("Choose a model:", models)
    if model == "o4-mini":
        st.sidebar.write("このモデルでは temperature は 1.0 固定です")
        temperature = 1.0
    else:
        temperature = st.sidebar.slider(
        "Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.1 
        )
    
    if model == "gpt-4.1-nano":
        st.session_state.model_name = "gpt-4.1-nano" #session_stateに保存
        # debug
        llm = ChatOpenAI(temperature=temperature, model=st.session_state.model_name)
        st.sidebar.write(f"[DEBUG]▶ Using LLM: {model}, temperature={getattr(llm, 'temperature', 'N/A')}")
        return llm

    elif model == "gpt-4.1-mini":
        st.session_state.model_name = "gpt-4.1-mini"    #session_stateに保存
        # debug
        llm = ChatOpenAI(temperature=temperature, model=st.session_state.model_name)
        st.sidebar.write(f"[DEBUG]▶ Using LLM: {model}, temperature={getattr(llm, 'temperature', 'N/A')}")
        return llm

    elif model == "o4-mini":
        st.session_state.model_name = "o4-mini"
        # debug
        llm = ChatOpenAI(temperature=1.0, model=st.session_state.model_name) # o4-miniはtemperatureをサポートしていないため、temperatureは指定しない
        st.sidebar.write(f"[DEBUG]▶ Using LLM: {model}, temperature={getattr(llm, 'temperature', 'N/A')}")
        return llm
    
    else:
        st.session_state.model_name = "gpt-4.1-nano" #session_stateに保存
        return ChatOpenAI(temperature=temperature, model=st.session_state.model_name)

def init_chain():
    llm = select_model()
    st.session_state.llm = llm
    
    prompt = ChatPromptTemplate.from_messages(
        [
            *st.session_state.message_history,  # 既存のメッセージ履歴を追加
            ("user", "{user_input}"),
        ]
    )
    output_parser = StrOutputParser()
    chain = prompt | st.session_state.llm | output_parser
    return chain


def get_message_counts(text):
    model_name = st.session_state.model_name
    
    # Gemini 系なら LLM インスタンスのメソッドに任せる
    if "gemini" in model_name:
        return st.session_state.llm.get_num_tokens(text)

    # GPT 系は tiktoken でカウント
    if "gpt" in model_name:
        try:
            encoding = tiktoken.encoding_for_model(model_name)
        except KeyError:
            # 未登録モデルが来たら標準の cl100k_base にフォールバック
            encoding = tiktoken.get_encoding("cl100k_base")
    else:
        # Claude 系など他モデルは仮に cl100k_base を使う
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(text))


def calc_and_display_costs():
    output_count = 0
    input_count = 0
    for role, message in st.session_state.message_history:
        # tiktokenを使ってトークン数をカウント
        token_count = get_message_counts(message)
        if role == "ai":
            output_count += token_count
        else:
            input_count += token_count
    
    # 初期状態で System Message のみが履歴に入っている場合はまだAPIコールが行われていない
    if len(st.session_state.message_history) == 1:
        return

    input_cost = MODEL_PRICES["Input"][st.session_state.model_name] * input_count
    output_cost = MODEL_PRICES["Output"][st.session_state.model_name] * output_count
    if "gemini" in st.session_state.model_name and (input_count + output_count) > 128000:
        input_cost *= 2
        output_cost *= 2
    
    cost = output_cost + input_cost

    st.sidebar.markdown("## コスト")
    st.sidebar.markdown(f"**トータルコスト: ${cost:.5f}**")
    st.sidebar.markdown(f"- 入力コスト: ${input_cost:.5f}")
    st.sidebar.markdown(f"- 出力コスト: ${output_cost:.5f}")


def main():
    init_page()
    init_messages()
    chain = init_chain()

    # チャット履歴の表示(第2章から少し位置が変更になっているので注意)
    for role, message in st.session_state.get("message_history", []):
        st.chat_message(role).markdown(message)
    
    if user_input := st.chat_input("聞きたいことを入力してな！"):
        st.chat_message("user").markdown(user_input)

        #LLMの返答をStreaming表示する
        with st.chat_message("ai"):
            response = st.write_stream(chain.stream({"user_input": user_input}))
        
        #チャット履歴に追加
        st.session_state.message_history.append(("user", user_input))
        st.session_state.message_history.append(("ai", response))

    #コストを計算して表示
    calc_and_display_costs()


if __name__ == "__main__":
    main()