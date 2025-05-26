from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages(
    [
        ("user", "{user_input}"),
    ]
)

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.0)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

response = chain.batch([
    {"user_input": "こんにちは"},
    {"user_input": "おはよう"},
    {"user_input": "明日の予定は？"}

])

print(response)
