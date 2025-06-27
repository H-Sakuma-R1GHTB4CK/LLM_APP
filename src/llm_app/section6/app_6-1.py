import base64
import streamlit as st
from langchain_openai import ChatOpenAI


def init_page():
    st.set_page_config(
        page_title="Image Recognizer",
        page_icon="📷")
    st.header("Image Recognizer 📷")
    st.sidebar.title("Options")


def main():
    init_page()

    llm = ChatOpenAI(
        # temperature=0,
        model="gpt-4.1-nano",
        # max_tokens=512, # なぜかmax_tokensを指定しないとエラーになるらしい
        )
    
    uploaded_file = st.file_uploader(
        label="Upload your Image file😇",
        type=["jpg", "jpeg", "png","gif", "webp"],
        )
    if uploaded_file:
        if user_input := st.chat_input("聞きたいことを入力して"):
            image_base64: str = base64.b64encode(uploaded_file.read()).decode()
            image: str = f"data:image/jpeg;base64,{image_base64}"

            query = [
                (
                    "user",
                    [
                        {"type":"text",
                         "text": user_input
                         },
                         {
                             "type":"image_url",
                             "image_url": {
                                 "url": image,
                                 "detail": "auto"
                            },
                        }
                    ]
                )
            ]
            st.markdown("### Question")
            st.write(user_input) # ユーザの質問を表示
            st.image(uploaded_file) # アップロードされた画像を表示
            st.markdown("### Answer")
            st.write_stream(llm.stream(query)) # type: ignore
    else:
        st.write("まずは画像をアップロードしてください。")  # ユーザに画像アップロードを促すメッセージ

if __name__ == "__main__":
    main()