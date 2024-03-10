from llm import get_local_llm, get_result_json

shijing_path="E:\\workspace\\chinese-poetry\\诗经\\shijing.json"

import json

# 读取JSON文件
with open(shijing_path, 'r',encoding='utf-8') as f:
    data = json.load(f)

output = []
# 打印内容
for item in data:
    print('标题:', item['title'])
    print('章节:', item['chapter'])
    print('节:', item['section'])
    item_dict = {}
    item_dict['标题'] = item['title']
    item_dict['章节'] = item['chapter']
    item_dict['节'] = item['section']
    item_dict['内容'] = item['content']
    item_dict['content'] = []
    content = item['content']
    for i in range(0, len(content), 2):
        merged_content = content[i] + ' ' + content[i+1] if i+1 < len(content) else content[i]
        try:
            merged_content="\n《诗经》\n"+'标题 '+item['title']+'\n章节 '+item['chapter']+'\n节 '+item['section']+"\n"+merged_content
            print('merged_content:', merged_content)
            result = get_result_json(merged_content)
            item_dict['content'].append(result)
        except Exception as e:
            print(f"An error occurred: {e}")
        print()
    output.append(item_dict)
    print()

with open('shijing-output2.json', 'w',encoding='utf-8') as f:
    json.dump(output, f, indent=4)
    f.close()
