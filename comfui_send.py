# This is an example that uses the websockets api to know when a prompt execution is done
# Once the prompt execution is done it downloads the images using the /history endpoint
import io
import json
import os
import random
import urllib.parse
import urllib.request
import uuid

import websocket  # NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
from PIL import Image

from poetry.push_sd_save import get_win_name

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())


def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
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
                    break  # Execution is done
        else:
            continue  # previews are binary data

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


# Create an illustration depicting Crystal Sea
def get_send_prompt(text, mark_path):
    # 读取 JSON 文件
    with open('./playground-v2.5/workflow-playground-v25.json', 'r',encoding='utf-8') as file:
        data = file.read()

    prompt_native = "(worst quality, low quality,illustration, 3d, 2d, painting, cartoons, sketch),nsfw,bad quality,bad anatomy,worst quality,low quality,low resolution,extra fingers,blur,blurry,ugly,wrong proportions,watermark,image artifacts,lowres,ugly,jpeg artifacts,deformed,noisy image,deformation,skin moles,"
    # 处理引号和转义字符
    prompt_tx = text.replace("'", "")
    prompt_tx = prompt_tx.replace('"', '')
    prompt_tx = prompt_tx.replace('\n', '')

    # 替换占位符
    data = data.replace("MARK-PROMPT", prompt_tx)
    data = data.replace("MARK-NATIVE-PROMPT", prompt_native)
    data = data.replace("MARK-PATH", ''+mark_path+"/ComfyUI")

    # 重新读取替换后的文本为 JSON
    prompt = json.loads(data)
    return prompt


def do_save_result(images, out_path):
    for node_id in images:
        for i, image_data in enumerate(images[node_id]):
            image = Image.open(io.BytesIO(image_data))
            rand_num = random.randint(100000, 999999)
            result_path = out_path + '-' + str(rand_num) + ".jpg"
            print(result_path)
            image.save(result_path)  # 保存图片到指定路径
            # image.show()


if __name__ == '__main__':
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

    out_path = "H:\\AI\\合集\\清明\\"
    # 打开JSON文件并加载数据
    with open('./DATA/清明v1-ch.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # # 循环遍历每个item
    for index, item in enumerate(data):
        for index_n, content_item in enumerate(item['prompt_content']):
            print(content_item)
            input_txt = content_item
            name = item['title'] + '-' + item['prompt_ch_content'][index_n][0:30]
            name = str(name).strip().replace('\n', '-')

            name = name.replace(' ', '')
            "(poetic atmosphere, high detail, serene, 16k, traditional Chinese art, HD,no watermark,) "
            input_txt = "(chinese art,no watermark) " + str(input_txt)
            print(input_txt)
            cf_out_path = get_win_name(str(name).split('-')[0])
            target_folder = out_path + cf_out_path
            images = get_images(ws, get_send_prompt(input_txt, cf_out_path))
            name = get_win_name(name)
            if not os.path.exists(target_folder):
                os.mkdir(target_folder)
            target_folder = target_folder + "\\" + name
            do_save_result(images, target_folder)
