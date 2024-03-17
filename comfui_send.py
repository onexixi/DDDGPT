#This is an example that uses the websockets api to know when a prompt execution is done
#Once the prompt execution is done it downloads the images using the /history endpoint
import random

import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import os
from PIL import Image
import io

from push_sd_save import get_win_name

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images

prompt_text = """
{
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "denoise": 1,
            "latent_image": [
                "5",
                0
            ],
            "model": [
                "4",
                0
            ],
            "negative": [
                "7",
                0
            ],
            "positive": [
                "6",
                0
            ],
            "sampler_name": "euler",
            "scheduler": "randomize",
            "seed": 8566257,
            "steps": 30,
            "cfg": 5,
            "sampler_name": "euler",
            "scheduler": "normal",
            "denoise": 1
        }
    },
    "4": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {
            "ckpt_name": "playgroundAisPlayground_playgroundV25Fp16.safetensors"
        }
    },
    "5": {
        "class_type": "EmptyLatentImage",
        "inputs": {
            "batch_size": 6,
            "height": 1024,
            "width": 1024
        }
    },
    "6": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "masterpiece best quality girl"
        }
    },
    "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": [
                "4",
                1
            ],
            "text": "bad hands"
        }
    },
    "8": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": [
                "3",
                0
            ],
            "vae": [
                "4",
                2
            ]
        }
    },
    "9": {
        "class_type": "SaveImage",
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": [
                "8",
                0
            ]
        }
    }
}
"""

#Create an illustration depicting Crystal Sea
def get_send_prompt(text):
    prompt = json.loads(prompt_text)
    # set the text prompt for our positive CLIPTextEncode
    prompt["6"]["inputs"]["text"] = text
    prompt["7"]["inputs"][
        "text"] = "(worst quality, low quality,illustration, 3d, 2d, painting, cartoons, sketch),nsfw,bad quality,bad anatomy,worst quality,low quality,low resolution,extra fingers,blur,blurry,ugly,wrong proportions,watermark,image artifacts,lowres,ugly,jpeg artifacts,deformed,noisy image,deformation,skin moles,"
    rand_num = random.randint(0, 9999999999)
    # set the seed for our KSampler node
    prompt["3"]["inputs"]["seed"] = rand_num
    return prompt


def do_save_result(images, out_path):
    for node_id in images:
        for i, image_data in enumerate(images[node_id]):
            image = Image.open(io.BytesIO(image_data))
            rand_num = random.randint(100000, 999999)
            result_path=out_path+'-'+str(rand_num)+ ".jpg"
            print(result_path)
            image.save(result_path)  # 保存图片到指定路径
            # image.show()




if __name__ == '__main__':
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

    out_path = "H:\\AI\\纳兰2\\"
    # 打开JSON文件并加载数据
    with open('纳兰性德-v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)


    # # 循环遍历每个item
    for index,item in enumerate(data[128:]):
        for index_n,content_item in enumerate(item['prompt_content']):
            print(content_item)
            input_txt = content_item
            name= item['title']+'-'+item['prompt_ch_content'][index_n][0:30]
            name=str(name).strip().replace('\n','-')

            name = name.replace(' ', '')
            "(poetic atmosphere, high detail, serene, 16k, traditional Chinese art, HD,no watermark,) "
            input_txt="(chinese art,no watermark) "+str(input_txt)
            print(input_txt)
            images = get_images(ws, get_send_prompt(input_txt))
            name = get_win_name(name)
            target_folder = out_path + get_win_name(str(name).split('-')[0])
            if not os.path.exists(target_folder):
                os.mkdir(target_folder)
            target_folder =target_folder+"\\"+name
            do_save_result(images, target_folder)
    # Commented out code to display the output images:
    # images = get_images(ws, get_send_prompt( " cinematic shot progression\n women at work, picking, crouching, gathering, bunched wild grass, graceful and strong movements, facial expressions of joy, laughter,田园 ambiance, fluttering butterflies, snowy background, falling snowflakes, harmonious soundscape\n",))
    # name = get_win_name("XXX")
    # name = out_path + name
    # do_save_result(images, name)

