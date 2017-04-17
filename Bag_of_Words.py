
# coding: utf-8

# In[4]:

import os
import nltk


print("Generating word bag...")
stopwords=['、','（','）','，','。','：','“','”','\n\u3000','\u3000','的','‘','’','　','.','\n','\\n','.\n'] #stop words

text=open('/Users/zhongjing/Downloads/training.txt','r').read()
count = 0
wb = []
fredist_list = []
finalstring = ''
for i in text.split('\n'):
    featuresstring = ''
    if count <= 3995:
        featuresstring+='1 '
    else:
        featuresstring+='0 '
    index=1 #word bag index
    count += 1
    wordbag={} #word bag
    fredist=nltk.FreqDist(i.replace('1\t','').replace('0\t','').replace('!', ' ').replace('.', ' ').replace(',', ' ').split(' ')) #单文件词频
    for localkey in fredist.keys(): #get distinct words
        if localkey in stopwords: #see if the word is stop word
            continue
        if localkey in wordbag.keys(): #see if the word already exist in the word bag
            continue
        else:
            wordbag[index]=localkey
            index=index+1
            
    wb.append(sorted(wordbag.items()))
    
    newtextstring='' 
    wordsfromtext=i.split(' ')
    for w in wordsfromtext:
        for item in wordbag.items():
            if item[1]==w and item[0]!='':
                newtextstring+=str(item[0])+' '

    fredist=nltk.FreqDist(newtextstring.split(' ')) #frequency of a single word
    fredist.pop(('')) #delete useless items
    
    temp=[]
    for i in fredist.items():
        temp.append([int(i[0]),int(i[1])])
    fredist=dict(temp)
    fredist_list.append(fredist)
    
    for item in sorted(fredist.items()): 
        featuresstring+= str(item[0])+":"+str(item[1])+" "
    featuresstring+='\n'
    finalstring = finalstring + featuresstring
    
f=open('/Users/zhongjing/Downloads/training_libsvm.txt','w')
f.write(finalstring)
print("Success.")
print finalstring
print count


# In[ ]:



