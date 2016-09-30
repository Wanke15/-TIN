# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 10:21:09 2016

@author: 10150
"""

from __future__ import division
import random
import numpy as np
import matplotlib.pyplot as plt
import time
#第一步，产生随机点，并用字典保存下来
def to_polar(x,y):
    '''
    直角坐标转换为极坐标;参数为直角坐标x和y
    '''
    if x==0:
        if y>0:
            my_angle=np.pi/2
        elif y<0:
            my_angle=np.pi*3/2
        else:
            my_angle=0
    else:
        if y==0:
            if x>=0:
                my_angle=0
            else:
                my_angle=np.pi
        else:
            my_angle=np.arctan(y/x)
            if (x<0 and y>0):
                my_angle=my_angle+np.pi
            elif (x<0 and y<0):
                my_angle=my_angle+np.pi
            elif (x>0 and y<0):
                my_angle=my_angle+2*np.pi
            elif (x>0 and y>0):
                my_angle=np.arctan(y/x)
    '''
    T = np.arctan2(y,x)
    return T
    '''
    return my_angle
        
def generate_point(N,left=1,right=100):
    '''
    产生随机点(以字典存储,编号为’键‘,坐标(numpy.array数组)为’值‘;参数为要产生的随机点个数N,随机点产生的范围left和right
    '''
    my_point={}
#    global min_x,max_x,min_y,max_y
    point_x=np.array([])
    point_y=np.array([])
    for i in range(N):
        point_x=np.append(point_x,random.uniform(left,right))
        point_y=np.append(point_y,random.uniform(left,right))
    #将第一个点置为x元素最小的那个点
    temp_x,temp_y=point_x[0],point_y[0]
    min_ind_y=point_y.argmin()#最小y值的下标
    my_point[1]=[point_x[min_ind_y],min(point_y)]
    my_point[min_ind_y+1]=[temp_x,temp_y]
    
    for p_x,p_y,k in zip(point_x,point_y,range(N)):
        if k+1==min_ind_y+1 or k+1==1:
            continue
        point=np.array([])
        point=np.append(point,p_x)
        point=np.append(point,p_y)
        my_point[k+1]=point
    return my_point
    
def show_point(my_point):#产生的原始点的显示
    '''
    产生的原始点的显示;参数为存储随机点的字典
    '''
    print "原始点"
    x=np.array([])
    y=np.array([])
    for item in my_point.values():
        x=np.append(x,item[0])
        y=np.append(y,item[1])
    min_x=min(x)
    max_x=max(x)
    min_y=min(y)
    max_y=max(y)
    plt.figure(u"原始点")
    plt.xlim(min_x-max_x/10,max_x+max_x/10)
    plt.ylim(min_y-max_y/10,max_y+max_y/10)
    global re_x,re_y
    re_x,re_y=[],[]
    for p in my_point.values():
        re_x.append(p[0])
        re_y.append(p[1])
        
    plt.plot(re_x,re_y,'.b')
    plt.show()

#第二步，确定点序
#计算每个点和第一个点的夹角余弦
def aim_point(my_point):#显示原始点和凸包final_y
    '''
    用于产生最后的凸包顶点的x坐标集合和y坐标集合;参数为存储随机点的字典
    '''
    N=len(my_point)
    angle=[0]
    for k,p in my_point.items():
        if k==1:
            continue
        angle.append(to_polar(p[0]-my_point[1][0],p[1]-my_point[1][1]))
    #得到每个点的点序
    sorted_angle=sorted(angle)#现对计算的余弦排序
    sorted_ind=[]#用于存放排序后的下标
    for i in sorted_angle:
        m=angle.index(i)+1
        while m in sorted_ind:
            m+=1
        sorted_ind.append(m)
    #利用排序后的下标重新组织my_point字典
    m_poi=my_point.copy()
    for k,s_k in zip(range(N),sorted_ind):    
        if k+1==1:
            continue
        my_point[k+1]=m_poi[s_k]
    #第三步，判断每个点是否满足和初始点的直线使得其他各点位于该直线的同一侧
    final_x=[my_point[1][0]]
    final_y=[my_point[1][1]]
    m2_poi=my_point.copy()
    count=1
    for m in range(N-1):
        final_k=2
        angle=[0]
    #    print m2_poi[1]
        for k,p in m2_poi.items():
            if k==1:
                continue
            else:
                angle.append(to_polar(p[0]-m2_poi[1][0],p[1]-m2_poi[1][1]))
        #得到每个点的点序
         
        sorted_angle=sorted(angle)#现对计算的余弦排序
        sorted_ind=[]#用于存放排序后的下标
        for i in sorted_angle:
            m=angle.index(i)+1
            while m in sorted_ind:
                m+=1
            sorted_ind.append(m)
        temp_poi=m2_poi.copy()
        for k,s_k in zip(range(N),sorted_ind):#问题就在这儿！！！！！
            m2_poi[k+1]=temp_poi[s_k]
            
        if count==1:#因为第一次时，已经确定第二个点一定是凸包上的点，所以直接跳过
            pass
        else:
            while sorted_angle[final_k-1]<last_angle:
                 final_k+=1
                 
        last_angle=sorted_angle[final_k-1]
        
        final_x=np.append(final_x,m2_poi[final_k][0])
        final_y=np.append(final_y,m2_poi[final_k][1])
        m2_poi[1],m2_poi[final_k]=m2_poi[final_k],m2_poi[1]
        count+=1
        if (m2_poi[1]==np.array(my_point[1])).all():
            break
    final_x=np.append(final_x,my_point[1][0])
    final_y=np.append(final_y,my_point[1][1])
    
    return final_x,final_y    
    
def show_graph(final_x,final_y):
    '''
    显示凸包图形,参数为凸包顶点的x坐标集合final_x和y坐标集合final_y
    '''
    print "凸包图形"
    plt.figure(u"凸包图形")
    min_x=min(final_x)
    max_x=max(final_x)
    min_y=min(final_y)
    max_y=max(final_y)
    plt.xlim(min_x-max_x/10,max_x+max_x/10)
    plt.ylim(min_y-max_y/10,max_y+max_y/10)
    plt.plot(re_x,re_y,'.b')
    plt.plot(final_x,final_y,'r')
    plt.show()

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

if __name__ == '__main__' : 
    sign=(input(u"随机产生点>'1',或者手动输入点>'2':"))
    if sign==1:
        number=input(u"要产生多少随机点:")
        l=float(input(u"随机范围最小值:"))
        r=float(input(u"随机范围最大值:"))
        start=time.time()
        my_point=generate_point(number,l,r)
    elif sign==2:
        my_point=input_point()
    else:
        print "无效的选择"
    show_point(my_point)    
    final_x,final_y=aim_point(my_point)
    show_graph(final_x,final_y)
    print "所用时间{0}".format(time.time()-start)
