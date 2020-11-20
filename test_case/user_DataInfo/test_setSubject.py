# -*- coding: utf-8 -*-
import unittest,sys,time,datetime
sys.path.append("..")
from base_method import configHttp
from base_method  import ReadConfig
from base_method  import configDB
from base_method .Log import MyLog
from base_method import Exceloperate
import urllib3
import requests
from public_method.login import loginByOpenid
# 禁用安全请求警告
urllib3.disable_warnings()
"""######实例化这个文件所要使用到的对象#####"""
#实例化读取配置文件对象
readconfig = ReadConfig.Config()
#实例化日志类对象
log = MyLog.get_log()
logger = log.get_logger()
MySql = configDB.Mysql()
filepath = "userDataInfo_API.xlsx"
sheetName = "设置用户科目组合"
data = Exceloperate.ExcelUtil(filepath, sheetName)
excel_test_data1= data.read_excel_dict("case_number")


class Test_set_Subject(unittest.TestCase):
    '''用户设置科目组合'''
    @classmethod
    def setUpClass(self):
        self.apiname="用户设置科目组合"
        self.base_url = readconfig.get_baseurl("base_url")
        self.path =excel_test_data1["test_case_000"]["API_PATH"]
        self.url =self.base_url+self.path
        print(self.url)
        self.s = requests.session()
        log.build_start_line("%s"%self.apiname)
        loginByOpenid("oSeNZ5OwwKGI62w_hWEVDD0ZJLqs","oIGU46Kk4a5Lyq5HmC92kAbMNbfk")


    @classmethod
    def tearDownClass(self):
        self.apiname = "用户设置科目组合"
        log.build_end_line("--------测试%s---------"%self.apiname)

    def test_case_000(self):
        '''传入正确参数'''

        subjectGroupId = int(excel_test_data1["test_case_000"]["subjectGroupId"])
        UB_UserAgent_appUserAuthToken = excel_test_data1["test_case_000"]["UB_UserAgent_appUserAuthToken"]
        sql1 = excel_test_data1["test_case_000"]["sql1"]

        print(subjectGroupId)
        print(UB_UserAgent_appUserAuthToken)

        datas = {
            "subjectGroupId": subjectGroupId,
            "UB_UserAgent_appUserAuthToken": UB_UserAgent_appUserAuthToken,
                    }
        re=self.s.post(url=self.url,data=datas, verify=False)
        info = re.json()["info"]
        status =re.json()["status"]

        print(sql1)
        subject_data = MySql.execute_find(sql1)[0][1]
        # #断言
        logger.info("断言接口返回的每个字段是否正确")
        self.assertEqual(info, "查询成功！", msg='返回info不正确，用例执行失败')
        self.assertEqual(status, 200, msg='返回status不正确，用例执行失败')
        self.assertAlmostEqual(subject_data,subjectGroupId,msg='科目设置不成功，用例执行失败')
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
