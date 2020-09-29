import cv2 as cv
import matplotlib.pyplot as plt
import os



# img=cv.imread('G:/fish.jpg')
# cv.imshow('abc',img)
# k = cv.waitKey(0)
# cv.imwrite('../../../src/res/first/temp.jpg',img)
# print(os.path.abspath('../../../src/res/first/temp.jpg'))

# gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

# cv.imwrite('../../../src/res/first/temp.jpg',gray)

def show_pic(name,img):
    cv.imshow(name,img)
    cv.waitKey(0)

def save_pic(name,img):
    cv.imwrite('../../../src/res/first/'+name+'.jpg',img)

img=cv.imread('G:/fish.jpg')
gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

ret,im_fixed1=cv.threshold(gray,100,255,cv.THRESH_BINARY)
ret,im_fixed2=cv.threshold(gray,110,255,cv.THRESH_BINARY)
ret,im_fixed3=cv.threshold(gray,105,255,cv.THRESH_BINARY)
ret,im_fixed4=cv.threshold(gray,102,255,cv.THRESH_BINARY)
ret,im_fixed5=cv.threshold(gray,107,255,cv.THRESH_BINARY)
ret,im_fixed6=cv.threshold(gray,115,255,cv.THRESH_BINARY)

titles = ['100','110', '105', '102', '107','115']
imgs = [im_fixed1, im_fixed2, im_fixed3, im_fixed4, im_fixed5, im_fixed6]

for i in range(6):
    save_pic('2val-'+titles[i],imgs[i])
#     plt.subplot(2,3,i+1)#注意，这和matlab中类似，没有0，数组下标从1开始
#     plt.imshow(imgs[i])
#     plt.title(titles[i])
# plt.show()





# 均值滤波
img_mean = cv.blur(img, (5,5))
# 高斯滤波
img_Guassian = cv.GaussianBlur(img,(5,5),0)
# 中值滤波
img_median = cv.medianBlur(img, 5)
# 双边滤波
img_bilater = cv.bilateralFilter(img,9,75,75)
# 展示不同的图片


titles = ['srcImg','mean', 'Gaussian', 'median', 'bilateral']
imgs = [img, img_mean, img_Guassian, img_median, img_bilater]

for i in range(5):
    save_pic(titles[i],imgs[i])
#     plt.subplot(2,3,i+1)#注意，这和matlab中类似，没有0，数组下标从1开始
#     plt.imshow(imgs[i])
#     plt.title(titles[i])
# plt.show()


'''双边滤波效果最好'''



exit(0)
