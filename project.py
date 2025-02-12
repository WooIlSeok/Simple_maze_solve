import cv2
from skimage.util import invert
from skimage.morphology import skeletonize
import numpy as np
import copy



#배경 제거
def rm_bg(img):
    rows, cols = img.shape
    point = []
    for i in range(rows-1):
        if np.count_nonzero(img[i,:] == 0) > cols*0.7 and np.count_nonzero(img[i,:] == 0) > np.count_nonzero(img[i+1,:] == 0):
            up_axis = i
            img[:up_axis, :] = 0
            break
    for i in range(rows-1, 0, -1):
        if np.count_nonzero(img[i,:] == 0) > cols*0.7 and np.count_nonzero(img[i,:] == 0) > np.count_nonzero(img[i-1,:] == 0):
            down_axis = i
            img[down_axis:, :] = 0
            break 
    for i in range(cols-1):
        if np.count_nonzero(img[:,i] == 0) > rows*0.7 and np.count_nonzero(img[:,i] == 0) > np.count_nonzero(img[:,i+1] == 0):
            for j in range(rows-1):
                if img[j,i] == 0 and img[j+1, i] == 255:
                    width1 = j
            for j in range(rows-1, 0, -1):
                if img[j,i] == 0 and img[j-1, i] == 255:
                    width2 = j
            point.append((int((width1+width2)/2), i))
            left_axis = i
            img[:, :left_axis] = 0
            break
    for i in range(cols-1, 0, -1):
        if np.count_nonzero(img[:,i] == 0) > rows*0.7 and np.count_nonzero(img[:,i] == 0) > np.count_nonzero(img[:,i-1] == 0):
            for j in range(rows-1):
                if img[j,i] == 0 and img[j+1, i] == 255:
                    width1 = j
            for j in range(rows-1, 0, -1):
                if img[j,i] == 0 and img[j-1, i] == 255:
                    width2 = j
            point.append((int((width1+width2)/2), i))
            right_axis = i
            img[:, right_axis:] = 0
            break
    return point

def match_point(skel_img, point):
    init_y, init_x = point
    if skel_img[init_y, init_x] == 255:
        return point
    else:
        i = 3
        rows, cols = skel_img.shape
        while i < 30:
            y_min, y_max, x_min, x_max = max(init_y-i, 0), min(init_y+i, rows), max(init_x - i, 0), min(init_x + i, cols)
            if (y_min or x_min) == 0 and y_max == rows and x_max == cols:
                return (-1, -1)
            roi = skel_img[y_min: y_max, x_min:x_max]
            roi_points = np.column_stack(np.where(roi == 255))
            if len(roi_points) > 0:
                idx_y, idx_x = roi_points[0][0] - i, roi_points[0][1] - i
                return (idx_y+init_y, idx_x +init_x)
            else: i = i + 3

class PathFind:
    def __init__(self, start, end, skel_img):
        self.turtles = [[start]]
        self.end = end
        self.ans_idx = None
        self.path_map = np.array(skel_img).astype(bool)

        
        
    def execute(self): #DFS
        while True:
            
            for i in range(len(self.turtles)):
               #if arrive
               if(self.turtles[i][-1]) == self.end: 
                   self.ans_idx == i
                   return self.turtles[i]
               y, x = self.turtles[i][-1]
               replace = False
               
               #send turtle to 4 direction
               if self.path_map[y-1, x] == True:
                   self.turtles[i].append((y-1,x))
                   replace = True
                       
               if self.path_map[y+1, x] == True:
                   if replace == False:
                       self.turtles[i].append((y+1,x))
                       replace = True
                   else:
                       self.turtles.append(self.turtles[i].copy())
                       self.turtles[-1].append((y+1,x))
                       
               if self.path_map[y, x-1] == True:
                   if replace == False:
                       self.turtles[i].append((y,x-1))
                       replace = True
                   else:
                       self.turtles.append(self.turtles[i].copy())
                       self.turtles[-1].append((y,x-1))
                       
               if self.path_map[y, x+1] == True:
                   if replace == False:
                       self.turtles[i].append((y,x+1))
                       replace = True
                   else:
                       self.turtles.append(self.turtles[i].copy())
                       self.turtles[-1].append((y,x+1))
               #erase way back
               self.path_map[y, x] = False
               #if i'st turtle blocked
               if replace == False:
                   self.turtles.pop(i)

     

       
        
        
        
        
if __name__ == '__main__': 
    
    DATA_PATH = 'C:\\Users\\james\\Downloads\\maze_img\\maze.PNG'

    np.set_printoptions(threshold=np.inf)

    img_gray = cv2.imread(DATA_PATH, cv2.IMREAD_GRAYSCALE)


    _, img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    
    polar_point = rm_bg(img)
    
    skeleton = skeletonize(img == 255)
    skel_img = (skeleton*255).astype(np.uint8)
    
    start = match_point(skel_img, polar_point[0])
    end = match_point(skel_img, polar_point[1])
    
    path = PathFind(start, end, skel_img)

    cv2.imshow('img', img)
    cv2.imshow('skeleton', skel_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()