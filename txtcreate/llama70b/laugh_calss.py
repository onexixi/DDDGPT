import retrying
from openai import OpenAI

from txtcreate.prompt import CLASSICAL_LAUGH, CLASSICAL_LAUGH_CHECK, CLASSICAL_LAUGH_MODIFY
import replicate

import os
import json

os.environ['REPLICATE_API_TOKEN'] = 'r8_Ut3QqQTmYH43ZDpr6CTBZZVk5zDXNFW23dDo9'

@retrying.retry(wait_fixed=10000, stop_max_attempt_number=3)
def get_local_llm(prompt):
    client = OpenAI(base_url="http://localhost:5000/v1", api_key="not-needed")
    completion = client.chat.completions.create(
        model="Meta",  # this field is currently unused
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1,
    )
    return completion.choices[0].message.content




# 假设 CLASSICAL_LAUGH, CLASSICAL_LAUGH_CHECK, CLASSICAL_LAUGH_MODIFY 和 get_local_llm 是已经定义好的函数和变量

def process_and_save_data(data, folder_name, save_folder_suffix, part_save_frequency, final_filename_suffix,
                          format_text):
    results_list = []
    part_results_list = []
    save_folder = f"{folder_name}/{save_folder_suffix}"
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
        print(f"文件夹'{save_folder}'已创建。")
    else:
        print(f"文件夹已存在。")

    for item in data:
        item_txt = format_text.format(name=item['name'], detail=item.get('detail', ''),laugh=item.get('laugh', ''),check=item.get('check', ''))
        result = get_local_llm(item_txt)
        print(result)
        item_json = {
            "name": item['name'],
            "detail": item['detail'],
            "laugh": result if '初版'==save_folder_suffix else item.get('laugh', ''),
            "check": result if '修改意见'==save_folder_suffix else item.get('check', ''),
            'modify': result if '修改后'==save_folder_suffix else ""
        }
        part_results_list.append(item_json)
        results_list.append(item_json)

        if len(part_results_list) % part_save_frequency == 0:
            part_filename = f'{save_folder}/{folder_name}_{final_filename_suffix}_{len(results_list) // part_save_frequency + 1}.json'
            with open(part_filename, 'w', encoding='utf-8') as json_file:
                json.dump(part_results_list, json_file, ensure_ascii=False, indent=4)
            part_results_list = []

    final_filename = f'{save_folder}/{final_filename_suffix}.json'
    with open(final_filename, 'w', encoding='utf-8') as json_file:
        json.dump(results_list, json_file, ensure_ascii=False, indent=4)


def do_create_first(folder_name):
    with open('../中华成语典故大全_清洗.json', 'r', encoding='utf-8') as json_file:
        class_data = json.load(json_file)
    process_and_save_data(class_data, folder_name, "初版", 50, "中华成语典故大全_古典_笑话_初版", CLASSICAL_LAUGH)


def do_create_step_second(folder_name):
    with open('./中华成语典故大全/初版/中华成语典故大全_古典_笑话_初版.json', 'r', encoding='utf-8') as json_file:
        fiest_data = json.load(json_file)
    process_and_save_data(fiest_data, folder_name, "修改意见", 50, "中华成语典故大全_古典_笑话_修改意见",
                          CLASSICAL_LAUGH_CHECK)


def do_create_step_third(folder_name):
    with open('./中华成语典故大全/修改意见/中华成语典故大全_古典_笑话_修改意见.json', 'r', encoding='utf-8') as json_file:
        fiest_data = json.load(json_file)
    process_and_save_data(fiest_data, folder_name, "修改后", 50, "中华成语典故大全_古典_笑话_修改后",
                          CLASSICAL_LAUGH_MODIFY)


if __name__ == '__main__':
    folder_name = "中华成语典故大全"

    # do_create_first(folder_name)
    # do_create_step_second(folder_name)
    do_create_step_third(folder_name)
