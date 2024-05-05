import json
import os

import retrying
from openai import OpenAI

from txtcreate.prompt import CLASSICAL_LAUGH, CLASSICAL_LAUGH_CHECK, CLASSICAL_LAUGH_MODIFY


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


def do_create_first(folder_name):
    with open('中华成语典故大全_清洗.json', 'r', encoding='utf-8') as json_file:
        class_data = json.load(json_file)
    # 假设 CLASSICAL_LAUGH 和 get_local_llm 是已经定义好的函数和变量
    # results_list 用于存储最终的全量结果
    results_list = []

    # part_results_list 用于存储每10个结果的部分结果，以便单独保存
    part_results_list = []

    # 检查文件夹是否已存在
    save_folder = folder_name + "/初版"
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
        print(f"文件夹'{save_folder}'已创建。")
    else:
        print(f"文件夹已存在。")

    # 循环遍历activities_list 3次，这里假设 class_data 是一个列表
    for item in class_data:  # 修改为3次循环以符合题目描述
        item_txt = CLASSICAL_LAUGH.format(name=item['name'], detail=item['detail'])
        result = get_local_llm(item_txt)
        print(result)
        item_json = {
            "name": item['name'],
            "detail": item['detail'],
            "laugh": result
        }
        # 将结果添加到部分结果列表中
        part_results_list.append(item_json)
        results_list.append(item_json)

        # 每处理10个项目，保存一次部分结果
        if len(part_results_list) % 10 == 0:
            # 将部分结果列表保存为JSON文件
            part_filename = f'{save_folder}/{folder_name}_part{len(results_list) // 10 + 1}.json'
            with open(part_filename, 'w', encoding='utf-8') as json_file:
                json.dump(part_results_list, json_file, ensure_ascii=False, indent=4)
            # 清空部分结果列表，为下一次保存做准备
            part_results_list = []

    # 最终保存全量结果
    final_filename = f'{save_folder}/中华成语典故大全_古典_笑话_初版.json'
    with open(final_filename, 'w', encoding='utf-8') as json_file:
        json.dump(results_list, json_file, ensure_ascii=False, indent=4)


def do_create_step_second(folder_name):
    with open('中华成语典故大全\中华成语典故大全_古典_笑话_初版.json', 'r', encoding='utf-8') as json_file:
        fiest_data = json.load(json_file)
    results_list = []

    # part_results_list 用于存储每10个结果的部分结果，以便单独保存
    part_results_list = []
    save_folder = folder_name + "/修改意见"
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
        print(f"文件夹'{save_folder}'已创建。")
    else:
        print(f"文件夹已存在。")

    for item in fiest_data:  # 修改为3次循环以符合题目描述
        item_txt = CLASSICAL_LAUGH_CHECK.format(name=item['name'], laugh=item['laugh'])
        result = get_local_llm(item_txt)
        print(result)
        item_json = {
            "name": item['name'],
            "detail": item['detail'],
            "laugh": item['laugh'],
            "check": result
        }
        # 将结果添加到部分结果列表中
        part_results_list.append(item_json)
        results_list.append(item_json)

        # 每处理10个项目，保存一次部分结果
        if len(part_results_list) % 50 == 0:
            # 将部分结果列表保存为JSON文件
            part_filename = f'{save_folder}/{folder_name}_修改意见_part{len(results_list) // 50 + 1}.json'
            with open(part_filename, 'w', encoding='utf-8') as json_file:
                json.dump(part_results_list, json_file, ensure_ascii=False, indent=4)
            # 清空部分结果列表，为下一次保存做准备
            part_results_list = []

    # 最终保存全量结果
    final_filename = f'{save_folder}/中华成语典故大全_古典_笑话_修改意见.json'
    with open(final_filename, 'w', encoding='utf-8') as json_file:
        json.dump(results_list, json_file, ensure_ascii=False, indent=4)


def do_create_step_third(folder_name):
    with open('中华成语典故大全/修改意见/中华成语典故大全_古典_笑话_修改意见.json', 'r', encoding='utf-8') as json_file:
        fiest_data = json.load(json_file)
    results_list = []

    # part_results_list 用于存储每10个结果的部分结果，以便单独保存
    part_results_list = []
    save_folder = folder_name + "/修改后"
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
        print(f"文件夹'{save_folder}'已创建。")
    else:
        print(f"文件夹已存在。")

    # 循环遍历activities_list 3次，这里假设 class_data 是一个列表
    for item in fiest_data:  # 修改为3次循环以符合题目描述
        item_txt = CLASSICAL_LAUGH_MODIFY.format(name=item['name'], check=item['check'], laugh=item['laugh'])
        result = get_local_llm(item_txt)
        print(result)
        item_json = {
            "name": item['name'],
            "detail": item['detail'],
            "laugh": item['laugh'],
            "check": item['check'],
            "modify": result
        }
        # 将结果添加到部分结果列表中
        part_results_list.append(item_json)
        results_list.append(item_json)

        # 每处理10个项目，保存一次部分结果
        if len(part_results_list) % 50 == 0:
            # 将部分结果列表保存为JSON文件
            part_filename = f'{save_folder}/{folder_name}_修改后_part{len(results_list) // 50 + 1}.json'
            with open(part_filename, 'w', encoding='utf-8') as json_file:
                json.dump(part_results_list, json_file, ensure_ascii=False, indent=4)
            # 清空部分结果列表，为下一次保存做准备
            part_results_list = []

    # 最终保存全量结果
    final_filename = f'{save_folder}/中华成语典故大全_古典_笑话_修改后.json'
    with open(final_filename, 'w', encoding='utf-8') as json_file:
        json.dump(results_list, json_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    folder_name = "中华成语典故大全"

    # do_create_first(folder_name)
    # do_create_step_second(folder_name)
    do_create_step_third(folder_name)
