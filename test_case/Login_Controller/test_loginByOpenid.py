# -*- coding: utf-8 -*-
import unittest,sys,time,datetime
sys.path.append("..")
from base_method import configHttp
from base_method  import ReadConfig
from base_method  import configDB
from base_method .Log import MyLog
from base_method import Exceloperate
from public_method.login import loginByOpenid
import requests
"""######实例化这个文件所要使用到的对象#####"""
#实例化读取配置文件对象
readconfig = ReadConfig.Config()
#实例化日志类对象
log = MyLog.get_log()
logger = log.get_logger()
MySql = configDB.Mysql()
filepath = "loginByOpendid_API.xlsx"
sheetName = "loginByOpenid"
data = Exceloperate.ExcelUtil(filepath, sheetName)
excel_test_data1= data.read_excel_dict("case_number")


class Test_loginByOpenid(unittest.TestCase):
    '''通过openid登录'''
    @classmethod
    def setUpClass(self):
        self.apiname='通过openid登录'

        log.build_start_line("%s"%self.apiname)

    @classmethod
    def tearDownClass(self):
        self.apiname = '通过openid登录'
        log.build_end_line("--------测试%s---------"%self.apiname)

    def test_case_000(self):
        '''传入正确参数进行登录'''

        openId = excel_test_data1["test_case_000"]["openId"]
        unionId = excel_test_data1["test_case_000"]["unionId"]
        result=loginByOpenid(openId,unionId)
        info = result[0]
        status = result[1]

        # #断言
        logger.info("断言接口返回的每个字段是否正确")
        self.assertEqual(info, "查询成功！", msg='返回info不正确，用例执行失败')
        self.assertEqual(status, 200, msg='返回status不正确，用例执行失败')
        logger.info("接口返回符合预期，用例执行通过")
    def test_case_001(self):
        '''openId为空'''

        openId = excel_test_data1["test_case_001"]["openId"]
        unionId = excel_test_data1["test_case_001"]["unionId"]
        result = loginByOpenid(openId, unionId)
        info = result[0]
        status = result[1]

        # #断言
        logger.info("断言接口返回的每个字段是否正确")
        self.assertEqual(info,"查询成功！",msg='返回info不正确，用例执行失败')
        self.assertEqual(status,200,msg='返回status不正确，用例执行失败')
        logger.info("接口返回符合预期，用例执行通过")


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(Test_Suite_getAlarms('test_case_000'))
# #     suite.addTest(Test_Suite_get_school_info("test_case_002"))
# #     suite.addTest(Test_Suite_get_school_info("test_case_003"))
# #     suite.addTest(Test_Suite_get_school_info("test_case_005"))
# #     #suite.addTest(Test_Suite_get_school_info("test_case_021"))
    # # runner.run(suite)
