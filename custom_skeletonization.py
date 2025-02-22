# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 18:24:17 2025

@author: james
"""
import numpy as np

def skeletonize(img_bin):
    img = img_bin.copy().astype(np.uint8)
    

    P1 = img[1:-1, 1:-1]
    P2 = img[:-2, 1:-1]
    P3 = img[:-2, 2:]
    P4 = img[1:-1, 2:]
    P5 = img[2:, 2:]
    P6 = img[2:, 1:-1]
    P7 = img[2:, :-2]
    P8 = img[1:-1, :-2]
    P9 = img[:-2, :-2]
    
    while True:
        prev = img.copy()
        
        #Zhang-Suen thinning
        object_n = P2 + P3 + P4 + P5 + P6 + P7 + P8 + P9


        transition_n = (
            ((P2==0) & (P3==1)).astype(np.uint8) +
            ((P3==0) & (P4==1)).astype(np.uint8) +
            ((P4==0) & (P5==1)).astype(np.uint8) +
            ((P5==0) & (P6==1)).astype(np.uint8) +
            ((P6==0) & (P7==1)).astype(np.uint8) +
            ((P7==0) & (P8==1)).astype(np.uint8) +
            ((P8==0) & (P9==1)).astype(np.uint8) +
            ((P9==0) & (P2==1)).astype(np.uint8)
        )
        
        condition1 = ((P2 * P4 * P6) == 0) & ((P4 * P6 * P8) == 0)
        mask = (P1 == 1) & ( (2 <= object_n) & (object_n <= 6) & (transition_n == 1) & condition1 )
        sub_img = img[1:-1, 1:-1]
        sub_img[mask] = 0
        
        
        
        object_n = P2 + P3 + P4 + P5 + P6 + P7 + P8 + P9
        transition_n = (
            ((P2==0) & (P3==1)).astype(np.uint8) +
            ((P3==0) & (P4==1)).astype(np.uint8) +
            ((P4==0) & (P5==1)).astype(np.uint8) +
            ((P5==0) & (P6==1)).astype(np.uint8) +
            ((P6==0) & (P7==1)).astype(np.uint8) +
            ((P7==0) & (P8==1)).astype(np.uint8) +
            ((P8==0) & (P9==1)).astype(np.uint8) +
            ((P9==0) & (P2==1)).astype(np.uint8)
        )
        
        condition2 = ((P6 * P8 * P2) == 0) & ((P8 * P2 * P4) == 0)
        mask = (P1 == 1) & ( (2 <= object_n) & (object_n <= 6) & (transition_n == 1) & condition2 )
        sub_img = img[1:-1, 1:-1]
        sub_img[mask] = 0
        
        if np.array_equal(prev, img):
            break

    return img