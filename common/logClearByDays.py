import os, shutil
import datetime,time
from common.configLog import logger

def log_clear_by_days(path,days):
    try:
        dir_list = os.listdir(path)
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        today_stamp = time.mktime(time.strptime(today,"%Y-%m-%d"))
        start_day_stamp = int(today_stamp-days*24*3600)
        status = 0
        for name in dir_list:
            file_day_stamp = int(time.mktime(time.strptime(name,'%Y-%m-%d')))
            diff = file_day_stamp - start_day_stamp
            if diff >= 0:
                pass
            else:
                log_dir_path = path + '/' + name
                shutil.rmtree(log_dir_path)
                status = 1
        if status == 0:
            logger.info(f'不存在{str(days)}天之前的日志文件')
        else:
            logger.info(f'已删除{str(days)}天之前的日志文件')
    except:
        pass