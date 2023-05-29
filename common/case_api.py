import os.path,pymysql
import time
from common.processYaml import processYaml
from common import utils
from common import mslunit
from configure.setting import host,username,pwd,dbname,port
from common.configLog import logger

class case_api(object):

    @classmethod
    @utils.catch_exception
    def getCasesData(cls,file_path):
       module = os.path.split(file_path)[1]
       file_path = file_path.replace('testCases','testDatas')
       case_datas = []
       pid = os.getpid()
       conn = mslunit.sqlConnect(host,username,pwd,dbname,port)
       caseNos = cls.get_case(conn,pid,module)
       case_ids = eval(caseNos[0])
       for case_id in case_ids:
           fp = os.path.join(file_path + '\\' + str(case_id) + '.yaml')
           ym = processYaml(fp)
           ymdata = ym.read_yaml()
           story = ymdata['story']
           title = ymdata['title']
           info = ymdata['info']
           case_datas.append((case_id, story, title, info))
       mslunit.sqlcls(conn)
       return case_datas

    @classmethod
    def save_cases(cls,conn,pid,module,module_caseNos):
        sql = 'insert into casenos_by_pid_by_module(pid, module, caseNos) values ("%s", "%s", "%s");' % (str(pid), str(module), str(module_caseNos))
        mslunit.insert(conn,sql)

    @classmethod
    def get_case(cls, conn, pid, module):
        """
        通过pid获取测试用例id列表
        :param pid:
        :return:
        """
        sql = "select caseNos from casenos_by_pid_by_module where pid=%s and module='%s'" % (str(pid), str(module))
        data = mslunit.select(conn,sql)
        return data

    @classmethod
    def delete_cases(cls,conn, pid, module):
        sql = "delete from casenos_by_pid_by_module where pid=%s and module='%s'" % (str(pid), str(module))
        mslunit.delete(conn,sql)

    @classmethod
    def truncate_cases(cls,conn):
        sql = "truncate table casenos_by_pid_by_module"
        mslunit.truncate(conn,sql)

if __name__ == '__main__':
    case_api = case_api.getCasesData(r'C:\projects\one\testCases\user')