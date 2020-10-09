import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime

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


img_src=cv.imread('G:/fish_.jpg')

add_pic('src',img_src)

img_gray=cv.cvtColor(img_src,cv.COLOR_BGR2GRAY)

add_pic('gray',img_gray)

img_gray[img_gray>220]=190

sobelx = cv.Sobel(img_gray,cv.CV_64F, 1, 0,ksize=3)
sobely = cv.Sobel(img_gray, cv.CV_64F, 0, 1, ksize=3)

sobelx_abs=cv.convertScaleAbs(sobelx)
sobely_abs=cv.convertScaleAbs(sobely)

img_sobelXY=cv.addWeighted(sobelx_abs,0.5,sobely_abs,0.5,10)

add_pic('sobelXY',img_sobelXY)

img_bilater = cv.bilateralFilter(img_sobelXY,9,75,75)
add_pic('bilater',img_bilater)

sobel_anti=np.array(img_bilater)
sobel_anti=255-sobel_anti
add_pic('sobel_anti',sobel_anti)

kernel=np.ones((1,1),np.uint8) #进行腐蚀膨胀操作
# erosion=cv.erode(img_bilater_2,kernel,iterations=5)
erosion=cv.erode(sobel_anti,kernel,iterations=3)
add_pic('erosion',erosion)

ret,soimg=cv.threshold(erosion,140,255,cv.THRESH_BINARY)
add_pic('soimg',soimg)

contours,hirearchy=cv.findContours(soimg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)# 找出连通域
contours_i2=[]
p = hirearchy[0][0][2]
while p!=-1:
    contours_i2.append(contours[p])
    p=hirearchy[0][p][0]

contours_i3=[]
p = hirearchy[0][0][2]
while p!=-1:
    q = hirearchy[0][p][2]
    while q != -1:
        contours_i3.append(contours[q])
        q = hirearchy[0][q][0]
    p=hirearchy[0][p][0]



area=[] #建立空数组，放连通域面积
contours_sl2=[]   #建立空数组，放减去后的数组
contours_sb2=[]
for i in contours_i2:
    # area.append(cv.contourArea(i))
    # print(area)
    if cv.contourArea(i)<=2:  # 计算面积 去除面积小的 连通域
        contours_sl2.append(i)
    else:
        contours_sb2.append(i)
print('fish less than 2',len(contours_sl2)) #计算连通域个数
print('fish more than 2',len(contours_sb2)) #计算连通域个数

img_dst=np.array(img_src)
img_dst_soimg=cv.cvtColor(img_gray,cv.COLOR_GRAY2BGR)


draw=cv.drawContours(img_dst,contours_sl2,-1,(0,255,0),1) #描绘连通域

# draw=cv.drawContours(img_dst_soimg,contours2,-1,(0,255,0),1) #描绘连通域
draw=cv.drawContours(img_dst_soimg,contours_i3,-1,(0,0,255),1)
draw=cv.drawContours(img_dst_soimg,contours_sl2,-1,(0,255,255),1)
draw=cv.drawContours(img_dst_soimg,contours_sb2,-1,(0,255,0),1)
add_pic('dst',img_dst)

add_pic('dst_soimg',img_dst_soimg)