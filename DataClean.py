#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 16:41:42 2018

@author: lee
"""
no_remove = [chr(i) for i in range(ord('a'), ord('z')+1)]+['-']+[' ']
token_count = {}

train = open("training.txt", "r")
tmp_out = open("step1tmp.txt", "w")

for line in train:
    tmp = line.split('\t')
    # lowercase and remove noisy characters
    s = tmp[1].lower()
    ss = ''
    for t in s:
        if t in no_remove:
            ss = ss+t
    #count tokens
    title = ss.split(' ')        
    for t in title:
        if t in token_count:
            token_count[t] += 1
        else:
            token_count[t] = 1
    tmp[1] = ss
    out = "\t".join(tmp)
    tmp_out.write(out)

train.close()
tmp_out.close()

tmp_in = open("step1tmp.txt", "r")
final_out = open("cleaned_data.txt", "w")

for line in tmp_in:
    tmp = line.split('\t')
    ss = tmp[1].split(' ')
    clean_title = []
    for t in ss:
        if token_count[t]>=5:
            clean_title.append(t)
    tmp[1] = ' '.join(clean_title)
    out = "\t".join(tmp)
    final_out.write(out)
    
tmp_in.close()
final_out.close()
            