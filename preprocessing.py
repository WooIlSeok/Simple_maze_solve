import numpy as np
import cv2



#img has alpha channel
def trans2gray(img):
    if (len(img.shape) == 2):
        return img
    elif img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif img.shape[2] == 4:
        shape = [*img.shape[0:2]]
        shape.append(3)
        filled_img = np.zeros(shape)
        
        alpha = img[:,:, 3] / 255.0
        for color in range(3): #B, G, R
            filled_img[:,:, color] = alpha * img[:,:,color] + (1-alpha) * 255
    
        return cv2.cvtColor(filled_img.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    




#find start-end point
def detect_point(arr_line):
    width1, width2 = 0, 0
    
    for i in range(len(arr_line) - 1):
         if arr_line[i] == 0 and arr_line[i+1] == 255:
             width1 = i
             break
    for i in range(len(arr_line) - 1, 0, -1):
         if arr_line[i] == 0 and arr_line[i-1] == 255:
             width2 = i
             break
    if width1 < width2:
         return int((width1 + width2)/2)
    else:
         None

#background make same with wall pixel 

def rm_bg(img):
    rows, cols = img.shape
    start_end = []
    
    row_threshold = np.max(np.count_nonzero(img == 0, axis= 1))*0.7
    col_threshold = np.max(np.count_nonzero(img == 0, axis= 0))*0.7
    
    for i in range(rows-1):
        wall_pxl = np.count_nonzero(img[i,:] == 0)
        if wall_pxl > row_threshold and wall_pxl > np.count_nonzero(img[i+1,:] == 0):
            
            point = detect_point(img[i, :])
            if point != None:
                start_end.append((i, point))
            up_axis = i
            break
    for i in range(rows-1, 0, -1):
        wall_pxl = np.count_nonzero(img[i, :] == 0)
        if wall_pxl > row_threshold and wall_pxl > np.count_nonzero(img[i-1,:] == 0):
            point = detect_point(img[i, :])
            if point != None:
                start_end.append((i, point))
            down_axis = i
            break 
    for i in range(cols-1):
        wall_pxl = np.count_nonzero(img[:,i] == 0)
        if wall_pxl > col_threshold and wall_pxl > np.count_nonzero(img[:,i+1] == 0):
            point = detect_point(img[:, i])
            if point != None:
                start_end.append((point, i))
            left_axis = i
            break
    
    for i in range(cols-1, 0, -1):
        wall_pxl = np.count_nonzero(img[:,i] == 0)
        if wall_pxl > col_threshold and wall_pxl > np.count_nonzero(img[:,i-1] == 0):
            point = detect_point(img[:, i])
            if point != None:
                start_end.append((point, i))  
            right_axis = i
            break
    img[:up_axis, :] = 0
    img[down_axis:, :] = 0
    img[:, :left_axis] = 0
    img[:, right_axis:] = 0
    return start_end

#find start-end point in sekelton near origin point
def match_point(skel_img, point):
    init_y, init_x = point

    if skel_img[init_y, init_x] == 255:
        return point


    indices = np.argwhere(skel_img == 255)
    if indices.size == 0:
        return None

    distances = np.sqrt((indices[:, 0] - init_y)**2 + (indices[:, 1] - init_x)**2)
    min_index = np.argmin(distances)
    return tuple(indices[min_index])