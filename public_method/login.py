# -*- coding: utf-8 -*-
#author xiaobo
import requests
import  urllib3
from base_method import configHttp
from base_method import ReadConfig
import time
from base_method.Exceloperate import  ExcelUtil
# 禁用安全请求警告
urllib3.disable_warnings()
localConfigHttp = configHttp.ConfigHttp()
readConfig = ReadConfig.Config()
base_url = readConfig.get_baseurl("base_url")
s=requests.session()
filepath = "loginByOpendid_API.xlsx"
sheetName = "loginByOpenid"
data = ExcelUtil(filepath, sheetName)
excel_test_data1= data.read_excel_dict("case_number")
rest_sign = excel_test_data1["test_case_000"]["rest_sign"]

# headers = {
#     "content-type": "application/json",
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
#     "UB_UserAgent_plat": "WECHATM",
#     "UB_UserAgent_deviceOSVersion": "v1.0.0",
#     "Connection": "keep-alive",
#
# }

def getWechatInfo():
    timestamp = str(int(round(time.time() * 1000)))
    path = '/subject/v2/rest/loginControl/getWechatInfo'
    url = base_url + path
    # print(timestamp)
    headers = {
        "rest_timestamp": timestamp,
        "rest_sign":rest_sign
    }

    json_data = {
        "jsCode": "0937iBFa1ATh0A0IJzJa1uHa8U17iBFQ",
        "encryptedData": "8Rg8dW6/QkciIUwoHnLqfwESYfH3vYnCQ9BabxYjKr5M82OQpRKHq6EJXRlR4RhbTFFj9sxis1Ae3DS3ZkmsvBQ7wrwHLvUOPuzlYvspzGqAeFXOpOSHP6tFd0d6Tz0SakxJusoe+PMjxpIVrTj5EJwcEJGwtvgm+OPgMv8jfq5jXXcGmHYuSdpStVQbuDzuaZvTNwO2fFu5wCCSipRdr1QAThhbYQFcHkQdwK88Y6I96LQHRdugm7Nn/hJCLobukRVPkniM6VAoEfR77nAiLhxvflfRG+17VMxv+ULkBzYsNa0pA85SRnPJbgnxp5TlGigyjV+INWzwFwAv/tBD3zg7RJUBiUjv9EDIjRJmAa5uC2gM0YRdrhPWNU94gf08AemLr2JMuHS+fIFe1lNkk88xXvkJBcXVaNKniG3dtZziTmBtZJxTEdcIvttDCfaCeaD7cNmjM3SoCk++be6j4mXoeQtz2GPxIBbcQhpPGaTlYW6Rf/WjsXDgOTgyljQeRFsg+NNvIq98mLOeQaPc6Tm0vSANsoMLOOByB2SjUgk=",
        "iv": "k7x48E0/jH/Fsi8RbhCdqA==",
        "minproId": 2
}

    re = s.post(url, headers=headers,json=json_data, verify=False)
    print(re.json())
    print(re.url)

def loginByOpenid(openId,unionId):
    timestamp = str(int(round(time.time() * 1000)))
    path = excel_test_data1["test_case_000"]["API_PATH"]
    # openId = excel_test_data1["test_case_000"]["openId"]
    # print(openId)
    # unionId = excel_test_data1["test_case_000"]["unionId"]
    print(unionId)
    url = base_url + path
    print(url)
    print(timestamp)
    headers = {
        "rest_timestamp": timestamp,
        "rest_sign": rest_sign,
        "Connection":"keep-alive",
        "UB_UserAgent_plat":"WECHATM",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "UB_UserAgent_appChannel":"applet",
        "plat":"1"
    }

    json_data = {
                "minproId": 2,
                "plat": 1,
                "openId": openId,
                "unionId": unionId,
                "invitedCode": "",
                "codeNo": 0,
                "userName": "rocky",
                "headImage": "https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIhh36w1Dibmaibuib7vib2gM6zyvOujfOMhbynA0PvZ42k6TGmia3yx7nLwRExDZE1Iic7wpk3BTeJlPAw/132",
                "gender": 1,
                "provinceName": "Sichuan",
                "cityName": "Chengdu"
                }

    re = s.post(url, headers=headers, data=json_data, verify=False)
    result = re.json()
    print(result)
    info = result["info"]
    status = result["status"]

    return info,status
    # print(re.url)



if __name__ == '__main__':
    # get_number('oSeNZ5MBw_C6eyWFa46kNmdgVFcA','1')
    # getWechatInfo()
    openId = excel_test_data1["test_case_000"]["openId"]
    unionId = excel_test_data1["test_case_000"]["unionId"]
    loginByOpenid(openId,unionId)

