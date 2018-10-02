import numpy as np

#Please change directory
directory="C:/Users/Amine Abouseir/Desktop/Projet S7/Codes"

#Load DB file
file=open(directory+"/DB/Feats.csv")
line=file.readline()
line=file.readline()

d_fea,d_mea,d_att,d_pat={},{},{},{}
d_fea["age"]=0
i_fea,i_mea,i_att,i_pat=1,0,0,0

while(line!=""):
    list=line.split(";")
    
    if(list[0][:7] not in d_pat):
        pat_set=set()
        pat_set.add(list[0])
        d_pat[list[0][:7]]=[i_pat,pat_set]
        i_pat+=1
    else:
        d_pat[list[0][:7]][1].add(list[0])
        
    if(list[1] not in d_mea):
        d_mea[list[1]]=i_mea
        i_mea+=1
        
    if(list[-1][:-2] not in d_fea):
        d_fea[list[-1][:-2]]=i_fea
        i_fea+=1
        
    line=file.readline();
file.close()

X=np.zeros((len(d_pat),len(d_fea)))
M_att=np.zeros(len(d_pat))

file=open(directory+"/DB/Feats.csv")
line=file.readline()
line=file.readline()

while(line!=""):
    list=line.split(";")
    i=d_pat[list[0][:7]][0]
    n_i=len(d_pat[list[0][:7]][1])
    j=d_fea[list[-1][:-2]]
    X[i][j]+=float(list[-2])/n_i
    M_att[i]=d_mea[list[1]]
    X[i][0]=float(list[2])
    line=file.readline()
file.close()


np.savetxt(directory+"/one test per subject/Feats_X.txt", X)
np.savetxt(directory+"/one test per subject/labels_att.txt", M_att)