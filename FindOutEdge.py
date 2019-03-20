# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 15:51:50 2019

@author: XLI015
"""

"""
find the outline edge from a Bianry image
8 neighborhood
"""

import sys
import cv2
import numpy as np
from scipy.ndimage import label

def segment_on_dt(a, img):
    border = cv2.dilate(img, None, iterations=5)
    border = border - cv2.erode(border, None)

    dt = cv2.distanceTransform(img, 2, 3)
    dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(np.uint8)
    _, dt = cv2.threshold(dt, 180, 255, cv2.THRESH_BINARY)
    lbl, ncc = label(dt)
    lbl = lbl * (255 / (ncc + 1))
    # Completing the markers now. 
    lbl[border == 255] = 255

    lbl = lbl.astype(np.int32);
    print(lbl.shape)
    cv2.watershed(a, lbl)

    lbl[lbl == -1] = 0
    lbl = lbl.astype(np.uint8)
    return 255 - lbl


def fill(img,n=4):
     """
     fill the edge
     default 4 neighborhood
     """
     neighbor = get_neighbor(n);
     w,h = img.shape;
     img_copy = img.copy();
     for i in range(1,w-1):
          for j in range(1,h-1):
               if(img[i][j] == 255): #白色点
                 for ne in neighbor:
                      img_copy[i+ne[0],j+ne[1]] = 255;
     return img_copy;



def get_neighbor(n):
     if(n==4):
          return [(-1,0),(1,0),(0,-1),(0,-1)];
     if(n==8):
          return [(-1,0),(1,0),(0,-1),(1,0),(-1,-1),(1,1),(-1,1),(1,-1)];
     return [];


def remove_noise(img):
     """
     remove any point but point which is on a circle 
     """
     n,m = img.shape;
     img_cp = img.copy();
     for i in range(n):
          for j in range(m):
               if(img[i,j] == 255):
                    if(not isoncircle(img,i,j)):
                         img_cp[i,j] = 0;
     return img_cp;

def isoncircle(img,i,j):
     """
     determine if the point is on a closed curve
     come back and without repeating
     """
     return 0;

img = cv2.imread("F:\\project_python\\my\\output\\image_gray\\25-65-CW_79.tif");
#Pre-processing.
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
#img_edge = cv2.Canny(img_gray,80,100);  
_, img_bin = cv2.threshold(img_gray, 0, 255,
        cv2.THRESH_OTSU)
img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN,np.ones((3,3),dtype=int))

result = segment_on_dt(img, img_bin)
#cv2.imwrite("output\\25.3-89-CW=20-result.tif", result)
result[result != 255] = 0
#result = cv2.dilate(result, None)
#img[result == 255] = (0, 0, 255)
cv2.imwrite("output\\25-65-CW_79-edgeimg.tif",result);

fill_result = fill(result);
cv2.imwrite("output\\25-65-CW_79-imgfill.tif",fill_result);
