import tiktoken

def main():
    print("Hello from llm_app.app.main()")

def count_tokens(text: str, model_name: str) -> int:
    # model_name = "gpt-3.5-turbo"
    encoding = tiktoken.encoding_for_model(model_name)
    # text = "This is a test for tiktoken."
    tokens = encoding.encode(text)
    print(f"Number of tokens in '{text}': {len(tokens)}")


def demo_streamlit():
    import streamlit as st
    st.write("Hello world. Let's learn how to build a AI-based app together.")


if __name__ == "__main__":
    main()
    # count_tokens("This is a test for tiktoken.", "gpt-3.5-turbo")
    # count_tokens("This is a test for tiktoken.", "gpt-4")
    # count_tokens("これはtiktokenのテストです。", "gpt-3.5-turbo")
    # count_tokens("これはtiktokenのテストです。", "gpt-4")
    demo_streamlit()