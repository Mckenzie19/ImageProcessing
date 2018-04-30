import numpy as np
import copy
import os
from PIL import Image
from imageFiles import *

def importImages():

    imageSet = []
    print(imageList.fileNames)
    for fn in fileNames:
        #print(os.path.isfile("imageFiles\\"+fn))
        if os.path.isfile("imageFiles\\"+fn):
            img = Image.open(fn)
            img.load()
            imgData = np.array(img, dtype = "uint8")
            imgData.flags.writeable = True
            data = np.zeros([len(imgData), len(imgData[0])])


            for i in range(len(imgData)):
                for j in range(len(imgData[i])):
                    if sum(imgData[i][j]) == 0:
                        data[i][j] = 1
                    else:
                        data[i][j] = 1 - (sum(imgData[i][j])/765)

            imageSet.append(data)

    return imageSet
            

#Code from Stackoverflow user Divakar
def outer_slice(x):
    return np.r_[x[0],x[1:-1,-1],x[-1,:0:-1],x[-1:0:-1,0]]

def rotate_steps(x, shift):
    out = np.empty_like(x)
    N = x.shape[0]
    idx = np.arange(x.size).reshape(x.shape)
    for n in range((N+1)//2):
        sliced_idx = outer_slice(idx[n:N-n,n:N-n])
        out.ravel()[sliced_idx] = np.roll(np.take(x,sliced_idx), shift)
    return out
