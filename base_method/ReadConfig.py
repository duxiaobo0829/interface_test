# -*- coding: utf-8 -*-
import os
import configparser
from base_method.common import *


class Config:
    """配置文件读取方法封装"""

    def __init__(self, config_file="config.ini"):
        # 获取配置文件所在目录
        self.conf_path = os.path.join(project_Dir(), "config")
        self.config_file = config_file
        # 生成配置文件完整路径
        self.config_name = os.path.basename(os.path.join(self.conf_path, self.config_file))
        self.conf = configparser.RawConfigParser()
        # 读取配置文件到conf对象(中文乱码问题需要添加encoding="utf-8-sig")
        self.conf.read(os.path.join(self.conf_path, self.config_name), encoding="utf-8-sig")

    def get_http(self, name):
        value = self.conf.get("HTTP", name)
        return value


    def get_baseurl(self, name):
        value = self.conf.get("URL", name)
        return value

    def get_email(self, name):
        value = self.conf.get("EMAIL", name)
        return value

    def get_mysql(self, db_conf, name):
        value = self.conf.get(db_conf, name)
        return value

    def get_oracle(self, name):
        value = self.conf.get("ORACLE", name)
        return value

    def get_vehicle(self, name):
        value = self.conf.get("VEHICLE", name)
        return value

    def get_interface_url(self, name):
        value = self.conf.get("INTERFACE_URL", name)
        return value

    def get_log(self, name):
        value = self.conf.get("LOG", name)
        return value

    def get_path(self, name):
        value = self.conf.get("PATH", name)
        return value


if __name__ == '__main__':
    c = Config()
    print(c.get_http("scheme"))
