# -*- coding: utf-8 -*-
"""
author xli015
datetime 2019-02-27 10:00:00
"""
 
# import the necessary packages
import numpy as np
from PIL import ImageEnhance,Image
import cv2
import os
  
# dict to count colonies
def EnhanceImage(image):
    #色度增强
    enh_col = ImageEnhance.Color(image);
    color = 1.5;
    image_colored = enh_col.enhance(color);

    return np.array(image_colored);


def ContourFilter(contours,min_area,max_area,rate):
     """
     contours 轮廓位置坐标数组
     min_area 轮廓围成的区域的最小面积
     max_area 轮廓围成的区域的最大面积
     轮廓先要满足min_area 和 max_area 条件，然后需要满足包含轮廓的最小矩形的长宽比小于rate
     """
     con = [];
     max_max_area = 0;
     select_max_area = 0;
     select_min_area = 1000;
     for c in contours:   
          a = cv2.contourArea(c);
          if(a>max_max_area):
               max_max_area = a;
          if((a > min_area) and (a < max_area)):
               min_rect = cv2.minAreaRect(c);
               #width 不一定比 height 小
               width = min_rect[1][0];
               height = min_rect[1][1];
               if(not (width/height > rate or height/width > rate)):
                    if(a > select_max_area):
                         select_max_area = a;
                    if(a<select_min_area):
                         select_min_area = a;
                    con.append(c);
          else:
               continue;
                    
     return con,max_max_area,select_max_area,select_min_area;


for f in os.listdir("output\\change_progress\\"):
     filepath = "output\\change_progress\\" + f;
     if(os.path.isfile(filepath)):
          os.remove(filepath);

files = os.listdir("input");
for f in files:
     # load the image
     filepath = "input\\"+f;
     filename = os.path.splitext(f)[0];
     image = Image.open(filepath);
     image_changed = EnhanceImage(image);
     
     
     assert len(image_changed.shape) == 3;
     image_orig = image_changed[:,:,:3];
         
     if(not isinstance(image_orig,type(np.array(0)))):
         image_orig = np.array(image_orig);
     height_orig, width_orig,chenal = image_orig.shape;
     
     # output image with contours
     image_contours = image_orig.copy();
     image_to_process = image_orig.copy();
         
     image_gray = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY);
        
     # perform edge detection, then perform a dilation + erosion to close gaps in between object edges
     image_cannyEdged = cv2.Canny(image_gray, 50, 120);
     #cv2.imshow('image_cannyEdged',image_cannyEdged)
     
     #add edge mask
#     # Pre-processing.   
#     _, img_bin = cv2.threshold(image_gray, 0, 255,
#             cv2.THRESH_OTSU)
#     img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN,np.ones((3,3),dtype=int))
     
#     result = segment_on_dt(image_orig, image_cannyEdged);
#     result[result != 255] = 0
#     result = fill(result,4);
#     cv2.imwrite("output\\contours\\"+f,result);
#     #image_erodeEdged 边界线条粗
#     image_cannyEdged[[result==255]] = 255
     
     dilatekernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2));
     #dilate edge to eliminate noise
     image_dilateEdged = cv2.dilate(image_cannyEdged, dilatekernel, iterations=1);
     
     dilatekernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)); 
     #dilate edge to eliminate noise
     image_dilateEdged = cv2.dilate(image_dilateEdged, dilatekernel, iterations=1);
     
     
     
#     cv2.imshow('image_dilateEdged',image_dilateEdged);
         
#     errodekernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2),anchor=(0,0));
#     #erode edge to separate point
#     image_erodeEdged = cv2.erode(image_dilateEdged, errodekernel, iterations=1);
#     
#     errodekernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2),anchor=(1,1));
#     #erode edge to separate point
#     image_erodeEdged = cv2.erode(image_erodeEdged, errodekernel, iterations=1);
     
#     errodekernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2),anchor=(-2,-2));
#     #erode edge to separate point
#     image_erodeEdged = cv2.erode(image_erodeEdged, errodekernel, iterations=1);
     
#     cv2.imshow('image_erodeEdged',image_erodeEdged);
#     cv2.waitKey(0);
#     cv2.destroyAllWindows();
     #find point and its edge
     im,contours, hierarchy = cv2.findContours(image_dilateEdged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE);
     print("the {0} is {1}".format(f,len(contours)));
     
     contours_filter,max_area,select_max_area,select_min_area = ContourFilter(contours,10.5,115,1.8);
     
     print("the {0} contour max area is {1}".format(f,max_area));
     print("the {0} selected contour max area is {1} the min aera is {2}".format(f,select_max_area,select_min_area));
     number = len(contours_filter);
     
     for cnt in contours_filter:
          min_rect = cv2.minAreaRect(cnt);
          min_rect = np.int0(cv2.boxPoints(min_rect));
          cv2.drawContours(image_contours,[min_rect],-1,(12,12,12),2);
     #draw point edge
     #cv2.drawContours(image_contours, contours, -1, (12,12,12));
     cv2.imwrite("output\\change_progress\\fillter-allcontours-"+ filename+"-"+str(number)+".tif",image_contours);
    

"""
#效果不错 3-4 15：28
dilatekernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2));
#dilate edge to eliminate noise
image_dilateEdged = cv2.dilate(image_cannyEdged, dilatekernel, iterations=1);

dilatekernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)); 
#dilate edge to eliminate noise
image_dilateEdged = cv2.dilate(image_dilateEdged, dilatekernel, iterations=1);

im,contours, hierarchy = cv2.findContours(image_dilateEdged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE);
print("the {0} is {1}".format(f,len(contours)));

contours_filter,max_area,select_max_area,select_min_area = ContourFilter(contours,10.5,115,1.8);
"""