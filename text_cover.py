import jieba.posseg as pseg

def extract_keywords_chinese(text):
    words = pseg.cut(text)  # 对中文文本进行分词和词性标注

    keywords = []
    for word, flag in words:
        if flag.startswith('n') or flag.startswith('a'):  # 选择名词（n）和形容词（a）
            keywords.append(word)

    return keywords

# 测试
text = "这是一个简单的例句，用来演示如何提取关键词。"
keywords = extract_keywords_chinese(text)
print(keywords)
