# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 17:35:14 2021

@author: user
"""

import numpy as np
import pandas as pd
import os
import natsort
import matplotlib.pyplot as plt
from sklearn import linear_model

eps=10**-5

def buat_garis (x1,x2,y1,y2):
    line=np.zeros([3])
    if(abs(x1-x2)<eps):#vertikal
        line[0]=1
        line[1]=0
        line[2]=-x1
    else:
        line[0]=-(y1-y2)/(x1-x2)
        line[1]=1
        line[2]=-(line[0]*x1)-y1
    return line

 