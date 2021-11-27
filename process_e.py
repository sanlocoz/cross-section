# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 07:03:26 2021

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 11:43:54 2021

@author: user
"""
import numpy as np
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

eps=10**-5
    
print("Loading... ")

#work_dir = os.path.dirname(sys.executable)
work_dir = os.getcwd()
input_dir = os.path.join(work_dir,'output')
input_r_dir = os.path.join(work_dir,'input_rencana')
output_dir= os.path.join(work_dir,'output_preprocessing_eksisting')
FileNames = os.listdir(input_dir)
FileNames_r = os.listdir(input_r_dir)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
delsep=';'

os.chdir(input_dir)

DataFrames = []
for f in FileNames: 
    DataFrames.append(pd.read_csv(f, delimiter=(delsep)))
    
os.chdir(input_r_dir)
DataFrames_r = []
for f in FileNames_r: 
    DataFrames_r.append(pd.read_csv(f, delimiter=(delsep)))


os.chdir(output_dir)

for i in range (len(FileNames)):
    tmp=FileNames[i].split('.')[0]
    FileNames[i]=tmp
    
for i in range (len(DataFrames)):
    col=DataFrames[i].columns
    unique_STA=DataFrames[i].iloc[:,0].unique() #STA di kolom 0
    for j in range(len(unique_STA)):
        bol=DataFrames[i].iloc[:,0]==unique_STA[j]
        ans=[]

        del_x=0
        x=0
        tambah_kiri=False
        tambah_kanan=False
        cnt=0
        a=0
        
        if(DataFrames_r[0].iat[0,26]=='y'):
            kiri=DataFrames_r[i].iat[j,27]
            kanan=DataFrames_r[i].iat[j,28]
        else:
            kiri=0
            kanan=0
        
        for k in range(len(bol)):
            if(bol[k] and kiri>eps and cnt==0):
                tambah_kiri=True
                ans.append(DataFrames[i].iloc[k])
                cnt+=1
                
            if(bol[k] and DataFrames[i].iat[k,1].lower()!="ma"):
                a=DataFrames[i].iloc[k]
                b=DataFrames[i].iloc[k]
                if(kiri>eps):
                    a.iat[4]+=kiri
                if(tambah_kiri and cnt==1):
                    a.iat[3]=kiri
                ans.append(a)
                cnt+=1
        
        if(kanan>eps):
            tambah_kanan=True
            b.iat[3]=kanan
            b.iat[4]+=kanan
            if(tambah_kiri):
                b.iat[4]+=kiri
            ans.append(b)
            cnt+=1
            
        ret=pd.DataFrame(ans)
        ret.to_csv(FileNames[i]+"_"+str(j)+".csv",index=False,sep=delsep)

os.chdir(work_dir)

print("Completed!")       