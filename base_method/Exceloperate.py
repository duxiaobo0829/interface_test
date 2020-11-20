# -*- coding: utf-8 -*-
#author:xiaobo
import xlrd

from base_method import ReadConfig
from base_method.common import *
from base_method import Log


class ExcelUtil:
    # Excel操作
    # 包括Excel文件的读、拷贝、写入
    def __init__(self, excelPath, sheetName="Sheet1"):
        self.log = Log.Log()
        self.logger = self.log.get_logger()
        self.excelPath = excelPath
        self.sheetName = sheetName
        self.readConfig = ReadConfig.Config()
        # 读取config文件内测试数据存放位置与传入具体文件名称拼接而成--初始化Excel测试数据文件目录
        project_path = project_Dir()

        self.test_data_path = os.path.join(project_path, self.readConfig.get_path('Excel_data_path'), self.excelPath)
        # # 初始化ddt报告目录
        # self.report_path = os.path.join(self.log.get_result_path(), "ddt_report.xlsx")
        self.data = xlrd.open_workbook(self.test_data_path)
        self.table = self.data.sheet_by_name(self.sheetName)
        # 获取第一行作为key值
        self.keys = self.table.row_values(0)
        # 获取总行数
        self.rowNum = self.table.nrows
        # 获取总列数
        self.colNum = self.table.ncols

    def read_excel(self):
        '''
        方法说明:
        1.读取Excel文件,返回类型为一个list,Excel文件内每一行数据为一个list元素
        2.每一个list内存放的为字典数据，根据KEY和VALUE的形式取值
        '''
        self.logger.info("读取%s文件%s sheet页测试数据" % (self.excelPath, self.sheetName))
        if self.rowNum <= 1:
            print("总行数小于1")
        else:
            r = []
            j = 1
            for i in list(range(self.rowNum - 1)):
                s = {}
                # 从第二行取对应values值
                s['rowNum'] = i + 2
                values = self.table.row_values(j)
                for x in list(range(self.colNum)):
                    s[self.keys[x]] = values[x]  # .encode("utf-8")
                r.append(s)
                j += 1
            return r

    def get_value(self, rowName, colName):
        '''
        方法说明:
        1.读取Excel文件,返回类型为一个list,Excel文件内每一行数据为一个list元素
        2.每一个list内存放的为字典数据，根据KEY和VALUE的形式取值
        '''
        self.logger.info("读取%s文件%s页测试数据" % (self.excelPath, self.sheetName))
        if self.rowNum <= 1:
            print("总行数小于1")
        else:
            r = self.table.row_values(0)
            c = self.table.col_values(1)
            for i in range(len(r)):
                if r[i] == colName:
                    n = i
            for j in range(self.rowNum):
                values = self.table.row_values(j)
                for x in range(len(values)):
                    if values[x] == rowName:
                        value = values[n]
            return value

    def read_excel_dict(self,key = "case_number"):
        '''
        方法说明：
        1.读取excel，格式为dict格式
        2.以excel内case_number为主键.例如：
        {
            "case_number1":
            {
                "case_name":"xxx"
            }
        }
        '''
        list = self.read_excel()
        dict_data = {}
        for i in list:
            dict_data[i[key]] = i
        return dict_data

    # def copy_excel(self):
    #     # 拷贝测试数据文件到配置文件ddt_report_path所设置的路径中
    #
    #     wb2 = openpyxl.Workbook()
    #     wb2.save(self.report_path)
    #     # 读取数据
    #     wb1 = openpyxl.load_workbook(self.test_data_path)
    #     wb2 = openpyxl.load_workbook(self.report_path)
    #     sheets1 = wb1.sheetnames
    #     sheets2 = wb2.sheetnames
    #     sheet1 = wb1[sheets1[0]]
    #     sheet2 = wb2[sheets2[0]]
    #     max_row = sheet1.max_row  # 最大行数
    #     max_column = sheet1.max_column  # 最大列数
    #
    #     for m in list(range(1, max_row + 1)):
    #         for n in list(range(97, 97 + max_column)):  # chr(97)='a'
    #             n = chr(n)  # ASCII字符
    #             i = '%s%d' % (n, m)  # 单元格编号
    #             cell1 = sheet1[i].value  # 获取data单元格数据
    #             sheet2[i].value = cell1  # 赋值到test单元格
    #
    #     wb2.save(self.report_path)  # 保存数据
    #     wb1.close()  # 关闭excel
    #     wb2.close()
    #
    # def Write_excel(self, row_n, col_n, value):
    #     '''写入数据，如(2,3，"hello"),第二行第三列写入数据"hello"'''
    #     self.wb = load_workbook(self.report_path)
    #     self.ws = self.wb.active
    #     self.ws.cell(row_n, col_n).value = value
    #     self.wb.save(self.report_path)
    #
    # def wirte_result(self, result):
    #     # 返回结果的行数row_nub
    #     row_nub = result['rowNum']
    #     # 写入statuscode
    #     self.Write_excel(row_nub, 11, result['statuscode'])  # 写入返回状态码statuscode,第8列
    #     self.Write_excel(row_nub, 12, result['times'])  # 耗时
    #     self.Write_excel(row_nub, 13, result['error'])  # 状态码非200时的返回信息
    #     self.Write_excel(row_nub, 16, result['result'])  # 测试结果 pass 还是fail
    #     self.Write_excel(row_nub, 17, result['msg'])  # 抛异常


if __name__ == "__main__":
    filepath = "loginByOpendid_API.xlsx"
    sheetName = "loginByOpenid"
    # c=ExcelUtil()
    #按行号来读取某一行某一列的值
    excel_test_data = ExcelUtil(filepath, sheetName).read_excel()
    print (excel_test_data)
    apiname = excel_test_data[1]["case_number"]
    print(apiname)
    #按测试用例编号来读取某一行某一列的值
    data = ExcelUtil(filepath, sheetName)
    excel_test_data1= data.read_excel_dict("case_number")
    print (excel_test_data1)
    print(excel_test_data1["test_case_000"]["case_name"])




