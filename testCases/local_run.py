import os,sys,shutil,json
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from start_all import startAll
from common.configLog import logger


def remove(local_report_dir):
    for f in os.listdir(local_report_dir):
        file_path = os.path.join(local_report_dir, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

class localRun:
    """
    本地调试脚本类
    """
    def __init__(self, cmd, allure_data_dir):
        self.startAll = startAll()
        # 需要运行的pytest命令
        self.cmd = cmd
        # allure报告保存位置
        self.allure_data_dir = allure_data_dir

    def collectFailedCases(self,src_file):
        with open(src_file, "r", encoding='utf-8') as sf:
            sfContent = sf.read()
            sfJson = json.loads(sfContent)
            childrens = sfJson["children"]
            caseSuccessTotal = 0
            caseFailTotal = 0
            casetotal = 0
            casesSuccess = []
            casesFail = []
            for child in childrens:
                subChildrens = child["children"]
                for scd in subChildrens:
                    for sscd in scd["children"]:
                        for ssscd in sscd["children"]:
                            if "---" in ssscd["name"]:
                                cid = ssscd["name"].split("---")
                                caseNo = cid[0]
                            elif "[" in ssscd["name"]:
                                cid = ssscd["name"].split("[")
                                cd = cid[-1].split("-")
                                caseNo = cd[0]
                            casetotal = casetotal + 1
                            if ssscd["status"] == "passed":
                                caseSuccessTotal = caseSuccessTotal + 1
                                casesSuccess.append(caseNo)
                            else:
                                caseFailTotal = caseFailTotal + 1
                                casesFail.append(caseNo)

            # logger.info("上次任务的成功用例：" + str(casesSuccess))
            if len(casesSuccess) == caseSuccessTotal:
                logger.info("上次任务的成功用例总数：" + str(caseSuccessTotal))
            if len(casesFail) == caseFailTotal:
                logger.info("上次任务的失败用例总数：" + str(caseFailTotal))
                logger.info("上次任务的失败用例：" + str(casesFail))
            logger.info("上次任务的用例总数：" + str(casetotal))
            return casesFail

    def run(self,task_cases):
        self.startAll.run(cmd=self.cmd,task_cases=task_cases,allure_dir=self.allure_data_dir)

if __name__ == '__main__':
    try:
        local_report_dir = rootPath + r'\local_report'
        # 是否失败重跑，可修改
        reRunFlag = False
        # reRunFlag为False时，本地运行用例编号，可修改
        case_ids = ['16000']
        # 设置运行次数，可修改
        count = 1
        # 是否自动打开在线报告，否的话可在控制台或者日志查看运行日志和结果，可修改
        isOpenReport = False
        # 本地运行虚假taskId，不修改
        taskId = 100
        # 本地存放报告路径，不修改
        allure_data_dir = local_report_dir + r'\allure_raw'
        allure_report_dir = local_report_dir + r'\allure_report'
        if os.path.exists(allure_data_dir):
            remove(allure_data_dir)
        cmd = ['-v', '-l', '-s', '--durations=0', '--instafail','--tb=line', f'--count={count}']
        report_cmd = f"allure serve {allure_data_dir}"
        generate_report_cmd = f'allure generate {allure_data_dir} -o {allure_report_dir} --clean'
        src_file = allure_report_dir + r'\data\suites.json'
        local_run = localRun(cmd, allure_data_dir)
        # 用例编号，取决于是否失败重跑
        case_ids = case_ids if not reRunFlag else local_run.collectFailedCases(src_file)
        print(case_ids)
        task_cases = {"taskId": taskId, "total": len(case_ids), "caseNos": case_ids}
        local_run = localRun(cmd,allure_data_dir)
        local_run.run(task_cases)
        os.system(generate_report_cmd)
        if isOpenReport:
            os.system(report_cmd)
    except BaseException as msg:
        raise Exception(logger.error(str(msg)))
    