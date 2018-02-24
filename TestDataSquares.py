import numpy as np


def makeTestData(numSquares):
    squares = []
    for x in range(numSquares):
        squares.append([])

    for s in range(len(squares)):
        squares[s] = np.zeros((500,500))
        for i in range(s+100, s+150):
            squares[s][i][s+10] = 1
            squares[s][i][s+11] = 1
            squares[s][i][s+12] = 1
            squares[s][i][s+58] = 1
            squares[s][i][s+59] = 1
            squares[s][i][s+60] = 1

        for j in range(s+10, s+60):
            squares[s][s+150][j] = 1
            squares[s][s+149][j] = 1
            squares[s][s+148][j] = 1
            squares[s][s+102][j] = 1
            squares[s][s+101][j] = 1
            squares[s][s+100][j] = 1
            
    return squares


'''                    
try:
     pixSlope = (nextY - cPixels[-1][0])/(nextX - cPixels[-1][1])
     if (pixSlope/shape[cShape]["equation"]) > unityLimit:
          cPixels.append([nextY, nextX])
          try:
               shape[cShape]["equation"] = (nextY - shape[cShape]["start"][0])/(nextX - shape[cShape]["start"][1]) #This makes an imperfect line. Replace with a best fit line (Also, needs to incorporate curves)
          except ZeroDivisionError:
               shape[cShape]["equation"] = float('inf')
     else:
          shape[cShape]["end"] = [cPixels[-1][0], cPixels[-1][1]]
          shape[len(shape)] = {"start": [nextY, nextX], "end": [nextY, nextX], "equation": 0}
          cPixels = [[nextY, nextX]]

except ZeroDivisionError:
     if abs(shape[cShape]["equation"]) > (1-unityLimit):
          shape[cShape]["end"] = [cPixels[-1][0], cPixels[-1][1]]
          shape[len(shape)] = {"start": [nextY, nextX], "end": [nextY, nextX], "equation": 0}
          cPixels = [[nextY, nextX]]
     else:
          cPixels.append([nextY, nextX])
          try:
               shape[cShape]["equation"] = (nextY - shape[cShape]["start"][0])/(nextX - shape[cShape]["start"][1]) #This makes an imperfect line. Replace with a best fit line (Also, needs to incorporate curves)
          except ZeroDivisionError:
               shape[cShape]["equation"] = float('inf')
'''

