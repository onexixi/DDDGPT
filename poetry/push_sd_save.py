import random

import requests

url = 'https://localhost:7860/sdapi/v1/txt2img'

import base64
import json
import re


def get_win_name(filename):
    filename = re.sub(r'[\\/:*?"<>|]', '', filename)
    return filename


def get_ask_body(prompt):
    payload = {
        "prompt": prompt,
        "negative_prompt": "(worst quality, low quality,illustration, 3d, 2d, painting, cartoons, sketch),nsfw,bad quality,bad anatomy,worst quality,low quality,low resolution,extra fingers,blur,blurry,ugly,wrong proportions,watermark,image artifacts,lowres,ugly,jpeg artifacts,deformed,noisy image,deformation,skin moles,",
        "seed": -1,
        "sampler_name": "DPM++ 2M Karras",
        "batch_size": 2,
        "steps": 35,
        "cfg_scale": 7.5,
        "width": 1024,
        "height": 1024,
        "checkpoint": "sdvn8Artxl_base.safetensors",
        "callback_url": ""
    }
    return payload


headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}


def do_save_result(response, name):
    if response.status_code == 200:
        images_data = response.json()['images']
        for i, image_data in enumerate(images_data):
            image_data = base64.b64decode(image_data)
            with open(f"{name}-{i}.png", 'wb') as f:
                f.write(image_data)
            print(f"Image {name} saved successfully")
    else:
        print(f"Request failed with status code {response.status_code}")

#Image H:\AI\诗经\《诗经》-标题清人-章节国风-节郑风-清人在彭，驷介旁旁。二矛重英，河上乎翱翔。清人在消，驷介麃麃。二矛重乔，河上乎逍遥。-662117 saved successfully

if __name__ == '__main__':

    out_path = "H:\\AI\\诗经\\"
    # 打开JSON文件并加载数据
    with open('../DATA/shijing-output.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('../DATA/shijing-output2.json', 'r', encoding='utf-8') as f:
        data2 = json.load(f)

    # 循环遍历每个item
    for index,item in enumerate(data):
        # 访问"content"列表中的每个元素，并打印出其"prompt"属性的值
        meg_item=data2[index]
        for index_n,content_item in enumerate(item['content']):
            print(content_item['prompt'])
            prompt = content_item['prompt']
            rand_num = random.randint(100000, 999999)
            name=meg_item['content'][index_n]['merged_content']+"-"+str(rand_num)
            name=str(name).strip().replace('\n','-')
            name = name.replace(' ', '')
            response = requests.post(url, json=get_ask_body(str(prompt)), headers=headers, verify=False)
            name = get_win_name(name)
            name=out_path+name
            do_save_result(response, name)
