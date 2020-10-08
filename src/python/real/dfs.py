import cv2 as cv
import numpy as np

img_src=cv.imread('I:\\workspace\\python\\count_fish\\src\\res\\real\\1008-170501\\7_soimg.jpg')
img_src=cv.cvtColor(img_src,cv.COLOR_BGR2GRAY)

img_src[img_src != 0]=1

vis = np.zeros(img_src.shape)
bound = []
bound_real=[]
def dfs(x, y, s1):
    if x >= 756 or x < 0 or y >= 745 or y < 0 or img_src[x][y] != 0:
        return 0
    if vis[x][y] == 1:
        return -1
    vis[x][y] = 1
    tmp = 0
    box = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
    flag = 0
    for b in box:
        tmp = dfs(x + b[0], y + b[1], s1)
        if tmp == 0 and flag == 0:
            bound[len(bound)-1].append([[y, x]])
            flag = 1
        if tmp == -1:
            tmp = 0
        s1 += tmp

    s1 += 1
    return s1

def solve():
    sums = 0
    sum2 = 0
    for x, line in enumerate(img_src):
        for y, num in enumerate(line):
            # print(img_src[x][y])
            # if img_src[x][y] == 0 :
            #     sums = sums + 1
            bound.append([])
            s1 = dfs(x, y, 0)
            sum2 += s1
            # print(bound[len(bound)-1])
            if len(bound[len(bound)-1]) < 4:
                bound.pop()
            if s1 >= 3:
                sums = sums + 1
    for ads in bound:
        bound_real.append(np.array(ads))
    return sums,sum2/70,sum2/90

def draw_pic():
    img = cv.imread('I:\\workspace\\python\\count_fish\\src\\res\\real\\1008-170501\\1_src.jpg')
    draw=cv.drawContours(img,bound_real,-1,(0,255,0),1) #描绘连通域
    cv.imwrite('g:/res.jpg', img)
    cv.imshow('',img)
    cv.waitKey(0)
