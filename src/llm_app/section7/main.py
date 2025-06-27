import streamlit as st

def init_page():
    st.set_page_config(
        page_title="Ask My PDF(s)",
        page_icon="📄"
    )
    # st.header("Ask My PDF(s) 📄")

def main():
    init_page()

    st.sidebar.success("↑のメニューから進んでね")

    st.markdown(
        """
        ### Ask My PDF(s) にようこそ！📄
        - このアプリでは、アップロードしたPDFに対して質問をすることができます
        - まずは左のメニューから`Upload PDF(s)`を選択してPDFをアップロードしてください
        - PDFをアップロードしたら、`PDF QA`を選択して、質問を入力してみてください
        """
    )

if __name__ == "__main__":
    main()