import json,os,math,multiprocessing,sys
import time
import pytest
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from common.configLog import logger
from configure.setting import host,username,pwd,dbname,port
from configure.setting import days
from common import utils
from common import case_api
from common.logClearByDays import log_clear_by_days
from common import mslunit
from configure.setting import users,TASKCASES_PATH
from configure.filepath import LOG_PATH,TEST_CASES_PATH,TEST_DATAS_PATH

class startAll:

    def __init__(self):
        self.users = users
        conn = mslunit.sqlConnect(host,username,pwd,dbname,port)
        case_api.case_api.truncate_cases(conn)

    @utils.catch_exception
    def get_modules_dirs(self,caseNos):
        all_data_dirs = os.listdir(TEST_DATAS_PATH)
        module_data_dirs = []
        modules_run_caseNos = {}
        run_caseNos = []
        for data_dir in all_data_dirs:
            module_data_dirs.append(os.path.join(TEST_DATAS_PATH,data_dir))
            modules_run_caseNos[data_dir] = []
        for module_data_dir in module_data_dirs:
            caseNoYamls = os.listdir(module_data_dir)
            for caseNo in caseNos:
                if f'{caseNo}.yaml' in caseNoYamls:
                    modules_run_caseNos[os.path.split(module_data_dir)[1]].append(caseNo)
                    run_caseNos.append(caseNo)
        logger.info(f"实际执行用例总数：{str(len(run_caseNos))}，用例列表：{str(run_caseNos)}")
        # print(modules_run_caseNos)
        return modules_run_caseNos

    @utils.catch_exception
    def assign_by_users(self,cmd,allure_dir,modules_run_caseNos):
        # user_modules = {
        #     "18965125035":['C:\\projects\\one\\testCases\\user', 'C:\\projects\\one\\testCases\\user2'],
        #     "13507589853":['C:\\projects\\one\\testCases\\user3', 'C:\\projects\\one\\testCases\\user4']
        # }
        i = 0
        user_modules = {}
        modules = []
        process = []
        for module in modules_run_caseNos.keys():
            if modules_run_caseNos[module] != []:
                modules.append(module)
        # 测试代码
        # modules = ['user', 'user2', 'user3']
        # modules = ['user', 'user2', 'user3', 'user4', 'user5']
        step = math.floor(len(modules) / len(self.users))
        for u in users:
            if step < len(modules) / len(self.users):
                # print(i,i + step + 1)
                user_modules[u["mobile"]] = modules[i: i + step + 1]
                i = i + step + 1
            else:
                # print(i, i + step)
                user_modules[u["mobile"]] = modules[i: i + step]
                i = i + step
        logger.info(f'用户分配模块：{user_modules}')
        for pn in user_modules.keys():
            modules = user_modules[pn]
            module_paths = []
            if modules != []:
                for module in modules:
                    module_path = os.path.join(TEST_CASES_PATH, module)
                    module_paths.append(module_path)
                    # module_caseNos = modules_run_caseNos[module]
                # print(pn,module_paths,modules_run_caseNos)
                password = [u.get("password") for u in users if u['mobile'] == pn][0]
                nickname = [u.get("nickname") for u in users if u['mobile'] == pn][0]
                message = [u.get("message") for u in users if u['mobile'] == pn][0]
                t = multiprocessing.Process(target=self.start_task,args=(pn,password,nickname,message,module_paths,modules_run_caseNos,cmd,allure_dir),daemon=True)
                process.append(t)
        return process

    @utils.catch_exception
    def start_task(self,mobile,password,nickname,message,module_paths,modules_run_caseNos,testcmd,allure_dir):
        # 测试代码
        # path = ['user','user2','user3','user4','user5']
        pid = os.getpid()
        conn = mslunit.sqlConnect(host, username, pwd, dbname, port)
        logger.info(f'账号：{mobile},进程id：{str(pid)},业务模块：{str(module_paths)}')
        for module_path in module_paths:
            path = os.path.split(module_path)[1]
            case_api.case_api.save_cases(conn,pid,path,modules_run_caseNos[path])
            cmd = [f'--mobile={mobile}',f'--password={password}',f'--nickname={nickname}',f'--message={message}',f'{path}',f'--alluredir={allure_dir}'] + testcmd
            logger.info(f'生成调用命令：{cmd}')
            try:
                pytest.main(cmd)
            except BaseException as error:
                raise Exception(logger.error('pytest.main报错%s' % str(error)))
        mslunit.sqlcls(conn)

    @utils.catch_exception
    def run(self,cmd=None,task_cases=None,allure_dir=None):
        log_clear_by_days(LOG_PATH,days)
        cmd = cmd if cmd else eval(sys.argv[1])
        allure_dir = allure_dir if allure_dir else sys.argv[2]
        if task_cases:
            task_cases = task_cases
        else:
            with open(TASKCASES_PATH, "r", encoding='utf-8') as ci:
                data = ci.read()
                task_cases = json.loads(data)
        taskId = task_cases["taskId"]
        caseTotal = task_cases["total"]
        caseNos = task_cases["caseNos"]
        logger.info(f"任务ID：{str(taskId)}，用例总数：{str(caseTotal)}，用例列表：{str(caseNos)}")
        modules_run_caseNos = self.get_modules_dirs(caseNos)
        process = self.assign_by_users(cmd,allure_dir,modules_run_caseNos)
        for p in process:
            p.start()
        for p in process:
            p.join()

if __name__ == '__main__':
    s = startAll()
    s.run()