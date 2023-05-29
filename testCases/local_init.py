import os,sys
from common import mslunit

package_dir = '../package'
os.system(f'pip3 install -r {package_dir}')

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from configure.setting import host,username,pwd,dbname,port

casenos_by_pid_by_modul_sql = "CREATE TABLE IF NOT EXISTS casenos_by_pid_by_module (ID int(10)  NOT NULL AUTO_INCREMENT,\
        pid varchar(100),\
        module varchar(1000),\
        caseNos varchar(15000),\
        PRIMARY KEY (ID))"

modules_normal_sql = "CREATE TABLE IF NOT EXISTS modules_normal (ID int(10)  NOT NULL AUTO_INCREMENT,\
        busModule varchar(100) UNIQUE,\
        path varchar(50),\
        status varchar(50),\
        createTime datetime,\
        updateTime datetime,\
        PRIMARY KEY (ID))"

modules_unusual_sql = "CREATE TABLE IF NOT EXISTS modules_unusual (ID int(10)  NOT NULL AUTO_INCREMENT,\
      busModule varchar(100) UNIQUE,\
      path varchar(50),\
      status varchar(50),\
      createTime datetime,\
      updateTime datetime,\
      PRIMARY KEY (ID))"

cases_normal_sql = "CREATE TABLE IF NOT EXISTS cases_normal (ID int(10)  NOT NULL AUTO_INCREMENT,\
      caseNo varchar(100) UNIQUE,\
      caseTitle varchar(10000),\
      caseFile varchar(1000),\
      caseType varchar(50),\
      caseLevel varchar(50),\
      busModuleId int(10),\
      status varchar(50),\
      createTime datetime,\
      updateTime datetime,\
      PRIMARY KEY (ID))"

cases_unusual_sql = "CREATE TABLE IF NOT EXISTS cases_unusual (ID int(10)  NOT NULL AUTO_INCREMENT,\
      caseNo varchar(100) UNIQUE,\
      caseTitle varchar(10000),\
      caseFile varchar(1000),\
      caseType varchar(50),\
      caseLevel varchar(50),\
      busModuleId int(10),\
      status varchar(50),\
      createTime datetime,\
      updateTime datetime,\
      PRIMARY KEY (ID))"

conn = mslunit.sqlConnect(host,username,pwd,dbname,port)
mslunit.createTbe(conn,casenos_by_pid_by_modul_sql)
mslunit.createTbe(conn,modules_normal_sql)
mslunit.createTbe(conn,modules_unusual_sql)
mslunit.createTbe(conn,cases_normal_sql)
mslunit.createTbe(conn,cases_unusual_sql)
mslunit.sqlcls(conn)