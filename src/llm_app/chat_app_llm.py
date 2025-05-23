import openai
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# resp = openai.models.list()
# print([m.id for m in resp.data])
      
user_input = "こんにちは！chatGPT！"

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.9)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "あなたは優秀なAIアシスタントです。絶対に関西弁で返答してください。"),
        ("user", "{input}"),
    ]
)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser
response = chain.invoke({"input": user_input})

print(response)