import base64
import os,sys,json,jsonpath

import allure

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
rootPath = os.path.split(rootPath)[0]
sys.path.append(rootPath)
from configure.setting import one_uri
from common.request import request
from common.processYaml import processYaml
from string import Template
from configure import filepath
from common.configLog import logger

class zone:
    '''可用区管理'''

    def __init__(self,one_uri=one_uri,mobile=None,password=None,nickname=None,message=None):
        self.one_uri = one_uri
        self.mobile = mobile
        self.password = password
        self.nickname = nickname
        self.message = message

    @allure.step('{step}')
    def zoneAdd(self, step, user_id, token, data):
        '''添加可用区'''
        url = self.one_uri + data['request']['api']
        headers = json.loads(Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
        response = request.api_request(data['request']['method'], url=url, headers=headers,
                                       data=data['request']['data'])
        validate = data['validate']
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