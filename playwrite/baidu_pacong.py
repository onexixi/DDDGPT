from playwright.sync_api import Playwright, sync_playwright, expect
import json
import random

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.cidianwang.com/gushiwen/7/c1187181757.htm")
    with open('../DATA/纳兰性德-v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # # 循环遍历每个item
    for index, item in enumerate(data[145:150]):

        name = item['title']
        name = str(name).strip().replace('\n', '-')
        name = name.replace(' ', '')
        print(name)
        try:
            rand_num = random.randint(0, 9999999999)
            output_path = name + "-" + str(rand_num)
            html_path = get_heml(output_path, page,name)
        except Exception as e:
            page = context.new_page()
            page.goto("https://www.cidianwang.com/gushiwen/7/c1187181757.htm")
            print(f"操作错误了: {e}")



    # ---------------------
    context.close()
    browser.close()


def get_heml(output_path, page,name):
    page.get_by_role("textbox", name="输入汉字").fill(name)
    page.get_by_role("button", name="搜索").click()
    client = page.context.new_cdp_session(page)
    mhtml = client.send("Page.captureSnapshot")['data']
    html_path = "tmp\\" + output_path + '.mhtml'
    with open(html_path, mode='w', encoding='UTF-8', newline='\n') as file:
        file.write(mhtml)
    print("--html--{}", html_path)
    return html_path


with sync_playwright() as playwright:
    run(playwright)
