# coding:utf-8
# @Time : 2022/11/23 22:54
# @Author : 郑攀
# @File ： extract AOP.py
# @Software : PyCharm
import csv
import re
import time

from paddlenlp import Taskflow


def extract(sentence):
    if sentence:
        relations = my_ie_en(sentence)
        opinion_set = []
        # print(relations[0]['Aspect'])
        if 'Aspect' in relations[0].keys():
            for relation1 in relations[0]['Aspect']:
                aspect = relation1['text']
                if 'relations' in relation1.keys():
                    for relation2 in relation1['relations']['Opinion']:
                        if relation2['probability'] > 0.7:
                            opinion_set.append(relation2['text'])
            opinion_set = list(set(opinion_set))
            opinion_set.sort()

            aspect_opinion = []
            for opinion_can in opinion_set:
                aspect_best = ''
                probability_best = 0
                for relation1 in relations[0]['Aspect']:
                    aspect = relation1['text']
                    if 'relations' in relation1.keys():
                        if len(relation1['relations']['Opinion']) == 1 and relation1['relations']['Opinion'][0][
                            'text'] == opinion_can:
                            aspect_best = aspect
                            break

                        for relation2 in relation1['relations']['Opinion']:
                            if relation2['text'] == opinion_can and relation2['probability'] - probability_best > 0:
                                aspect_best = aspect
                                probability_best = relation2['probability']
                aspect_opinion.append([aspect_best, opinion_can])
            return aspect_opinion

        else:
            return []

    else:
        return []

def sentence_slipt(sentence):
    sentence_slipt_list = []
    while 1:
        sentence_now = re.split('[.?!]',sentence[0:800])
        if len(sentence_now) > 1:
            record = len(sentence_now[-1])
        else:
            record = 0
        sentence_slipt_list.append(sentence[0:800-record])

        # print(sentence + '\n')
        if not sentence:
            break
        sentence = sentence[800-record:]
    return sentence_slipt_list

schema = {'Aspect': 'Opinion'}
my_ie_en = Taskflow(task="information_extraction", schema=schema,use_fast=True,device_id=0)

AOP_id = 1
with open("The Piccadilly London West End.csv", "r", encoding='utf8') as f:
    lines = csv.reader(f)
    next(lines)
    for line in lines:
        try:
            if len(line[2] + '. ' + line[3]) < 800:
                # print(line[4] + '. ' + line[5])
                aspect_opinion_list = extract(line[2] + '. ' + line[3])
            else:
                review_split = sentence_slipt(line[2] + '. ' + line[3])
                aspect_opinion_list = []
                for k in range(len(review_split)):
                    # print(review_split[k])
                    aspect_opinion_list += extract(review_split[k])
            for j in range(len(aspect_opinion_list)):
                if '的' not in aspect_opinion_list[j][1]:
                    # print(aspect_opinion_list[j])
                    fp = open('The Piccadilly London West End AOP.csv', "a+", encoding='utf8', newline='')
                    write = csv.writer(fp)
                    write.writerow(
                        [AOP_id, aspect_opinion_list[j][0], aspect_opinion_list[j][1]])
                    print(AOP_id,aspect_opinion_list[j][0], aspect_opinion_list[j][1])
                    AOP_id += 1
                    fp.close()
        except:
            print(line[2] + '. ' + line[3])
