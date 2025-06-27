import base64
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper


GPT4V_PROMPT = """
まず、以下のユーザーのリクエストとアップロードされた画像を注意深く読んでください。

次に、アップロードされた画像に基づいて画像を生成するというユーザーのリクエストに沿ったDALL-Eプロンプトを作成してください。
DALL-Eプロンプトは必ず英語で作成してください。

ユーザー入力: {user_input}

プロンプトでは、ユーザーがアップロードした写真に何が描かれているか、どのように構成されているかを詳細に説明してください。
写真に何が写っているのかはっきりと見える場合は、示されている場所や人物の名前を正確に書き留めてください。
写真の構図とズームの程度を可能な限り正確に説明してください。
写真の内容を可能な限り正確に再現することが重要です。

DALL-E 3向けのプロンプトを英語で回答してください:

"""


def init_page():
    st.set_page_config(
        page_title="Image Converter with DALL-E",
        page_icon="📷"
    )
    st.header("Image Converter with DALL-E 📷")


def main():
    init_page()

    llm = ChatOpenAI(
        model="gpt-4.1-nano",
    )

    dalle3_image_url = None
    uploaded_file = st.file_uploader(
        label = "Upload your Image file😇",
        type = ["jpg", "jpeg", "png", "gif", "webp"]
    )
    if uploaded_file:
        if user_input := st.chat_input("画像をどのように加工したか教えてね"):
            # 読み取ったファイルをBase64でエンコード
            image_base64: str = base64.b64encode(uploaded_file.read()).decode()
            image: str = f"data:image/jpeg;base64,{image_base64}"

            query = [
                (
                    "user",
                    [
                        {"type": "text", "text": GPT4V_PROMPT.format(user_input=user_input)},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image,
                                "detail": "auto"
                            },
                        }
                    ]
                )
            ]
            st.markdown("### Image Prompt")
            image_prompt = st.write_stream(llm.stream(query))  # type: ignore

            with st.spinner("DALL-E 3が画像を生成しています..."):
                dalle3 = DallEAPIWrapper(
                    model="dall-e-3",
                    size="1024x1024",
                    n=1,
                )
                dalle3_image_url = dalle3.run(image_prompt) # type: ignore
    else:
        st.write("まずは画像をアップロードしてください。")

    if dalle3_image_url and uploaded_file:
        st.markdown("### Question")
        st.write(user_input)  # ユーザの質問を表示 # type: ignore
        st.image(
            uploaded_file,
            use_column_width="auto"
        )

        st.markdown("### DALL-E 3 Image")
        st.image(
            dalle3_image_url,
            caption="DALL-E 3によって生成された画像",
            use_column_width="auto"
        )

if __name__ == "__main__":
    main()
    