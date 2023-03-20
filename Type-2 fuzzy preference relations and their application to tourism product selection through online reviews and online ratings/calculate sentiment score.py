# coding:utf-8
# @Time : 2022/11/29 13:59
# @Author : 郑攀
# @File ： Calculate sentiment score.py
# @Software : PyCharm
import csv

import numpy as np
from paddlenlp import Taskflow

dictionary = ['staff','facility','cleanliness','comfort','money','location','WiFi']

from nltk.corpus import wordnet as wn


def wordnetSim(word1, word2):##有问题？
    """
    语义相似度，基于wordnet
    计算词语相似度时，总以包含词语概念的语义相似度的最大值来表示词语的语义相似度，将其也应用于短文本（短语），即基于最大值的短文本语义相似度
    ##对于短语中部分词相等的处理
    :param word1: 词
    :param word2: 词
    :return: 基于最大值的wordnet的语义相似度
    """
    phrase1 = word1
    phrase2 = word2
    word1 = phrase1.split(' ')
    word2 = phrase2.split(' ')
    path_sim = 0
    for w1 in word1:
        for w2 in word2:
            synsets1 = wn.synsets(w1)
            synsets2 = wn.synsets(w2)
            #path_sim = 0
            for tmpword1 in synsets1:
                for tmpword2 in synsets2:
                    if tmpword1.pos() == tmpword2.pos():
                        try:   ###对于短语中部分词相等的处理
                            sim = tmpword1.path_similarity(tmpword2)
                            path_sim = max(path_sim, sim)  # 取最大值
                        except Exception as e:
                            continue
                            #print(tmpword1, tmpword2)
                            #print("path: " + str(e))
    return path_sim

schema = 'Sentiment classification [negative, positive]'
my_ie_en = Taskflow(task="information_extraction", schema=schema, model='uie-base-en')

AOPs = []
with open("The Piccadilly London West End AOP.csv", "r", encoding='utf8') as f:  # 打开文件
    lines = csv.reader(f)
    next(lines)
    for line in lines:
        AOPs.append([line[1],line[2]])

fp = open('The Piccadilly London West End 7个方面.csv', "a+", encoding='utf8', newline='')
write = csv.writer(fp)
sentiment_all = []
for dic in dictionary:
    sentiment = []
    for i in range(len(AOPs)):
        if wordnetSim(AOPs[i][0], dic) > 0.5 or wordnetSim(AOPs[i][1], dic) > 0.5:
            print(i,AOPs[i][0],AOPs[i][1], dic)
            if my_ie_en(AOPs[i][0] + ' ' + AOPs[i][1]) == [{}]:
                sentiment_score = 0.5

            else:
                sentiment_dic = my_ie_en(AOPs[i][0] + ' ' + AOPs[i][1])[0]['Sentiment classification [negative, positive]'][0]
                if sentiment_dic['text'] == 'negative':
                    sentiment_score = 1 - float(sentiment_dic['probability'])
                else:
                    sentiment_score = float(sentiment_dic['probability'])

            sentiment.append(sentiment_score)
            write.writerow([dic,AOPs[i][0],AOPs[i][1],sentiment_score])
    sentiment_all.append(np.mean(sentiment))

print(sentiment_all)


