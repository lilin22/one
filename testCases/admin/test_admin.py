import os,sys,allure,pytest,traceback
from common.configLog import logger
from common.case_api import case_api
from configure.filepath import TEST_CASES_PATH
from configure.setting import one_uri


class Test_cases:

    @pytest.mark.parametrize('case_id,story,title,info',case_api.getCasesData(os.path.dirname(__file__)))
    def test_cases(self, userReady, case_id, story, title, info):
        try:
            logger.info(f"执行用例：{title}")
            allure.dynamic.story(story)
            allure.dynamic.title(f'{case_id}---{title}')
            user_id, token, mobile, password, nickname, message, admin_id, admin_token = userReady
            cur_module = os.path.split(os.path.dirname(__file__))[1]
            sys.path.append(TEST_CASES_PATH + '\\' + cur_module)
            try:
                ip_module = __import__(cur_module)
                module_class = getattr(ip_module, cur_module)
            except:
                ip_module = __import__(f'{cur_module}.{cur_module}', fromlist=[cur_module])
                module_class = getattr(ip_module, cur_module)
            cls_obj = module_class(one_uri, mobile, password, nickname, message)
            for sp in info:
                if 'module' not in sp.keys():
                    step = sp["step"]
                    function = sp['function']
                    data = sp['data']
                    cls_obj.run(admin_id, token, step, function, data)
                else:
                    module = sp["module"]
                    sys.path.append(TEST_CASES_PATH + '\\' + module)
                    ip_module = __import__(module)
                    module_class = getattr(ip_module, module)
                    module_obj = module_class(one_uri, mobile, password, nickname, message)
                    step = sp["step"]
                    function = sp['function']
                    data = sp['data']
                    module_obj.run(admin_id, token, step, function, data)
        except Exception:
            raise Exception(logger.error(traceback.format_exc()))