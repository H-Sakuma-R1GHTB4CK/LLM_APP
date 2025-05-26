from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import ConfigurableField

model = ChatOpenAI(temperature=0.0).configurable_fields(
    model_name = ConfigurableField(
        id = "model_name",
        name = "Model Name",
        description = "The name of the model to use.",
    )
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("user", "{user_input}"),
    ]
)

output_parser = StrOutputParser()

# prompt | model | output_parser をまず作成
base_chain = prompt | model | output_parser

# .with_config をチェーンに適用
configured_chain = base_chain.with_config(configurable={"model_name": "gpt-4.1-nano"})

# invoke のときにモデル名を指定済み
response = configured_chain.invoke({"user_input": "こんにちは"})
print(response)