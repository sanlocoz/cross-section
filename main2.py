# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 00:47:39 2021

@author: user
"""

import numpy as np
import pandas as pd
import process_r
import process_e
import os
import natsort
import matplotlib.pyplot as plt
from sklearn import linear_model

def interpolation (x_1,y_1,x_2,y_2,x_target):
    reg=linear_model.LinearRegression()
    X=np.array([[x_1],[x_2]])
    Y=np.array([y_1,y_2])
    reg.fit(X,Y)
    X_pred=np.array([[x_target]])
    y_target = reg.predict(X_pred)
    return y_target
    
def galtim (rencana, eksisting, pias, saveplt, save):
    plt.figure()
    plt.plot(rencana[0],rencana[1])
    plt.plot(eksisting[0],eksisting[1])
    
    x_mulai=rencana[0].min()
    x_akhir=rencana[0].max()
    x_iter=np.linspace(x_mulai,x_akhir,pias)
    galian=0
    timbunan=0
    
    r_iter=0
    e_iter=0
    
    y_now_rencana=rencana[1][0]
    y_now_eksisting=eksisting[1][0]
    y_next_rencana=0
    y_next_eksisting=0
    
    for i in range(1,pias):
        x_now=x_iter[i-1]
        x_next=x_iter[i]
        
        delta_x=(x_next-x_now)
        
        while(rencana[0][r_iter]<x_next):
            r_iter+=1
            
        while(eksisting[0][e_iter]<x_next):
            e_iter+=1
            
        y_next_rencana=interpolation(rencana[0][r_iter],rencana[1][r_iter],rencana[0][r_iter-1],rencana[1][r_iter-1],x_next)
        y_next_eksisting=interpolation(eksisting[0][e_iter],eksisting[1][e_iter],eksisting[0][e_iter-1],eksisting[1][e_iter-1],x_next)
        
        #print(x_now,x_next,y_now_eksisting,y_now_rencana,y_next_eksisting,y_next_rencana)
        x_plot=np.array([x_now,x_now])
        y_plot=np.array([y_now_eksisting,y_now_rencana])
        
        if(y_now_rencana<=y_now_eksisting):#Galian
            galian+=abs(delta_x/2*((y_now_eksisting-y_now_rencana)+(y_next_eksisting-y_next_rencana)))
            plt.plot(x_plot,y_plot,color='r')
        else:
            timbunan+=abs(delta_x/2*((y_now_eksisting-y_now_rencana)+(y_next_eksisting-y_next_rencana)))
            plt.plot(x_plot,y_plot,color='b')
            
        y_now_rencana=y_next_rencana
        y_now_eksisting=y_next_eksisting
        
    ans=np.array([galian,timbunan])
    if(save):
        plt.savefig(saveplt,dpi=50)
        plt.close('all')

    return ans
        
print("Loading... ")

work_dir = os.getcwd()
input_eksisting = os.path.join(work_dir,'output_preprocessing_eksisting')#filename [input].csv
input_rencana = os.path.join(work_dir,'output_preprocessing_rencana')#filename [input].csv
input_dir = os.path.join(work_dir,'input_rencana')

output_galtim= os.path.join(work_dir,'output_galtim')
output_tabel= os.path.join(work_dir,'output_tabel')

if not os.path.exists(output_galtim):
    os.makedirs(output_galtim)
    
if not os.path.exists(output_tabel):
    os.makedirs(output_tabel)
    
process_r
process_e

pias=250#maksimum 10000

FileNames = natsort.natsorted(os.listdir(input_dir))
FileNames_e = natsort.natsorted(os.listdir(input_eksisting))
FileNames_r = natsort.natsorted(os.listdir(input_rencana))


delsep=';'

DataFrames = []
DataFrames_e = []
DataFrames_r = []

os.chdir(input_dir)

for f in FileNames: 
    DataFrames.append(pd.read_csv(f, delimiter=(delsep)))
    
os.chdir(input_eksisting)

for f in FileNames_e: 
    DataFrames_e.append(pd.read_csv(f, delimiter=(delsep)))
    
os.chdir(input_rencana)

for f in FileNames_r: 
    DataFrames_r.append(pd.read_csv(f, delimiter=(delsep)))
    
for i in range (len(FileNames_e)):
    tmp=FileNames_e[i].split('.')[0]
    FileNames_e[i]=tmp
    
for i in range (len(FileNames_r)):
    tmp=FileNames_r[i].split('.')[0]
    FileNames_r[i]=tmp

nama_prev=FileNames_r[0].split('_')[0]
ans_global=[]

os.chdir(output_tabel)

for i in range (len(DataFrames_r)):
    nama_curr=FileNames_r[i].split('_')[0]
    if(DataFrames[0].iat[i,24]=='s'):#saluran
        rencana=np.array([DataFrames_r[i].iloc[16:20,1],DataFrames_r[i].iloc[16:20,2]])
        
    if(DataFrames[0].iat[i,24]=='ki'):#tanggul kiri
        rencana=np.array([DataFrames_r[i].iloc[12:16,1],DataFrames_r[i].iloc[12:16,2]])
        
    if(DataFrames[0].iat[i,24]=='ka'):#tanggul kanan
        rencana=np.array([DataFrames_r[i].iloc[20:24,1],DataFrames_r[i].iloc[20:24,2]])
        
    eksisting=np.array([DataFrames_e[i].iloc[:,4],DataFrames_e[i].iloc[:,2]])
    x_awal=min(rencana[0][0],eksisting[0][0])
    z_awal=eksisting[1][0]
    
    x_akhir=max(rencana[0][len(rencana[0])-1],eksisting[0][len(eksisting[0])-1])
    z_akhir=eksisting[1][len(eksisting[0])-1]
    
    k_awal=np.array([x_awal,z_awal]).reshape(2,1)
    k_akhir=np.array([x_akhir,z_akhir]).reshape(2,1)
    
    eksisting=np.concatenate((k_awal,eksisting,k_akhir),axis=1)
    
    saveplt=os.path.join(output_galtim,FileNames_e[i].split('_')[0]+" "+DataFrames_r[i].iat[0,0]+".png")
    
    if(i%10==0):
        gt=galtim(rencana,eksisting,pias,saveplt,True)
    else:
        gt=galtim(rencana,eksisting,pias,saveplt,False)
    
    ans=np.array([DataFrames_r[i].iat[0,0],np.float64(gt[0]),np.float64(gt[1])]).reshape(1,3)
    
    if(nama_curr==nama_prev):
        if(i==0):
            ans_global=ans
        else:
            ans_global=np.concatenate((ans_global,ans))
            
    if (nama_curr!=nama_prev or i==len(DataFrames_r)-1): #save file
        col=['sta','galian','timbunan']
        ret=pd.DataFrame(ans_global,columns=col)
        ret.to_csv(nama_prev+"_galtim.csv",index=False,sep=delsep)
        
    if(nama_curr!=nama_prev):
        ans_global=[]
        ans_global=np.concatenate((ans_global,ans))
        
    nama_prev=nama_curr
print("Completed!")


