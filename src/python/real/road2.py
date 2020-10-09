import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
import sys
sys.setrecursionlimit(10000)
imgList={}


def count_fish(img):
    contours, hirearchy = cv.findContours(img, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_NONE)  # 找出连通域
    area = []  # 建立空数组，放连通域面积
    contours1 = []  # 建立空数组，放减去后的数组
    for i in contours:
        # area.append(cv.contourArea(i))
        # print(area)
        if cv.contourArea(i)>1:  # 计算面积 去除面积小的 连通域
            contours1.append(i)
    print(len(contours1) - 1)  # 计算连通域个数

def add_pic(name:str,img):
    imgList[name]=img

def show_process_pic():
    cols=len(imgList) / 3 +1
    for index,name in enumerate(imgList.keys()):

        plt.subplot(3,cols,index+1)#注意，这和matlab中类似，没有0，数组下标从1开始
        plt.imshow(imgList[name])
        plt.title(name)
    plt.show()

def output_precess():
    path='../../../src/res/real/'+str(datetime.datetime.now().strftime('%m%d-%H%M%S'))
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    for index,name in enumerate(imgList.keys()):
        cv.imwrite(path+'/'+str(index+1)+'_'+name+'.jpg',imgList[name])


img_src=cv.imread('G://fish_.jpg')
img_src=cv.cvtColor(img_src,cv.COLOR_BGR2GRAY)

vis = np.zeros(img_src.shape)
bound = []
bound_real=[]

# def su(g1, b1, r1, g2, b2 ,r2, delt):
#     # print(abs(b1 - b2))
#     if(abs(int(g1) - int(g2)) < delt and abs(int(b1) - int(b2)) < delt and abs(int(r1) - int(r2)) < delt):
#         return False
#     return True

def dfs(x, y, luminance):
    s1 = 0
    delt = 3

    if x >= img_src.shape[0] or x < 0 or y >= img_src.shape[1] or y < 0 or \
            luminance > 167 or luminance < 16 or\
            not (abs(int(luminance) - int(img_src[x][y])) < delt):
        return 0, 255

    if vis[x][y] == 1:
        return -1, 255
    allmax = img_src[x][y]
    if luminance<30:
        print(luminance)
    # print(x, y, abs(int(luminance) - int(img_src[x][y])))
    vis[x][y] = 1
    box = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    flag = 0
    for b in box:
        tmp, submax = dfs(x + b[0], y + b[1], img_src[x][y])
        if submax < allmax:
            allmax = submax
        if tmp == 0 and flag == 0:
            bound[len(bound)-1].append([[y, x]])
            flag = 1
        if tmp == -1:
            tmp = 0
        if tmp == -2:
            return -2, 255
        s1 += tmp

    s1 += 1
    if s1 > 60:
        return -2, 255
    return s1, allmax

def solve():
    sums = 0
    sum2 = 0
    for x, line in enumerate(img_src):
        for y, num in enumerate(line):
            # print(img_src[x][y])
            # if img_src[x][y] == 0 :
            #     sums = sums + 1
            bound.append([])
            s1, allmax = dfs(x, y, img_src[x][y])
            if s1 > 0 and allmax < 30:
                print(s1)
                sum2 += s1
            # print(img_src[x][y][0], img_src[x][y][1], img_src[x][y][2])
            if len(bound[len(bound)-1]) < 4:
                bound.pop()
            if s1 > 0 and allmax < 45:
                sums = sums + 1
    for ads in bound:
        bound_real.append(np.array(ads))
    return sums, sum2/70, sum2/90

def draw_pic():
    img = cv.imread('I:\\workspace\\python\\count_fish\\src\\res\\real\\1008-170501\\1_src.jpg')
    draw=cv.drawContours(img,bound_real,-1,(0,255,0),1) #描绘连通域
    cv.imwrite('g:/res.jpg', img)
    cv.imshow('',img)
    cv.waitKey(0)

