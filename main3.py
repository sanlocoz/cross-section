# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 00:05:31 2021

@author: user
"""

import numpy as np
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
from sklearn import linear_model
import natsort

eps=10**-5

def interpolation (x_1,y_1,x_2,y_2,x_target):
    reg=linear_model.LinearRegression()
    X=np.array([[x_1],[x_2]])
    Y=np.array([y_1,y_2])
    reg.fit(X,Y)
    X_pred=np.array([[x_target]])
    y_target = reg.predict(X_pred)
    return y_target

def cek_elev_poly(eksisting,x):
    if(x<=min(eksisting[:,0])):
        return eksisting[0][1]
    elif(x>=max(eksisting[:,0])):
        return eksisting[len(eksisting[:,0])-1][1]
    a=np.searchsorted(eksisting[:,0],x)
    return np.double(interpolation(eksisting[a][0],eksisting[a][1],eksisting[a-1][0],eksisting[a-1][1],x))

def elev_eksisting (layer,basepo,po,datum,fil):
    print(("_layer set "+layer+" "),file=fil)
    dat=datum
    rpo=po+basepo#belum dikurang datum
    print("PLINE ",end='',file=fil)
    for i in rpo:
        print(i[0],",",i[1]-dat,sep='',file=fil)
    print("\n",end='',file=fil)
    return 0;

def garis_putus (layer,basepo,po,datum,fil):
    print(("_layer set "+layer+" "),file=fil)
    dat=datum
    rpo=po+basepo
    for i in range(len(rpo)):
        print("LINE ",end='',file=fil)
        if(i==len(rpo)-1):
            print(rpo[i][0],",",rpo[i][1]-dat," ",rpo[i][0],",",basepo[1],sep='',end="\n",file=fil)
        else:
            print(rpo[i][0],",",rpo[i][1]-dat," ",rpo[i][0],",",basepo[1],sep='',end=" \n",file=fil)
    print("\n",end='',file=fil)
    return 0;

def garis_tabel (layer,basepo,po,datum,fil,t_elev,t_jrk):
    print(("_layer set "+layer+" "),file=fil)
    dat=datum
    rpo=po+basepo
    for i in range(len(rpo)):
        print("LINE ",end='',file=fil)
        if(i==len(rpo)-1):
            print(rpo[i][0],",",basepo[1]-t_elev-t_jrk," ",rpo[i][0],",",basepo[1]-t_elev,sep='',end="\n",file=fil)
        else:
            print(rpo[i][0],",",basepo[1]-t_elev-t_jrk," ",rpo[i][0],",",basepo[1]-t_elev,sep='',end=" \n",file=fil)
    print("\n",end='',file=fil)
    return 0;

def txt_elev (layer,basepo,po,datum,fil,t_elev):
    print(("_layer set "+layer+" "),file=fil)
        
    dat=datum
    rpo=po+basepo
    for i in range(len(rpo)):
        print('text s st1 j mc {:.5f},{:.5f} 90 {:.3f}'.format(rpo[i][0],basepo[1]-t_elev/2,point[i][1]),file=fil)
    return 0;

def txt_jrk (layer,basepo,po,datum,fil,t_elev,t_jrk):
    print(("_layer set "+layer+" "),file=fil)
        
    dat=datum
    rpo=po+basepo
    for i in range(len(rpo)-1):
        print('text s st1 j mc {:.5f},{:.5f} 90 {:.3f}'.format((rpo[i][0]+rpo[i+1][0])/2,basepo[1]-t_elev-t_jrk/2,-rpo[i][0]+rpo[i+1][0]),file=fil)
    return 0;

def elev_rencana (layer,basepo,po,datum,fil):
    print(("_layer set "+layer+" "),file=fil)
    dat=datum
    rpo=po+basepo#belum dikurang datum
    print("PLINE ",end='',file=fil)
    for i in rpo:
        print(i[0],",",i[1]-dat,sep='',file=fil)
    print("\n",end='',file=fil)
    return 0;

def txt_jrk_r (layer,basepo,po,datum,fil,t_elev,t_jrk,t_elev_r):
    print(("_layer set "+layer+" "),file=fil)
        
    dat=datum
    rpo=po+basepo
    for i in range(len(rpo)):
        print('text s st1 j mc {:.5f},{:.5f} 90 {:.3f}'.format(rpo[i][0],basepo[1]-t_elev-t_jrk-t_elev_r/2,point_r[i][1]),file=fil)
    return 0;

def txt_datum(layer,basepo,datum,fil,param,jrk_x_datum,jrk_y_datum):
    print(("_layer set "+layer+" "),file=fil)
    sign=""
    if(dat>0):
        sign="+"
    print('text s Standard j {} {:.5f},{:.5f} 360 {}{:.2f} M'.format(param,basepo[0]+jrk_x_datum,basepo[1]+jrk_y_datum,sign,datum),file=fil)
    return 0;

def txt_grid(layer,basepo,datum,fil,param,jrk_x_datum,jmlh,step):
    print(("_layer set "+layer+" "),file=fil)
    for i in range(1,jmlh+1,np.longlong(step)):
        print('text s Standard j {} {:.5f},{:.5f} 360 {:.2f}'.format(param,basepo[0]+jrk_x_datum,basepo[1]+i,datum+i),file=fil)
    return 0;

def frame_tabel(layer,basepo,max_x,fil,t_elev,t_jrk,t_rencana):
    print(("_layer set "+layer+" "),file=fil)
    print("LINE ",end='',file=fil)
    print(basepo[0]-0.5,",",basepo[1]," ",basepo[0]+max_x+0.5,",",basepo[1],sep='',end="\n",file=fil)
    print("\n",end='',file=fil)
    
    print("LINE ",end='',file=fil)
    print(basepo[0]-0.5,",",basepo[1]-t_elev," ",basepo[0]+max_x+0.5,",",basepo[1]-t_elev,sep='',end="\n",file=fil)
    print("\n",end='',file=fil)
    
    print("LINE ",end='',file=fil)
    print(basepo[0]-0.5,",",basepo[1]-t_elev-t_jrk," ",basepo[0]+max_x+0.5,",",basepo[1]-t_elev-t_jrk,sep='',end="\n",file=fil)
    print("\n",end='',file=fil)

    print("LINE ",end='',file=fil)
    print(basepo[0]-0.5,",",basepo[1]-t_elev-t_jrk-t_rencana," ",basepo[0]+max_x+0.5,",",basepo[1]-t_elev-t_jrk-t_rencana,sep='',end="\n",file=fil)
    print("\n",end='',file=fil)
    
    print("LINE ",end='',file=fil)
    print(basepo[0]+max_x+0.5,",",basepo[1]," ",basepo[0]+max_x+0.5,",",basepo[1]-t_elev-t_jrk-t_rencana,sep='',end="\n",file=fil)
    print("\n",end='',file=fil)
    
    return 0;

def judul_sta(layer,basepo,sta,fil,param,jrk_x_sta,jrk_y_sta):
    print(("_layer set "+layer+" "),file=fil)
    print('text s Verdana j {} {:.5f},{:.5f} 360 {}'.format(param,basepo[0]+jrk_x_sta/2,basepo[1]-jrk_y_sta,sta),file=fil)
    return 0;
    
def judul_galtim(layer,basepo,sta,fil,param,jrk_x_sta,jrk_y_sta):
    print(("_layer set "+layer+" "),file=fil)
    print('text s STAGT j {} {:.5f},{:.5f} 360 {}'.format(param,basepo[0]+jrk_x_sta/2,basepo[1]-jrk_y_sta/2,sta),file=fil)
    return 0;

def galtim(layer,basepo,galtim,fil,param,jrk_x_galtim,jrk_y_galtim):#ubah ini
    print(("_layer set "+layer+" "),file=fil)
    print('text s GT j {} {:.5f},{:.5f} 360 {:.4f}'.format(param,basepo[0]+jrk_x_galtim,basepo[1]-jrk_y_galtim,galtim),file=fil)
    return 0;

def dimensi_horizontal(layer,basepo,po,datum,fil,jenis,dim1,dim2,jrk_h):
    print(("_layer set "+layer+" "),file=fil)
    dat=datum
    rpo=po+basepo#belum dikurang datum
    maxi=rpo[:,1].max()+jrk_h
    mini=rpo[:,1].min()-jrk_h
    
    if(jenis=='l'):#gambar lengkap
        if(abs(rpo[1][0]-rpo[2][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f} '.format(rpo[1][0],maxi-dat,rpo[2][0],maxi-dat,rpo[2][0],maxi-dat+dim1),file=fil)
        if(abs(rpo[5][0]-rpo[6][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f} '.format(rpo[5][0],maxi-dat,rpo[6][0],maxi-dat,rpo[6][0],maxi-dat+dim1),file=fil)
        if(abs(rpo[9][0]-rpo[10][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f} '.format(rpo[9][0],maxi-dat,rpo[10][0],maxi-dat,rpo[10][0],maxi-dat+dim1),file=fil)
        if(abs(rpo[0][0]-rpo[3][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f} '.format(rpo[0][0],maxi-dat,rpo[3][0],maxi-dat,rpo[3][0],maxi-dat+dim2),file=fil)
        if(abs(rpo[3][0]-rpo[4][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f} '.format(rpo[3][0],maxi-dat,rpo[4][0],maxi-dat,rpo[4][0],maxi-dat+dim2),file=fil)
        if(abs(rpo[4][0]-rpo[7][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f} '.format(rpo[4][0],maxi-dat,rpo[7][0],maxi-dat,rpo[7][0],maxi-dat+dim2),file=fil)
        if(abs(rpo[7][0]-rpo[8][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f} '.format(rpo[7][0],maxi-dat,rpo[8][0],maxi-dat,rpo[8][0],maxi-dat+dim2),file=fil)
        if(abs(rpo[8][0]-rpo[11][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f}'.format(rpo[8][0],maxi-dat,rpo[11][0],maxi-dat,rpo[11][0],maxi-dat+dim2),file=fil)
    elif(jenis=='ki' or jenis=='ka'):
        if(abs(rpo[1][0]-rpo[2][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f} '.format(rpo[1][0],maxi-dat,rpo[2][0],maxi-dat,rpo[2][0],maxi-dat+dim1),file=fil)
        if(abs(rpo[0][0]-rpo[3][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f}'.format(rpo[0][0],maxi-dat,rpo[3][0],maxi-dat,rpo[3][0],maxi-dat+dim2),file=fil)
    elif(jenis=='s'):
        if(abs(rpo[1][0]-rpo[2][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f} '.format(rpo[1][0],mini-dat,rpo[2][0],mini-dat,rpo[2][0],mini-dat-dim1),file=fil)
        if(abs(rpo[0][0]-rpo[3][0])>eps):
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} H {:.5f},{:.5f}'.format(rpo[0][0],mini-dat,rpo[3][0],mini-dat,rpo[3][0],mini-dat-dim2),file=fil)
    return 0;

def dimensi_vertikal(layer,basepo,po,datum,fil,jenis,dim1,jrk_v):
    print(("_layer set "+layer+" "),file=fil)
    dat=datum
    rpo=po+basepo#belum dikurang datum
    if(jenis=='l'):#gambar lengkap
        if(abs(rpo[0][1]-rpo[1][1])>eps):
            mini=rpo[0][0]-dim1
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} V {:.5f},{:.5f} '.format(mini,rpo[0][1]-dat,mini,rpo[1][1]-dat,mini-jrk_v,rpo[1][1]-dat),file=fil)
        if(abs(rpo[3][1]-rpo[5][1])>eps):
            mini=rpo[3][0]-dim1
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} V {:.5f},{:.5f} '.format(mini,rpo[3][1]-dat,mini,rpo[5][1]-dat,mini-jrk_v,rpo[5][1]-dat),file=fil)
        if(abs(rpo[10][1]-rpo[11][1])>eps):
            mini=rpo[11][0]+dim1
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} V {:.5f},{:.5f}'.format(mini,rpo[10][1]-dat,mini,rpo[11][1]-dat,mini+jrk_v,rpo[11][1]-dat),file=fil)
    elif(jenis=='ki'):
        if(abs(rpo[0][1]-rpo[1][1])>eps):
            mini=rpo[0][0]-dim1
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} V {:.5f},{:.5f}'.format(mini,rpo[0][1]-dat,mini,rpo[1][1]-dat,mini-jrk_v,rpo[1][1]-dat),file=fil)
    elif(jenis=='ka'):
        if(abs(rpo[2][1]-rpo[3][1])>eps):
            mini=rpo[3][0]+dim1
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} V {:.5f},{:.5f}'.format(mini,rpo[2][1]-dat,mini,rpo[3][1]-dat,mini+jrk_v,rpo[2][1]-dat),file=fil)
    elif(jenis=='s'):
        if(abs(rpo[0][1]-rpo[1][1])>eps):
            mini=rpo[0][0]-dim1
            print('DIMLINEAR {:.5f},{:.5f} {:.5f},{:.5f} V {:.5f},{:.5f}'.format(mini,rpo[0][1]-dat,mini,rpo[1][1]-dat,mini-jrk_v,rpo[1][1]-dat),file=fil)

    return 0;

def extr(eks,ren,fil,jenis,const_win):
    #eksisting
    po_eks=np.zeros([9,2])
    po_eks[0][0]=eks[0]-const_win;po_eks[0][1]=eks[1]+const_win
    po_eks[1][0]=eks[0];po_eks[1][1]=eks[1]+const_win
    po_eks[2][0]=eks[0]+const_win;po_eks[2][1]=eks[1]+const_win
    
    po_eks[3][0]=eks[0]-const_win;po_eks[3][1]=eks[1]
    po_eks[4][0]=eks[0];po_eks[4][1]=eks[1]
    po_eks[5][0]=eks[0]+const_win;po_eks[5][1]=eks[1]
    
    po_eks[6][0]=eks[0]-const_win;po_eks[6][1]=eks[1]-const_win
    po_eks[7][0]=eks[0];po_eks[7][1]=eks[1]-const_win
    po_eks[8][0]=eks[0]+const_win;po_eks[8][1]=eks[1]-const_win
    
    #rencana
    po_ren=np.zeros([9,2])
    po_ren[0][0]=ren[0]-const_win;po_ren[0][1]=ren[1]+const_win
    po_ren[1][0]=ren[0];po_ren[1][1]=ren[1]+const_win
    po_ren[2][0]=ren[0]+const_win;po_ren[2][1]=ren[1]+const_win
    
    po_ren[3][0]=ren[0]-const_win;po_ren[3][1]=ren[1]
    po_ren[4][0]=ren[0];po_ren[4][1]=ren[1]
    po_ren[5][0]=ren[0]+const_win;po_ren[5][1]=ren[1]
    
    po_ren[6][0]=ren[0]-const_win;po_ren[6][1]=ren[1]-const_win
    po_ren[7][0]=ren[0];po_ren[7][1]=ren[1]-const_win
    po_ren[8][0]=ren[0]+const_win;po_ren[8][1]=ren[1]-const_win
        
    list_koor=[4,0,2,6,8,4,3,0,5,2,4,5,8,3,6,5,3,2]
    
    if (jenis.lower()=="trim"):
        print("TRIM FENCE",file=f)
        for i in range (len(list_koor)):
            if (i==len(list_koor)-1):
                print("{:.30f},{:.30f} \n".format(po_eks[list_koor[i]][0],po_eks[list_koor[i]][1]),file=f)
            else:
                print("{:.30f},{:.30f}".format(po_eks[list_koor[i]][0],po_eks[list_koor[i]][1]),file=f)
        #print("-layer OFF GarisElevasiTanah ",file=f)
        print("FENCE",file=f)
        for i in range (len(list_koor)):
            if (i==len(list_koor)-1):
                print("{:.30f},{:.30f} \n".format(po_ren[list_koor[i]][0],po_ren[list_koor[i]][1]),file=f)
            else:
                print("{:.30f},{:.30f}".format(po_ren[list_koor[i]][0],po_ren[list_koor[i]][1]),file=f)
    elif (jenis.lower()=="extend"):
        print("EXTEND FENCE",file=f)
        for i in range (len(list_koor)):
            if (i==len(list_koor)-1):
                print("{:.30f},{:.30f} \n".format(po_eks[list_koor[i]][0],po_eks[list_koor[i]][1]),file=f)
            else:
                print("{:.30f},{:.30f}".format(po_eks[list_koor[i]][0],po_eks[list_koor[i]][1]),file=f)
        #print("-layer OFF GarisElevasiTanah ",file=f)
        print("FENCE",file=f)
        for i in range (len(list_koor)):
            if (i==len(list_koor)-1):
                print("{:.30f},{:.30f} \n".format(po_ren[list_koor[i]][0],po_ren[list_koor[i]][1]),file=f)
            else:
                print("{:.30f},{:.30f}".format(po_ren[list_koor[i]][0],po_ren[list_koor[i]][1]),file=f)

def te(base,po,po_r,dat,fil,jenis,b_ki,b_ka):
    #print(base,po,po_r,dat)
    const_win=0.001
    rpo=po+base
    rpo_r=po_r+base
    rpo[:,1]-=dat
    rpo_r[:,1]-=dat
    #print(rpo,rpo_r)
    
    po_eks=rpo[0]
    po_r_kiri=rpo_r[0]
    po_r_kanan=rpo_r[len(rpo_r)-1]
    
    #print(po_eks,po_r_kiri,po_r_kanan)
    print("-layer ON Rencana ",file=f)
    print("-layer ON GarisElevasiTanah ",file=f)
    
    if(jenis=="s"): #galian
        if(cek_elev_poly(po,po_r[0,0])<po_r[0,1]):#jika rencana di atas eksisting  untuk KIRI
            if(b_ki):#extend
                extr(po_eks,po_r_kiri,fil,"EXTEND",const_win)
                #print('EXTEND\n{:.3f},{:.3f} {:.3f},{:.3f} \n{:.3f},{:.3f} {:.3f},{:.3f} '.format(po_eks[0]+const_win,po_eks[1]-const_win,po_eks[0]-const_win,po_eks[1]+const_win,po_r_kiri[0]+const_win,po_r_kiri[1]-const_win,po_r_kiri[0]-const_win,po_r_kiri[1]+const_win),file=fil)
            else:#trim
                extr(po_eks,po_r_kiri,fil,"TRIM",const_win)
        elif(cek_elev_poly(po,po_r[0,0])>po_r[0,1]):#rencana di bawah eksisting untuk KIRI
            if(b_ki):#extend
                extr(po_eks,po_r_kiri,fil,"TRIM",const_win)
                #print('EXTEND\n{:.3f},{:.3f} {:.3f},{:.3f} \n{:.3f},{:.3f} {:.3f},{:.3f} '.format(po_eks[0]+const_win,po_eks[1]-const_win,po_eks[0]-const_win,po_eks[1]+const_win,po_r_kiri[0]+const_win,po_r_kiri[1]-const_win,po_r_kiri[0]-const_win,po_r_kiri[1]+const_win),file=fil)
            else:#extend
                extr(po_eks,po_r_kiri,fil,"EXTEND",const_win) 
        
        if(cek_elev_poly(po,po_r[len(po_r)-1,0])<po_r[len(po_r)-1,1]):#jika rencana di atas eksisting untuk KANAN
            if(b_ka):#extend
                extr(po_eks,po_r_kanan,fil,"EXTEND",const_win)
                #print('EXTEND\n{:.3f},{:.3f} {:.3f},{:.3f} \n{:.3f},{:.3f} {:.3f},{:.3f} '.format(po_eks[0]+const_win,po_eks[1]-const_win,po_eks[0]-const_win,po_eks[1]+const_win,po_r_kiri[0]+const_win,po_r_kiri[1]-const_win,po_r_kiri[0]-const_win,po_r_kiri[1]+const_win),file=fil)
            else:#trim
                extr(po_eks,po_r_kanan,fil,"TRIM",const_win)
        elif(cek_elev_poly(po,po_r[len(po_r)-1,0])>po_r[len(po_r)-1,1]):#jika rencana di atas eksisting untuk KANAN
            if(b_ka):#extend
                extr(po_eks,po_r_kanan,fil,"TRIM",const_win)
                #print('EXTEND\n{:.3f},{:.3f} {:.3f},{:.3f} \n{:.3f},{:.3f} {:.3f},{:.3f} '.format(po_eks[0]+const_win,po_eks[1]-const_win,po_eks[0]-const_win,po_eks[1]+const_win,po_r_kiri[0]+const_win,po_r_kiri[1]-const_win,po_r_kiri[0]-const_win,po_r_kiri[1]+const_win),file=fil)
            else:#trim
                extr(po_eks,po_r_kanan,fil,"EXTEND",const_win)
    else:
        if(cek_elev_poly(po,po_r[0,0])<po_r[0,1]):#jika rencana di atas eksisting  untuk KIRI
            if(b_ki):
                extr(po_eks,po_r_kiri,fil,"TRIM",const_win)
                #print('EXTEND\n{:.3f},{:.3f} {:.3f},{:.3f} \n{:.3f},{:.3f} {:.3f},{:.3f} '.format(po_eks[0]+const_win,po_eks[1]-const_win,po_eks[0]-const_win,po_eks[1]+const_win,po_r_kiri[0]+const_win,po_r_kiri[1]-const_win,po_r_kiri[0]-const_win,po_r_kiri[1]+const_win),file=fil)
            else:#trim
                extr(po_eks,po_r_kiri,fil,"EXTEND",const_win)
        elif(cek_elev_poly(po,po_r[0,0])>po_r[0,1]):#rencana di bawah eksisting untuk KIRI
            if(b_ki):#extend
                extr(po_eks,po_r_kiri,fil,"EXTEND",const_win)
                #print('EXTEND\n{:.3f},{:.3f} {:.3f},{:.3f} \n{:.3f},{:.3f} {:.3f},{:.3f} '.format(po_eks[0]+const_win,po_eks[1]-const_win,po_eks[0]-const_win,po_eks[1]+const_win,po_r_kiri[0]+const_win,po_r_kiri[1]-const_win,po_r_kiri[0]-const_win,po_r_kiri[1]+const_win),file=fil)
            else:#extend
                extr(po_eks,po_r_kiri,fil,"TRIM",const_win) 
        
        if(cek_elev_poly(po,po_r[len(po_r)-1,0])<po_r[len(po_r)-1,1]):#jika rencana di atas eksisting untuk KANAN
            if(b_ka):#extend
                extr(po_eks,po_r_kanan,fil,"TRIM",const_win)
                #print('EXTEND\n{:.3f},{:.3f} {:.3f},{:.3f} \n{:.3f},{:.3f} {:.3f},{:.3f} '.format(po_eks[0]+const_win,po_eks[1]-const_win,po_eks[0]-const_win,po_eks[1]+const_win,po_r_kiri[0]+const_win,po_r_kiri[1]-const_win,po_r_kiri[0]-const_win,po_r_kiri[1]+const_win),file=fil)
            else:#trim
                extr(po_eks,po_r_kanan,fil,"EXTEND",const_win)
        elif(cek_elev_poly(po,po_r[len(po_r)-1,0])>po_r[len(po_r)-1,1]):#jika rencana di atas eksisting untuk KANAN
            if(b_ka):#extend
                extr(po_eks,po_r_kanan,fil,"EXTEND",const_win)
                #print('EXTEND\n{:.3f},{:.3f} {:.3f},{:.3f} \n{:.3f},{:.3f} {:.3f},{:.3f} '.format(po_eks[0]+const_win,po_eks[1]-const_win,po_eks[0]-const_win,po_eks[1]+const_win,po_r_kiri[0]+const_win,po_r_kiri[1]-const_win,po_r_kiri[0]-const_win,po_r_kiri[1]+const_win),file=fil)
            else:#trim
                extr(po_eks,po_r_kanan,fil,"TRIM",const_win)
       
def ha(po,angle,tipe,skala,fil,po_ki,po_ka):
    print(("_layer set Arsir "),file=fil)
    print("ZOOM W {:.15f},{:.15f} {:.15f},{:.15f}".format(po_ki[0],po_ki[1],po_ka[0],po_ka[1]),file=fil)
    print("-HATCH P {} {} {}".format(tipe,skala,angle),file=fil)
    for i in range(len(po)):
        print("{:.15f},{:.15f}".format(po[i][0],po[i][1]),file=fil)
    
def hatch(base,po,po_r,dat,fil,jenis):
    x_mini=0
    x_maxi=0
    if(jenis=="l"):
        x_mini=po_r[1][0]
        x_maxi=po_r[10][0]
    else:
        x_mini=po_r[1][0]
        x_maxi=po_r[2][0]
        
    galian=[]
    timbunan=[]
    increment=1
    while (x_mini<x_maxi):
        eks=cek_elev_poly(po,x_mini)
        ren=cek_elev_poly(po_r,x_mini)
        if(eks>ren):
            galian.append([x_mini,(eks+ren)/2])
        else:
            timbunan.append([x_mini,(eks+ren)/2])
        x_mini+=increment
        
    if(len(galian)>0):
        galian=np.array(galian)
        galian+=base
        galian[:,1]-=dat
        
    if(len(timbunan)>0):
        timbunan=np.array(timbunan)
        timbunan+=base
        timbunan[:,1]-=dat
    
    po_ki=np.zeros([2])
    po_ka=np.zeros([2])
    
    po_ki[0]=min(min(po[:,0]),min(po_r[:,0]))
    po_ki[1]=max(max(po[:,1]),max(po_r[:,1]))
    
    po_ka[0]=max(max(po[:,0]),max(po_r[:,0]))
    po_ka[1]=min(min(po[:,1]),min(po_r[:,1]))
    
    po_ki+=base
    po_ka+=base
    po_ki[1]-=dat
    po_ka[1]-=dat
    
    if(len(galian)>0):
        ha(galian,45,"ANSI31",1,fil,po_ki,po_ka)
        print("\n\n",file=fil)
        
    if(len(timbunan)>0):
        ha(timbunan,135,"ANSI31",1,fil,po_ki,po_ka)
        print("\n\n",file=fil)
    
    
print("Loading!")    
#work_dir = os.path.dirname(sys.executable)
work_dir = os.getcwd()
input_dir = os.path.join(work_dir,'input_acad')
input_eksisting_dir= os.path.join(work_dir,'output_preprocessing_eksisting')
input_rencana_dir= os.path.join(work_dir,'output_preprocessing_rencana')
input_rencana = os.path.join(work_dir,'input_rencana')
output_galtim = os.path.join(work_dir,'output_tabel')
output_dir= os.path.join(work_dir,'output_scr')

FileNames = natsort.natsorted(os.listdir(input_dir))
FileNames_e= natsort.natsorted(os.listdir(input_eksisting_dir))
FileNames_r= natsort.natsorted(os.listdir(input_rencana_dir))
FileNames_param_r= natsort.natsorted(os.listdir(input_rencana))
FileNames_galtim= natsort.natsorted(os.listdir(output_galtim))

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
delsep=';'

#input dulu
os.chdir(input_dir)
DataFrames_param = []
for f in FileNames: 
    DataFrames_param.append(pd.read_csv(f, delimiter=(delsep)))
    
os.chdir(input_eksisting_dir)
DataFrames_e= []
for f in FileNames_e: 
    DataFrames_e.append(pd.read_csv(f, delimiter=(delsep)))

os.chdir(input_rencana_dir) 
DataFrames_r= []
for f in FileNames_r: 
    DataFrames_r.append(pd.read_csv(f, delimiter=(delsep)))
    
os.chdir(input_rencana) 
DataFrames= []
for f in FileNames_param_r: 
    DataFrames.append(pd.read_csv(f, delimiter=(delsep)))
    
os.chdir(output_galtim) 
DataFrames_galtim= []
for f in FileNames_galtim: 
    DataFrames_galtim.append(pd.read_csv(f, delimiter=(delsep)))
    
#baru output
os.chdir(output_dir)
f = open("1 acad.scr", "w")
f.close()
f = open("2 acad_rencana.scr","w")
f.close()
f = open("3 acad_pelengkap.scr","w")
f.close()
f = open("4 acad_dimensi.scr","w")
f.close()
f = open("5 acad_te.scr","w")
print("zoom\ne",file=f)
print("-layer OFF * y ",file=f)
print("-layer ON Rencana ",file=f)
print("-layer ON GarisElevasiTanah ",file=f)
print("-layer LOCK GarisElevasiTanah ",file=f)
f.close()

f = open("6 acad_ha.scr","w")
print("zoom\ne",file=f)
print("-layer OFF * y ",file=f)
print("-layer ON Rencana ",file=f)
print("-layer ON Arsir ",file=f)
print("-layer ON GarisElevasiTanah ",file=f)
print("-layer LOCK GarisElevasiTanah ",file=f)
f.close()

f = open("1 acad.scr", "a")

#elevasi eksisting
layer_g_tabel=DataFrames_param[0].iat[0,1]
layer_g_putus=DataFrames_param[0].iat[1,1]
layer_skala_elev=DataFrames_param[0].iat[2,1]
layer_elev=DataFrames_param[0].iat[3,1]
layer_txtelevdist=DataFrames_param[0].iat[4,1]
layer_rencana=DataFrames_param[0].iat[5,1]
layer_txt=DataFrames_param[0].iat[6,1]
layer_txt_english=DataFrames_param[0].iat[36,1]
layer_dimensi=DataFrames_param[0].iat[37,1]

n=np.longlong(np.double(DataFrames_param[0].iat[9,1]))#Jumlah kertas (kolom) 10
m=np.longlong(np.double(DataFrames_param[0].iat[10,1]))#Jumlah kertas (baris) 10
jn=np.longlong(np.double(DataFrames_param[0].iat[11,1]))#Jarak antar kertas (kolom) 50
jm=np.longlong(np.double(DataFrames_param[0].iat[12,1]))#Jarak antar kertas (baris) 50
i=np.longlong(np.double(DataFrames_param[0].iat[13,1]))#Jumlah gambar 1 kertas (baris) 2
j=np.longlong(np.double(DataFrames_param[0].iat[14,1]))#Jumlah gambar 1 kertas (kolom) 1
ji=np.longlong(np.double(DataFrames_param[0].iat[15,1]))#Jarak antar baris  gambar 1 kertas 13
jj=np.longlong(np.double(DataFrames_param[0].iat[16,1]))#Jarak antar kolom gambar 1 kertas 0

x_galtim=np.double(DataFrames_param[0].iat[17,1])#X galtim
y_galtim=np.double(DataFrames_param[0].iat[18,1])#Y galtim
lebar_judul_galtim=np.double(DataFrames_param[0].iat[19,1])#lebar judul galtim
tinggi_judul_galtim=np.double(DataFrames_param[0].iat[20,1])#tinggi judul galtim
lebar_kotak_galtim=np.double(DataFrames_param[0].iat[21,1])#lebar kotak galtim
tinggi_kotak_galtim=np.double(DataFrames_param[0].iat[22,1])#tinggi kotak galtim
lebar_tulisan_galtim=np.double(DataFrames_param[0].iat[23,1])#lebar tulisan galtim

tinggi_elev_asli=np.double(DataFrames_param[0].iat[24,1])#Tinggi kotak elev tanah asli
tinggi_jarak=np.double(DataFrames_param[0].iat[25,1])#Tinggi kotak jarak
tinggi_elev_rencana=np.double(DataFrames_param[0].iat[26,1])#Tinggi kotak elev rencana

pengurang_datum=np.double(DataFrames_param[0].iat[27,1])#Pengurang Datum Elevasi dari Min

x_grid=np.double(DataFrames_param[0].iat[28,1])
y_grid=np.double(DataFrames_param[0].iat[29,1])
jrk_grid_ke_skala=np.double(DataFrames_param[0].iat[30,1])
jrk_x_datum=np.double(DataFrames_param[0].iat[31,1])
jrk_y_datum=np.double(DataFrames_param[0].iat[32,1])
jumlah_grid=np.longlong(np.double(DataFrames_param[0].iat[33,1]))
step=np.double(DataFrames_param[0].iat[34,1])

jrk_judul_sta=np.double(DataFrames_param[0].iat[35,1])

ukuran_dimensi_1=np.double(DataFrames_param[0].iat[38,1])#ukuran dimensi lapis1 (dalam)
ukuran_dimensi_2=np.double(DataFrames_param[0].iat[39,1])#ukuran dimensi lapis2 (luar)
jarak_horizontal=np.double(DataFrames_param[0].iat[40,1])#jarak dimensi horizontal
jarak_vertikal=np.double(DataFrames_param[0].iat[41,1])#jarak dimensi vertikal

jumlah_gambar_1kertas=i*j
    
for i in range(len(DataFrames_e)):
    judul=DataFrames[0].iat[i,0]
    kertas=int(i/jumlah_gambar_1kertas) #urutan kertas
    urutan=i%jumlah_gambar_1kertas #urutan gambar dalam kertas
    row_kertas=int(urutan/j) #baris gambar dalam kertas
    col_kertas=urutan%j #kolom gambar dalam kertas
    row=int(kertas/n)
    col=kertas%n
    base=np.array([np.double(DataFrames_param[0].iat[7,1]),np.double(DataFrames_param[0].iat[8,1])])
    base[0]+=(col*jn)+(col_kertas*jj)
    base[1]-=(row*jm)+(row_kertas*ji)
    
    base_galtim=np.array([x_galtim,y_galtim])
    base_galtim[0]+=(col*jn)+(col_kertas*jj)
    base_galtim[1]-=(row*jm)+(row_kertas*ji)
    
    base_grid=np.array([x_grid,y_grid])
    base_grid[0]+=(col*jn)+(col_kertas*jj)
    base_grid[1]-=(row*jm)+(row_kertas*ji)
    
    
    #print(base)
    #print(kertas,urutan,row_kertas,col_kertas,row,col)
    point=np.array([DataFrames_e[i].x.to_numpy(),DataFrames_e[i].z.to_numpy()]).transpose()
    point_r=np.array([DataFrames_r[i].x.to_numpy(),DataFrames_r[i].z.to_numpy()]).transpose()
    galian=True
    
    if(DataFrames[0].iat[i,25].lower()=='s'): #galian
        point_r=point_r[4:8]
        galian=True
    elif(DataFrames[0].iat[i,25].lower()=='l'): #timbunan
        point_r=point_r[0:12]
        galian=False
    elif(DataFrames[0].iat[i,25].lower()=='ki'): #timbunan
        point_r=point_r[0:4]#ubah ini
        galian=False
    elif(DataFrames[0].iat[i,25].lower()=='ka'): #timbunan
        point_r=point_r[8:12]#ubah ini
        galian=False
    
    nilai_galtim=0
    
    if(galian):
        nilai_galtim=DataFrames_galtim[0].iat[i,1]
    else:
        nilai_galtim=DataFrames_galtim[0].iat[i,2]
        
    dat=np.floor(min(point[:,1]))-pengurang_datum
    ret=elev_eksisting(layer_elev,base,point,dat,f)
    ret=garis_putus(layer_g_putus,base,point,dat,f)
    ret=garis_tabel(layer_g_tabel,base,point,dat,f,tinggi_elev_asli,tinggi_jarak)
    ret=txt_elev(layer_txtelevdist,base,point,dat,f,tinggi_elev_asli)
    ret=txt_jrk(layer_txtelevdist,base,point,dat,f,tinggi_elev_asli,tinggi_jarak)

    f.close()
    
    f = open("4 acad_dimensi.scr", "a")
    ret=dimensi_horizontal(layer_dimensi,base,point_r,dat,f,DataFrames[0].iat[i,25].lower(),ukuran_dimensi_1,ukuran_dimensi_2,jarak_horizontal)
    ret=dimensi_vertikal(layer_dimensi,base,point_r,dat,f,DataFrames[0].iat[i,25].lower(),ukuran_dimensi_1,jarak_vertikal)
    f.close()
    
    balik_kiri=False
    balik_kanan=False
    
    if(DataFrames[0].iat[i,25].lower()=='s'): #galian
        if(cek_elev_poly(point,point_r[1,0])<point_r[1,1]): #Saluran di atas eksisting
            point_r[0,1]-=2*(point_r[0,1]-point_r[1,1])
            balik_kiri=True
        if(cek_elev_poly(point,point_r[2,0])<point_r[2,1]): #Saluran di atas eksisting
            point_r[3,1]-=2*(point_r[3,1]-point_r[2,1])
            balik_kanan=True
    elif(DataFrames[0].iat[i,25].lower()=='l'): #timbunan
        if(cek_elev_poly(point,point_r[1,0])>point_r[1,1]): #Timbunan di bawah eksisting
            point_r[0,1]+=2*(point_r[1,1]-point_r[0,1])
            balik_kiri=True
        if(cek_elev_poly(point,point_r[10,0])>point_r[10,1]): #Timbunan di bawah eksisting
            point_r[11,1]+=2*(point_r[10,1]-point_r[11,1])
            balik_kanan=True
    elif(DataFrames[0].iat[i,25].lower()=='ki'): #timbunan
        if(cek_elev_poly(point,point_r[1,0])>point_r[1,1]): #Timbunan di bawah eksisting
            point_r[0,1]+=2*(point_r[1,1]-point_r[0,1])
            balik_kiri=True
        if(cek_elev_poly(point,point_r[2,0])>point_r[2,1]): #Timbunan di bawah eksisting
            point_r[3,1]+=2*(point_r[2,1]-point_r[3,1])
            balik_kanan=True
    elif(DataFrames[0].iat[i,25].lower()=='ka'): #timbunan
        if(cek_elev_poly(point,point_r[1,0])>point_r[1,1]): #Timbunan di bawah eksisting
            point_r[0,1]+=2*(point_r[1,1]-point_r[0,1])
            balik_kiri=True
        if(cek_elev_poly(point,point_r[2,0])>point_r[2,1]): #Timbunan di bawah eksisting
            point_r[3,1]+=2*(point_r[2,1]-point_r[3,1])
            balik_kanan=True
        
    f = open("2 acad_rencana.scr", "a")
    ret=elev_rencana(layer_rencana,base,point_r,dat,f)
    ret=txt_jrk_r(layer_txtelevdist,base,point_r,dat,f,tinggi_elev_asli,tinggi_jarak,tinggi_elev_rencana)
    f.close()
    
    f = open("3 acad_pelengkap.scr", "a")
    ret=txt_datum(layer_txt,base_grid,dat,f,"mc",jrk_x_datum,jrk_y_datum)
    ret=txt_grid(layer_skala_elev,base_grid,dat,f,"mr",jrk_grid_ke_skala,jumlah_grid,step)
    ret=frame_tabel(layer_g_tabel,base,point[:,0].max(),f,tinggi_elev_asli,tinggi_jarak,tinggi_elev_rencana)
    ret=judul_sta(layer_txt,base,judul,f,"mc",point[:,0].max(),jrk_judul_sta)
    ret=judul_galtim(layer_txt,base_galtim,judul,f,"mc",lebar_judul_galtim,tinggi_judul_galtim)
    if(galian):
        ret=galtim(layer_txt_english,base_galtim,nilai_galtim,f,"mc",lebar_tulisan_galtim+lebar_kotak_galtim/2,tinggi_judul_galtim+tinggi_kotak_galtim*0.5)
    else:
        ret=galtim(layer_txt_english,base_galtim,nilai_galtim,f,"mc",lebar_tulisan_galtim+lebar_kotak_galtim/2,tinggi_judul_galtim+tinggi_kotak_galtim*1.5)
        
    f.close()
    
    f = open("5 acad_te.scr","a")
    ret=te(base,point,point_r,dat,f,DataFrames[0].iat[i,25].lower(),balik_kiri,balik_kanan)
    f.close()
    
    f = open("6 acad_ha.scr","a")
    ret=hatch(base,point,point_r,dat,f,DataFrames[0].iat[i,25].lower())
    f.close()
    
    f = open("1 acad.scr", "a")
#back to working directory  
f.close()

f = open("5 acad_te.scr","a")
print("-layer ON * ",file=f)
print("-layer UNLOCK GarisElevasiTanah ",file=f)

f.close()

f = open("6 acad_ha.scr","a")
print("-layer ON * ",file=f)
print("-layer UNLOCK GarisElevasiTanah ",file=f)

f.close()

os.chdir(work_dir)

print("Completed!")    