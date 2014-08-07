#!/usr/bin/python2.7
#@Author: Aadesh Neupane
#Version: 0.0.1
##Program that implements Bayes Rule for spam filtering
import re
import math

#Simple Naive Bayes implementation for spam filtering
class BuildBayesModel():
    #Variable defination for bayes model
    def __init__(self,llist):
        self.totalData=0
        self.cat1Data=0
        self.cat2Data=0
        self.data={}
        self.wordsCat={}
        self.llist=llist
        self.totalCntCat={}
        self.wordCnt={}
        self.dicto={}
    #Determine the number of category
    def countCat(self,cat):
        return len(self.data[cat])
    #Determine the total number of words
    def countTotWords(self):
        for cat in self.data.keys():
            count=0
            for lline in self.data[cat]:
                count=count+len(lline)
            self.totalCntCat[cat]=count
        return self.totalCntCat
    #Count words in each category
    def countWord(self,word):
        for cat in self.data.keys():
            count=0
            for lline in self.data[cat]:
                if word in lline:
                    for lwords in lline:
                        self.dicto[lwords]=''
                        if word in lwords:
                            count=count+1
                else:
                    for lwords in lline:
                        self.dicto[lwords]=''
            self.wordCnt[cat]=count
        return self.wordCnt
    #Find the inverse category
    def invCat(self,cat):
        k=self.data.keys()
        if cat in k[0]:
            tac=k[1]
        else:
            tac=k[0]
        return tac
    #Find the prior probability of given category using Lapaceian smoothing
    def priporProbLS(self,cat1):
        tot=0
        k=1
        for cat in self.data.keys():
            tot=tot+self.countCat(cat)
        return (self.countCat(cat1)+k)/float(tot+k*len(self.data.keys()))
    #Find the prior probability of given category
    def priporProb(self,cat1):
        tot=0
        for cat in self.data.keys():
            tot=tot+self.countCat(cat)
        #print tot
        return self.countCat(cat1)/(float(tot))
    #Find the conditional probability of given category
    def mlProb(self,word,cat):
        wordcnt1=self.countWord(word)
        #print wordcnt1
        return wordcnt1[cat]/(float(self.totalCntCat[cat]))
    #Find the conditional probability of given category using lapaceian smoothing
    def lsProb(self,word,cat):
        k=1
        wordcntl=self.countWord(word)
        return (wordcntl[cat]+k)/float(self.totalCntCat[cat]+k*len(self.dicto.keys()))
    #Calculating probability using bayes rule
    def brule(self,cat,words):
        tpobnue=1.0
        tpobden=1.0
        for word in words:
            #print word
            tpobnue=tpobnue*self.lsProb(word,cat)
            tpobden=tpobden*self.lsProb(word,self.invCat(cat))
        calcnume=tpobnue*self.priporProbLS(cat)
        calcdeno=tpobden*self.priporProbLS(self.invCat(cat))
        #print calcdeno
        return calcnume/(calcnume+calcdeno)
    #Extract data given for training
    def extractInfo(self):
        for a in self.llist:
            elist=[]
            text,cat=a.split(':')
            text=text.split()
            if cat in self.data.keys():
                self.data[cat].append(text)
            else:
                self.data[cat]=elist
                self.data[cat].append(text)
        #print self.data
        
#Build list of messages for training
llist=["offer is secret :SPAM","click secret link :SPAM","secret sports link:SPAM","play sports today:HAM","went play sports:HAM","secret sports event:HAM","sports is today:HAM","sports costs money:HAM"]
b1=BuildBayesModel(llist)
b1.extractInfo()
b1.countTotWords()
mes='today is secret'
mes=mes.split()
print b1.brule("SPAM",mes)
