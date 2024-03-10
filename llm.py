import requests
from langchain.output_parsers import BooleanOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers.json import parse_partial_json, parse_json_markdown
from openai import OpenAI

from config import LLM_OPENAI_API_KEY, LLM_OPENAI_API_BASE, LLM_MODEL
from prompt import ancient_poetry_prompt
import retrying


def send_chat_request(user_content):
    client = OpenAI(base_url=LLM_OPENAI_API_BASE, api_key=LLM_OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model=LLM_MODEL,  # this field is currently unused
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_content}
        ],
        temperature=1,
    )
    return completion.choices[0].message.content
# Example: reuse your existing OpenAI setup
@retrying.retry(wait_fixed=1000, stop_max_attempt_number=3)
def get_local_llm(user_input):
    global completion
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=[
            {"role": "user", "content": ancient_poetry_prompt.format(user_input)}
        ],
        temperature=0.7,
    )
    return completion.choices[0].message.content

@retrying.retry(wait_fixed=1000, stop_max_attempt_number=3)
def get_result_json(user_input):
    result_json={}
    # result=get_local_llm(user_input)
    # result_json= parse_json_markdown(json_string=result)
    # print(result_json['title'])
    # print(result_json['description'])
    # print(result_json['prompt'])
    result_json['merged_content']=user_input

    return result_json



# Point to the local server




if __name__ == '__main__':
    user_content = "Introduce yourself."
    try:
        result = get_result_json("孤鸿海上来")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    print(result)

    # completion = send_chat_request(user_content)
    # print("Response:"+completion)



