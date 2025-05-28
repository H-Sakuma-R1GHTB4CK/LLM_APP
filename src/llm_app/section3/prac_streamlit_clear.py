import streamlit as st
from langchain_openai import ChatOpenAI

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
    temperature = st.sidebar.slider(
        "Temperature:", min_value=0.0, max_value=2.0, value=0.0, step=0.1 
        )
    models = ["gpt-4.1-nano", "gpt-4.1-mini", "o4-mini"]
    model = st.sidebar.radio("Choose a model:", models)
    if model == "gpt-4.1-nano":
        st.session_state.model_name = "gpt-4.1-nano" #session_stateに保存
        return ChatOpenAI(temperature=temperature, model=st.session_state.model_name)

    elif model == "gpt-4.1-mini":
        st.session_state.model_name = "gpt-4.1-mini"    #session_stateに保存
        return ChatOpenAI(temperature=temperature, model=st.session_state.model_name)

    elif model == "o4-mini":
        st.session_state.model_name = "o4-mini"
        return ChatOpenAI(temperature=temperature, model=st.session_state.model_name)
    

if __name__ == "__main__":
    AI_model = select_model()
    if AI_model:
        st.write(f"temperature is {AI_model.temperature}")
        st.write(f"model_name is {AI_model.model_name}")
        st.write(f"AI_model is {AI_model}")
    init_messages()