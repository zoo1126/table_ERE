#  -*- coding = utf-8 -*-
#  @time: 2023/12/6 15:57
#  Author: yyzhang
#  @file: sanwen_data_processor.py


import json
import os
import re
import string

import jieba


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

# 针对原数据集中txt段落和ann文件标注进行整合处理，将其处理为json数据集格式
def integrate_data_txt(unique_name, input_path, output_path):
    path = input_path + unique_name + ".txt"
    ann_path = input_path + unique_name + ".ann"
    data_txt = ""
    with open(path, 'r', encoding='utf8') as txtFp:
        lines = txtFp.readlines()
        for line in lines:
            data_txt += line.strip()
    sentences = []
    sentence = ""
    quotation_mark_num = 0
    colon = False
    word_before_quotation = False

    for i, character in enumerate(data_txt):
        if sentence == "" and character == '…':
            continue

        # 如果sentence不为空，判断最后一位字符处是否应该结束
        if sentence != "":
            # 判断为句子末尾
            last_char = sentence[-1:]
            if last_char == '：':
                colon = True
            if last_char == '“':
                quotation_mark_num += 1
                fore_char = sentence[-2:-1]
                if is_Chinese(fore_char):
                    word_before_quotation = True
            if last_char == '”':
                quotation_mark_num -= 1
                fore_char = sentence[-2:-1]
                if colon and character != '，' and character != ',':
                    colon = False
                    if fore_char == '。' or fore_char == '？' or fore_char == '！' or fore_char == '.' or fore_char == '?' or fore_char == '!' or fore_char == '…':
                        sentences.append(sentence)
                        sentence = ""
                        word_before_quotation = False
                elif colon and (character == '，' or character == ','):
                    colon = False
                elif not colon:
                    if (fore_char == '。' or fore_char == '？' or fore_char == '！' or fore_char == '.' or fore_char == '?' or fore_char == '!' or fore_char == '…') and not word_before_quotation:
                        sentences.append(sentence)
                        sentence = ""
                        word_before_quotation = False
            if quotation_mark_num == 0 and (last_char == '。' or last_char == '？' or last_char == '！' or last_char == '.' or last_char == '?' or last_char == '!'
                                                           or last_char == '…'):
                if last_char == '…':
                    sentence += '…'
                    if sentence == "……":
                        sentence = ""
                    else:
                        sentences.append(sentence)
                        colon = False
                        sentence = ""
                        word_before_quotation = False
                elif last_char == '.':
                    if not character.isdigit():
                        sentences.append(sentence)
                        colon = False
                        sentence = ""
                        word_before_quotation = False
                elif sentence == '。' or sentence == '？' or sentence == '！' or sentence == '.' or sentence == '?' or sentence == '!' or sentence == '…':
                    colon = False
                    sentence = ""
                else:
                    sentences.append(sentence)
                    colon = False
                    sentence = ""
                    word_before_quotation = False
        sentence += character

    if sentence != "…" and sentence != "。" and sentence != "？" and sentence != "！" and sentence != "." and sentence != "?" and sentence != "!":
        sentences.append(sentence)
    with open(output_path + unique_name + ".txt", 'w', encoding='utf8') as fp:
        for sentence in sentences:
            fp.write(sentence)
            fp.write("\n")


def open_ann(file_path):
    with open(file_path, 'r', encoding='utf8') as fp:
        lines = fp.readlines()
        msg = []
        for line in lines:
            line_msg = line.strip().split("	")
            msg.append(line_msg)
    for m in msg:
        # 实体类型
        if m[0][0:1] is 'T':
            print("entity" + m[0][1:])
        # 关系类型
        elif m[0][0:1] is 'R':
            print("relation" + m[0][1:])
        # 特殊*号
        else:
            print("special")

def get_file_names(path):
    names = os.listdir(path)

    def file_filter(f):
        if f[-4:] == '.txt':
            return True
        else:
            return False

    return list(filter(file_filter, names))



if __name__ == '__main__':
    # integrate_data_txt("5", "../raw_data/SanWen/Training/", "../processed_data/SanWen/Training/")
    # files = get_file_names("../raw_data/SanWen/Testing/")
    # for file_path in files:
    #     integrate_data_txt(file_path, "../raw_data/SanWen/Testing/", "../processed_data/SanWen/Testing/")
    open_ann("../raw_data/SanWen/Training/0.ann")
