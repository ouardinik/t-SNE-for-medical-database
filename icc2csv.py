# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 17:36:43 2018
@author: oesteban
from:
https://github.com/nipy/nipype/blob/6239693dfabfa753b682b51be68f040748a05390/nipype/algorithms/icc.py#L27
based on NIPYPE: Neuroimaging in Python: Pipelines and Interfaces
"""
import numpy as np
from numpy import ones, kron, mean, eye, hstack, dot, tile
from scipy.linalg import pinv
import random

def ICC_rep_anova(Y):
    '''
    the data Y are entered as a 'table' ie subjects are in rows and repeated
    measures in columns
    One Sample Repeated measure ANOVA
    Y = XB + E with X = [FaTor / Subjects]
    '''

    [nb_subjects, nb_conditions] = Y.shape
    dfc = nb_conditions - 1
    dfe = (nb_subjects - 1) * dfc
    dfr = nb_subjects - 1

    # Compute the repeated measure effect
    # ------------------------------------

    # Sum Square Total
    mean_Y = mean(Y)
    SST = ((Y - mean_Y) ** 2).sum()

    # create the design matrix for the different levels
    x = kron(eye(nb_conditions), ones((nb_subjects, 1)))  # sessions
    x0 = tile(eye(nb_subjects), (nb_conditions, 1))  # subjects
    X = hstack([x, x0])

    # Sum Square Error
    predicted_Y = dot(dot(dot(X, pinv(dot(X.T, X))), X.T), Y.flatten('F'))
    residuals = Y.flatten('F') - predicted_Y
    SSE = (residuals ** 2).sum()

    residuals.shape = Y.shape

    MSE = SSE / dfe

    # Sum square session effect - between colums/sessions
    SSC = ((mean(Y, 0) - mean_Y) ** 2).sum() * nb_subjects
    MSC = SSC / dfc / nb_subjects

    session_effect_F = MSC / MSE

    # Sum Square subject effect - between rows/subjects
    SSR = SST - SSC - SSE
    MSR = SSR / dfr

    # ICC(3,1) = (mean square subjeT - mean square error) / (mean square subjeT + (k-1)*-mean square error)
    ICC = (MSR - MSE) / (MSR + dfc * MSE)

    e_var = MSE  # variance of error
    r_var = (MSR - MSE) / nb_conditions  # variance between subjects

    return ICC, r_var, e_var, session_effect_F, dfc, dfe
    
################################################################################

#Create a csv files cantaining icc value for every feature and every subjects' category

#Please change diractory
directory="C:/Users/Amine Abouseir/Desktop/Projet S7/Codes"

#Load features matrix and labels, Make sure to change the directory of the files
X = np.loadtxt(directory+"/DB/Feats_X.txt")
labels_att = np.loadtxt(directory+"/DB/labels_att.txt")
labels_pat = np.loadtxt(directory+"/DB/labels_pat.txt")

#Select the number of test per subject for ICC
numb_tests=4

d=[[] for i in range(10)]
j=-1
(n,_)=X.shape
M=['LER','T','ArtH','NEUP','LCA','PAR','CER','ArtG','Genou','SC']
L=[]
ICC_list=[["" for i in range(11)] for j in range(107)]

for i in range(n):
    if int(labels_pat[i])==j:
        L+=[i]
    else:
        if len(L)>=numb_tests:
            maladie=int(labels_att[i-1])
            d[maladie].append(L)
        j=int(labels_pat[i])
        L=[i]
        
if len(L)>=numb_tests:
    maladie=int(labels_att[i-1])
    d[maladie].append(L)
    
ICC_list[0]=[""]+M

file=open(directory+"/Files/Feats Formatted.csv")
line=file.readline()
list=line.split(",")
for i in range(1,107):
    ICC_list[i][0]=list[i+2]
        
for maladie in range(10):
    if len(d[maladie])>0:
        Y=np.zeros((len(d[maladie]),numb_tests))
        for feature in range(106):
            i=0
            for subject in d[maladie]:
                L=random.sample(subject,numb_tests)
                for j in range(numb_tests):
                    Y[i][j]=X[L[j]][feature]
                i+=1
            ICC_list[feature+1][maladie+1]=ICC_rep_anova(Y)[0]

np.savetxt(directory+"/Files/ICC.csv", np.array(ICC_list) , delimiter=',', fmt="%s")