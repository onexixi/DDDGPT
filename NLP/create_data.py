import random
import re
import csv

from llm import get_local_llm_result

increment_list = [
    "增幅", "增量", "比上年", "时点", "比上月", "top3", "最多", "最少", "月末", "年末""同比增长",
    "环比增长",
    "复合年增长率",
]

prompt_txt = """
你现在是招商银行分行的运营人员，现在需要测试一款对话软件，请根据提供的指标和维度，询问一些可能会问到的一些问题：
-你负责的机构：{branch}
-你可以询问的一些维度：{dim}
-请使用中文输出
-请只输出10个问题，不要解释
-请切合实际的业务场景
-可以询问最近10年的指标数据

<案例>
单机构单指标查询|请帮我查询北京分行自营贷款|北京分行|自营贷款
单机构多指标查询|帮我查看上海分行自营贷款和个人存款比上年，比上月的值|上海分行|个人存款
多机构单指标查询|天津分行，上海分行，湛江支行的自营存款是多少|天津分行、上海分行、湛江支行|自营存款
多机构多指标查询|天津分行的自营存款，上海分行的自营贷款是多少|天津分行、上海分行|自营存款、自营贷款
</案例>

你可以查询的指标：
{index}


"""



prompt_sign="""
帮我标记用户问题按照如下分类：
-请参照例子进行分类
-只输出分类禁止解释
-可以多询问多机构的信息
例子：
请帮我查询北京分行自营贷款  分类：单机构单指标查询|北京分行|自营贷款
帮我查看上海分行自营贷款和个人存款比上年，比上月的值 分类：单机构多指标查询|上海分行|个人存款
天津分行，上海分行，湛江支行的自营存款是多少 分类：多机构单指标查询|天津分行、上海分行、湛江支行|自营存款
天津分行的自营存款，上海分行的自营贷款是多少 分类：多机构多指标查询|天津分行、上海分行|自营存款、自营贷款

用户问题：
{question}  
"""

# 打开文件并读取内容
with open('./create/branch.txt', 'r', encoding='utf-8') as file:
    # 使用strip()去除每行末尾的换行符，并分割成列表
    content = file.read()
# 使用正则表达式分割字符串，换行符和空格都作为分隔符
bank_branches = re.split(r'\n| ', content)
# 过滤掉可能产生的空字符串（如果分行名称之间有空格）
bank_branches = [branch for branch in bank_branches if branch]

with open('./create/index.txt', 'r', encoding='utf-8') as file:
    # 使用strip()去除每行末尾的换行符，并分割成列表
    index_content = file.read()
# 使用正则表达式分割字符串，换行符和空格都作为分隔符
index_list = re.split(r'\n| ', index_content)
# 过滤掉可能产生的空字符串（如果分行名称之间有空格）
index_list = [index_item for index_item in index_list if index_item]

# 定义一个写入CSV的函数
def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in data:
            csvwriter.writerow(row)
def get_random_list(list):
    # 随机选择1到2个元素
    list = random.sample(list, random.randint(1,10))
    # 打印结果
    print(list)
    return ",".join(list)

#创作指标集
# if __name__ == '__main__':
#     with open('create/result2.txt', 'a', encoding='utf-8') as result_file:
#         for i in range(100):
#             prompt=prompt_txt.format(branch=get_random_list(bank_branches), index=get_random_list(index_list),dim=get_random_list(increment_list))
#             print(prompt)
#             result = get_local_llm_result(prompt)
#             print(result)
#             result_file.write(result + '\n\n')
#     print("结果已保存至 result.json 文件。")


# 打开文件并逐行读取
with open('./create/result2.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 去除每行的前后空白字符（包括换行符）并创建一个新列表
lines = [line.strip() for line in lines if line.strip()]

lines_seen = set()
lines_unique = []
for line in lines:
    if line not in lines_seen:
        lines_seen.add(line)
        lines_unique.append(line)

if __name__ == '__main__':

    data_to_write=[]
    with open('./create/first-result3.txt', 'a', encoding='utf-8') as result_file:
        for index_item in lines_unique:
            prompt=prompt_sign.format(question=index_item)
            print(prompt)
            result = get_local_llm_result(prompt)
            print(result)
            result_file.write(index_item+"|"+result + '\n')
            data_to_write.append([index_item, "|"+result])
    write_to_csv(data_to_write, './create/questions_and_results3.csv')
    print("结果已保存至 result 文件。")

