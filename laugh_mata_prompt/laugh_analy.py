import re

import retrying
from openai import OpenAI

from laugh_mata_prompt.laugh_rule_prompt import prompt_list
from txtcreate.prompt import CLASSICAL_LAUGH, CLASSICAL_LAUGH_CHECK, CLASSICAL_LAUGH_MODIFY
import replicate
import random

import os
import json

os.environ['REPLICATE_API_TOKEN'] = 'r8_Ut3QqQTmYH43ZDpr6CTBZZVk5zDXNFW23dDo9'


# @retrying.retry(wait_fixed=10000, stop_max_attempt_number=3)
def get_local_llm(prompt):
    client = OpenAI(base_url="http://localhost:5000/v1", api_key="not-needed")
    completion = client.chat.completions.create(
        model="Meta",  # this field is currently unused
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
    )
    return completion.choices[0].message.content


def is_number_start(s):
    if re.match(r'^\d+', s['text']):
        return True
    else:
        return False


# 假设 CLASSICAL_LAUGH, CLASSICAL_LAUGH_CHECK, CLASSICAL_LAUGH_MODIFY 和 get_local_llm 是已经定义好的函数和变量

def do_add_prompt(prom_txt):
    txt = """
你是一个专业的幽默笑话大师，请参考下面的内容，给用户的笑话幽默文本分析该笑话的思路：
-请简洁分析该文本，笑点分析，逻辑分析。
-禁止给出修改后的内容
-一句话给出可以增强的方向

"""
    prom_txt = txt + prom_txt + "\n\n待修改和处理的笑话文本：{text}"
    return prom_txt


def process_and_save_data(data, folder_name, save_folder, part_save_frequency):
    results_list = []
    part_results_list = []
    for item in data:
        selected_prompts = random.sample(prompt_list, 3)
        for prom_txt in selected_prompts:
            if item:
                format_text = do_add_prompt(prom_txt)
                if item.get('text', ''):
                    item_txt = format_text.format(text=item.get('text', ''))
                    print(item_txt)
                    result = get_local_llm(item_txt)
                    print(result)
                    item_json = {
                        "name": item['file_path'],
                        "laugh": item['text'],
                        "check": result,
                    }
                    part_results_list.append(item_json)
                    results_list.append(item_json)

                    if len(part_results_list) % part_save_frequency == 0:
                        part_filename = f'{folder_name}_{len(results_list) // part_save_frequency + 1}.json'
                        with open(part_filename, 'w', encoding='utf-8') as json_file:
                            json.dump(part_results_list, json_file, ensure_ascii=False, indent=4)
                        part_results_list = []


    with open(save_folder, 'w', encoding='utf-8') as json_file:
        json.dump(results_list, json_file, ensure_ascii=False, indent=4)


def do_create_first(out_path,file_path,file_name):
    with open(
            file_name,
            'r', encoding='utf-8') as json_file:
        class_data = json.load(json_file)
    json_filename = os.path.splitext(file)[0] + '_out.json'
    output_file = os.path.join(out_path, json_filename + '.json')
    process_and_save_data(class_data, file_name, output_file, 20)
def doc_file_name(file_dir):
    fileList = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                fileList.append(os.path.join(root, file))
                # 若.doc文档所在目录不存在docx子目录则自动创建
                docx_dir = root + '\\处理后'
                if not os.path.exists(docx_dir):
                    os.makedirs(docx_dir)
    return fileList

if __name__ == '__main__':
    file_path="H:\\XLdown\\34.脱口秀剧本台词文案教程搞笑段子单人口播素材笑话抖音快手短视频\\json"
    file_list = doc_file_name(file_path)
    print(len(file_list))
    for file in file_list:
        do_create_first(file_path+"\\处理后",file_path,file)

