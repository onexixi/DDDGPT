import random

from openai import OpenAI

from txtcreate.prompt import laught_add
import retrying
import json

@retrying.retry(wait_fixed=10000, stop_max_attempt_number=3)
def get_local_llm(user_input,prompt):
    client = OpenAI(base_url="http://localhost:5000/v1", api_key="not-needed")
    completion = client.chat.completions.create(
        model="Qwen/Qwen1.5-14B-Chat-GGUF/qwen1_5-14b-chat-q4_k_m.gguf",  # this field is currently unused
        messages=[
            {"role": "user", "content": prompt.format(user_input)}
        ],
        temperature=1,
    )
    return completion.choices[0].message.content


activities_list = [
    "喝点啤啤",
    "来根小烟儿",
    "打场球球",
    "撸个串串",
    "开一把开一把",
    "刷刷微博",
    "装个机",
    "唱个KK",
    "钓个鱼鱼",
    "洗个脚脚"
]


if __name__ == '__main__':


    # 用于存储结果的列表
    results_list = []

    # 循环遍历activities_list 3次
    for i in range(2):
        for activity in activities_list:
            result = get_local_llm(activity, laught_add)
            print(result)
            results_list.append(result)

    # 将结果列表保存为JSON文件
    with open('results6.json', 'w', encoding='utf-8') as json_file:
        json.dump(results_list, json_file, ensure_ascii=False, indent=4)