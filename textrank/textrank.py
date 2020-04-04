from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords 
from collections import defaultdict 
from string import punctuation 
from heapq import nlargest
import math
from itertools import product, count
import nltk
import os
from tqdm import tqdm

nltk.download('stopwords')
nltk.download('punkt')
stopwords = set(stopwords.words('english') + list(punctuation))

def calculate_similarity(sen1, sen2):
    counter = 0
    for word in sen1:
       if word in sen2:
           counter += 1
    return counter / (math.log(len(sen1)) + math.log(len(sen2)))


def create_graph(word_sent):
    num = len(word_sent)
    board = [[0.0 for _ in range(num)] for _ in range(num)]

    for i, j in product(range(num), repeat=2):
       if i != j:
           board[i][j] = calculate_similarity(word_sent[i], word_sent[j])
    return board


def weighted_pagerank(weight_graph):
    scores = [0.5 for _ in range(len(weight_graph))]
    old_scores = [0.0 for _ in range(len(weight_graph))]

    while different(scores, old_scores):
       for i in range(len(weight_graph)):
           old_scores[i] = scores[i]

       for i in range(len(weight_graph)):
           scores[i] = calculate_score(weight_graph, scores, i)
    return scores


def different(scores, old_scores):
    flag = False
    for i in range(len(scores)):
       if math.fabs(scores[i] - old_scores[i]) >= 0.0001:
           flag = True
           break
    return flag


def calculate_score(weight_graph, scores, i):
    length = len(weight_graph)
    d = 0.85
    added_score = 0.0


    for j in range(length):
       fraction = 0.0
       denominator = 0.0
       fraction = weight_graph[j][i] * scores[j]
       for k in range(length):
           denominator += weight_graph[j][k]
       added_score += fraction / denominator
    weighted_score = (1 - d) + d * added_score

    return weighted_score


def Summarize(text,n):
    sents = sent_tokenize(text)
    word_sent = [word_tokenize(s.lower()) for s in sents]

    for i in range(len(word_sent)):
       for word in word_sent[i]:
           if word in stopwords:
               word_sent[i].remove(word)
    similarity_graph = create_graph(word_sent)
    scores = weighted_pagerank(similarity_graph)
    sent_selected = nlargest(n, zip(scores, count()))
    sent_index = []
    for i in range(n):
      sent_index.append(sent_selected[i][1])
    return [sents[i] for i in sent_index]


if __name__ == '__main__':
    text_file_path = [n for n in os.listdir() if n.find('.txt') != -1]
    for text_path in tqdm(text_file_path):
    	with open(text_path,'r',encoding='UTF-8') as file:
    		df = file.readlines()

    	with open(text_path[:-4]+'_rank.txt','w',encoding='UTF-8') as file:

    		for num,content in enumerate(df):
    			if not num == 0:
    				file.write(50*'-' + '\n')

    			content = content.replace('\n','')
    			try:
    				result = '.'.join(Summarize(content,2))
    			except:
    				result = content
    			file.write(result + '\n')