# coding=utf-8
"""
通过字典的方式去爆破子域名, 结合多线程
思路很简单
1. 将文件的内容读取出来
2. 和域名进行拼接
3. 验证域名是否存在
4. 存放文件中
"""
import sys
# 设置环境变量
sys.path.append("../")
from config import domain_dict_path
from common import do_get
from common import jindu
from common import save
from queue import Queue
import requests
import threading


class Brute(object):
    def __init__(self, domain, thread_count):
        self._domain = domain
        self._queue = Queue()
        self._thread_count = thread_count
        self._threads = []
        self._total_count = 0
        self._result = []

    def _init(self):
        # 读取字典的内容
        with open(domain_dict_path, "r") as f:
            for d in f:
                # 拼接域名
                scan_domain = d.strip() + "." + self._domain
                # 将域名放入队列
                self._queue.put("http://"+scan_domain)
        self._total_count = self._queue.qsize()

    def start(self):
        print("brute模块开始执行......")
        # 初始化
        self._init()
        # 准备线程
        for i in range(self._thread_count):
            self._threads.append(self.Brute_run(self._queue, self._total_count, self._result))
        # 启动
        for t in self._threads:
            t.start()
        # 等待子线程结束
        for t in self._threads:
            t.join()

        # 保存结果
        save(data=self._result, module="brute", domain=self._domain)
        print("brute模块运行完成！")



    class Brute_run(threading.Thread):
        def __init__(self, queue, total_count, result):
            super().__init__()
            self._queue = queue
            self._total_count = total_count
            self._result = result

        def run(self):
            while not self._queue.empty():
                scan_domain = self._queue.get()
                # 显示进度
                threading.Thread(target=self._msg).start()
                try:
                    response = do_get(scan_domain)
                    if response.status_code != 404:
                        # 存放在一个result
                        self._result.append(scan_domain.lstrip("http://"))
                except Exception as e:
                    pass

        def _msg(self):
            # 算百分比
            already_do = round((100-(self._queue.qsize()/self._total_count)*100),2)
            jindu(already_do)
