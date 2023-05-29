import os,sys,json,jsonpath

import allure

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]
sys.path.append(rootPath)
from configure.setting import one_uri,adminUser
from common.request import request
from common.processYaml import processYaml
from string import Template
from configure import filepath
from common.configLog import logger

class admin:
    '''管理员'''

    def __init__(self,one_uri=one_uri,username=adminUser.get("username"),password=adminUser.get("password")):
        self.one_uri = one_uri
        self.username = username
        self.password = password

    def login(self):
        ym = processYaml(filepath.ADMINLOGIN_PATH_YAML)
        ymdata = ym.read_yaml()
        for sp in ymdata["info"]:
            logger.info(f"执行前置：{sp['step']}")
            url = self.one_uri + sp['data']['request']['api']
            headers = sp['data']['request']['headers']
            data = sp['data']['request']['data']
            data = json.loads(Template(json.dumps(data, ensure_ascii=False)).safe_substitute(
                {"username": self.username, "password": self.password}))
            response = request.api_request(sp['data']['request']['method'], sp['step'], url=url, headers=headers, data=data)
            validate = sp['data']['validate']
            for vd in validate:
                if "eq" in vd.keys():
                    vdkey = vd.get("eq")[0]
                    actual_result = jsonpath.jsonpath(response.json(), vdkey)
                    expect_result = vd.get("eq")[1]
                    try:
                        assert actual_result[0] == expect_result
                    except:
                        raise Exception(logger.error(f"实际结果：{actual_result[0]},期望结果：{expect_result}"))
        return response.json()

    def run(self,user_id,token,step,function,data):
        func = getattr(self,function)
        if not data:
            data = dict()
        logger.info(f'步骤：{step}')
        func(step,user_id,token,data)

if __name__ == '__main__':
    # u = user()
    # u.userRegister()
    # response = u.userLogin()
    # token = jsonpath.jsonpath(response, '$.data.token')
    # u.userUpdate(token[0])
    import os

    print(os.path.dirname(__file__))