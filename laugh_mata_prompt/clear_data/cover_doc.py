"""
修改文档格式.doc转为.docx，并保存在子目录docx下
"""
import pythoncom
import os
import win32com.client as wc


# 从最后开始替换某字符串几次
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


# 读取文件夹下的doc文件名列表
def doc_file_name(file_dir):
    fileList = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.doc':
                fileList.append(os.path.join(root, file))
                # 若.doc文档所在目录不存在docx子目录则自动创建
                docx_dir = root + '\\docx'
                if not os.path.exists(docx_dir):
                    os.makedirs(docx_dir)
    return fileList


# doc文件另存为docx
def doc_to_docx(doc_name):
    pythoncom.CoInitialize()
    try:
        word = wc.Dispatch("Word.Application")
        doc = word.Documents.Open(doc_name, Encoding='utf-8')
        # 上面的地方只能使用完整绝对地址，相对地址找不到文件，且，只能用“\\”，不能用“/”，哪怕加了 r 也不行，涉及到将反斜杠看成转义字符。
        doc_name = rreplace(doc_name, "\\", "\\docx\\", 1)
        doc.SaveAs(doc_name.replace(".doc", ".docx"), 12, False, "", True, "", False, False, False, False)
        # 转换后的文件,12代表转换后为docx文件
        doc.Close
    except Exception as e:
        print(e.message)
    finally:
        # 对com操作，一定要确保退出word应用
        if word:
            word.Quit
            del word
        # 释放资源
        pythoncom.CoUninitialize()


def main():
    file_list = doc_file_name("H:\\XLdown\\34.脱口秀剧本台词文案教程搞笑段子单人口播素材笑话抖音快手短视频\\02可以拍短视频的9600条段子\\9600个")
    print(len(file_list))
    for file in file_list:
        doc_to_docx(file)


if __name__ == '__main__':
    main()
