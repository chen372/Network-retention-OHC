import json
import datetime
import numpy as np
import pandas as pd
from collections import Counter
#import matplotlib.pyplot as plt
import networkx as nx
import csv
import random
import nltk
import gensim

# load json file
data = {}
for i in range(546, 0, -1):
    with open('/u/chen372/breast_data/breast_data'+str(i)+'.txt') as json_file:         
        dat = json.load(json_file)
        data.update(dat)

#extract all features, including texts
post_time = []
text = []
post_type = []
post_type_c = []
user = []
for key in data:
    post_time.append(data[key]['post_time'])
    text.append(data[key]['text'])
    post_type_c.append('initial')
    post_type.append(1)
    user.append(data[key]['user'])
    
    i = 0
    while i < 50:
        try:
            post_time.append(data[key]['reply'][i]['post_time'])
            text.append(data[key]['reply'][i]['text'])
            user.append(data[key]['reply'][i]['user'])
            if data[key]['user'] == data[key]['reply'][i]['user']:  #identify self reply
                post_type_c.append('self_reply')
                post_type.append(3)
            else:
                post_type_c.append('reply')
                post_type.append(2)
        except:
            pass
        i += 1


# remove punctuation
text2 = []
punc = ['<br/>\\n', '</p>\\n</div>', '</p>\\n<p>', '\\xa0'] 
for t in text:
    for c in punc:
        if c in t:
            t = t.replace(c, '')
    text2.append(t)

# lowercase, remove stopwords and punctuations
stopword_list = []
f = open('/u/chen372/stopwords_cancer.txt','r')
for line in f.readlines():
        stopword_list.append(line.strip())

stopwords = set(stopword_list)
#stopwords

# split text into bag of words
seg_list = []         # each element in the seg_list is a list of tokenized post
for t in text2:
    t = ''.join(c for c in t if c not in (',', '!', '?', '.', ':', '(', ')',';'))  # remove punc such as '?' in 'you?'
    words = []
    for w in t.split():       
        if w.lower() not in stopwords:
            words.append(w.lower())
    seg_list.append(words)  

#len(seg_list)
#seg_list[0]  

	
# Use topic modeling
#pip install -U gensim
from gensim import corpora, models
dictionary = corpora.Dictionary(seg_list)
corpus = [dictionary.doc2bow(post) for post in seg_list]
corpus[0]

import gensim
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=20, id2word = dictionary, passes=20)
#ldamodel.print_topics(num_topics=10, num_words=20)