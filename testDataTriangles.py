import numpy as np

def makeTriangleTest():
    tri = np.zeros((50,50))

    y = 10
    for x in range(10, 15):
        tri[10][x] = 1
        tri[y][x] = 1
        y+=1

    for x in range(15, 20):
        tri[10][x] = 1
        tri[y][x] = 1
        y-=1

    return tri    



