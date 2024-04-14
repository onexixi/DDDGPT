import json
import requests

url = "https://localhost:7860/agent-scheduler/v1/queue/txt2img"


def get_ask_body(prompt):
    payload = {
        "prompt": prompt,
        "negative_prompt": "(worst quality, low quality,illustration, 3d, 2d, painting, cartoons, sketch),nsfw,bad quality,bad anatomy,worst quality,low quality,low resolution,extra fingers,blur,blurry,ugly,wrong proportions,watermark,image artifacts,lowres,ugly,jpeg artifacts,deformed,noisy image,deformation,skin moles,",
        "seed": -1,
        "sampler_name": "DPM++ 2M Karras",
        "batch_size": 1,
        "steps": 40,
        "cfg_scale": 8.5,
        "width": 1024,
        "height": 1024,
        "checkpoint": "sdvn8Artxl_base.safetensors",
        "vae": "",
        "callback_url": ""
    }
    return payload




headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

if __name__ == '__main__':
    import json

    # 打开JSON文件并加载数据
    with open('../DATA/shijing-output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 循环遍历每个item
    for item in data[0:2]:
        # 访问"content"列表中的每个元素，并打印出其"prompt"属性的值
        for content_item in item['content']:
            print(content_item['prompt'])
            prompt=content_item['prompt']
            response = requests.post(url, json=get_ask_body(item['标题']+str(prompt)), headers=headers, verify=False)



    if response.status_code == 200:
        print("Request successful")
    else:
        print(f"Request failed with status code {response.status_code}")
