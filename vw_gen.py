#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import jieba

def clean(s):
    s = s.replace('？', '?')
    s = s.replace('！', '')
    s = s.replace('。', '')
    s = s.replace('，', '')
    s = s.replace('；', '')
    s = s.replace('：', '')
    s = s.replace('“', '')
    s = s.replace('”', '')
    s = s.replace('‘', '')
    s = s.replace('’', '')
    s = s.replace('、', '')
    s = s.replace('', '')
    return s

f = open('items.json')
o = open('questions.vw', 'w')
quest_dict = json.load(f)
for q in quest_dict:
    q = clean(q['question'].encode('utf8'))
    v_q = list(jieba.cut(q))
    s = '| ' + ' '.join(v_q) + '\n'
    o.write(s.encode('utf8'))
f.close()
o.close()
