from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [
        ("user", "{user_input}"),
    ]
)
llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.0, streaming=True)
# ここでstreaming=Trueを指定することで、ストリーミングモードを有効にする(Falseがデフォルト,Falseでも動作はする)
# ただし、ストリーミングモードはバッチ処理には対応していないため、invokeメソッドを使用する必要がある

output_parser = StrOutputParser()
chain = prompt | llm | output_parser

for response in chain.invoke({"user_input": "こんにちは"}):
    # ストリーミングモードでは、invokeメソッドはイテレータを返す
    # そのため、forループでイテレータを回すことで、ストリーミングされた結果を受け取ることができる
    # print(response)
    print(response, end="", flush=True)
    # flush=Trueを指定することで、バッファリングを無効にし、即座に出力されるようにする