# coding=utf-8
"""
子域名的收集程序设计
"""
from modules.crt import Crt_spider
from modules.brute import Brute
import threading
from common import out_put

domain = "wuyecao.net"
crt = Crt_spider(domain)
brute = Brute(domain, 100)
# 利用线程启动
threads = [threading.Thread(target=crt.start), threading.Thread(target=brute.start)]

for t in threads:
    t.start()
for t in threads:
    t.join()

out_put(domain)



