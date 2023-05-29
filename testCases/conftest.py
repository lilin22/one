import json
import sys,os,re,pytest,jsonpath,allure
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5
from testCases.verifyCode.verifyCode import verifyCode
from testCases.user.user import user
from testCases.admin.admin import admin
from common.configLog import logger

def pytest_addoption(parser):
    parser.addoption(
        "--mobile", action="store", default="18965125035", help="my option: type1 or type2"
    )
    parser.addoption(
        "--password", action="store", default="qa123456!", help="my option: type1 or type2"
    )
    parser.addoption(
        "--nickname", action="store", default="test", help="my option: type1 or type2"
    )
    parser.addoption(
        "--message", action="store", default="520634", help="my option: type1 or type2"
    )

@pytest.fixture(scope="session")
def mobile(request):
    return request.config.getoption("--mobile")

@pytest.fixture(scope="session")
def password(request):
    return request.config.getoption("--password")


@pytest.fixture(scope="session")
def nickname(request):
    return request.config.getoption("--nickname")

@pytest.fixture(scope="session")
def message(request):
    return request.config.getoption("--message")

def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :param items:
    :return:
    """
    for item in items:
        try:
            re_case_name = re.findall(r"(\[.*\])", item._nodeid)
            if re_case_name:
                case_name = re_case_name[0]
                item._nodeid = item._nodeid.replace(case_name, case_name.encode("utf-8").decode("unicode-escape"))
        except Exception as e:
            logger.error(e)


@pytest.fixture(scope='session',autouse=True)
def userReady(mobile,password,nickname,message):
    logger.info(f"测试用户：{mobile},密码：{password},昵称：{nickname},验证码：{message}")
    # 管理员登录返回授权码，待补充
    adn = admin()
    response = adn.login()
    admin_id = jsonpath.jsonpath(response, '$.data.id')[0]
    admin_token = jsonpath.jsonpath(response, '$.data.token')[0]
    # admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzM5ODk5NDUsImlhdCI6MTY3OTM4MTk0NSwicm9sZSI6NCwidXNlcl9pZCI6MX0.kLdXNiHEhF1u2nq84FPtHmdIf0uXM668JYkzOCRneDo"
    # vc = verifyCode(mobile=mobile,password=password,nickname=nickname,message=message)
    # vc.sendCode()
    u = user(mobile=mobile,password=password,nickname=nickname,message=message)
    # u.userRegister()
    response = u.pubkey()
    key = jsonpath.jsonpath(response, '$.data.key')[0]
    cipher_pub = PKCS1_v1_5.new(RSA.importKey(key))
    response = u.login(cipher_pub)
    user_id = jsonpath.jsonpath(response, '$.data.id')[0]
    token = jsonpath.jsonpath(response, '$.data.token')[0]
    yield user_id,token,mobile,password,nickname,message,admin_id,admin_token
    u.userLogout()
    u.userDelete()