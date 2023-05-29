import json,jsonpath

def json_extract(json_path,expression):
    with open(json_path,encoding="utf-8") as f:
        data = json.load(f)
    return jsonpath.jsonpath(data,expression)

if __name__ == '__main__':
    print(json_extract("data.json","$.data.manage_orgs.*.name"))