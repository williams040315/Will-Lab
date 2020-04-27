# -*- coding: utf-8 -*-
"""
@author:    Williams BRETT
@date:      24-03-2020
@brief:     
"""

import numpy as np
import cv2
import os

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
    

tab_images=[]
tab_masks=[]
tab_images_name=[]
tab_masks_name=[]

if __name__ == "__main__":

    dir_images='./training2/original/Position2a-BF/'
    dir_masks='./training2//original/Position2a-RFP/'

    list_file=os.listdir(dir_images)
    for fichier in sorted(list_file):
        if fichier.split('.')[1] == 'tiff':
            print('Creating and change {}'.format(dir_images+fichier))
            tab_images.append(bytescaling(cv2.imread(dir_images+fichier,cv2.IMREAD_UNCHANGED)))
            tab_images_name.append(np.flipud(fichier.split('-'))[0])
            
    list_file=os.listdir(dir_masks)
    for fichier in sorted(list_file):
        if fichier.split('.')[1] == 'tiff':
            print('Creating and change {}'.format(dir_masks+fichier))
            tab_masks.append(cv2.imread(dir_masks+fichier,cv2.IMREAD_UNCHANGED))
            tab_masks_name.append(np.flipud(fichier.split('-'))[0])
            
    for id in range(20):
        random_id = np.random.randint(202)
        print(random_id)
        cv2.imwrite('./training2/images/'+str(random_id)+'_training.tiff',tab_images[random_id])
        print(tab_images_name[random_id])
        img_orig = bytescaling(tab_masks[random_id])
        #cv2.imwrite('./training2/1st_manual/'+str(random_id)+'_manual2.tiff',img_orig)
        blur = cv2.GaussianBlur(img_orig,(5,5),0)
        kernel = np.array((
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, 24, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1]), dtype="int")
        convolution = cv2.filter2D(blur, -1, kernel)
        ret2,th2 = cv2.threshold(convolution,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        cv2.imwrite('./training2/1st_manual/'+str(random_id)+'_manual1.tiff',th2)
        print(tab_masks_name[random_id])
        
    if False:
        if not os.path.isdir(dir_masks):
            quit("The directory {} don't exist !".format(dir_masks))   
        list_file=os.listdir(dir_masks)
        if list_file is None:
            quit("No file in {} !".format(dir_masks))    
        for fichier in sorted(list_file):
            if fichier.split('.')[1] == 'tiff':
                img_orig=cv2.imread(dir_masks+fichier,cv2.IMREAD_UNCHANGED)
                print('Creating and change {}'.format(dir_masks+fichier))
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
                ret2,th2 = cv2.threshold(convolution,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                cv2.imwrite('./training2/1st_manual/'+fichier.replace('.tiff', '_manual1.tiff'),th2)
                #photo = Image.open('./training2/1st_manual/tiff/'+fichier.replace('.tiff', '_manual1.tiff'))
                #photo.save('./training2/1st_manual/gif/'+fichier.replace('.tiff', '_manual1.gif'))
            
            
            
            
            
            
            
            