import os,time
from configure.filepath import PRO_PATH

def fetch_path(dir_path):
    """
       生成目录路径
       * @ param path: 目录路径
       * @ return 若目录不存在，则生成
    """
    path = os.path.join(PRO_PATH, dir_path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def fetch_path_with_time(dir_path, suffix):
    """
       生成文件路径
       * @ param dir_path: 路径
       * @ param suffix: 文件名后缀
       * @ return 路径+当前日期+当前时间+后缀
    """
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    now = time.strftime('%H_%M_%S', time.localtime(time.time()))
    file_path = os.path.join(fetch_path(dir_path), day)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_name = os.path.join(file_path, now + '-' + str(os.getpid()) + suffix)
    return file_name