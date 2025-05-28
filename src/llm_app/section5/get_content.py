import streamlit as st
import requests
from bs4 import BeautifulSoup
import traceback

def get_content(url :str) -> str|None:
    try:
        with st.spinner("Fetching Content... / コンテンツを取得中..."):
            response = requests.get(url)

            # レスポンスをresponse.contentとしてbytesのままsoupに渡す
            soup = BeautifulSoup(response.content, 'html.parser')
            # 参考書ではresponse.textを使用していたが、試したら文字化けしていた
            # bytesのまま渡すことでエンコーディングの問題を回避
            # .textは　requests が自動判定する
            # .contentを使用してバイナリデータをBeautifulSoupに渡して、BeautifulSoupが適切なエンコーディングを自動的に判別する
            
            # なるべく本文である可能性が高い要素を抽出
            if soup.main:
                return soup.main.get_text()
            elif soup.article:
                return soup.article.get_text()
            elif soup.body:
                return soup.body.get_text()
            else:
                # それでも本文が見つからない場合は、全体のテキストを返す
                return soup.get_text()
    except:
        st.write(traceback.format_exc()) # エラーが発生した場合はエラー内容を表示
        return None


if __name__ == "__main__":
    st.title("Content Fetcher")
    url = st.text_input("Enter URL:", "https://example.com")
    if st.button("Fetch Content"):
        content = get_content(url)
        print(content)
        if content:
            st.text_area("Fetched Content", content, height=300)
        else:
            st.error("Failed to fetch content. Please check the URL.")