#  -*- coding = utf-8 -*-
#  @time: 2023/11/30 15:01
#  Author: yyzhang
#  @file: duie_data_processor.py
#  将raw_data加工成为训练用数据


import json

from tokenization import BasicTokenizer
from transformers import BertTokenizer

basicTokenizer = BasicTokenizer(do_lower_case=False)
bertTokenizer = BertTokenizer.from_pretrained('../pre_trained_bert')


def process(in_path, out_path):
    res = []
    with open(in_path, 'r', encoding='utf8') as fp:
        data = fp.readlines()
        total = len(data)
        for i,d in enumerate(data):
            print(i+1, total)
            d = eval(d)
            tmp = {}
            text = d['text']
            tmp_text = basicTokenizer.tokenize(text)
            if len(tmp_text) > 100:
                continue
            spo_list = d['spo_list']
            tmp['text'] = text
            tmp['triple_list'] = []
            for spo in spo_list:
                rel = spo['predicate']
                subject = spo['subject']
                object = spo['object']['@value']
                subject_type = spo['subject_type']
                object_type = spo['object_type']['@value']
                if subject in text[:100] and object in text[:100]:
                    tmp['triple_list'].append([subject, rel, object, subject_type, object_type])
            if tmp['triple_list']:
                res.append(tmp)
    with open(out_path, 'w', encoding='utf8') as fp:
        json.dump(res, fp, ensure_ascii=False)

def get_rels(out_path):
    schema_path = '../raw_data/DUIE/duie_schema.json'
    def get_rel(path):
        res = []
        with open(path, 'r', encoding='utf8') as fp:
            data = fp.readlines()
            for d in data:
                d = eval(d)
                predicate = d['predicate']
                if predicate not in res:
                    res.append(predicate)
        return res
    rels = get_rel(schema_path)
    rels = list(set(rels))
    rel2id = {}
    id2rel = {}
    for i, rel in enumerate(rels):
        rel2id[rel] = i
        id2rel[str(i)] = rel
    with open(out_path, 'w', encoding='utf8') as fp:
        json.dump([id2rel, rel2id], fp, ensure_ascii=False)

def get_subject_type(out_path):
    schema_path = '../raw_data/DUIE/duie_schema.json'
    subject_type = []
    with open(schema_path, 'r', encoding='utf8') as fp:
        schema = fp.readlines()
        for s in schema:
            s = eval(s)
            subject = s['subject_type']
            if subject not in subject_type:
                subject_type.append(subject)
    subject_type = list(set(subject_type))
    subject2id = {}
    id2subject = {}
    for i, subject in enumerate(subject_type):
        subject2id[subject] = i
        id2subject[str(i)] = subject
    with open(out_path, 'w', encoding='utf8') as fp:
        json.dump([id2subject, subject2id], fp, ensure_ascii=False)


def get_object_type(out_path):
    schema_path = '../raw_data/DUIE/duie_schema.json'
    object_type = []
    with open(schema_path, 'r', encoding='utf8') as fp:
        schema = fp.readlines()
        for s in schema:
            s = eval(s)
            object = s['object_type']
            if object['@value'] not in object_type:
                object_type.append(object['@value'])
    object_type = list(set(object_type))
    object2id = {}
    id2object = {}
    for i, object in enumerate(object_type):
        object2id[object] = i
        id2object[str(i)] = object
    with open(out_path, 'w', encoding='utf8') as fp:
        json.dump([id2object, object2id], fp, ensure_ascii=False)


if __name__ == '__main__':
    process('../raw_data/DUIE/duie_sample.json', '../processed_data/DUIE/sample_triples.json')
    process('../raw_data/DUIE/duie_dev.json', '../processed_data/DUIE/dev_triples.json')
    process('../raw_data/DUIE/duie_train.json', '../processed_data/DUIE/train_triples.json')
    # get_rels('../processed_data/DUIE/rel2id.json')
    # get_subject_type('../processed_data/DUIE/subject_type.json')
    # get_object_type('../processed_data/DUIE/object_type.json')
