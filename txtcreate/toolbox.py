import os

import retrying
from langchain_text_splitters import CharacterTextSplitter
from openai import OpenAI

from txtcreate.prompt import JOKE_EXTRACTION, JOKE_RULE_EXTRACTION, JOKE_RULE_EXTRACTION_COMBINE


@retrying.retry(wait_fixed=10000, stop_max_attempt_number=3)
def get_local_llm(prompt):
    client = OpenAI(base_url="http://localhost:5000/v1", api_key="not-needed")
    completion = client.chat.completions.create(
        model="Meta/Llama3-8B-Chinese-Chat-GGUF",  # this field is currently unused
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1,
    )
    return completion.choices[0].message.content


text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=4096,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)


def do_cove(input_file, output_file):
    with open(input_file, "r", encoding='utf-8') as f:
        state_of_the_union = f.read()

    texts = text_splitter.create_documents([state_of_the_union])
    result_list = []
    for item in texts:
        item_txt = JOKE_RULE_EXTRACTION_COMBINE.format(text=item)
        result = get_local_llm(item_txt)
        print(result)
        result_list.append(result)
    with open(output_file, "a", encoding='utf-8') as f:
        f.write("\n\n\n\n")
        f.write("\n".join(result_list))

def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith("_rule_result.txt"):
                file_path = os.path.join(root, file)
                output_file = f"{os.path.splitext(file_path)[0]}_plan_rule_result.txt"
                print(f"Processing {file_path}")
                do_cove(file_path, output_file)


if __name__ == "__main__":
    folder_path = "D:\\Desktop\\笑话素材组"
    process_folder(folder_path)
