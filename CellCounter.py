# -*- coding: utf-8 -*-
"""
Bacteria counter
 
    Counts blue and white bacteria on a Petri dish
 
    python bacteria_counter.py -i [imagefile] -o [imagefile]
 
@author: Alvaro Sebastian (www.sixthresearcher.com)
"""
 
# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2
  
# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#     help="path to the input image")
# ap.add_argument("-o", "--output", required=True,
#     help="path to the output image")
# args = vars(ap.parse_args())
  
# dict to count colonies
counter = {}
 
# load the image
image_orig = cv2.imread(".\\input\\25.3-89.tif")
height_orig, width_orig = image_orig.shape[:2]
 
# output image with contours
image_contours = image_orig.copy()

image_to_process = image_orig.copy()

image_gray = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY)
cv2.imshow('cvtColor',image_gray)
cv2.waitKey(0)
cv2.destroyAllWindows() 
# image_gaussianBlur = cv2.GaussianBlur(image_gray, (5, 5), 0)
# cv2.imshow('GaussianBlur',image_gaussianBlur)
# cv2.waitKey(0)
# cv2.destroyAllWindows() 

# perform edge detection, then perform a dilation + erosion to close gaps in between object edges
image_cannyEdged = cv2.Canny(image_gray, 50, 100)
cv2.imshow('CannyEdged',image_cannyEdged)
cv2.waitKey(0)
cv2.destroyAllWindows() 

image_dilateEdged = cv2.dilate(image_cannyEdged, None, iterations=1)
cv2.imshow('DilateEdged',image_dilateEdged)
cv2.waitKey(0)
cv2.destroyAllWindows() 

image_erodeEdged = cv2.erode(image_dilateEdged, None, iterations=1)
cv2.imshow('ErodeEdged',image_erodeEdged)
cv2.waitKey(0)
cv2.destroyAllWindows() 

cnts = cv2.findContours(image_erodeEdged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

cv2.imshow('findContours',image_erodeEdged)
cv2.waitKey(0)
cv2.destroyAllWindows() 

# loop over the contours individually
counter = 0
for c in cnts:

    ctr = np.array(c).reshape((-1,1,2)).astype(np.int32)
    # prints contours in green color
    cv2.drawContours(image_contours,[ctr],0,(0,255,0),-1)
    counter = counter +1
print(counter)

    #cv2.putText(image_contours, "{:.0f}".format(cv2.contourArea(c)), (int(hull[0][0][0]), int(hull[0][0][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

# Print the number of colonies of each color
#print("{} {} colonies".format(counter[color],color))
 
# Writes the output image
cv2.imwrite("\\output\\output.tif",image_contours)