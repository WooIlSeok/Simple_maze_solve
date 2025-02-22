import cv2
import numpy as np
from PIL import Image
import time
import preprocessing as prep
import custom_skeletonization as skel
import pathfind    
      

      
##only rectangle maze##
        
if __name__ == '__main__': 
    
    start_time = time.time()
    
    DATA_PATH = r'.\maze_img\success sample\success1.PNG'
    np.set_printoptions(threshold=np.inf)

    img_origin = cv2.imread(DATA_PATH, cv2.IMREAD_UNCHANGED)
    if img_origin is None: #when cv2.imread is unavailable
        img_pil = Image.open(DATA_PATH).convert('RGB')
        img_origin = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    img_gray = prep.trans2gray(img_origin)


    _, img_bin = cv2.threshold(img_gray, 230, 255, cv2.THRESH_BINARY)
    

    polar_point = prep.rm_bg(img_bin)
    


    
    skeleton = skel.skeletonize(img_bin == 255)
    skel_img = (skeleton*255).astype(np.uint8)

    start = prep.match_point(skel_img, polar_point[0])
    end = prep.match_point(skel_img, polar_point[1])

    
    path = pathfind.PathFind(skel_img, start, end)
    img_complete = img_origin.copy()

    
    for i in range(len(path)):
        img_complete[path[i]] = 0

    img_ratio = img_complete.shape[1]/img_complete.shape[0]
    if(img_complete.shape[0] > 800):
        img_complete = cv2.resize(img_complete, (800, int(img_ratio * 800)), interpolation=cv2.INTER_AREA)
        

    cv2.imshow('complete', img_complete)
    cv2.waitKey(0)
    cv2.destroyAllWindows()