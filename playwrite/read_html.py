import re

import requests
import os

import os
import time
directory="H:\\AI\\纳兰-v3"


while True:
    # 获取tmp目录下的所有文件
    with os.scandir('./tmp') as entries:
        # 判断文件夹是否为空
        if not any(entries):
            break
        # 遍历文件列表
        for entry in entries:
            # 判断是否为文件
            if entry.is_file():
                # 打开文件并读取内容
                with open(entry, 'r') as f:
                    content = f.read()
                    print(entry.name)
                    # 进行操作
                    pattern = r'https:\/\/[^\s"]+\.png'

                    urls = re.findall(pattern, content)
                    result=entry.name.split('-')
                    name=entry.name.split('.mh')[0]
                    target_folder=os.path.join(directory,result[0])
                    if not os.path.exists(target_folder):
                         os.mkdir(target_folder)
                    # 发送 GET 请求并下载图片
                    urls = set(urls)
                    print(urls)
                    for url in urls:
                        if 'tmp' in str(url) and 'file=3D'not in str(url):
                            response = requests.get(url,timeout=30)
                            time.sleep(5)
                            if response.status_code == 200:
                                filename = os.path.join(target_folder, name+'.png')
                                with open(filename, 'wb') as f:
                                    f.write(response.content)
                                print('Image saved to', filename)
                                # 删除文件
                os.remove(entry)


    # 等待一段时间后再次扫描文件夹
    time.sleep(10)




