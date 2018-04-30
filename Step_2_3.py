#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 14:36:38 2018

@author: lee
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import f1_score, precision_score, recall_score

f = open("cleaned_training.txt", "r")
title_train = []
lb_train = []
for line in f:
    tmp = line.split('\t')
    title_train.append(tmp[1])
    lb_train.append(tmp[2])   
       
f.close()

X = CountVectorizer(tokenizer=lambda a: a.split(' '))
arr = X.fit_transform(title_train)

f = open("labels.txt","r")
tmp = f.readlines()
lb = [k.strip('\n') for k in tmp]
f.close()

Y = LabelEncoder()
Y.fit(lb)
brr = Y.transform(lb_train) 

clf = SGDClassifier()
clf.fit(arr, brr)

#crr = clf.predict(arr)
#f1_score(brr, crr, average = 'macro')
#f1_score(brr, crr, average = 'micro')

""" output for subset """
f = open("cleaned_subset.txt", "r")
f2 = open("text_features.txt", "w")

title = []
lb = []
for line in f:
    tmp = line.split('\t')
    feature = X.transform([tmp[1]]).toarray()[0].tolist()
    f2.write(','.join([str(k) for k in feature])+'\t'+str(Y.transform([tmp[2]])[0])+'\n')
f.close()
f2.close()

"""Validation Part"""
f_vali = open("cleaned_validation.txt", "r")
title_vali = []
lb_vali = []
for line in f_vali:
    tmp = line.split('\t')
    title_vali.append(tmp[1])
    lb_vali.append(tmp[2])   
f_vali.close()

x_vali = X.transform(title_vali)
pred_vali = clf.predict(x_vali)
y_vali = Y.transform(lb_vali)
f1_score(y_vali, pred_vali, average = 'macro')
f1_score(y_vali, pred_vali, average = 'micro')
precision_vali = precision_score(y_vali, pred_vali, average = None)
recall_vali = recall_score(y_vali, pred_vali, average = None)

order = set(y_vali)
order.update(set(pred_vali))
venue = list(Y.inverse_transform(list(order)))

f = open("precision_recall.txt", "w")
for i in range(len(venue)):
        f.write(venue[i]+'\t'+str(precision_vali[i])+'\t'+str(recall_vali[i])+'\n')
f.close()
"""Test Set"""

f_test = open("cleaned_test_set.txt", "r")
title_test = []
id_test = []
for line in f_test:
    tmp = line.split('\t')
    id_test.append(tmp[0])
    title_test.append(tmp[1])
f_test.close()

x_test = X.transform(title_test)
pred_test = clf.predict(x_test)

f = open("text_feature_predictions.txt", "w")
for i in range(len(pred_test)):
    f.write(id_test[i]+'\t'+str(pred_test[i])+'\n')
f.close()
