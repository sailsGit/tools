# coding=utf-8
"""
主要是解析crt.sh 站点提供的子域名结果
"""
import sys
# 设置环境变量
sys.path.append("../")
from common import *
from bs4 import BeautifulSoup



class Crt_spider(object):
    def __init__(self, domain):
        self._base_url = "https://crt.sh/?q="
        self._domain = domain

    def start(self):
        print("crt模块开始执行......")
        scan_url = self._base_url+self._domain
        # 发起请求-调用公共模块的get/post方法
        flag = True
        response = ""
        while flag:
            response = do_get(scan_url)
            print(response.status_code)
            if response.status_code == 200:
                flag = False
        # 开始解析
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "lxml")
            # 解析子域名
            tds = soup.find_all(name="td", attrs={"style": None, "class": None})
            domain_list = []
            for td in tds:
                try:
                    if is_domain(td.string): # 是域名的才加入列表
                        domain_list.append(td.string)
                except Exception as e:
                    pass
            # 去重
            domain_list = list(set(domain_list))
            # 缓存起来
            save(data=domain_list, module="crt", domain=self._domain)
        print("crt模块运行完成！")


