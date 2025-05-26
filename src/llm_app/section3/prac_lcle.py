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
print(chain) # debug
print(type(chain)) # debug

response = chain.invoke({"user_input": "こんにちは"})
print(response)
print(type(response)) # debug