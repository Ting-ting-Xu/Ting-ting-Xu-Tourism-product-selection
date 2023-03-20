# coding:utf-8
# @Time : 2022/11/29 19:34
# @Author : 郑攀
# @File ： Calculating M and N for online reviews.py
# @Software : PyCharm
import csv

dictionary = ['staff','facility','cleanliness','comfort','money','location','WiFi']

MN = []
for dic in dictionary:
    with open("The Piccadilly London West End 7个方面.csv", "r", encoding='utf8') as f:  # 打开文件
        lines = csv.reader(f)
        next(lines)
        M = 0
        N = 0
        for line in lines:
            if line[0] == dic:
                N += 1
                if float(line[3]) > 0.5:
                    M += 1
        MN.append([M,N])

print(MN)
