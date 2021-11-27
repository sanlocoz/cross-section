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
    
print("Loading... ")

#work_dir = os.path.dirname(sys.executable)
work_dir = os.getcwd()
input_dir = os.path.join(work_dir,'input_rencana')
output_dir= os.path.join(work_dir,'output_preprocessing_rencana')
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
    for j in range(len(DataFrames[i])):
        ans=np.zeros([24,2])
        ans[0][0]=0
        ans[1][0]=0
        ans[1][0]=DataFrames[i].iat[j,2]*DataFrames[i].iat[j,4]
        ans[1][1]=DataFrames[i].iat[j,4]
        ans[2][0]=ans[1][0]+DataFrames[i].iat[j,3]
        ans[2][1]=DataFrames[i].iat[j,4]
        ans[3][0]=ans[2][0]+DataFrames[i].iat[j,4]*DataFrames[i].iat[j,5]
        ans[3][1]=0
        ans[4][0]=ans[3][0]+DataFrames[i].iat[j,6]
        ans[4][1]=0
        ans[5][0]=ans[4][0]+DataFrames[i].iat[j,8]*DataFrames[i].iat[j,10]
        ans[5][1]=-DataFrames[i].iat[j,10]
        ans[6][0]=ans[5][0]+DataFrames[i].iat[j,9]
        ans[6][1]=-DataFrames[i].iat[j,10]
        ans[7][0]=ans[6][0]+DataFrames[i].iat[j,10]*DataFrames[i].iat[j,11]
        ans[7][1]=0
        ans[8][0]=ans[7][0]+DataFrames[i].iat[j,13]
        ans[8][1]=0
        ans[9][0]=ans[8][0]+DataFrames[i].iat[j,14]*DataFrames[i].iat[j,16]
        ans[9][1]=DataFrames[i].iat[j,16]
        ans[10][0]=ans[9][0]+DataFrames[i].iat[j,15]
        ans[10][1]=DataFrames[i].iat[j,16]
        ans[11][0]=ans[10][0]+DataFrames[i].iat[j,16]*DataFrames[i].iat[j,17]
        ans[11][1]=0
        
        ans[13]=ans[1]
        ans[14]=ans[2]
        ans[17]=ans[5]
        ans[18]=ans[6]
        ans[21]=ans[9]
        ans[22]=ans[10]
        
        ans[12]=ans[13]
        ans[12][0]-=DataFrames[i].iat[j,20]*DataFrames[i].iat[j,2]
        ans[12][1]-=DataFrames[i].iat[j,20]
        
        ans[15]=ans[14]
        ans[15][0]+=DataFrames[i].iat[j,20]*DataFrames[i].iat[j,5]
        ans[15][1]-=DataFrames[i].iat[j,20]
        
        ans[16]=ans[17]
        ans[16][0]-=DataFrames[i].iat[j,21]*DataFrames[i].iat[j,8]
        ans[16][1]+=DataFrames[i].iat[j,21]
        
        ans[19]=ans[18]
        ans[19][0]+=DataFrames[i].iat[j,21]*DataFrames[i].iat[j,11]
        ans[19][1]+=DataFrames[i].iat[j,21]
        
        ans[20]=ans[21]
        ans[20][0]-=DataFrames[i].iat[j,22]*DataFrames[i].iat[j,14]
        ans[20][1]-=DataFrames[i].iat[j,22]

        ans[23]=ans[22]
        ans[23][0]+=DataFrames[i].iat[j,22]*DataFrames[i].iat[j,17]
        ans[23][1]-=DataFrames[i].iat[j,22]
        #print(ans)
        koor_awal=np.array([ans[11][0],ans[11][1]])
        koor_awal/=2 #dijadikan as
        if DataFrames[i].iat[j,23].lower()=="ki":
            koor_awal[1]=ans[1][1]
        elif DataFrames[i].iat[j,23].lower()=="ka":
            koor_awal[1]=ans[9][1]
        elif DataFrames[i].iat[j,23].lower()=="s":
            koor_awal[1]=ans[5][1]
        #print(koor_awal)
        #print(ans)
        ans=ans.transpose()
        
        if(DataFrames[i].iat[j,26]=='y'):
            ans[0]+=(DataFrames[i].iat[j,18]-koor_awal[0]+DataFrames[i].iat[j,27])
        else:
            ans[0]+=(DataFrames[i].iat[j,18]-koor_awal[0])
            
        ans[1]+=(DataFrames[i].iat[j,19]-koor_awal[1])
        
        #plt.figure()
        #plt.plot(ans[0],ans[1])
        
        ans=ans.transpose()
        sta=np.array([DataFrames[i].iat[j,0]]*len(ans)).reshape(len(ans),1)
        ans=np.concatenate((sta,ans), axis=1)
        col=['sta','x','z']
        ret=pd.DataFrame(ans,columns=col)
        #print(ans)
        tmp=FileNames[i].split('_')[0]
        ret.to_csv(tmp+"_"+str(j)+".csv",index=False,sep=delsep)
        #print(DataFrames[i].iloc[j])
        #ret.to_csv(FileNames[i]+"_"+str(j)+".csv",index=False,sep=delsep)

os.chdir(work_dir)
print("Completed!")