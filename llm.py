import requests
from langchain.output_parsers import BooleanOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers.json import parse_partial_json, parse_json_markdown
from openai import OpenAI

from config import LLM_OPENAI_API_KEY, LLM_OPENAI_API_BASE, LLM_MODEL
from prompt import art_poetry_prompt, art_translate_prompt
import retrying
import re

def send_chat_request(user_content):
    client = OpenAI(base_url=LLM_OPENAI_API_BASE, api_key=LLM_OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model=LLM_MODEL,  # this field is currently unused
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": user_content}
        ],
        temperature=1,
    )
    return completion.choices[0].message.content
# Example: reuse your existing OpenAI setup
@retrying.retry(wait_fixed=1000, stop_max_attempt_number=3)
def get_local_llm(user_input,prompt):
    client = OpenAI(base_url="http://localhost:5000/v1", api_key="not-needed")
    completion = client.chat.completions.create(
        model="Qwen/Qwen1.5-14B-Chat-GGUF/qwen1_5-14b-chat-q4_k_m.gguf",  # this field is currently unused
        messages=[
            {"role": "user", "content": prompt.format(user_input)}
        ],
        temperature=0.7,
    )
    return completion.choices[0].message.content

@retrying.retry(wait_fixed=1000, stop_max_attempt_number=3)
def get_result_json(user_input):
    result_list=[]
    result_ch_list = []
    try:
        result = get_local_llm(user_input,art_poetry_prompt)
        print(result)
        scenes = result.split('\n\n画面')
        match_add_txt=''
        for match in scenes:
            try:
                print(match)
                tr_txt=''
                match_add_txt=match_add_txt+match
                while len(tr_txt)==0 :
                    tr_txt = get_local_llm(match_add_txt, art_translate_prompt)
                    print('++循环++')
                print(tr_txt)
                cleaned_text = re.sub(r'\d+\.', '', tr_txt)
                cleaned_text= cleaned_text.replace('#','')
                print(cleaned_text.strip())
                result_ch_list.append(match)
                result_list.append(cleaned_text)
            except Exception as e:
                print(f"翻译错误了: {e}")
        tr_txt = get_local_llm(str(result), art_translate_prompt)
        result_ch_list.append(result)
        result_list.append(str(tr_txt))
    except Exception as e:
        print(f"解析画面错误了: {e}")

    return result_list,result_ch_list



# Point to the local server




if __name__ == '__main__':
    user_content = """
     "人生若只如初见，何事秋风悲画扇",
      "等闲变却故人心，却道故心人易变",
      "骊山语罢清宵半，泪雨霖铃终不怨",
      "何如薄幸锦衣郎，比翼连枝当日愿"
    """
    try:
        result_list ,result_ch_list   = get_result_json(user_content)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    print(result_list)
    print(result_ch_list)

    # completion = send_chat_request(user_content)
    # print("Response:"+completion)



