import pytest,sys,os,requests
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from common.configLog import logger
from configure.setting import bridgeURI
from common.mslunit import sqlConnect
from configure.setting import one_host,one_username,one_pwd,one_dbname,one_port

@pytest.fixture(scope='class',autouse=True)
def initial_vm(userReady):
    user_id, token, mobile, password, nickname, message, admin_id, admin_token = userReady
    conn = sqlConnect(one_host,one_username,one_pwd,one_dbname,one_port)

def send_case_status(host,token,caseId,step,result):
    send_url = host + '/taskProcess'
    data = {
        "headers": {
            "token": token
        },
        "params": {
            "caseNo": caseId,
            "when": step,
            "status": result
        }
    }
    res = requests.post(url=send_url,json=data,timeout=3)
    logger.info(res.json())

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    获取每个用例状态的钩子函数
    :param item:
    :param call:
    :return:
    '''
    # 获取钩子方法的调用结果
    host = bridgeURI
    outcome = yield
    try:
        rep = outcome.get_result()
        # 仅仅获取用例call 执行结果是失败的情况, 不包含 setup/teardown
        nodeid = rep.nodeid
        nodeid1 = nodeid.split('[')[1]
        caseId = nodeid1.split('-')[0]
        step = rep.when
        result = rep.outcome
        logger.info('用例id:%s' % caseId)
        # print('测试报告：%s' % report)
        logger.info('步骤：%s' % step)
        # print('nodeid：%s' % report.nodeid)
        # print('description:%s' % str(item.function.__doc__))
        logger.info(('运行结果: %s' % rep.outcome))
        login_url = host + '/login'
        data = {"username": "organization", "password": "organization"}
        res = requests.post(url=login_url, json=data, timeout=10)
        token = res.json()['token']
        logger.info(token)
        send_case_status(host, token, caseId, step, result)
    except BaseException as msg:
        logger.error(str(msg))



