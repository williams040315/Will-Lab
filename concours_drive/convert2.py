# -*- coding: utf-8 -*-
"""
@author:    Williams BRETT
@date:      24-03-2020
@brief:     
"""

import numpy as np
import cv2
import os

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
    

if __name__ == "__main__":

    dir_masks='./test/cell-missmarple/' 
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
            cv2.imwrite('./test/cell-missmarple-convert/'+fichier,img_orig)

    dir_masks='./predictions/' 
    list_file=os.listdir(dir_masks)
    if list_file is None:
        quit("No file in {} !".format(dir_masks))    
    for fichier in sorted(list_file):
        if fichier.split('.')[1] == 'png':
            img_orig=cv2.imread(dir_masks+fichier,cv2.IMREAD_UNCHANGED)
            print('Creating and change {}'.format(dir_masks+fichier))
            img_orig = bytescaling(img_orig)
            cv2.imshow('img_orig',img_orig)
            cv2.waitKey(0)