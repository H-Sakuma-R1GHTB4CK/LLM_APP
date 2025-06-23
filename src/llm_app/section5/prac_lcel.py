from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

prompt = PromptTemplate.from_template(
    "Say: {content}"
    )

# 大文字に変換する関数
def to_upper_fn(input):
    return {"content": input["content"].upper()}

# ランナブルを作成
to_upper = RunnableLambda(to_upper_fn)

# chainを実行
to_upper_chain = to_upper | prompt
print(to_upper_chain.invoke({"content": "hello world"}))

