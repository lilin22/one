import os,sys,json,jsonpath
import allure
from configure.filepath import ORGLIST_PATH_YAML,ORGEl_PATH_YAML

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

class org:
    '''组织管理'''

    def __init__(self,one_uri=one_uri,mobile=None,password=None,nickname=None,message=None):
        self.one_uri = one_uri
        self.mobile = mobile
        self.password = password
        self.nickname = nickname
        self.message = message
        self.org_id = None
        self.member_token = None

    def org_list(self,token):
        ym = processYaml(filepath.ORGLIST_PATH_YAML)
        ymdata = ym.read_yaml()
        for sp in ymdata["info"]:
            logger.info(f"执行前置：{sp['step']}")
            url = self.one_uri + sp['data']['request']['api']
            headers = json.loads(Template(json.dumps(sp['data']['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
            response = request.api_request(sp['data']['request']['method'], url=url, headers=headers)
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

    def org_del(self,token,ids):
        ym = processYaml(filepath.ORGEl_PATH_YAML)
        ymdata = ym.read_yaml()
        for sp in ymdata["info"]:
            logger.info(f"执行前置：{sp['step']}")
            url = self.one_uri + sp['data']['request']['api']
            headers = json.loads(
                Template(json.dumps(sp['data']['request']['headers'], ensure_ascii=False)).safe_substitute(
                    {"token": token}))
            sp['data']['request']['data']['ids'] = ids
            response = request.api_request(sp['data']['request']['method'], url=url, headers=headers,data=sp['data']['request']['data'])
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

    @allure.step('{step}')
    def orgAdd(self, step, user_id, token, data):
        '''新增组织'''
        url = self.one_uri + data['request']['api']
        headers = json.loads(
            Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
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

    @allure.step('{step}')
    def orgList(self, step, user_id, token, data):
        '''罗列所在组织'''
        url = self.one_uri + data['request']['api']
        headers = json.loads(Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
        response = request.api_request(data['request']['method'], url=url, headers=headers)
        validate = data['validate']
        validate[2]['eq'] = eval(Template(str(validate[2]['eq'])).safe_substitute({"mobile": self.mobile}))
        validate[3]['eq'] = eval(Template(str(validate[3]['eq'])).safe_substitute({"nickname": self.nickname}))
        for vd in validate:
            if "eq" in vd.keys():
                vdkey = vd.get("eq")[0]
                actual_result = jsonpath.jsonpath(response.json(), vdkey)
                expect_result = vd.get("eq")[1]
                try:
                    assert actual_result[0] == expect_result
                except:
                    raise Exception(logger.error(f"实际结果：{actual_result[0]},期望结果：{expect_result}"))
        self.org_id = jsonpath.jsonpath(response.json(), '$.data.manage_orgs.*.id')[1]
        return response.json()

    @allure.step('{step}')
    def orgDetails(self, step, user_id, token, data):
        '''获取组织详情'''
        url = self.one_uri + data['request']['api'] + str(self.org_id)
        headers = json.loads(
            Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
        response = request.api_request(data['request']['method'], url=url, headers=headers)
        validate = data['validate']
        # validate[2]['eq'] = eval(Template(str(validate[2]['eq'])).safe_substitute({"mobile": self.mobile}))
        # validate[3]['eq'] = eval(Template(str(validate[3]['eq'])).safe_substitute({"nickname": self.nickname}))
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
    def orgDel(self, step, user_id, token, data):
        '''解散组织'''
        url = self.one_uri + data['request']['api']
        headers = json.loads(
            Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
        response = request.api_request(data['request']['method'], url=url, headers=headers,data=data['request']['data'])
        validate = data['validate']
        # validate[2]['eq'] = eval(Template(str(validate[2]['eq'])).safe_substitute({"mobile": self.mobile}))
        # validate[3]['eq'] = eval(Template(str(validate[3]['eq'])).safe_substitute({"nickname": self.nickname}))
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
    def orgMemberAdd(self, step, user_id, token, data):
        '''添加组织成员'''
        url = self.one_uri + data['request']['api']
        headers = json.loads(
            Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
        data['request']['data']['org_id'] = self.org_id
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

    @allure.step('{step}')
    def orgMemberList(self, step, user_id, token, data):
        '''添加组织成员'''
        url = self.one_uri + Template(data['request']['api']).safe_substitute({"org_id": self.org_id})
        headers = json.loads(
            Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
        response = request.api_request(data['request']['method'], url=url, headers=headers)
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
    def orgMemberDel(self, step, user_id, token, data):
        '''剔除组织成员'''
        url = self.one_uri + data['request']['api']
        headers = json.loads(
            Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
        data['request']['data']['org_id'] = self.org_id
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

    @allure.step('{step}')
    def orgExit(self, step, user_id, token, data):
        '''退出组织'''
        url = self.one_uri + data['request']['api']
        headers = json.loads(
            Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": self.member_token}))
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

    @allure.step('{step}')
    def orgExitGetList(self, step, user_id, token, data):
        '''退出组织后罗列组织'''
        url = self.one_uri + data['request']['api']
        headers = json.loads(
            Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": self.member_token}))
        response = request.api_request(data['request']['method'], url=url, headers=headers)
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

        if len(response.json()['data']['manage_orgs']) == 1:
            return response.json()
        else:
            raise Exception(logger.error(f"退出组织失败，剩余组织个数为{len(response.json()['data']['manage_orgs'])}"))

    @allure.step('{step}')
    def orgDelGetList(self, step, user_id, token, data):
        '''解散组织后罗列组织'''
        url = self.one_uri + data['request']['api']
        headers = json.loads(
            Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute(
                {"token": token}))
        response = request.api_request(data['request']['method'], url=url, headers=headers)
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

        if len(response.json()['data']['manage_orgs']) == 1:
            return response.json()
        else:
            raise Exception(logger.error(f"退出组织失败，剩余组织个数为{len(response.json()['data']['manage_orgs'])}"))

    @allure.step('{step}')
    def orgModify(self, step, user_id, token, data):
        '''修改组织信息'''
        url = self.one_uri + data['request']['api']
        headers = json.loads(
            Template(json.dumps(data['request']['headers'], ensure_ascii=False)).safe_substitute({"token": token}))
        data['request']['data']['id'] = self.org_id
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
        return func(step,user_id,token,data)