#Create csv files for every feature and every subjects' category that can be used with SPSS

import numpy as Math
import random

#Please change diractory
directory="C:/Users/Amine Abouseir/Desktop/Projet S7/Codes"

#Load features matrix and labels, Make sure to change the directory of the files
X = Math.loadtxt(directory+"/DB/Feats_X.txt")
labels_att = Math.loadtxt(directory+"/DB/labels_att.txt")
labels_pat = Math.loadtxt(directory+"/DB/labels_pat.txt")

#Select the number of test per subject for ICC
numb_tests=4

d=[[] for i in range(10)]
j=-1
(n,_)=X.shape
M=['LER','T','ArtH','NEUP','LCA','PAR','CER','ArtG','Genou','SC']
L=[]

for i in range(n):
    if int(labels_pat[i])==j:
        L+=[i]
    else:
        if len(L)>3:
            maladie=int(labels_att[i-1])
            d[maladie].append(L)
        j=int(labels_pat[i])
        L=[i]
        
if len(L)>3:
    maladie=int(labels_att[i-1])
    d[maladie].append(L)
        
for maladie in range(10):
    if len(d[maladie])>0:
        Y=Math.zeros((len(d[maladie]),numb_tests))
        for feature in range(106):
            i=0
            for subject in d[maladie]:
                L=random.sample(subject,numb_tests)
                for j in range(4):
                    Y[i][j]=X[L[j]][feature]
                i+=1
            Math.savetxt(directory+"/Files/SPSS/"+str(M[maladie])+'_feature_'+str(feature)+'.csv', Y , delimiter=',', fmt="%s")