import numpy as np


def squareDataTest():

    dataSet = makeTestData(50)
    tiltSq1 = np.zeros((10,10))

    tiltSq1[1][4] = 0.5
    tiltSq1[2][3] = 0.5
    tiltSq1[2][4] = 0.8
    tiltSq1[2][5] = 0.5
    tiltSq1[3][2] = 0.5
    tiltSq1[3][3] = 0.8
    tiltSq1[3][5] = 0.8
    tiltSq1[3][6] = 0.5
    tiltSq1[4][1] = 0.5
    tiltSq1[4][2] = 0.8
    tiltSq1[4][6] = 0.8
    tiltSq1[4][7] = 0.5
    tiltSq1[5][2] = 0.5
    tiltSq1[5][3] = 0.8
    tiltSq1[5][5] = 0.8
    tiltSq1[5][6] = 0.5
    tiltSq1[6][3] = 0.5
    tiltSq1[6][4] = 0.8
    tiltSq1[6][5] = 0.5
    tiltSq1[7][4] =  0.5

    return dataSet, tiltSq1



def makeTestData(numSquares):
    squares = []
    for x in range(numSquares):
        squares.append([])

    for s in range(len(squares)):
        squares[s] = np.zeros((500,500))
        for i in range(s+100, s+150):
            squares[s][i][s+100] = 1
            squares[s][i][s+101] = 1
            squares[s][i][s+102] = 1

            squares[s][i][s+147] = 1
            squares[s][i][s+148] = 1
            squares[s][i][s+149] = 1

        for j in range(s+100, s+150):
            squares[s][s+149][j] = 1
            squares[s][s+148][j] = 1
            squares[s][s+147][j] = 1

            squares[s][s+102][j] = 1
            squares[s][s+101][j] = 1
            squares[s][s+100][j] = 1
            
    return squares


def makeTestImage():
    square = np.zeros((50,50))
    for i in range(10,20):
        square[10][i] = 1
        square[11][i] = 1

        square[19][i] = 1
        square[18][i] = 1

    for j in range(10,20):
        square[j][10] = 1
        square[j][11] = 1

        square[j][19] = 1
        square[j][18] = 1

    return square
        
