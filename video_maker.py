import cv2
import numpy as np
import glob
import os

frameSize = (640, 480)

out = cv2.VideoWriter('ped_expct_video.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 3, frameSize)


for filename in sorted(glob.glob('/Users/sebastianvomdorff/Documents/Promotion/likelihood_CA/ped_expct_map_images/*.png'), key=os.path.getmtime):
    img = cv2.imread(filename)
    out.write(img)

out.release()