# -*- coding: utf-8 -*-
import pymysql
# import cx_Oracle
from base_method import ReadConfig
from base_method import Log

readConfig = ReadConfig.Config()


class Mysql:

    def __init__(self, db_conf='MYSQL'):
        global host, username, password, port, database, config
        host = readConfig.get_mysql(db_conf, "host")
        username = readConfig.get_mysql(db_conf, "username")
        password = readConfig.get_mysql(db_conf, "password")
        port = readConfig.get_mysql(db_conf, "port")
        database = readConfig.get_mysql(db_conf, "database")
        config = {
            'host': str(host),
            'user': username,
            'passwd': password,
            'port': int(port),
            'db': database
        }
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None

    def connect_Mysql(self):
        """
        connect to database
        """
        try:
            # connect to DB
            self.db = pymysql.connect(**config)
            self.logger.info("connect DB %s:%s/%s" % (host, port, database))
            # create cursor
            self.cursor = self.db.cursor()
            self.logger.info("Connect DB successfully!")
        except ConnectionError as ex:
            self.logger.error(str(ex))

    def execute_edit_commit(self, sql=''):
        """
        execute sql数据增删改操作
        :param sql:
        :return:
        """
        try:
            self.connect_Mysql()
            # executing sql执行增删改操作
            self.cursor.execute(sql)
            # 日志文件中记录执行操作内容
            self.logger.info("执行增删改： " + str(sql))
            # executing by committing to DB
            self.db.commit()
        except pymysql.Error as ex:
            self.logger.error("数据库返回错误error： " + str(ex))
        finally:
            self.close_Mysql()

    def execute_find(self, sql=''):
        """
        execute sql数据查询操作
        :param sql:
        :return:tuple类型数据
        """
        try:
            self.connect_Mysql()
            # executing sql执行查询操作
            self.cursor.execute(sql)
            # 日志文件中记录执行操作内容
            self.logger.info("执行查询： " + str(sql))
            # 查询当前返回结果的全部数据
            value = self.get_all(self.cursor)
            return value
        except pymysql.Error as ex:
            self.logger.error("数据库返回错误error： " + str(ex))
        finally:
            self.close_Mysql()

    def get_all(self, cursor):
        """
        get all result afrer execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        self.logger.info("sql查询结果：" + str(value))
        return value

    def get_one(self, cursor):
        """
        get one result after execute sql
        :param cursor:
        :return:
        """
        value = self.cursor.fetchone()
        self.logger.info("sql查询结果：" + str(value))
        return value

    def close_Mysql(self):
        """
        close database
        :return:
        """
        self.db.close()
        self.logger.info("关闭数据库连接")


# class MyOracle:
#
#     def __init__(self):
#         """
#         oracle数据库操作
#         """
#         global username, password, ip, post, service_name
#         username = readConfig.get_oracle('USERNAME')
#         password = readConfig.get_oracle('PASSWORD')
#         ip = readConfig.get_oracle('IP')
#         post = readConfig.get_oracle('POST')
#         service_name = readConfig.get_oracle('SERVICE_NAME')
#         """
#         初始化
#         """
#         self.dns = cx_Oracle.makedsn(ip, post, service_name)
#         self.conn = None
#         self.cursor = None
#         self.log = Log.MyLog.get_log()
#         self.logger = self.log.get_logger()
#
#     def ReConnect(self):
#         """
#         建立连接
#         """
#         try:
#             self.conn = cx_Oracle.connect(username, password, self.dns)
#             self.cursor = self.conn.cursor()
#             self.logger.info("Connect DB successfully!")
#         except ConnectionError as e:
#             self.logger.error(e)
#
#     def closeDB(self):
#         """
#         关闭连接
#         """
#         self.conn.close()
#         self.logger.info("Database closed!")
#         self.conn = None
#
#     def executeSQL(self, sql):
#         """
#         数据操作
#         :param sql:
#         :return:
#         """
#         self.ReConnect()
#         self.cursor.execute(sql)
#         self.conn.commit()
#         return self.cursor
#
#     def get_all(self, cursor):
#         """
#         get all result after execute sql
#         :param cursor:
#         :return:
#         """
#         value = cursor.fetchall()
#         return value
#
#     def get_one(self, cursor):
#         """
#         get one result after execute sql
#         :param cursor:
#         :return:
#         """
#         value = cursor.fetchone()
#         return value
# debug



if __name__ == '__main__':
    Mysql1 = Mysql()
    from base_method import Exceloperate

    filepath = "Alarm_Data_API.xlsx"
    sheetName = "getAlarms.do"

    # 按行号来读取某一行某一列的值

    # excel_test_data = Exceloperate.ExcelUtil('Alarm_Data_API.xlsx', "getAlarms.do").read_excel()
    # print(excel_test_data)
    # sql = excel_test_data[1]["sql1"]
    sql = 'select * from tab_career_researcher_config'
    print(sql)

    # sql = exceloperate.ExcelUtil('test_data.xlsx').read_excel()[0]['sql']
    # print(sql % 2)
    ex = Mysql1.execute_find(sql)[0][1]
    print(ex)

    # Mysql2 = Mysql('MYSQL1')
    # sql2="SELECT * FROM my_table"
    # ex2=Mysql2.execute_find(sql2)
