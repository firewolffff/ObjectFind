# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 13:21:56 2019

@author: XLI015
"""
import numpy as np
from PIL import ImageEnhance,Image
import cv2
import os
import sys

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
#     max_max_area = 0;
#     select_max_area = 0;
#     select_min_area = 1000;
     for c in contours:   
          a = cv2.contourArea(c);
#          if(a>max_max_area):
#               max_max_area = a;
          if((a > min_area) and (a < max_area)):
               min_rect = cv2.minAreaRect(c);
               #width 不一定比 height 小
               width = min_rect[1][0];
               height = min_rect[1][1];
               if(not (width/height > rate or height/width > rate)):
#                    if(a > select_max_area):
#                         select_max_area = a;
#                    if(a<select_min_area):
#                         select_min_area = a;
                    con.append(c);
          else:
               continue;
                    
     return con;

def CountObjectInImage(files,save_path):
     print("start to find object in image");
     n = len(files);
     for filepath in files:
          # load the image
          f = os.path.split(filepath)[1];
          filename = os.path.splitext(f)[0];
          image = Image.open(filepath);
          image_contours = np.array(image);
          
          image_changed = EnhanceImage(image);
          cv2.imwrite(save_path+"\\image_enhance\\"+filename+".tif",image_changed);
          
          assert len(image_changed.shape) == 3;
          image_to_process = image_changed[:,:,:3];
              
          image_gray = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY);
          cv2.imwrite(save_path+"\\image_gray\\"+filename+".tif",image_gray);   
          # perform edge detection, then perform a dilation + erosion to close gaps in between object edges
          image_cannyEdged = cv2.Canny(image_gray, 50, 120);
          
          dilatekernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3));
          #dilate edge to eliminate noise
          image_dilateEdged = cv2.dilate(image_cannyEdged, dilatekernel, iterations=2);
          cv2.imwrite(save_path+"\\image_dilate\\"+filename+".tif",image_dilateEdged);
          
          errodekernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8));
          #erode edge to separate point
          image_erodeEdged = cv2.erode(image_dilateEdged, errodekernel, iterations=1);
          cv2.imwrite(save_path+"\\image_erode\\"+filename+".tif",image_erodeEdged);
          #find point and its edge
          contours, hierarchy = cv2.findContours(image_erodeEdged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE);#cv2 version
          
          cv2.drawContours(image_to_process,contours,-1,(12,12,12),2);
          cv2.imwrite(save_path+"\\image_contours\\"+filename+".tif",image_to_process);
          
          contours_filter = ContourFilter(contours,3.5,50,2.5);
          
          number = 0;
          
          for cnt in contours_filter:
               min_rect = cv2.minAreaRect(cnt);
               min_rect = np.int0(cv2.boxPoints(min_rect));
               cv2.drawContours(image_contours,[min_rect],-1,(12,12,12),2);
               number = number + 1;
               
          #draw point edge
          #cv2.drawContours(image_contours, contours, -1, (12,12,12));
          cv2.imwrite(save_path +"\\image_contours_fillter\\"+ filename+"-"+str(number)+".tif",image_contours);
     
     print("This process  processed {0} images".format(n));
     print("end the proceess");

if __name__ == '__main__':
     params = sys.argv[1:];
     #获取参数
     #参数输入格式 image=value image_dir=value save_dir=value
     dic = {};
     image_list = [];
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
     
     CountObjectInImage(image_list,dic['save_dir']);
     sys.exit(0);
     
     
          
          
     
