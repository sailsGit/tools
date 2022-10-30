# coding=utf-8

import sys
# 写一下进度条
# ==========>
per = 100
# 根据百分比 算出 = 号的个数
count = int(per)
sys.stdout.write("\r")
for i in range(count):
    sys.stdout.write("=")
sys.stdout.write(">")
sys.stdout.write(f" [{per}%]")





