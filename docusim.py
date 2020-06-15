import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import math

def twoCharGram(dataset):
    with open(dataset, 'r') as data:
        textFile = data.read().replace('\n', ' ')
        kGrams = set()
        # 2-Char gram
        for i in range(len(textFile)-1):
            if textFile[i] + textFile[i+1] not in kGrams:
                kGrams.add(textFile[i] + textFile[i+1])
    return kGrams

def threeCharGram(dataset):
    with open(dataset, 'r') as data:
        textFile = data.read().replace('\n', ' ')
        kGrams = set()
        # 3-Char gram
        for i in range(len(textFile)-2):
            if textFile[i] + textFile[i+1] + textFile[i+2] not in kGrams:
                kGrams.add(textFile[i] + textFile[i+1] + textFile[i+2])
    return kGrams

def twoWordGram(dataset):
    with open(dataset, 'r') as data:
        tokens = str.split(data.read().replace('\n', ' '))
        kGrams = set()
        #2-word gram
        for i in range(len(tokens)-1):
            if tokens[i] + ' ' + tokens[i+1] not in kGrams:
                kGrams.add(tokens[i] + ' ' + tokens[i+1])
    return kGrams

for dataset in ['save0','save1','save2','save3']:
    print(dataset + ' two char gram size: %d' % len(twoCharGram('tosave/'+dataset)))

for dataset in ['save0','save1','save2','save3']:
    print(dataset + ' three char gram size: %d' % len(threeCharGram('tosave/'+dataset)))

for dataset in ['save0','save1','save2','save3']:
    print(dataset + ' two word gram size: %d' % len(twoWordGram('tosave/'+dataset)))

def jaccard(d1,d2,d3,d4, message):
    print('save0\'s '+ message +' similarity with save1 is: %.6f percent' % (100.* len(D1set.intersection(D2set))/ len(D1set.union(D2set))))
    print('save0\'s '+ message +' similarity with save2 is: %.6f percent' % (100.* len(D1set.intersection(D3set))/ len(D1set.union(D3set))))
    print('save0\'s '+ message +' similarity with save3 is: %.6f percent' % (100.* len(D1set.intersection(D4set))/ len(D1set.union(D4set))))
    print('save1\'s '+ message +' similarity with save2 is: %.6f percent' % (100.* len(D2set.intersection(D3set))/ len(D2set.union(D3set))))
    print('save1\'s '+ message +' similarity with save3 is: %.6f percent' % (100.* len(D2set.intersection(D4set))/ len(D2set.union(D4set))))
    print('save2t\'s '+ message +' similarity with save3 is: %.6f percent' % (100.* len(D3set.intersection(D4set))/ len(D3set.union(D4set))))
D1set = twoCharGram('tosave/save0')
D2set = twoCharGram('tosave/save1')
D3set = twoCharGram('tosave/save2')
D4set = twoCharGram('tosave/save3')
jaccard(D1set,D2set,D3set,D4set, 'two char gram')
D1set = threeCharGram('tosave/save0')
D2set = threeCharGram('tosave/save1')
D3set = threeCharGram('tosave/save2')
D4set = threeCharGram('tosave/save3')
jaccard(D1set,D2set,D3set,D4set, 'two char gram')
D1set = twoWordGram('tosave/save0')
D2set = twoWordGram('tosave/save1')
D3set = twoWordGram('tosave/save2')
D4set = twoWordGram('tosave/save3')
jaccard(D1set,D2set,D3set,D4set, 'two char gram')
D1Gram = threeCharGram('tosave/save0')
D2Gram = threeCharGram('tosave/save1')
DTotal = list(D1Gram.union(D2Gram))
for k in [20,60,150,300,600]:
    successCounter = 0
    for t in range (k):
        #minNum = [math.inf, math.inf]
        minNum = [float('inf'), float('inf')]
        for i in range (len(DTotal)):
            current = hash(str(t)+DTotal[i]+str(t)) % 10000
            if DTotal[i] in D1Gram: # this is how we'll emulate the vector representation of this D1
                if (current < minNum[0]):
                    minNum[0] = current
            if DTotal[i] in D2Gram: # this is how we'll emulate the vector representation of this D2
                if (current < minNum[1]):
                    minNum[1] = current
        if minNum[0] == minNum[1]:
            successCounter = successCounter+1
    print("with t = %d"%k, " we get a minhash similarity of ", successCounter/k)