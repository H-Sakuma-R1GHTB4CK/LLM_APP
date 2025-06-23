from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from typing import TypedDict
class ContentInput(TypedDict):
    content: str

split: RunnableLambda[ContentInput, list[str]] = RunnableLambda(lambda x: [word for word in x["content"].split(' ')])  # 空白で分割し、空文字を除外
to_upper: RunnableLambda[str, str] = RunnableLambda(lambda x: x.upper())
join: RunnableLambda[list[str], str] = RunnableLambda(lambda x: ' '.join(x))

to_upper_chain = split | to_upper.map() | join
# splitで入力が分割され、それぞれにto_upperを適用するために.map()を使用

print(to_upper_chain.invoke({"content": "hi, hello world"}))  # 出力: "HELLO WORLD"