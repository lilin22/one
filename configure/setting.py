# ENV分为DEV（集成环境）、UAT（测试环境）、PROD（生产环境）
ENV = 'DEV'
one_uri = 'http://one.172.16.33.27.nip.io:30911' if ENV == 'DEV' else 'http://one.172.16.33.27.nip.io:30399' if ENV == 'UAT' else 'https://xxxxxxxx'
# one测试用户
users = [
    {"mobile": "15711593316","password": "123456@wzl","nickname": "15711593316","message": "666888"},
    {"mobile": "18965125035","password": "qa123456!","nickname": "李","message": "666888"},
    {"mobile": "13507589853","password": "qa123457!","nickname": "test1","message": "666888"},
    {"mobile": "15869164072","password": "qa123458!","nickname": "test2","message": "666888"}
]

adminUser = {"username": "admin","password":"1234567a"}

# oneBridge地址
bridgeURI = 'http://127.0.0.1:18080/one'

#数据库
host = '127.0.0.1'
username = 'root'
pwd = 'cpy123456!'
dbname = 'one'
port = 3306

#one数据库
one_host = '127.0.0.1'
one_username = 'root'
one_pwd = 'cpy123456!'
one_dbname = 'one'
one_port = 3306

#日志保留最近天数
days = 3

TASKCASES_PATH = r"C:\projects\oneCtl\taskCases.txt"
