from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 60,
    chunk_overlap = 20,
    separators = ["\n\n", "\n", "。", "、", " ", ""]
)

input_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. \n\n Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
output = text_splitter.split_text(input_text)
print(output)
print(f"Type of output: {type(output)}")
print(f"Number of chunks: {len(output)})")
print([len(chunk) for chunk in output])  # 各チャンクの長さを表示