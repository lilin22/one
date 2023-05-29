import json,requests,time
from common.configLog import logger

class request:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def retry(func):
        """失败重试，默认3次"""
        def wrapper(*args, **kwargs):
            if kwargs.get("data"):
                if isinstance(kwargs.get("data"), str):
                    kwargs['data'] = json.loads(kwargs.get("data"))
            # print(args[1])
            i = 1
            while i < 4:
                try:
                    logger.info(f"第{i}次请求，参数:{kwargs}")
                    response = func(*args, **kwargs)
                    if response.status_code == 200:
                        logger.info(f"第{i}次返回，响应:{response.json()}")
                        return response
                    else:
                        raise Exception(logger.error(f"第{i}次http请求状态码：{response.status_code}"))
                except BaseException as msg:
                    logger.error(str(msg))
                    i += 1
                    time.sleep(1)
            logger.error(f"{i-1}次请求异常！请求参数:{kwargs}")
        return wrapper

    @classmethod
    @retry
    def api_request(*args, **kwargs):
        if args[1] == "GET" or args[1] == "get":
            response = requests.get(url=kwargs.get('url'), headers=kwargs.get('headers'),timeout=3)
            return response
        elif args[1] == "POST" or args[1] == "post":
            if kwargs.get('headers')['Content-Type'] == 'application/json':
                response = requests.post(url=kwargs.get('url'),headers=kwargs.get('headers'),json=kwargs.get('data'),timeout=3)
                return response
            elif kwargs.get('headers')['Content-Type'] == 'application/x-www-form-urlencoded':
                response = requests.post(url=kwargs.get('url'), headers=kwargs.get('headers'), data=kwargs.get('data'),timeout=3)
                return response
            else:
                logger.error(f"不支持的Content-Type类型：{kwargs.get('headers')['Content-Type']}")
        elif args[1] == "PATCH" or args[1] == "patch":
            if kwargs.get('headers')['Content-Type'] == 'application/json':
                response = requests.patch(url=kwargs.get('url'),headers=kwargs.get('headers'),json=kwargs.get('data'),timeout=3)
                return response
            elif kwargs.get('headers')['Content-Type'] == 'application/x-www-form-urlencoded':
                response = requests.patch(url=kwargs.get('url'), headers=kwargs.get('headers'), data=kwargs.get('data'),timeout=3)
                return response
            else:
                logger.error(f"不支持的Content-Type类型：{kwargs.get('headers')['Content-Type']}")
        elif args[1] == "PUT" or args[1] == "put":
            response = requests.put(url=kwargs.get('url'), headers=kwargs.get('headers'), data=json.dumps(kwargs.get('data'),ensure_ascii=False),timeout=3)
            return response
        elif args[1] == "DELETE" or args[1] == "delete":
            response = requests.delete(url=kwargs.get('url'), headers=kwargs.get('headers'), json=kwargs.get('data'),timeout=3)
            return response
        else:
            logger.error(f"不支持的请求类型：{args[1]}")

    @retry
    def get(self, *args, **kwargs):
        response = requests.get(**kwargs)
        if response.status_code == 200:
            return response
        else:
            raise Exception(logger.error("该请求得到响应：%s ,响应码: %s" % (response, response.status_code)))

    @retry
    def post(self, *args, **kwargs):
        response = requests.post(**kwargs)
        if response.status_code == 200:
            return response
        else:
            raise Exception(logger.error("该请求得到响应：%s ,响应码: %s" % (response, response.status_code)))

    @retry
    def post_status(self, *args, **kwargs):
        response = requests.post(**kwargs)
        if response.status_code == 200:
            return response, response.status_code
        else:
            return response, response.status_code

    def queryUrl(self, url, queryDict):
        try:
            query = '?' + '&'.join([str(key)+"="+str(value) for key, value in queryDict.items()])
            new_url = "".join((url, query))
        except Exception as msg:
            logger.error(msg)
        return new_url

if __name__ == "__main__":
    r = request()
    res = r.get(4, url='https://www.baidu.com/', timeout=5)
    print("res: ", res)