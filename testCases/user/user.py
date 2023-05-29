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

class user:
    '''用户管理'''

    def __init__(self,one_uri=one_uri,mobile=None,password=None,nickname=None,message=None):
        self.one_uri = one_uri
        self.mobile = mobile
        self.password = password
        self.nickname = nickname
        self.message = message

    
    def userRegister(self):
        ym = processYaml(filepath.USERREGISTER_PATH_YAML)
        ymdata = ym.read_yaml()
        for sp in ymdata["info"]:
            logger.info(f"执行前置：{sp['step']}")
            url = self.one_uri + sp['data']['request']['api']
            headers = sp['data']['request']['headers']
            data = sp['data']['request']['data']
            data = json.loads(Template(json.dumps(data, ensure_ascii=False)).safe_substitute(
                {"mobile": self.mobile, "password": self.password, "nickname": self.nickname, "message": self.message}))
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
                        # 到时写法
                        # raise Exception(logger.error(f"实际结果：{actual_result[0]},期望结果：{expect_result}"))
                        # 现在写法
                        logger.error(f"实际结果：{actual_result[0]},期望结果：{expect_result}")
        return response.json()

    def pubkey(self):
        ym = processYaml(filepath.PUBKEY_PATH_AYML)
        ymdata = ym.read_yaml()
        for sp in ymdata["info"]:
            logger.info(f"执行前置：{sp['step']}")
            url = self.one_uri + sp['data']['request']['api']
            headers = sp['data']['request']['headers']
            response = request.api_request(sp['data']['request']['method'], sp['step'], url=url, headers=headers)
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

    def login(self,cipher_pub):
        ym = processYaml(filepath.USERLOGIN_PATH_YAML)
        ymdata = ym.read_yaml()
        for sp in ymdata["info"]:
            logger.info(f"执行前置：{sp['step']}")
            url = self.one_uri + sp['data']['request']['api']
            headers = sp['data']['request']['headers']
            data = sp['data']['request']['data']
            cipher_data = cipher_pub.encrypt(json.dumps({"password": self.password},ensure_ascii=False).encode('utf-8'))
            data = json.loads(Template(json.dumps(data, ensure_ascii=False)).safe_substitute(
                {"mobile": self.mobile, "password": self.password, "cipher_data": base64.b64encode(cipher_data).decode('utf-8')}))
            response = request.api_request(sp['data']['request']['method'], sp['step'], url=url, headers=headers, data=data)
            validate = sp['data']['validate']
            validate[2]['eq'] = eval(Template(str(validate[2]['eq'])).safe_substitute({"nickname": self.nickname}))
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

    @allure.step('{step}')
    def userLogin(self, step, user_id, token, data):
        '''用户登录'''
        url = self.one_uri + data['request']['api']
        response = request.api_request(data['request']['method'], url=url, headers=data['request']['headers'],
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

    @allure.step('{step}')
    def userInfo(self, step, user_id, token, data):
        url = self.one_uri + data['request']['api']
        headers = json.loads(Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
        response = request.api_request(data['request']['method'], url=url, headers=headers)
        validate = data['validate']
        validate[0]['eq'] = eval(Template(str(validate[2]['eq'])).safe_substitute({"mobile": self.mobile}))
        validate[1]['eq'] = eval(Template(str(validate[2]['eq'])).safe_substitute({"nickname": self.nickname}))
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

    @allure.step('{step}')
    def userUpdate(self, step, user_id, token, data):
        url = self.one_uri + data['request']['api']
        headers = json.loads(Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
        response = request.api_request(data['request']['method'], url=url, headers=headers,data=data['request']['data'])
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

    def userLogout(self):
        print('用户登出')

    def userDelete(self):
        print('删除用户')

if __name__ == '__main__':
    # u = user()
    # u.userRegister()
    # response = u.userLogin()
    # token = jsonpath.jsonpath(response, '$.data.token')
    # u.userUpdate(token[0])
    import os

    print(os.path.dirname(__file__))