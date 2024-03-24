import re
import chardet
import codecs

from llm import send_chat_request
from prompt import CH_TO_EN, EXTRACT_ENTITIES
from text_cover import extract_keywords_chinese


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    result = chardet.detect(rawdata)
    return result['encoding']


def convert_gbk_to_utf8_if_gbk(gbk_file_path, utf8_file_path):
    with codecs.open(gbk_file_path, 'r', encoding='gbk') as gbk_file:
        gbk_text = gbk_file.read()

    with codecs.open(utf8_file_path, 'w', encoding='utf-8') as utf8_file:
        utf8_file.write(gbk_text)
    print("转换完成！")


def split_text_by_chapters(file_path):
    with open(file_path, 'r', encoding='gbk') as file:
        text = file.read()

    chapters = re.split(r'第[一二三四五六七八九十百千万零\d]+章', text)

    # 去除空白章节
    chapters = [chapter.strip() for chapter in chapters if chapter.strip()]

    for i, chapter_content in enumerate(chapters):
        print(f"第{i+1}章：")

        # 初始化一个空字符串来存储合并后的5句话
        combined_sentences = ""
        # 按句号分割章节内容
        sentences = re.split('。', chapter_content)

        for idx, sentence in enumerate(sentences):
            if sentence.strip():  # 确保句子不是空的
                combined_sentences += sentence + "。"  # 将句子和句号组合起来

                # 每5句话合并一次并进行翻译
                if (idx + 1) % 5 == 0:
                    input_txt = EXTRACT_ENTITIES.format(combined_sentences)
                    result = send_chat_request(input_txt)
                    # keywords = extract_keywords_chinese(combined_sentences)
                    # print(keywords)
                    print(result)

                    # 重置合并后的句子
                    combined_sentences = ""

        # 处理剩余的句子
        if combined_sentences.strip():
            input_txt = EXTRACT_ENTITIES.format(combined_sentences)
            result = send_chat_request(input_txt)
            print(result)
            # keywords = extract_keywords_chinese(combined_sentences)
            # print(keywords)



if __name__ == '__main__':
    file_path = '../DATA/《神秘复苏》作者：佛前献花.txt'
    utf8_file_path = str(file_path).replace(".txt", "_utf-8.txt")

    # convert_gbk_to_utf8_if_gbk(file_path, utf8_file_path)
    split_text_by_chapters(file_path)



