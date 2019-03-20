# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 09:31:08 2019

@author: XLI015
"""

import cv2
import numpy as np
import os


def select_loc(arr,w_offset,h_offset):
    """
    arr: the loc point,X = arr[:,0],Y = arr[:,1]
    w_offset: the baise of the X_i and X_j.abs(X_i - X_j)<w_offset
    h_offset: the baise of the Y_i and Y_j.abs(Y_i - Y_j)<h_offset
    """
    arr_c = arr.copy();
    N = len(arr);
    for i in range(N-1):
        for j in range(i+1,N):
            if(abs(arr_c[i][0] - arr_c[j][0])<w_offset and abs(arr_c[i][1] - arr_c[j][1])<h_offset): 
                arr_c[j][0] = int((arr_c[i][0] + arr_c[j][0])/2);
                arr_c[j][1] = int((arr_c[i][1] + arr_c[j][1])/2);
                
                arr_c[i][0] = -1;
                arr_c[i][1] = -1;
    
    selected = arr_c[np.where(arr_c!=-1,True,False)].reshape(-1,2)
    return selected;


def read_mask(mask_path):
     """
     mask_path: the file path of the mask image
     mask file name must be fit the example filename#num.[tif,png,jpg]. num is in (0,1)
     return: mask of gray image arr,the minimum width in the masks, the mininum height in the masks
     """
     dic = {};
     filelist = os.listdir(mask_path);
     min_width = 200;
     min_height = 200;
     max_width = 0;
     max_height = 0;
     for file in filelist:
          filepath = os.path.join(mask_path,file);
          extension = os.path.splitext(file)[1]; 
          if(extension.lower() not in ['.tif','.png','.jpg','.jpeg']):
               continue;
          template = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE);
          h,w = template.shape;
          if(h < min_height):
               min_height = h;
          if(w < min_width):
               min_width = w;
          
          if(h > max_height):
               max_height = h;
          if(w > max_width):
               max_width = w;
               
          filewholename = os.path.splitext(file)[0];
          
          name_num = filewholename.split('#');
          assert len(name_num) == 2;
          tdic = {'image':template,'threshold':float(name_num[1])};
          dic[name_num[0]] = tdic;
     return dic,min_width,min_height,max_width,max_height;

def match(masks_gray,image_gray,w_offset,h_offset):
     """
     masks_gray:dict. the mask dict{imagename:{'image':value,'threshold':value},....}
     image_gray: array. the gray image of the image has target point
     w_offset: the baise of the horizontal axis
     h_offset: the baise of the vertical axis
     return: array. the locations of the target points
     """
     X = [];
     Y = [];
     for k in masks_gray.keys():
          mask = masks_gray[k];
          template_result = cv2.matchTemplate(image, mask['image'], cv2.TM_CCOEFF_NORMED);
          loc = np.where(template_result >= mask['threshold']);
          X.extend(list(loc[0]));
          Y.extend(list(loc[1]));
     
     arr = np.array([X,Y]);
     arr = arr.T;
     arr = select_loc(arr,w_offset,h_offset);
     return arr;

          
#image = cv2.imread(options.imageFileName, cv2.CV_LOAD_IMAGE_GRAYSCALE)
input_dir = "F:\\project_python\\my\\input";
file_list = os.listdir(input_dir);
masks_dic,min_width,min_height,max_width,max_height = read_mask("mask");

for file in file_list:
     filepath = os.path.join(input_dir,file);
     image_rgb = cv2.imread(filepath);
     image_process = image_rgb.copy();
     image = cv2.cvtColor(image_process, cv2.COLOR_BGR2GRAY)
     
     #find the edge to remove the background
     image_canny = cv2.Canny(image,60,120);
     dilatekernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5));
          #dilate edge to eliminate noise
     dilate = cv2.dilate(image_canny, dilatekernel, iterations=1);
     rows,cols = dilate.shape
     
     for i in range(rows):
         for j in range(cols):
             if dilate[i,j]==0:#0代表黑色的点
                 image_process[i,j,0]= 230;
                 image_process[i,j,1]= 231;
                 image_process[i,j,2]= 228;
          
#     cv2.imshow("image_withoutback_rgb",image_rgb);
#     cv2.waitKey(0);
#     cv2.destroyAllWindows();
#     cv2.imwrite("output\\remove_backgroud\\"+file,image_rgb);
     
     image = cv2.cvtColor(image_process, cv2.COLOR_BGR2GRAY)
     #
     # Template matching
     #
     loc = match(masks_dic,image,max_width,max_height);
     
     for pt in loc:
          right_bottom = (pt[1] + min_width, pt[0] + min_height);
          cv2.rectangle(image_rgb, (pt[1],pt[0]), right_bottom, (0, 0, 255), 2);
          
         
     cv2.imwrite(os.path.join("output","mask-"+file),image_rgb);
         # Exit on user pressing escape key