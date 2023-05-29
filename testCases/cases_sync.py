import os,sys,datetime
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from configure.filepath import TEST_CASES_PATH,TEST_DATAS_PATH
from common.configLog import logger
from common.processYaml import processYaml
from common.mslunit import sqlConnect,truncate,insert,selectAll,sqlcls
from configure.setting import host,username,pwd,dbname,port

class cases_sync:
    '''用例数据管理'''
    def __init__(self):
        self.conn = sqlConnect(host,username,pwd,dbname,port)

    def modules(self):
        try:
            truncate_modulesSuccess_sql = "truncate table modules_normal"
            truncate_modulesFail_sql = "truncate table modules_unusual"
            truncate(self.conn,truncate_modulesSuccess_sql)
            truncate(self.conn, truncate_modulesFail_sql)
            filesList = os.listdir(TEST_CASES_PATH)
            data = {}
            modules_success = []
            modules_fail = []
            modules = []
            for file in filesList:
                if os.path.isdir(TEST_CASES_PATH + '\\' + file) and '__' not in file:
                    modules.append(file)
            for module in modules:
                try:
                    mde_success = {}
                    sys.path.append(TEST_CASES_PATH + '\\' + module)
                    ip_module = __import__(module)
                    module_class = getattr(ip_module,module)
                    cls_obj = module_class()
                    mde_success['module'] = cls_obj.__doc__
                    mde_success['path'] = module
                    mde_success['status'] = '1'
                    if os.path.exists(TEST_CASES_PATH + '\\' + module + '\\' + f'test_{module}.py') and os.path.exists(TEST_CASES_PATH + '\\' + module + '\\conftest.py'):
                        modules_success.append(mde_success)
                    else:
                        raise Exception(logger.error(f'{module}不存在test_{module}.py或者conftest.py文件'))
                except BaseException as msg:
                    mde_fail = {}
                    mde_fail['module'] = ""
                    mde_fail['path'] = module
                    mde_fail['status'] = '0'
                    modules_fail.append(mde_fail)
                    logger.error(f'获取{module}异常')
                    logger.error(str(msg))
            data['modulesSuccess'] = modules_success
            data['modulesFail'] = modules_fail
            logger.info(f"获取模块数据：{data}")
            modulesSuccess_sql = "insert into modules_normal(busModule,path,status,createTime,updateTime) values"
            if modules_success != []:
                for ms in modules_success:
                    createTime = datetime.datetime.now()
                    modulesSuccess_sql += f"('{ms['module']}','{ms['path']}','{ms['status']}','{str(createTime)}','{str(createTime)}'),"
                logger.info(f"正常模块数据sql：{modulesSuccess_sql.strip(',')}")
                insert(self.conn,modulesSuccess_sql.strip(','))
            modulesFail_sql = "insert into modules_unusual(busModule,path,status,createTime,updateTime) values"
            if modules_fail != []:
                for mf in modules_fail:
                    createTime = datetime.datetime.now()
                    modulesFail_sql += f"('{mf['module']}','{mf['path']}','{mf['status']}','{str(createTime)}','{str(createTime)}'),"
                logger.info(f"异常模块数据sql：{modulesFail_sql.strip(',')}")
                insert(self.conn, modulesFail_sql.strip(','))
        except BaseException as msg:
            raise Exception(logger.error(str(msg)))

    def cases(self):
        try:
            truncate_casesSuccess_sql = "truncate table cases_normal"
            truncate_casesFail_sql = "truncate table cases_unusual"
            truncate(self.conn, truncate_casesSuccess_sql)
            truncate(self.conn, truncate_casesFail_sql)
            modules_sql = 'select * from modules_normal'
            modules_rows = selectAll(self.conn,modules_sql)
            data = []
            for md in modules_rows:
                module = {}
                module['id'] = md[0]
                module['module'] = md[1]
                module['path'] = md[2]
                module['status'] = md[3]
                data.append(module)
            modules_data = {'data': data}
            filesList = os.listdir(TEST_DATAS_PATH)
            data = {}
            cases_success = []
            cases_fail = []
            modules = []
            for file in filesList:
                if os.path.isdir(TEST_DATAS_PATH + '\\' + file) and '__' not in file:
                    modules.append(file)
            for module in modules:
                filesList = os.listdir(TEST_DATAS_PATH + '\\' + module)
                id = [m.get("id") for m in modules_data['data'] if m['path'] == module][0]
                # print(id)
                for file in filesList:
                    suffix = file.split(".")[0]
                    if suffix.isdigit():
                        cases = {}
                        cases['caseNo'] = suffix
                        cases['moduleId'] = id
                        ym = processYaml(TEST_DATAS_PATH + '\\' + module + '\\' + file)
                        ymdata = ym.read_yaml()
                        try:
                            cases['caseTitle'] = ymdata['title']
                            if ymdata['caseType'].strip() == '冒烟测试':
                                cases['caseType'] = '1'
                            elif ymdata['caseType'].strip() == '回归测试':
                                cases['caseType'] = '2'
                            else:
                                cases_fail.append(cases)
                                logger.error(f'编号{suffix}类型填写错误')
                                continue


                            if ymdata['caseLevel'].strip() == '高':
                                cases['caseLevel'] = '1'
                            elif ymdata['caseLevel'].strip() == '中':
                                cases['caseLevel'] = '2'
                            elif ymdata['caseLevel'].strip() == '低':
                                cases['caseLevel'] = '3'
                            else:
                                cases_fail.append(cases)
                                logger.error(f'编号{suffix}等级填写错误')
                                continue

                            if ymdata['status'].strip() == '启用':
                                cases['status'] = '1'
                            elif ymdata['status'].strip() == '禁用':
                                cases['status'] = '0'
                            else:
                                cases_fail.append(cases)
                                logger.error(f'编号{suffix}状态填写错误')
                                continue
                            cases_success.append(cases)
                        except BaseException as msg:
                            cases_fail.append(cases)
                            logger.error(f'编号{suffix}异常')
                            logger.error(str(msg))
            data['casesSuccess'] = cases_success
            data['casesFail'] = cases_fail
            logger.info(f"获取用例数据：{data}")
            casesSuccess_sql = "insert into cases_normal(caseNo,caseTitle,caseType,caseLevel,busModuleId,status,createTime,updateTime) values"
            if cases_success != []:
                for cs in cases_success:
                    createTime = datetime.datetime.now()
                    casesSuccess_sql += f"('{cs['caseNo']}','{cs['caseTitle']}','{cs['caseType']}','{cs['caseLevel']}',{cs['moduleId']},'{cs['status']}','{str(createTime)}','{str(createTime)}'),"
                logger.info(f"正常模块数据sql：{casesSuccess_sql.strip(',')}")
                insert(self.conn, casesSuccess_sql.strip(','))
            casesFail_sql = "insert into cases_unusual(busModule,path,status,createTime,updateTime) values"
            if cases_fail != []:
                for cf in cases_fail:
                    createTime = datetime.datetime.now()
                    casesFail_sql += f"('{cf['caseNo']}','{cf['caseTitle']}','{cf['caseType']}','{cf['caseLevel']}',{cf['moduleId']},'{cf['status']}','{str(createTime)}','{str(createTime)}'),"
                logger.info(f"异常模块数据sql：{casesFail_sql.strip(',')}")
                insert(self.conn, casesFail_sql.strip(','))
        except BaseException as msg:
            raise Exception(logger.error(str(msg)))
    def sync(self):
        if len(sys.argv) <= 1:
            self.modules()
            self.cases()
        else:
            function = sys.argv[1]
            func = getattr(self, function)
            return func()

    def __del__(self):
        sqlcls(self.conn)

if __name__ == '__main__':
    cs = cases_sync()
    cs.sync()