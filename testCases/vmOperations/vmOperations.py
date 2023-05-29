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

class vmOperations:
    '''vm应用状态'''
    def __init__(self,one_uri=one_uri,mobile=None,password=None,nickname=None,message=None):
        self.one_uri = one_uri
        self.mobile = mobile
        self.password = password
        self.nickname = nickname
        self.message = message

    def run(self,user_id,token,step,function,data):
        func = getattr(self, function)
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