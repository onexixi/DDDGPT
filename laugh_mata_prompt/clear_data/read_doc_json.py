import json
import os
import re

from docx import Document
import docx
import win32com.client as wc


def clean_text(text):
    return text

def split_by_tip(lst):
    text="".join(lst)
    pattern = r'\b\d+[、，.,]'
    # 找到第一个匹配的模式
    match = re.search(pattern, text)
    if match:
        # 获取匹配到的字符串
        delimiter = match.group()

        # 获取数字后面的标点符号
        punctuation = delimiter[-1]
        pattern_item = r'\b\d+['+punctuation+']'

        # 使用第一个匹配的模式作为分隔符进行分割
        print(f"第一个匹配的分隔符: {delimiter}")
        print(f"数字后面的标点符号: {punctuation}")
        print(f"分割后的文本:")
        parts = re.split(pattern_item, text)
        filtered_parts = [part for part in parts if part]

        return filtered_parts
    else:
        print("没有找到匹配的模式")
        return split_by_empty_triples(lst)


def split_by_empty_triples(lst):
    # 初始化结果列表
    result = []
    # 初始化一个临时列表来存储当前片段的元素
    temp = []

    # 遍历输入列表
    for item in lst:
        # 如果当前元素不是空字符串，则添加到临时列表
        if item:
            temp.append(item)
        else:
            # 如果当前元素是空字符串，检查是否连续出现三个
            if len(temp) > 0 and len(temp) % 2 == 0:
                # 如果临时列表的长度是3的倍数，将临时列表添加到结果列表
                result.append(temp)
                # 清空临时列表以准备下一个片段
                temp = []
            else:
                # 如果不是三个连续的空字符串，将非空元素添加到临时列表
                temp.append(item)

    # 检查最后一个片段是否需要添加到结果列表
    if temp:
        result.append(temp)

    return result

def do_save_json(file_path, output_file):
    output_file = output_file.replace("【MXH】", '')
    doc = Document(file_path)
    paragraphs_info = []
    current_page_content = []

    # 遍历文档中的每个段落
    paragraphs_txt = []
    split_list=[]
    for i, paragraph in enumerate(doc.paragraphs):
        paragraphs_txt.append(paragraph.text)
        if paragraph.text:
            split_list.append(paragraph.text)
    result1=split_list
    result2 = split_by_tip(current_page_content)
    result3 = split_by_empty_triples(current_page_content)

    # 找出元素数量最多的结果
    max_result = None
    max_length = -1

    for result in (result1, result2, result3):
        if len(result) > max_length:
            max_length = len(result)
            max_result = result

    for item_list in max_result:
        paragraphs_info.append({
            'file_path': file_path,
            'text': clean_text("".join(item_list).strip())  # 使用strip()移除文本两端的空白字符
        })

    # 将列表转换为JSON格式的字符串
    json_data = json.dumps(paragraphs_info, ensure_ascii=False, indent=4)
    # 写入JSON文件
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)


def process_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".docx"):
                # 以相同的文件名（不包括 .docx 扩展名）命名 JSON 文件
                json_filename = os.path.splitext(file)[0] + '.json'
                # JSON 文件与 .docx 文件在相同的目录下
                output_file = os.path.join(root_directory,"清洗", json_filename)
                # 检查输出目录是否存在，如果不存在则创建
                output_dir = os.path.dirname(output_file)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                print(f"Processing {file_path}")
                do_save_json(file_path, output_file)


# 指定要搜索的根目录
# root_directory = 'H:\\XLdown\\34.脱口秀剧本台词文案教程搞笑段子单人口播素材笑话抖音快手短视频\\06-搞笑精品笑话'

root_directory = r'H:\XLdown\34.脱口秀剧本台词文案教程搞笑段子单人口播素材笑话抖音快手短视频\02可以拍短视频的9600条段子\9600个\docx'

if __name__ == '__main__':
    # save_doc_to_docx(root_directory)
    process_folder(root_directory)
