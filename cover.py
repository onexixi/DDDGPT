import json


def read_json_file(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as fp:
            result = json.load(fp)
    except Exception as e:
        raise e
    else:
        return result


def dump_json_file(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        raise e
    else:
        return True

if __name__ == '__main__':
    data=read_json_file('shijing-prompt-v2.json')
    dump_json_file('shijing-prompt-v2-ch.json',data)
