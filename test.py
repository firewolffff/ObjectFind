# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageEnhance
import imutils
import cv2
import numpy as np

"""
#原始图像
image = Image.open('input\\25-58-CW=79.tif')
image.show()

#色度增强
enh_col = ImageEnhance.Color(image)
color = 1.5
image_colored = enh_col.enhance(color)
#image_colored.show()
image_colored.save("output\\25-58-CW=79_color.tif")
 
#对比度增强
enh_con = ImageEnhance.Contrast(image)
contrast = 1.5
image_contrasted = enh_con.enhance(contrast)
#image_contrasted.show()
image_contrasted.save("output\\25-58-CW=79_contrast.tif")


#锐度增强

enh_sha = ImageEnhance.Sharpness(image)
sharpness = 3.0
image_sharped = enh_sha.enhance(sharpness)
#image_sharped.show()
image_sharped.save("output\\25-58-CW=79_sharpness.tif")
"""

"""
image_orig = cv2.imread("input\\25.3-89.tif")
height_orig, width_orig = image_orig.shape[:2];
     
# output image with contours
image_contours = image_orig.copy();

image_to_process = image_orig.copy();

image_gray = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY);

# perform edge detection, then perform a dilation + erosion to close gaps in between object edges
image_cannyEdged = cv2.Canny(image_gray, 50, 100);
#dilate edge to eliminate noise
image_dilateEdged = cv2.dilate(image_cannyEdged, None, iterations=1);
#erode edge to separate point
image_erodeEdged = cv2.erode(image_dilateEdged, None, iterations=1);
#find point and its edge
im,contours, hierarchy = cv2.findContours(image_erodeEdged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);
print("the contours is {0}".format(len(contours)));
"""

"""
image_orig = cv2.imread(".\\input\\25.3-89.tif");
image_gray = cv2.cvtColor(image_orig, cv2.COLOR_BGR2GRAY);
for i in range(30,80,10):
     for j in range(100,150,10):
          image_cannyEdged = cv2.Canny(image_gray, i, j);
          cv2.imwrite("output\\25.3-89-"+ str(i)+'-' + str(j)+".tif",image_cannyEdged);
#          cv2.imshow('CannyEdged',image_cannyEdged)
#          cv2.waitKey(0)
#          cv2.destroyAllWindows() 

"""
def imconv(image_array,suanzi):
    '''计算卷积
        image_array 原灰度图像矩阵
        suanzi      算子
        原图像与算子卷积后的结果矩阵
    '''
    image = image_array.copy()     # 原图像矩阵的深拷贝
    
    dim1,dim2 = image.shape;
    m,n = suanzi.shape;

    # 对每个元素与算子进行乘积再求和(忽略最外圈边框像素)
    for i in range(0,dim1-m):
        for j in range(0,dim2-n):
            temp = image_array[i:m+i,j:n+j];
            image[i,j] = np.multiply(temp,suanzi).sum();
    
    # 由于卷积后灰度值不一定在0-255之间，统一化成0-255
    image = image*(255.0/image.max())

    # 返回结果矩阵
    return image

import matplotlib.pyplot as plt
import os;

#files = os.listdir("output\\contours")
#for f in files:
#     filepath = "output\\contours\\" + f;
#     con = cv2.imread(filepath);
#     image_gray = cv2.cvtColor(con, cv2.COLOR_BGR2GRAY)
#     circle = cv2.HoughCircles(image_gray, cv2.HOUGH_GRADIENT, 1, 180, param1=100, param2=50, minRadius=200, maxRadius=800);
#     if(isinstance(circle,type(np.array(0)))):
#          circle = circle[0,:,:];
#          cv2.circle(con,(circle[0][0],circle[0][1]),circle[0][2],(255,0,0),5);
#          cv2.imwrite("output\\circle\\"+f,con);
#     else:
#          continue;
import sys

if __name__ == '__main__':
     params = sys.argv[1:];
     #获取参数
     #参数输入格式 image=value image_dir=value save_dir=value
     dic = {};
     image_list = [];
     print(params);
     for param in params:
          pv = param.split('=');
          assert len(pv)==2;
          dic[pv[0]] = pv[1];
     
     if('save_dir' in dic):
          if(not os.path.exists(dic['save_dir'])):
               os.mkdir(dic['save_dir']);
          elif(not os.path.isdir(dic['save_dir'])):
               print("{} is not a directory,please check and try again".format(dic['save_dir']));
               sys.exit(0);
     else:
          print('there is not directory to save the result.please set it by save_dir=value.');
          sys.exit(0);
     
     if(not ('image' in dic or 'image_dir' in dic)):
          print('one of the image and image_dir should be set.set by image=value image_dir=value');
          sys.exit(0);
          
     if('image' in dic):
          if(not os.path.exists(dic['image'])):
               print('the file {0} does not exist'.format(dic['image']));
               sys.exit(0);
          else:
               #check if it is a picture
               f = os.path.split(dic['image'])[1];
               extension = os.path.splitext(f)[1];
               if(extension.lower() in ['.jpg','.png','.tif','.jpeg']):
                    image_list.append(dic['image']);
               else:
                    print("the file {0} is not a picture.please check and try again".format(dic['image']));
                    sys.exit(0);
     
     if('image_dir' in dic):
          if(os.path.exists(dic['image_dir'])):
               if(os.path.isdir(dic['image_dir'])):
                    files = os.listdir(dic['image_dir']);
                    file_path = [os.path.join(dic['image_dir'],f) for f in files];
                    image_list.extend(file_path);
               else:
                    print("the path {0} is not a directory.please check and try again".format(dic['image_dir']));
                    sys.exit(0);
               
          else:
               print("the image_dir {0} does not exist.please check and try again".format(dic['image_dir']));
               sys.exit(0);
     
     print(dic);
     