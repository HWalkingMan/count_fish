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




img_src=cv.imread('G:/fish.jpg')

add_pic('src',img_src)

img_gray=cv.cvtColor(img_src,cv.COLOR_BGR2GRAY)

add_pic('gray',img_gray)

# 双边滤波
# img_bilater = cv.bilateralFilter(img_gray,9,75,75)
# add_pic('bilater',img_bilater)
#由于鱼苗过小，很容易被误认为噪音，考虑去除滤波操作
img_gray[img_gray>220]=190

sobelx = cv.Sobel(img_gray,cv.CV_64F, 1, 0,ksize=3)
sobely = cv.Sobel(img_gray, cv.CV_64F, 0, 1, ksize=3)

sobelx_abs=cv.convertScaleAbs(sobelx)
sobely_abs=cv.convertScaleAbs(sobely)

img_sobelXY=cv.addWeighted(sobelx_abs,0.5,sobely_abs,0.5,10)

add_pic('sobelXY',img_sobelXY)

img_bilater = cv.bilateralFilter(img_sobelXY,9,75,75)
add_pic('bilater',img_bilater)

# ret,sobelXY_2v=cv.threshold(img_sobelXY,50,255,cv.THRESH_BINARY)
#
# add_pic('sobelXY_2v',sobelXY_2v)

#sobel_gray=cv.cvtColor(img_src,cv.COLOR_BGR2GRAY)
# add_pic('sobel_gray',sobel_gray)
# #可能无用
#非但无用，反而会抹除全部的鱼


sobel_anti=np.array(img_bilater)
sobel_anti=255-sobel_anti
add_pic('sobel_anti',sobel_anti)

# img_bilater_2 = cv.bilateralFilter(sobel_anti,9,75,75)
# add_pic('bilater_2',img_bilater_2)

kernel=np.ones((1,1),np.uint8) #进行腐蚀膨胀操作
# erosion=cv.erode(img_bilater_2,kernel,iterations=5)
erosion=cv.erode(sobel_anti,kernel,iterations=3)
add_pic('erosion',erosion)

# dilation=cv.dilate(erosion,kernel,iterations=5)
# add_pic('dilation',dilation)

ret,soimg=cv.threshold(erosion,140,255,cv.THRESH_BINARY)
add_pic('soimg',soimg)


# img=cv.imread('G:/fish-sobel.jpg')
#
# img_b = cv.bilateralFilter(img,9,75,75)
#
# gray=access_pixels(img_b)
# gray=cv.cvtColor(gray,cv.COLOR_BGR2GRAY)
#
#
# kernel=np.ones((2,2),np.uint8) #进行腐蚀膨胀操作
# erosion=cv.erode(gray,kernel,iterations=5)
# dilation=cv.dilate(erosion,kernel,iterations=5)
#
# ret,soimg=cv.threshold(dilation,50,255,cv.THRESH_BINARY)
# cv.imshow('so',)

contours,hirearchy=cv.findContours(soimg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)# 找出连通域

img_dst=np.array(img_src)
img_dst_soimg=np.array(soimg)

area=[] #建立空数组，放连通域面积
contours1=[]   #建立空数组，放减去后的数组
for i in contours:
    # area.append(cv.contourArea(i))
    # print(area)
    if cv.contourArea(i)>2:  # 计算面积 去除面积小的 连通域
        contours1.append(i)
print(len(contours1)-1) #计算连通域个数
draw=cv.drawContours(img_dst,contours1,-1,(0,255,0),1) #描绘连通域

draw=cv.drawContours(img_dst_soimg,contours1,-1,(0,255,0),1) #描绘连通域

add_pic('dst',img_dst)

add_pic('dst_soimg',img_dst_soimg)

# show_process_pic()




