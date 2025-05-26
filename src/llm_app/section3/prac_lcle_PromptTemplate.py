from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import ConfigurableField

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0.0)

prompt = PromptTemplate.from_template(
    "このお題でジョークを言ってください: {topic}"
).configurable_alternatives(
    ConfigurableField(id="prompt"),
    default_key="joke",
    haiku=PromptTemplate.from_template("このお題の俳句を書いてください: {topic}"),
    )

output_parser = StrOutputParser()


chain = prompt | llm | output_parser

response = chain.invoke({"topic": "冬"})
print(response)

response = chain.with_config(configurable={"prompt": "haiku"})\
    .invoke({"topic": "冬"})
print(response)
