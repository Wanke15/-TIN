# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 13:10:40 2016

@author: 10150
"""

import numpy as np
'''
def input_point():
    point_set={}
    print "输入你的点编号和坐标信息：(从编号1开始;若输入编号0，则结束点的录入)"
    while 1:
        n=int(input(u"编号："))
        if n==0:
            print "结束录入！"
            break
        x=float(input(u"x坐标："))
        y=float(input(u"y坐标："))
        point_set[n]=np.array([x,y])
    return point_set
'''
def input_point():
    point_set={}
    key=[]
    p_x,p_y=np.array([]),np.array([])
    print "输入你的点编号和坐标信息：(从编号1开始;若输入编号0，则结束点的录入)"
    while 1:
        n=int(input(u"编号："))
        if n==0:
            print "结束录入！"
            break
        x=float(input(u"x坐标："))
        y=float(input(u"y坐标："))
        key.append(n)
        p_x=np.append(p_x,x)
        p_y=np.append(p_y,y)
        
    temp_x,temp_y=p_x[0],p_y[0]
    min_ind_y=p_y.argmin()#最小y值的下标
    point_set[1]=[p_x[min_ind_y],min(p_y)]
    print point_set[1]
    point_set[min_ind_y+1]=[temp_x,temp_y]
    
    for n,x,y in zip(key,p_x,p_y):
        if n==1 or n==min_ind_y+1:
            continue
        point=np.array([])
        point=np.append(point,x)
        point=np.append(point,y)
        point_set[n]=point
        
    global original_point
    original_point=point_set.copy()
    
    return point_set
    
if __name__ == '__main__':
    my_point=input_point()
    print my_point
    
