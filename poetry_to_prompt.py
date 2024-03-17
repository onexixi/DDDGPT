from llm import get_local_llm, get_result_json

shijing_path="E:\\workspace\\chinese-poetry\\纳兰性德\\纳兰性德诗集.json"

import json

# 读取JSON文件
with open(shijing_path, 'r',encoding='utf-8') as f:
    data = json.load(f)

output = []
# 打印内容
for item in data:
    print('标题:', item['title'])
    print('作者:', item['author'])
    print('内容:', item['para'])
    item_dict = {}
    item_dict['title'] = item['title']
    item_dict['content'] = item['para']
    prompt_content = []
    prompt_ch_content = []
    try:
        merged_content = item['title'] +'\n'+  '\n'.join(item_dict['content'])
        print('merged_content:', merged_content)
        result,ch_result =  get_result_json(merged_content)
        if len(result) == 0:
            result,ch_result = get_result_json(merged_content)
        for contet_txt in result:
            prompt_content.append(contet_txt)
        for ch_txt in ch_result:
            prompt_ch_content.append(ch_txt)
    except Exception as e:
        print(f"处理错了: {e}")
    item_dict['prompt_content']=prompt_content
    item_dict['prompt_ch_content']=prompt_ch_content
    output.append(item_dict)
    print()

with open('纳兰性德-v2.json', 'w',encoding='utf-8') as f:
    json.dump(output, f, indent=4, ensure_ascii=False)
    f.close()
