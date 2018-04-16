from testDataSquares import *
from MEMO import *


data = makeTestImage()
s1 = SimpleBWImage()
s2 = SimpleBWImage()

def runTest1():
     s1.updateChildren(data, "square")

dataSet = makeTestData(50)
def runTest2():
     for i in range(0, 45):
          s1.updateChildren(dataSet[i], "square")

     for i in range(45, 50):
          print(s1.identifyImage(dataSet[i]))

def tiltTest():
     dSet, tilt = squareDataTest()
     s1.updateChildren(tilt, "square")


def mergeTest():
     dSet, tilt = squareDataTest()
     s1.updateChildren(data, "square")
     s2.updateChildren(tilt, "square")
     print("s1 Square Pattern: ", s1.children["square"].pattern)
     print("s2 Square Pattern: ", s2.children["square"].pattern)

     s1.updateChildren(tilt, "square")
     print("s1 Square Pattern After Merge: ", s1.children["square"].pattern)
     print(s1.identifyImage(dataSet[2]))
     print(s1.identifyImage(data))
     
