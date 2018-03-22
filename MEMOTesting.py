from TestDataSquares import *
from MEMO import *


data = makeTestImage()
SBW1 = SimpleBWImage()

def runTest1():
     SBW1.updateChildren(data, "square")
     print(SBW1.children)

dataSet = makeTestData(50)
def runTest2():
     for i in range(0, 45):
          SBW1.updateChildren(dataSet[i], "square")

     for i in range(45, 50):
          print(SBW1.identifyImage(dataSet[i]))

