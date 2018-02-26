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


def makeTestImage():
    square = np.zeros((500,500))
    for i in range(10,20):
        square[10][i] = 1
        square[11][i] = 1

        square[20][i] = 1
        square[19][i] = 1

    for j in range(10,20):
        square[j][10] = 1
        square[j][11] = 1

        square[j][20] = 1
        square[j][19] = 1

    return square
        
