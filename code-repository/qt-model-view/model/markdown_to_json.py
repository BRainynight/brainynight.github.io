import yaml
import json
import os
from datetime import datetime
from pprint import pprint
from multiList import MultiList

PATH = "../../../content/zh-tw/notes"

def convert_md_to_json(md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        lines = md_file.readlines()

    # Extract YAML metadata
    yaml_content = ""
    content = []
    in_yaml = False
    times = 0
    for line in lines:
        if line.strip() == "---" and times <2:
            times += 1
            in_yaml = not in_yaml
            continue
        if in_yaml:
            yaml_content += line
        else:
            content.append(line)

    # Parse YAML metadata
    metadata = yaml.safe_load(yaml_content)
    title = md_file_path.split("/")[-1].replace(".md", "")
    metadata['title'] = title

    # Convert to JSON
    json_data = {
        "metadata": metadata,
        "content": "".join(content).strip()
    }
    

    return json_data



json_file_path = 'example.json'

files = os.listdir(PATH)
js_lt = [ ]
for file in files:
    if not file.endswith(".md"):
        continue
    fp = os.path.join(PATH, file)
    print(fp)
    js = convert_md_to_json(fp)
    js_lt.append(js)


def default_converter(o):
    '''
    Convert datetime object to string.
    '''
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(js_lt, json_file, indent=4, ensure_ascii=False, default=default_converter)
    