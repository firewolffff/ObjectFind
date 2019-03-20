# -*- coding: utf-8 -*-
"""
author xli015
datetime 2019-02-27 15:30:00
reference http://www.cnblogs.com/chnhideyoshi/p/FindMaxima.html
"""
from PIL import Image
import numpy as np

class Int16Double:
    def __init__(self,x,y):
        self.X = x;
        self.Y = y;
        
class Int16DoubleWithValue:
    def __init__(self,x, y, value):
        self.X = x;
        self.Y = y;
        self.V = value;

    def CompareTo(self,other):
        r = 0;
        if(self.V < other.V):
            r = -1;
        if(self.V > other.V):
            r = 1;
        return -r;
    
class BitMap2d:
     def __init__(self,width,height,v):
          self.width = width;
          self.height = height;
          self.data = [float(v) for i in range(width*height)];
   
     def SetPixel(self, x, y, v):
          self.data[x + y * self.width] = v;
   
     def GetPixel(self,x, y):
          return self.data[x + y * self.width];
     """
    def ReadRaw(self,path):
        sr = Image.open(path);

        for i in range(self.width * self.height):
            floatBytes = sr.ReadBytes(4);

            # swap the bytes

            temp = floatBytes[0];

            floatBytes[0] = floatBytes[3];

            floatBytes[3] = temp;

            temp = floatBytes[1];

            floatBytes[1] = floatBytes[2];

            floatBytes[2] = temp;

            # get the float from the byte array

            value = BitConverter.ToSingle(floatBytes, 0);
            data[i] = value;
        return;
        """
     def MakeBmp(self):
          min_ = 256;
          max_ = -1;
          for i in range(self.width):
               for j in range(self.height):
                    r = self.GetPixel(i,j);
                    if(r > max_):
                         max_ = r;
                    if(r < min_):
                         min_ = r;
          delta=max_ - min_;
          bmp = np.zeros((self.width,self.height,3),dtype=np.uint8);
          for i in range(self.width):
               for j in range(self.height):
                    r = self.GetPixel(i,j);
                    b = int(255 * (r - min_) / delta);
                    bmp[i,j] = b;
          return bmp;

class FlagMap2d:
    def __init__(self,width, height, v):
        self.width = width;
        self.height = height;
        self.action_get_count = 0;
        self.action_set_count = 0;
        self.flags = [v for i in range(width * height)];
        
    def SetFlagOn(self,x, y, v):
        self.flags[x + y * self.width] = v;
        self.action_set_count = self.action_set_count + 1;
        
    def GetFlagOn(self,x, y):
        self.action_get_count = self.action_get_count + 1;
        return self.flags[x + y * self.width];

    
class MaximunFinder:
     UNPROCESSED = 0;
     VISITED = 1;
     PROCESSED = 2;
    
     Delta = [Int16Double(-1,-1),Int16Double(-1,0),Int16Double(-1,1),Int16Double(0,-1),
             Int16Double(0,1),Int16Double(1,-1),Int16Double(1,0),Int16Double(1,1)];

     def __init__(self,bmp, torlerance):
          """
          bmp BitMap2d
          """
          self.bmp = bmp;
          self.torlerance = torlerance;

     def FindMaxima(self):
          list_ = self.FindLocalMaxima();
          sorted(list_,key=lambda x:x.V);
          flag = FlagMap2d(self.bmp.width,self.bmp.height,0);
          r = [];
          temp = [];
          for i in range(len(list_)):
               if (flag.GetFlagOn(list_[i].X, list_[i].Y) == MaximunFinder.UNPROCESSED):
                    ret = self.FloodFill(list_[i].X, list_[i].Y,temp,flag);
                    if (ret):
                         r.append(list_[i]);
                         self.MarkAll(temp, MaximunFinder.PROCESSED, flag);
                    else:
                         self.MarkAll(temp, MaximunFinder.UNPROCESSED, flag);
                         flag.SetFlagOn(list[i].X, list[i].Y, MaximunFinder.PROCESSED);
               temp = [];
          
          return r;

     def FindLocalMaxima(self):
          list_ = [];
          for i in range(1,self.bmp.width - 1):
               for j in range(1, self.bmp.height - 1):
                    if (self.IsMaxima(i, j)):
                         list_.append(Int16DoubleWithValue(i, j,self.bmp.GetPixel(i,j)));
             
          return list_;
   
     def IsMaxima(self, i, j):
          v = self.bmp.GetPixel(i, j);
          b1 = v > self.bmp.GetPixel(i - 1, j - 1);
          b2 = v > self.bmp.GetPixel(i, j - 1);
          b3 = v > self.bmp.GetPixel(i +1, j - 1);
          
          b4 = v > self.bmp.GetPixel(i - 1, j);
          b5 = v > self.bmp.GetPixel(i + 1, j);
          
          b6 = v > self.bmp.GetPixel(i - 1, j + 1);
          b7 = v > self.bmp.GetPixel(i, j + 1);
          b8 = v > self.bmp.GetPixel(i + 1, j + 1);
          return b1 & b2 & b3 & b4 & b5 & b6 & b7 & b8;
   

     def FloodFill(self, x, y, ret, flag):
          """
          ret list[Int16Double]
          flag FlagMap2d
          """
          ret = [];
          queue = [];
          ret.append(Int16Double(x, y));
          pvalue = self.bmp.GetPixel(x, y);
          flag.SetFlagOn(x, y, MaximunFinder.VISITED);
          queue.append(Int16Double(x, y));
          while (len(queue) != 0):
               p = queue.pop(0);
               for i in range(8):
                    tx = p.X + MaximunFinder.Delta[i].X;
                    ty = p.Y + MaximunFinder.Delta[i].Y;
                    if(self.InRange(tx, ty)):
                         f= flag.GetFlagOn(tx,ty);
                         if(f == MaximunFinder.PROCESSED):
                              return False;
                         else:
                              minum = [False];
                         if (self.IncludePredicate(tx, ty, pvalue,minum) & f == MaximunFinder.UNPROCESSED):
                              if (minum[0]):
                                   return False;
                              t = Int16Double(tx, ty);
                              queue.append(t);
                              flag.SetFlagOn(tx, ty, MaximunFinder.VISITED);
                              ret.append(t);
          return True;

     def InRange(self, tx, ty):
          return tx >= 0 & tx < self.bmp.width & ty >= 0 & ty < self.bmp.height;

     def IncludePredicate(self, x, y, pv, min_):
          """min_ 引用传递"""
          v = self.bmp.GetPixel(x, y);
          if (pv < v):
               min_[0] = True;
          return pv - v <= self.torlerance;

     def MarkAll(ret, v, flag):
          """
          ret list[Int16Double]
          flag FlagMap2d
          """
          for i in range(len(ret)):
               flag.SetFlagOn(ret[i].X, ret[i].Y, v);

image_orig = Image.open("input\\25.3-89.tif");
L = image_orig.convert('1');
img_arr = np.array(L);
height_orig, width_orig = img_arr.shape;
bmp = BitMap2d(width_orig,height_orig,0);

for i in range(height_orig):
     for j in range(width_orig):
          if(img_arr[i,j]):
               bmp.SetPixel(j,i,255);
          else:
               bmp.SetPixel(j,i,0);
          

maxima = MaximunFinder(bmp,100);
r = maxima.FindMaxima();
