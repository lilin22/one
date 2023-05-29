import os

'''根目录'''
PRO_PATH = os.path.dirname(os.path.realpath(__file__)[:os.path.realpath(__file__).find('configure')])  # 获取项目目录

'''一级目录'''
TEST_CASES_PATH = os.path.join(PRO_PATH, 'testCases')  # 测试用例存放目录
TEST_DATAS_PATH = os.path.join(PRO_PATH, 'testDatas')  # 测试文件存放目录
LOG_PATH = os.path.join(PRO_PATH, 'logs')  # 日志文件存放目录
REPORTS_PATH = os.path.join(PRO_PATH, 'reports')  # 测试报告存放目录

'''测试数据(仅前后置)二级目录'''
VERIFYCODE_PATH = os.path.join(TEST_DATAS_PATH, 'verifyCode')    # 验证码
USER_PATH = os.path.join(TEST_DATAS_PATH, 'user')    # 用户鉴权
ORG_PATH = os.path.join(TEST_DATAS_PATH,'org')   # 组织管理
ADMIN_PATH = os.path.join(TEST_DATAS_PATH, 'admin')    # 管理员鉴权

'''测试数据(仅前后置)三级目录'''
VERIFYCODE_PATH_YAML = os.path.join(VERIFYCODE_PATH, 'verifyCode.yaml')    # 验证码
USERREGISTER_PATH_YAML = os.path.join(USER_PATH, 'register.yaml')    # 用户注册
PUBKEY_PATH_AYML = os.path.join(USER_PATH, 'pubkey.yaml')    # RSA加解密
USERLOGIN_PATH_YAML = os.path.join(USER_PATH, 'login.yaml')    # 用户登录
ORGLIST_PATH_YAML = os.path.join(ORG_PATH, 'orgList.yaml')    # 组织列表
ORGEl_PATH_YAML = os.path.join(ORG_PATH, 'orgDel.yaml')    # 解散组织
ADMINLOGIN_PATH_YAML = os.path.join(ADMIN_PATH, 'login.yaml')    # 管理员登录
