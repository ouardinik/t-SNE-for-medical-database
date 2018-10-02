import numpy as Math

#Please change directory
directory="C:/Users/Amine Abouseir/Desktop/Projet S7/Codes"

#Load DB file
file=open(directory+"/DB/Feats.csv")
line=file.readline()
line=file.readline()

d_fea,d_pat={},{},{}
i_fea,i_pat=2,0

d_fea["ATT"]=0
d_fea["AGE"]=1


while(line!=""):
    list=line.split(";")
    
    if(list[0][:7] not in d_pat):
        pat_set=set()
        pat_set.add(list[0])
        d_pat[list[0][:7]]=[i_pat,pat_set]
        i_pat+=1
    else:
        d_pat[list[0][:7]][1].add(list[0])
        
    if(list[-1][:-2] not in d_fea):
        d_fea[list[-1][:-2]]=i_fea
        i_fea+=1
        
    line=file.readline();
file.close()

X=[[0 for i in range(len(d_fea)+2)] for j in range(len(d_pat)+1)]

inv_d_fea = {v: k for k, v in d_fea.items()}

inv_d_pat = {v[0]: k for k, v in d_pat.items()}

for i in range(len(d_pat)):
    X[i+1][0]=inv_d_pat[i]

for j in range(len(d_fea)):
    X[0][j+1]=inv_d_fea[j]

X[0][0]="PAT"

file=open(directory+"/DB/Feats.csv")
line=file.readline();
line=file.readline();

while(line!=""):
    list=line.split(";")
    i=d_pat[list[0][:7]][0]+1
    j=d_fea[list[-1][:-2]]+1
    n_i=len(d_pat[list[0][:7]][1])
    X[i][j]+=float(list[-2])/n_i
    X[i][1]=list[1]
    X[i][2]=float(list[2])
    line=file.readline()
file.close()

Math.savetxt(directory+"/one test per subject/Feats Formatted.csv", Math.array(X) , delimiter=',', fmt="%s")