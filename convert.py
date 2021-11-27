# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 10:28:52 2021

@author: user
"""

import numpy as np
import pandas as pd
import os
import sys
import natsort
import matplotlib.pyplot as plt
from sklearn import linear_model

eps=10**-5

def translatecoor (arr,base):
    return arr+base

def rotatecoor (arr,angle,base):
    rot_mat=np.array([[np.cos(np.radians(angle)),-np.sin(np.radians(angle))],[np.sin(np.radians(angle)),np.cos(np.radians(angle))]])
    arr2=translatecoor(arr,-base)
    hasil=np.matmul(rot_mat,arr2)
    return translatecoor(hasil,base)

print("Loading... ")

work_dir = os.getcwd()
#work_dir = os.path.dirname(sys.executable)
input_dir = os.path.join(work_dir,'output_preprocessing')
output_dir= os.path.join(work_dir,'output')
output_gambar= os.path.join(work_dir,'output_verifikasi')
output_cross= os.path.join(work_dir,'output_cross')

FileNames = natsort.natsorted(os.listdir(input_dir))

delsep=';'

os.chdir(input_dir)

DataFrames = []
for f in FileNames: 
    DataFrames.append(pd.read_csv(f, delimiter=(';')))
    
reg=linear_model.LinearRegression()

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

if not os.path.exists(output_gambar):
    os.makedirs(output_gambar)
    
if not os.path.exists(output_cross):
    os.makedirs(output_cross)
    
az_list=[]

idx=0

os.chdir(output_dir)

for i in range (len(FileNames)):
    tmp=FileNames[i].split('.')[0]
    FileNames[i]=tmp

nama_prev=FileNames[0].split('_')[0]
ans_global=[]

for f in DataFrames:
    #preprocessing
    nama_curr=FileNames[idx].split('_')[0]
    er=True
    while(er):
        try:
            rd=1 #random agar tidak error kalau vertikal atau horizontal
            f.E=f.E-min(f.E)
            f.N=f.N-min(f.N)
            
            arr_pre=np.zeros([2,len(f.E)])
            arr_pre[0]=f.E
            arr_pre[1]=f.N
            
            ret_pre=rotatecoor(arr_pre,rd,np.array([[0],[0]]))
            
            f.E=ret_pre[0]
            f.N=ret_pre[1]
            
            #processing
            X=f.E.to_numpy()
            Y=f.N.to_numpy()
            Z=f.Z.to_numpy()
            X=np.reshape(X, (len(X), 1))
            reg.fit(X,Y)
            m=reg.coef_
            c=reg.intercept_
            
            ki=np.zeros(2)
            ka=np.zeros(2)
            jum_z=0
            banyak_z=0
            
            for i in range (len(f)):
                if(f.iat[i,1].lower()=="a"):#kode kiri
                    ki[0]=f.E[i]
                    ki[1]=f.N[i]
                if(f.iat[i,1].lower()=="b"):#kode kanan
                    ka[0]=f.E[i]
                    ka[1]=f.N[i]
                if(f.iat[i,1].lower()[0]=="d"):#kode rata-rata d
                    jum_z+=f.Z[i]
                    banyak_z+=1
            
            if(banyak_z!=0):
                rerata_d_z=jum_z/banyak_z #rata-rata z
            else:
                rerata_d_z=0
                    
            X_pred=[[ki[0]],[ka[0]]]
            Y_pred = reg.predict(X_pred)
            
            ki_pred=np.array([ki[0],Y_pred[0]])
            ka_pred=np.array([ka[0],Y_pred[1]])
        
            delta=ka_pred-ki_pred
            
            if(delta[1]>0):
                az=(360+np.degrees(np.arctan(delta[0]/delta[1])))%360
            elif(delta[1]<0):
                az=180+np.degrees(np.arctan(delta[0]/delta[1]))
                  
            az_list.append(az)
            
            arr=np.zeros([2,len(X)])
            arr[0]=X.reshape(len(X))
            arr[1]=Y
            
            ret=rotatecoor(arr,-450+az,ki_pred.reshape(2,1))
            
            if(idx%10==0):
                plt.figure()#plotting x y eksisting
                #plt.plot(ret[0],ret[1])
                plt.plot(X,Y)
                #plt.plot(X_pred,Y_pred)
                #plt.plot(ret_pre[0],ret_pre[1])
                plt.savefig(os.path.join(output_gambar,FileNames[idx]+'.png'),dpi=50)
                plt.close('all')
            
            ret=np.array([ret[0],Z])
            
            a=ret[0]
            b=ret[1]
            
            ind = np.lexsort((b,a)) 
            
            ans=[(b[i],0,a[i],0,0,0,0,0,0) for i in ind]
            ans=np.array(ans).transpose()
            ans_index=np.array([[f.iloc[i,0],f.iloc[i,1]] for i in ind])
            
            b=ans_index.T
           
            #post processing
            ans[2]=ans[2]-ans[2].min()
            
            for i in range(1,len(ans[0])): #jarak antar
               ans[1][i]=ans[2][i]-ans[2][i-1]
            
            for i in range(0,len(ans[0])): #z
               ans[4][i]=rerata_d_z
               
            tki=np.zeros(2)
            tka=np.zeros(2)
            
            for i in range(0,len(ans[0])):
                if(b[1][i].lower()=="t1"): #tanggul kiri
                    tki[0]=ans[2][i]#x
                    tki[1]=ans[0][i]#z
                if(b[1][i].lower()=="t2"): #tanggul kanan
                    tka[0]=ans[2][i]#x
                    tka[1]=ans[0][i]#z
                    
            rerata_t_x=(tki+tka)/2
            
            for i in range(0,len(ans[0])): #x
               ans[3][i]=rerata_t_x[0]
               if(tki[0]<=tka[0]):
                   ans[5][i]=tki[0]
                   ans[6][i]=tki[1]
                   ans[7][i]=tka[0]
                   ans[8][i]=tka[1]
               else:
                   ans[5][i]=tka[0]
                   ans[6][i]=tka[1]
                   ans[7][i]=tki[0]
                   ans[8][i]=tki[1]
                   
            if(idx%10==0):
                plt.figure()
                plt.plot(ans[2],ans[0])
                plt.savefig(os.path.join(output_cross,FileNames[idx]+'.png'),dpi=50)
                plt.close('all')
            
            if(nama_curr==nama_prev):
                if(idx==0):
                    ans_global=np.concatenate((b,ans), axis=0)
                else:
                    c=np.concatenate((b,ans), axis=0)
                    ans_global=np.concatenate((ans_global,c), axis=1)
                    
            if (nama_curr!=nama_prev or idx==len(DataFrames)-1): #save file
                col=['sta','code','z','delta x','x','rerata_x','rerata_z','x_tki','z_tki','x_tka','z_tka']
                ret=pd.DataFrame(ans_global.transpose(),columns=col)
                ret.to_csv(nama_prev+"_o.csv",index=False,sep=delsep)
                
            if(nama_curr!=nama_prev):
                ans_global=[]
                ans_global=np.concatenate((b,ans), axis=0)
            
            nama_prev=nama_curr
            er=False
        except:
            print("Sudut error pada id {}".format(idx))
    idx+=1

print("Completed!")