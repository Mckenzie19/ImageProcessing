from testDataSquares import *
from MEMO import *


data = makeTestImage()
s1 = SimpleBWImage()


def runTest1():
     s1.updateChildren(data, "square")
     print("s1: ", s1.children["square"].pattern)


dataSet = makeTestData(50)
def runTest2():
     for i in range(0, 45):
          s1.updateChildren(dataSet[i], "square")

     for i in range(45, 50):
          print(s1.identifyImage(dataSet[i]))

def tiltTest():
     dSet, tilt = squareDataTest()
     s1.updateChildren(tilt, "square")
