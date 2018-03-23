from testDataSquares import *
from MEMO import *


data = makeTestImage()
s1 = SimpleBWImage()
s2 = SimpleBWImage()
s3 = SimpleBWImage()
s4 = SimpleBWImage()
s5 = SimpleBWImage()

def runTest1():
     s1.updateChildren(data, "square")
     #s2.updateChildren(data, "square")
     #s3.updateChildren(data, "square")
     #s4.updateChildren(data, "square")
     #s5.updateChildren(data, "square")
     print("s1: ", s1.children["square"].pattern)
     #print("s2: ", s2.children["square"].pattern)
     #print("s3: ", s3.children["square"].pattern)
     #print("s4: ", s4.children["square"].pattern)
     #print("s5: ", s5.children["square"].pattern)

dataSet = makeTestData(50)
def runTest2():
     for i in range(0, 45):
          s1.updateChildren(dataSet[i], "square")

     for i in range(45, 50):
          print(s1.identifyImage(dataSet[i]))

