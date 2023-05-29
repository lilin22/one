import json,yaml

def json_to_yaml(json_path):
    with open(json_path,encoding="utf-8") as f:
        data = json.load(f)
    yaml_data = yaml.dump(data,indent=5,sort_keys=False,allow_unicode=True)
    return yaml_data

def yaml_to_json(yamlPath):
    with open(yamlPath,encoding='utf-8') as f:
        datas = yaml.load(f,Loader=yaml.FullLoader)
    json_data = json.dumps(datas,indent=5)
    return json_data

if __name__ == '__main__':
    print(json_to_yaml("data.json"))
    # print(yaml_to_json(r"D:\projects\helloCloud\testDatas\user\10001.yaml"))