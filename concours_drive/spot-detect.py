# -*- coding: utf-8 -*-
"""
@author:    Williams BRETT
@date:      24-01-2019
@brief:     convert 16bits to 8bits, apply color mapping, adjust gamma, brightness and contrst auto 
"""

import numpy as np
import cv2
import os
from PIL import Image

def nothing(x):
    pass

def getsize(img):
    h, w = img.shape[:2]
    return w, h

def bytescaling(data, cmin=None, cmax=None, high=255, low=0):
    if data.dtype == np.uint8:
        return data
    if high > 255:
        high = 255
    if low < 0:
        low = 0
    if high < low:
        raise ValueError("`high` should be greater than or equal to `low`.")
    if cmin is None:
        cmin = data.min()
    if cmax is None:
        cmax = data.max()
    cscale = cmax - cmin
    if cscale == 0:
        cscale = 1
    scale = float(high - low) / cscale ; bytedata = (data - cmin) * scale + low
    return (bytedata.astype(np.uint8))
    
bins = np.arange(256).reshape(256,1)
def hist_curve(im, autoBC, activate):
    global Imin, Imax
    h = np.ones((300,256,3))
    h2 = np.ones((300,256,3))
    if len(im.shape) == 2:
        color = [(255,255,255)]
    elif im.shape[2] == 3:
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([im],[ch],None,[256],[0,256])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        cdf = hist.cumsum() #histogramm cumulé
        cdf_normalized = cdf / cdf.max() # between 0 et 1
        hist_normalized = hist / hist.max()  # between 0 et 1
        if autoBC == False:
            Imin = np.where(cdf_normalized>=0.01)[0][0]
            Imax  = np.where(cdf_normalized>=0.99)[0][0]
        #pts = np.int32(np.column_stack((bins,cdf_normalized)))
        #cv2.polylines(h,[pts],False,col)
        #cv2.polylines(h2,[pts],False,col)
        if activate == True :
            cv2.line(h,(Imax,300),(Imin,0),(255,0,0),1)
            cv2.line(h2,(Imax,300),(Imin,0),(255,0,0),1)
            i = 0
            for el in cdf_normalized :
                cv2.circle(h,(i,int(300*cdf_normalized[i])),1, (255,0,255), 1)
                i = i + 1
                if i > 0 and i < 256:
                    cv2.line(h,(i,int(300*cdf_normalized[i])),(i-1,int(300*cdf_normalized[i-1])),(255,0,255),1)
            i = 0
            for el in hist_normalized :
                cv2.circle(h2,(i,int(hist_normalized[i][0])),1, (255,0,255), 1)
                i = i + 1
                if i > 0 and i < 256 : 
                    cv2.line(h2,(i,int(300*hist_normalized[i])),(i-1,int(hist_normalized[i-1])),(255,0,255),1)
                      
    y = np.flipud(h) 
    y2 = np.flipud(h2) 
    return y,y2


if __name__ == "__main__":

    dir_masks='./training2/mask/'
    list_file=os.listdir(dir_masks)
    for fichier in list_file:
        if fichier.split('.')[1] == 'tiff':
            img_orig=cv2.imread(dir_masks+fichier,cv2.IMREAD_UNCHANGED)
            img_orig = bytescaling(img_orig)
            cv2.imshow('Origin',img_orig)
            curve, curve2 = hist_curve(img_orig,False,True)
            cv2.imshow('histogram_cumul',curve)
            cv2.imshow('histogram',curve2)
            
        if True:
            img_orig = bytescaling(img_orig)
            initial = img_orig.copy()
            blur = cv2.GaussianBlur(img_orig,(5,5),0)
            kernel = np.array((
        	        [-1, -1, -1, -1, -1],
        	        [-1, -1, -1, -1, -1],
        	        [-1, -1, 24, -1, -1],
        	        [-1, -1, -1, -1, -1],
        	        [-1, -1, -1, -1, -1]), dtype="int")
            convolution = cv2.filter2D(blur, -1, kernel)
            cv2.imshow('Laplacian',convolution)
            ret2,th2 = cv2.threshold(convolution,50,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            cv2.imshow('Thresh',th2)
            
            
            cv2.waitKey(0)