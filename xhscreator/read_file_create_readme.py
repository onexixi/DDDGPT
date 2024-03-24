import os
import re
import pandas as pd

from llm import send_chat_request
from prompt import red_describe_prompt, red_title_prompt, red_tag_prompt

from tkinter import Tk
from tkinter.filedialog import askdirectory

from PIL import Image
import os
import shutil

def get_parameters_info(image_path):
    try:
        with Image.open(image_path) as img:
            metadata = img.info
            parameters_info = metadata.get("parameters")
            # 如果未找到参数信息，则返回空字符串
            if parameters_info is None:
                return ""
            # 去除 "Steps:" 字符后面的所有内容
            parameters_info = parameters_info.split("Steps:", 1)[0]
            return parameters_info.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None



def get_file_name(folder_path):
    file_names = os.listdir(folder_path)
    file_name_dict = {}
    for file_name in file_names:
        if file_name.__contains__(".png")or file_name.__contains__(".jpg"):
            parameters = get_parameters_info(folder_path + "/" + file_name)
            print(parameters)
            extracted_text = str(parameters).split("Negative")[0]
            file_name_dict[extracted_text] = True
            print(extracted_text)
    return file_name_dict


def get_tag(text):
    user_content = red_tag_prompt.format(text)
    result = send_chat_request(user_content)
    print("生成标签" + result)
    return result


def get_title(text):
    user_content = red_title_prompt.format(text)
    result = send_chat_request(user_content)
    print("生成标题" + result)
    return result


def get_describe(text):
    user_content = red_describe_prompt.format(text)
    result = send_chat_request(user_content)
    print("生成描述" + result)
    return result


def create_txt_file(folder_path, content, csv=None):
    # 检查文件目录是否存在，如果不存在则创建
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name = "output.xlsx"
    file_path = os.path.join(folder_path, file_name)
    # 创建一个DataFrame对象
    df = pd.DataFrame(content)

    # 将DataFrame保存到Excel文件
    df.to_excel(file_path, index=False)
    print("excel文件写入完成。")


def sanitize_filename(filename):
    # 定义不允许作为文件名的特殊字符
    invalid_chars = r'[<>:"/\\|?*]'

    # 使用正则表达式替换不合法的字符为空格
    sanitized_filename = re.sub(invalid_chars, ' ', filename)

    # 去除首尾空格
    sanitized_filename = sanitized_filename.strip()

    return sanitized_filename

if __name__ == '__main__':


    # 源文件夹路径
    source_folder = 'H:\\AI\\sd-webui-aki-v4\\outputs\\txt2img-images'

    # 目标文件夹路径
    target_folder = 'H:\\AI\\小红书发布'
    # file_name_dict = get_file_name(source_folder)
    # list_result = []
    # for name in file_name_dict.keys():
    #     tag = get_tag(name)
    #     title = get_title(name)
    #     desc = ""
    #     data = {
    #         'content': str(name),
    #         'tag': tag,
    #         'title': title,
    #         'desc': desc,
    #         'path': source_folder
    #     }
    #     list_result.append(data)
    # create_txt_file(source_folder, list_result)

    # 遍历源文件夹中的文件
    for filename in os.listdir(source_folder):
        # 拼接完整的文件路径
        file_path = os.path.join(source_folder, filename)

        # 判断是否为文件
        if os.path.isfile(file_path):
            # 截取文件名中间部分
            parts = filename.split('-')
            if len(parts) >= 3:
                extracted_part = parts[2]

                # 创建目标文件夹
                extracted_part=sanitize_filename(extracted_part)
                target_path = os.path.join(target_folder, extracted_part)
                os.makedirs(target_path, exist_ok=True)
                filename=filename.replace(str(parts[2]),".png")
                # 移动文件到目标文件夹
                shutil.move(file_path, os.path.join(target_path, filename))





