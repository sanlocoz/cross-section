# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 11:43:54 2021

@author: user
"""
import numpy as np
import pandas as pd
import os
import sys

print("Loading... ")

#work_dir = os.path.dirname(sys.executable)
work_dir = os.getcwd()
input_dir = os.path.join(work_dir,'input')
output_dir= os.path.join(work_dir,'output_preprocessing')
FileNames = os.listdir(input_dir)

delsep=';'

os.chdir(input_dir)

DataFrames = []
for f in FileNames: 
    DataFrames.append(pd.read_csv(f, delimiter=(delsep)))

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
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
        for k in range(len(bol)):
            if(bol[k]):
                ans.append(DataFrames[i].iloc[k])
        ret=pd.DataFrame(ans)
        ret.to_csv(FileNames[i]+"_"+str(j)+".csv",index=False,sep=delsep)

os.chdir(work_dir)
print("Completed!")       