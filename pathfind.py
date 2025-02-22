# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 18:27:49 2025

@author: james
"""

import numpy as np
from collections import deque

def PathFind(skel_img, start, end):
    path_map = np.array(skel_img).astype(bool)
    queue = deque([start])
    parent = {start: None} #for saving path nodes
    rows, columns = skel_img.shape
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)] # 8 direction
    

    path_map[start[0], start[1]] = False

    while queue:
        current = queue.popleft()
        if current == end:
            
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]
        
        y, x = current
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < columns and path_map[ny, nx]:
                queue.append((ny, nx)) 
                path_map[ny, nx] = False #erase path back
                parent[(ny, nx)] = current #record pre-node

    return None