# -*- coding: utf-8 -*-
import os
import logging
import datetime as dt
from datetime import datetime
import threading
import shutil
from base_method import ReadConfig
from base_method.common import *

class Log:
    def __init__(self):
        # 设置日志目录
        c = ReadConfig.Config()
        self.console_output_level = c.get_log("console_level")
        self.file_output_level = c.get_log("file_level")
        self.pattern = c.get_log("pattern")
        self.formatter = logging.Formatter(self.pattern)
        self.resultPath = os.path.join(project_Dir(), "logs")
        self.log_file_name = c.get_log('file_name') if c and c.get_log('file_name') else 'output.log'  # 日志文件
        # self.backup_count = c.get_log('backup_count') if c and c.get_log('backup_count') else 5  # 保留的日志数量
        # 初始化
        self.logger = logging.getLogger()
        # 设置日志级别
        self.logger.setLevel(self.file_output_level)
        self.file_failure = int(c.get_log("file_failure"))
        listdir = [d for d in os.listdir(self.resultPath)]
        if listdir == [] :
            self.logPath = os.path.join(self.resultPath, str(datetime.now().strftime("%Y%m%d%H%M")))
            os.mkdir(self.logPath)
            listdir = [d for d in os.listdir(self.resultPath)]
        self.old_log_file_name = listdir[-1]
        self.new_log_file_name = str(datetime.now().strftime("%Y%m%d%H%M"))
        self.logPath = os.path.join(self.resultPath, self.old_log_file_name)
        if (int(self.new_log_file_name)-int(self.old_log_file_name)) > self.file_failure:
            self.logPath = os.path.join(self.resultPath, str(datetime.now().strftime("%Y%m%d%H%M")))
            os.mkdir(self.logPath)

    def get_logger(self):
        """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回
        我们这里添加两个句柄，一个输出日志到控制台，另一个输出到日志文件。
        两个句柄的日志级别不同，在配置文件中可设置。
        """
        if not self.logger.handlers:  # 避免重复日志
            # 创建一个FileHandler，用于写入日志文件
            file_handler = logging.FileHandler(os.path.join(self.logPath, self.log_file_name),'a', encoding='utf-8')
            """
            file_handler = TimedRotatingFileHandler(filename=os.path.join(self.logPath, self.log_file_name),
                                        when='m',
                                        interval=1,
                                        delay=True,
                                        backupCount=self.backup_count,
                                        encoding='utf-8'
                                        )
            """
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)

            # 给控制台添加handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)
        return self.logger

    def build_start_line(self, case_no):
        """
        write start line
        :param case_no:
        :return:
        """
        self.logger.info("------" + case_no + " API test Start------")

    def build_end_line(self, case_no):
        """
        write end line
        :param case_no:
        :return:
        """
        self.logger.info("--------" + case_no + " END--------")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info((case_name + " - Code:" + code + " - msg:" + msg))

    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = os.path.join(self.logPath, "report.html")
        return report_path

    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return self.logPath

    def write_result(self, result):
        """
        write result in logfile
        :param result:
        :return:
        """
        result_path = os.path.join(self.resultPath, self.log_file_name)
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            self.logger.error(str(ex))


class DeleteLog:
    def __init__(self):
        c = ReadConfig.Config()
        self.backup_days = c.get_log("backup_days")
        self.del_path = os.path.join(project_Dir(), "results")
        if not os.path.exists(self.del_path):
            os.mkdir(self.del_path)
        self.delList = os.listdir(self.del_path)  # 需要删除目录下所有文件或文件夹列表
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def compare_file_time(self, file):
        time_of_last_mod = dt.date.fromtimestamp(os.path.getctime(file))
        days_between = (dt.date.today() - time_of_last_mod).days
        if int(days_between) >= int(self.backup_days):
            return True
        return False

    def delete_file(self):
        try:
            if self.delList:
                print("日志文件夹中存在文件或文件夹")
        except Exception as e:
            print('Error:', e)
        else:
            for f in self.delList:  # 遍历该列表

                filePath = os.path.join(self.del_path, f)  # 如果列表项是文件
                if self.compare_file_time(filePath) and (os.path.isfile(filePath)):
                    self.logger.info('日志文件目录中存在时间超过有效期%s天的文件' % self.backup_days)
                    os.remove(filePath)
                    print("天啊，这是文件不是文件夹，删除错了")
                    print(filePath + " was removed!")
                '''   
                elif os.path.isdir(filePath):  # 如果不是文件，肯定是文件夹
                    print("文件夹存在")
                    for i in [os.sep.join([filePath, v]) for v in os.listdir(filePath)]:
                        if self.compare_file_time(i) and (os.path.isfile(i)):
                            shutil.rmtree(filePath, True)  # shutil（高级文件操作）shutil.rmtree() 的方法，不仅是清空，直接连文件夹都一起删掉
                            print("Directory:" + filePath + " was removed")
                '''
                try:
                    if os.path.isdir(filePath) and self.compare_file_time(filePath):  # 删除log目录
                        self.logger.info('日志文件目录中存在时间超过有效期%s天的文件夹' % self.backup_days)
                        for root, dirs, files in os.walk(filePath):  # (root:'目录x'，dirs:[目录x下的目录list]，files:目录x下面的文件)
                            for name in files:
                                # delete the log and test result
                                del_file = os.path.join(root, name)
                                os.remove(del_file)
                                self.logger.info(u'remove file[%s] successfully' % del_file)
                        shutil.rmtree(filePath)
                        self.logger.info(u'remove dir[%s] successfully' % filePath)
                except Exception as e:
                    self.logger.error(str(e))


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log


if __name__ == "__main__":
    log = MyLog.get_log()
    logger = log.get_logger()
    logger.debug("test debug")
    logger.info("test info")
    d = DeleteLog()
    d.delete_file()
