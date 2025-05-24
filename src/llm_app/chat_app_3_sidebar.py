import streamlit as st

# サイドバーのタイトルを表示
st.sidebar.title("Options")

# サイドバーにオプションボタンを設置
model = st.sidebar.radio("Choose a model:", ("gpt-4.1-nano", "gpt-4.1-mini", "o4-mini"))
print(type(model)) # debug
print(model) # debug
# st.write(f"選択されたモデル: {model}") # debug

# サイドバーにスライダーを追加し、temperatureを0から2までの範囲で設定可能する
# 初期値は0.0, 刻み幅は0.1
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, value=0.0, step=0.1)

# Streamlitはmarkdownを書けばいい感じにHTMLで表示してくれる
# (サイドバー以外の場所でもmarkdownは使える)
st.sidebar.markdown("## Costs")
st.sidebar.markdown("**Total cost**")
st.sidebar.markdown("- Input cost: $0.001 ") # dummy
st.sidebar.markdown("- Output cost: $0.001") # dummy