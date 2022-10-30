# coding=utf-8
"""
公共的函数库
"""
import requests
from fake_useragent import UserAgent
from config import *
import re
import os
import json
import time
import sys


def get_headers():
    """
    用于产生随机UA
    :return:
    """
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Referer": "https://crt.sh"
    }
    return headers


def do_get(url):
    # 获取随机头
    headers = get_headers()
    # 发起请求
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        return response
    except Exception as e:
        pass


def is_domain(domain):
    """
    判断是否是有效域名
    :param domain:
    :return:
    """
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9])).'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    return True if pattern.match(domain) else False


def save(**dict):
    """
    base_path : ./cache
    path = ./cache/模块/域名/域名.时间.json
    :param dict: 动态参数的  data: 数据  module: 模块 domain: 域名
    :return:
    """
    # 分别获取数据
    data = dict['data']
    module = dict['module']
    domain = dict['domain']
    if data is not None and module is not None and domain is not None:
        # 先创建文件夹
        save_path = cache_base_path + module + "/" + domain + "/"
        make_dir(save_path)
        # 准备保存的完整路径
        save_path = save_path + domain + "." + str(time.time()) + ".json"
        # 保存数据
        with open(save_path, "a+") as f:
            json.dump(data, f, indent=4)


def make_dir(path):
    """
    用于生成路径
    :param path:
    :return:
    """
    if not os.path.exists(path):
        # 创建
        os.makedirs(path)


def jindu(per):
    """
    进度展示
    :param per:
    :return:
    """
    count = int(per)
    sys.stdout.write("\r" + ("=" * count) + f">[{per}%]")


def out_put(domain):
    """
    最后的输出方法
    :param domain: 域名
    :return:
    """
    # 准备一个大的列表
    domain_unique = []
    # 先准备路径 cache_base_path+module+domain
    for m in module_list:
        path = cache_base_path + m + "/" + domain
        if os.path.exists(path):
            # 去读取文件： 只需要获取最新生成文件
            files = os.listdir(path)
            # 取最新的文件
            file = files[-1]
            # 再读取文件的内容
            with open(path + "/" + file, "r") as f:
                data = json.load(f)
                domain_unique += data
    # 去重
    domain_unique = list(set(domain_unique))
    # 输出
    print("~~~~~~~~~~~~~~~~~最终结果~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for d in domain_unique:
        print(d)
