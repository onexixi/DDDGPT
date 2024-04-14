import concurrent.futures
import random
import json
import shutil

import os
import time

import retrying
from gradio_client import Client
import re
import requests

proxypool_url = 'http://8.140.254.36:5555/random'

import socks
import socket

@retrying.retry(wait_fixed=1000, stop_max_attempt_number=3)
def up_global_proxy():
    """
    开启全局代理
    :return:
    """
    proxy = get_random_proxy()
    print(proxy)

    os.environ["http_proxy"] = 'http://' + proxy
    os.environ["https_proxy"] = 'http://' + proxy

    print(f"全局代理设置成功，当前代理为:{proxy}")



negative_prompt = "(worst quality, low quality,illustration, 3d, 2d, painting, cartoons, sketch),nsfw,bad quality,bad anatomy,worst quality,low quality,low resolution,extra fingers,blur,blurry,ugly,wrong proportions,watermark,image artifacts,lowres,ugly,jpeg artifacts,deformed,noisy image,deformation,skin moles,",
save_folder = "H:\\AI\\纳兰-v3\\"
max_retries = 100  # 最大重试次数
retry_interval = 10  # 重试间隔时间（秒）

exec_patch = 3  # 执行次数

def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()
def get_win_name(filename):
    filename = re.sub(r'[\\/:*?"<>|]', '', filename)
    return filename


def get_client_result(client, prompt,name):
    print("--投递任务--")
    result = client.predict(
        prompt,  # str  in 'Prompt' Textbox component
        negative_prompt,  # str  in 'Negative prompt' Textbox component
        True,  # bool  in 'Use negative prompt' Checkbox component
        0,  # float (numeric value between 0 and 2147483647) in 'Seed' Slider component
        1024,  # float (numeric value between 256 and 1536) in 'Width' Slider component
        1024,  # float (numeric value between 256 and 1536) in 'Height' Slider component
        6,  # float (numeric value between 0.1 and 20) in 'Guidance Scale' Slider component
        True,  # bool  in 'Randomize seed' Checkbox component
        api_name="/run"
    )
    result = result[0][0]['image']
    print(result)
    target_folder = save_folder + get_win_name(str(name).split('-')[0])
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    target_folder =os.path.join(target_folder, name+".png")
    shutil.copy(result, target_folder)

def get_pic_url(url, prompt,name):
    result = ""

    client = Client(url)
    # 使用 while 循环来实现重试
    retries = 0
    while retries < max_retries:
        try:
            get_client_result(client, prompt,name)
            break  # 如果没有异常，跳出循环
        except Exception as e:
            retries += 1
            url = random.choice(clients)
            client = Client(url)
            print(f"执行出错，正在进行第 {retries} 次重试...异常{e}...")
            time.sleep(retry_interval)

    else:
        print("重试次数已达上限，程序退出。")
        print("---生成图片异常")


if __name__ == '__main__':
    clients = [
        "https://playgroundai-playground-v2-5.hf.space/--replicas/amkzc/",
        "https://ddosxd-playground-v2.hf.space/--replicas/qhc6d/",
        "https://nymbo-simple-image-model.hf.space/--replicas/hhejm/",
        "https://artples-playground-v2-5-multipleimagegeneration.hf.space/--replicas/gmhwf/",
        "https://doevent-playground-v2-5.hf.space/--replicas/3nc66/",
    ]
    out_path = "H:\\AI\\纳兰2\\"
    # 打开JSON文件并加载数据
    with open('../DATA/纳兰性德-v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)


    # # 循环遍历每个item
    prompt_list = []
    for index,item in enumerate(data[170:200]):
        for index_n,content_item in enumerate(item['prompt_content']):
            prompt={}
            print(content_item)
            input_txt = content_item
            rand_num = random.randint(100000, 999999)
            name= item['title']+'-'+item['prompt_ch_content'][index_n][0:40]+"-"+str(rand_num)
            name=str(name).strip().replace('\n','-')
            name = name.replace(' ', '')
            prompt['name'] = name
            "(poetic atmosphere, high detail, serene, 16k, traditional Chinese art, HD,no watermark,) "
            input_txt="(chinese art,no watermark) "+str(input_txt)
            prompt['input_txt'] = input_txt
            prompt_list.append(prompt)
    prompt_list *= exec_patch
    print(prompt_list)
    #
    # for item in prompt_list:
    #     url = random.choice(clients)
    #     up_global_proxy()
    #     get_pic_url(url, str(item['input_txt']),str(item['name']))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        url = random.choice(clients)
        # submit tasks to executor
        futures = [executor.submit(get_pic_url, url, str(item['input_txt']),str(item['name'])) for item in prompt_list]
        # get results as they become available
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

