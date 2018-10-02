#Create a csv file containing the average of the variance of each feature for every normal subject

import numpy as Math

#Please change directory
directory="C:/Users/Amine Abouseir/Desktop/Codes"

#Load features matrix and labels, Make sure to change the directory of the files
X = Math.loadtxt(directory+"/DB/Feats_X.txt")
labels_att = Math.loadtxt(directory+"/DB/labels_att.txt")
labels_pat = Math.loadtxt(directory+"/DB/labels_pat.txt")

#Standardize the features matrix
(n,d)=X.shape
espX=Math.sum(X,0)/n
X=X-espX
varX=Math.sum(Math.square(X),0)/n
X=X/Math.sqrt(varX)

def varZ(X,L):
    (n,d)=X.shape
    m=len(L)
    I=Math.zeros((m,n))
    for i in range(m):
        I[i][L[i]]=1
    Z=Math.dot(I,X)
    espZ=Math.sum(Z,0)/m
    Z=Z-espZ
    return Math.sum(Math.square(Z),0)/m

V=Math.zeros(106)
L=[]
N=0
M=0
j=-1

for i in range(n):
    if int(labels_att[i])==1:
        if j==-1:
            L=[i]
            N=1
            M+=1
            j=int(labels_pat[i])
        elif int(labels_pat[i])!=j:
            V+=varZ(X,L)
            L=[i]
            N=1
            M+=1
            j=int(labels_pat[i])
        else:
            L+=[i]
            N+=1

if int(labels_att[n-1])==1:
    V+=varZ(X,L)/N

#Write the variance list
V=V/M
Math.savetxt(directory+"/Files/moy_var.csv", V , delimiter=',', fmt="%s")