import yaml,os,json
from common.configLog import logger
from configure import filepath


class processYaml:
    def __init__(self, filename):
        """
        filename 文件名
        """
        self.filename = filename

    def read_yaml(self):
        """获取yaml中数据"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    file_data = f.read()
                data = yaml.load(file_data, Loader=yaml.FullLoader)
                return data
            except BaseException as msg:
                raise Exception(logger.error(msg))
        else:
            raise FileNotFoundError(logger.error("没有找到文件:%s" % self.filename))

    def write_yaml(self,data):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'w', encoding='utf-8') as f:
                    yaml.dump(data,stream=f,allow_unicode=True)
            except BaseException as msg:
                raise Exception(logger.error(msg))
        else:
            raise FileNotFoundError(logger.error("没有找到文件:%s" % self.filename))

if __name__ == "__main__":
    print(filepath.OAUTH_PATH_YAML)
    ym = processYaml(filepath.OAUTH_PATH_YAML)
    data = ym.read_yaml()
    print(data)
    print(data["title"])