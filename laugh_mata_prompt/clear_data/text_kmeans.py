import itertools
import json
import os

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# 指定包含JSON文件的文件夹路径


# 读取文件夹中的所有JSON文件
def read_json_files(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):  # 确保它是JSON文件
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data_list = json.load(f)  # 假设这里data是一个JSON对象的列表
                for data in data_list:  # 遍历列表中的每个元素
                    if 'file_path' in data and 'text' in data:
                        documents.append((data['text'], data['file_path']))
    return documents


# 聚类文本
def load_chinese_stopwords(stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
    return stopwords


def cluster_texts(documents, num_clusters=3, stopwords_file='cn_stopwords.txt'):
    texts = [doc[0] for doc in documents]  # 从元组中提取文本
    # 加载中文停用词
    chinese_stopwords = load_chinese_stopwords(stopwords_file)

    # 使用TF-IDF向量化文本，并使用中文停用词过滤
    tfidf_vectorizer = TfidfVectorizer(stop_words=chinese_stopwords, encoding='utf-8')
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

    # 应用K-means聚类
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)

    # 返回每个文本的聚类标签和文本本身及其文件路径
    labels = kmeans.labels_
    clustered_documents = list(zip(labels, documents))

    return clustered_documents


# 主函数
def main():
    documents = read_json_files(folder_path)
    clustered_documents = cluster_texts(documents)
    TF = []  # 所有文章的词频

    # 找出重复度高的文本，这里我们简单地查找标签相同的文本
    unique_texts = []
    for label, group in itertools.groupby(clustered_documents, key=lambda x: x[0]):
        texts_in_cluster = list(text for text in group)
        if len(texts_in_cluster) > 1:  # 如果一个聚类中有多个文本
            unique_text = list(set(text[1][0] for text in texts_in_cluster))  # deduplicate texts
            for text in unique_text:
                unique_texts.append({
                    "instruction": texts_in_cluster[0][1][1],  # Use the file path from the first document in the cluster
                    "input": "",
                    "output": text
                })

    with open('output_9600条段子.json', 'w', encoding='utf-8') as f:
        json.dump(unique_texts, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    folder_path = 'H:\\XLdown\\34.脱口秀剧本台词文案教程搞笑段子单人口播素材笑话抖音快手短视频\\02可以拍短视频的9600条段子\\9600个\\docx\\清洗'

    main()