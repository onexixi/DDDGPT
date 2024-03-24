import json
import random
import re
import time

from playwright.sync_api import Playwright, sync_playwright


def get_win_name(filename):
    filename = re.sub(r'[\\/:*?"<>|]', '', filename)
    return filename


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    out_path = "H:\\AI\\纳兰2\\"
    "(poetic atmosphere, high detail, serene, 16k, traditional Chinese art, HD,no watermark,) "
    neg_prompt = "(worst quality, low quality,illustration, 3d, 2d, painting, cartoons, sketch),nsfw,bad quality,bad anatomy,worst quality,low quality,low resolution,extra fingers,blur,blurry,ugly,wrong proportions,watermark,image artifacts,lowres,ugly,jpeg artifacts,deformed,noisy image,deformation,skin moles,"
    # 打开JSON文件并加载数据
    with open('../DATA/纳兰性德-v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # # 循环遍历每个item
    for index, item in enumerate(data[145:150]):
        for index_n, content_item in enumerate(item['prompt_content']):
            print(content_item)
            input_txt = content_item
            name = item['title'] + '-' + item['prompt_ch_content'][index_n][0:30]
            name = str(name).strip().replace('\n', '-')
            name = name.replace(' ', '')
            input_txt = "(chinese art,no watermark) " + str(input_txt)
            print(input_txt)
            try:
                rand_num = random.randint(0, 9999999999)
                output_path = name + "-" + str(rand_num)
                html_path = do_click_save(page, input_txt, neg_prompt, output_path)
            except Exception as e:
                page = context.new_page()
                print(f"操作错误了: {e}")

    # page.frame_locator("#iFrameResizer0").get_by_test_id("container_el").get_by_label("Thumbnail 1 of").click(button="right")
    # page.keyboard.insert_text("V")

    # ---------------------
    context.close()
    browser.close()


def do_click_save(page, prompt, neg_prompt, output_path):
    clients = [
        "https://playgroundai-playground-v2-5.hf.space/--replicas/amkzc/",
        "https://ddosxd-playground-v2.hf.space/--replicas/qhc6d/",
        "https://nymbo-simple-image-model.hf.space/--replicas/hhejm/",
        "https://artples-playground-v2-5-multipleimagegeneration.hf.space/--replicas/gmhwf/",
        "https://doevent-playground-v2-5.hf.space/--replicas/3nc66/",
    ]
    url = random.choice(clients)
    page.goto(url)
    page.get_by_placeholder("Enter your prompt").dblclick()
    page.get_by_placeholder("Enter your prompt").fill(prompt)
    rand_num = random.randint(0, 2)
    time.sleep(rand_num)
    page.get_by_role("button", name="Advanced options ▼").click()
    page.get_by_label("Use negative prompt").check()
    page.get_by_placeholder("Enter a negative prompt").dblclick()
    page.get_by_placeholder("Enter a negative prompt").fill(neg_prompt)
    rand_num = random.randint(0, 2)
    time.sleep(rand_num)
    page.get_by_role("button", name="Run").click()
    page.get_by_label("Thumbnail 1 of").click()
    client = page.context.new_cdp_session(page)
    rand_num = random.randint(0, 10)
    time.sleep(rand_num)
    mhtml = client.send("Page.captureSnapshot")['data']
    html_path = "tmp\\" + output_path + '.mhtml'
    with open(html_path, mode='w', encoding='UTF-8', newline='\n') as file:
        file.write(mhtml)
    print("--html--{}", html_path)
    return html_path


with sync_playwright() as playwright:
    run(playwright)
