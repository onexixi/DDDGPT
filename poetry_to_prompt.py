from llm import get_result_json

shijing_path="E:\\workspace\\chinese-poetry\\宋词\\ci.song.3000.json"
# shijing_path = "E:\\workspace\\DDDGPT\\DATA\\清明.json"
output_path = shijing_path.split('.json')[0] + "v1-ch.json"

import json

# 读取JSON文件
with open(shijing_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

output = []
# 打印内容
for item in data:

    item_dict = {}
    item_dict['title'] = item['rhythmic']
    item_dict['content'] = str(item['paragraphs'])
    item_dict['author'] = item['author']
    print('标题:', item_dict['title'])
    print('作者:', item_dict['author'])
    # print('内容:', item_dict['content'])
    prompt_content = []
    prompt_ch_content = []
    try:
        merged_content = item_dict['title'] + '\n' + item_dict['content']
        print('merged_content:', merged_content)
        result, ch_result = get_result_json(merged_content)

        for contet_txt in result:
            prompt_content.append(contet_txt)
        for ch_txt in ch_result:
            prompt_ch_content.append(ch_txt)
    except Exception as e:
        print(f"处理错了: {e}")
    item_dict['prompt_content'] = prompt_content
    item_dict['prompt_ch_content'] = prompt_ch_content
    output.append(item_dict)
    print()

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=4, ensure_ascii=False)
    f.close()
