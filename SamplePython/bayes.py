'''
Created on Dec 5, 2012

@author: dwaijam
'''
from numpy import *
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute','I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how','to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1] #1 is abusive, 0 not
    return postingList,classVec

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = zeros(len(vocabList))
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def bagOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def trainNB0(trainMatrix, trainCategory):
    numDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Den = 2.0
    p1Den = 2.0
    for i in range(numDocs):
        if trainCategory[i] == 0:
            p0Num += trainMatrix[i]
            p0Den += sum(trainMatrix[i])
        else:
            p1Num += trainMatrix[i]
            p1Den += sum(trainMatrix[i])
            
     
    p0Vect = log(p0Num/p0Den) #change to log()
    p1Vect = log(p1Num/p1Den)
    
    return p0Vect, p1Vect, pAbusive


listOPosts,listClasses = loadDataSet()
vocabList = createVocabList(listOPosts)
trainMatrix = []
for post in listOPosts:
    trainMatrix.append(setOfWords2Vec(vocabList, post))

p0, p1 , pAb = trainNB0(trainMatrix, listClasses)
print vocabList
print p0
print p1
print pAb
print len(vocabList)

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0
      

def textParse(bigString):
    import re
    wordList = re.split(r'\W*', bigString)
    return [tok.lower() for tok in wordList if len(tok) > 2]

def spam():
    docList = []
    classList = []
    fullText = []
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainSet = range(50)
    testSet = []
    trainMat = []
    trainClasses = []
    for i in range(10):
        rand = int(random.uniform(0, len(trainSet)))
        testSet.append(trainSet[rand])
        del(trainSet[rand])
    for i in trainSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[i])) 
        trainClasses.append(classList[i])  
    p0, p1, pSpam = trainNB0(trainMat, trainClasses)
    errorCount = 0
    for i in testSet:
         thisDoc = setOfWords2Vec(vocabList, docList[i])
         if(classifyNB(thisDoc, p0, p1, pSpam) != classList[i]):
             errorCount += 1 
    print 'the error rate is: ',float(errorCount)/len(testSet)   
    return errorCount
    
def repeat(count):
    sum = 0.0
    for i in range(count):
        sum += spam()
    print 'the error rate is: ',float(sum)/(10*count)
      
repeat(10)            
               
        
