# -*- coding: utf-8 -*-
"""
自动安装Python接口自动化厕所框架所需要的库
"""
import os

if __name__ == '__main__':
    installFile = os.path.join(os.path.dirname(__file__), 'use_package')
    print (installFile)
    os.system('python -m  pip install -r  ' + installFile)
