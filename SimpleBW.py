import math
from TestDataSquares import *


'''
Assuming that the image file has been uploaded as aa array of pixels with their
value equalling the color stored in it. Current calculations assume
that images are in grayscale, and that each pixel has an intensity between 0 and 1.
This should be changed to a more applicable number scale later on.
'''

class OOI: #ObjectOfInterest

     def __init__(self, parents = None, children = None, pattern = None):
          self.parents = parents
          self.children = children
          self.pattern = pattern


     def getPattern(self):
          return self.pattern



     #Takes in two patterns, and returns the list of index pairs that results in the most agreement between the elements
     #It is assumed that items within nested lists are in absolute order
     def alignPatterns(self, patt1, patt2):
          aWeight = 0
          agreementTotal = 0

          






     def findMatchRatio(self, patt1, patt2):
          matchWeight = 0
          matchTotal = 0

          index = 0
          #Deconstructs patterns as it goes
          while len(patt1)>=0 or len(patt2)>=0:
               #Find most similar item in patt2
               match = 0
               matchIndex = 0
               if len(patt1) != 0 and len(patt2) != 0:
                    for itemIndex in range(len(patt2)):
                         partMatch = 0
                         
                         if isinstance(patt2[itemIndex], list) and isinstance(patt1[index], list):
                              if len(patt2[itemIndex]) == len(patt1[index]):
                                   for i in range(len(patt2[itemIndex])):
                                        partMatch += patt2[itemIndex][i] / patt1[index][i]

                                   partMatch /= len(patt2[itemIndex])

                         elif isinstance(patt2[itemIndex], float) and isinstance(patt1[index], float):
                              partMatch = patt2[itemIndex]/patt1[index]

                         if partMatch > match:
                              match = partMatch
                              matchIndex = itemIndex

                         patt2.remove(patt2[matchIndex])
                         patt1.remove(patt1[index])

               matchWeight += 1
               matchTotal += match
               index += 1

          matchRatio = matchTotal/matchWeight

          return matchRatio

               
                      
               

'''
Simple Black and White Image (Single object images)

Children will eventually consist of the different shapes (square, rectangle, etc). Stored as a dictionary?
Functions:
     identifyImage: Given an image, will return what shape the program identifies it as
     updatePattern: Updates what it means to be a SimpleBWImage given an image
     updateChildren: Given an image and what shape that image represents, updates the pattern of the corresponding child
     analyzeImage: Used to determine the pattern shown by a given image
     isPOI: Determines if a given pixel is within the focus bounds
     findPOI: Finds the initial pixel of interest by scanning the image
     expand: Finds the next POI for the program to look at
     setRelations: After POI analysis, determines the relations between the different parts of the object
'''
class SimpleBWImage(OOI):

     def __init__(self, parents = {}, children = {}, pattern = []):
          super().__init__(parents, children, pattern)


     def updatePattern(self, image, focus = 0.5, unityLimit = 0.8):
          return
     

     def identifyImage(self, image, focus = 0.5, unityLimit = 0.8, proxRatio = 0.8):
          imagePattern = self.analyzeImage(image, focus, unityLimit)
          bestRatio = 0
          bestChild = None
          #Determines which child best matches the pattern given
          for child in self.children:
               matchRatio = self.findMatchRatio(self.children[child], imagePattern)
               if matchRatio >= bestRatio:
                    bestRatio = matchRatio
                    bestChild = child

          if bestRatio >= proxRatio:
               return bestChild
          else:
               return None


     #Each pattern needs a certain weight to it, so that "new" patterns are changed more by new inputs, while old patterns are changed less
     def updateChildren(self, image, childName, focus = 0.5, unityLimit = 0.8):
          imagePattern = self.analyzeImage(image, focus, unityLimit)
          if childName not in self.children:
               self.children[childName] = [1, imagePattern] #Follows format [weight, pattern]
          else:
               self.children[childName][0] += 1 #Increases weight of pattern by 1
               if imagePattern[0] > self.children[childName][1][0]: #Checks number of parts in each pattern
                    self.children[childName][1][0] = self.children[childName][1][0] + (imagePattern[0]/self.children[childName][0])
               else:
                    self.children[childName][1][0] = self.children[childName][1][0] - (imagePattern[0]/self.children[childName][0])

               angleSetPairs = self.patternMatch(imagePattern[1], self.children[childName][1][1]) #Matches which sets of angles are the closest matches to each other

               #Adjusts each angle within the list of angles (assumed that within a single angle set, each angle is in a fixed order)
               for anglePair in angleSetPairs:
                    for angle in self.children[childName][1][1][anglePair[1]]:
                         if self.children[childName][1][1][anglePair[1]][angle] > imagePattern[1][anglePair[0]][angle]:
                              self.children[childName][1][1][anglePair[1]][angle] = self.children[childName][1][1][anglePair[1]][angle] + (imagePattern[1][anglePair[0]][angle]/self.children[childName][0])
                         else:
                              self.children[childName][1][1][anglePair[1]][angle] = self.children[childName][1][1][anglePair[1]][angle] - (imagePattern[1][anglePair[0]][angle]/self.children[childName][0])

          return
          

     #Focus is what is used to determine if there is enough intensity in the pixel to determine if it is a PIO
     #Continuity is being defined as having a straight line (~1). Anything breaking that by a significant portion
     #is considered to be a new "part" of the object
     def analyzeImage(self, image, focus, unityLimit):
          y, x = self.findPOI(image, focus)
          shape = {1: {"start": [y, x], "end": [y, x], "equation": 0}} #Holds information on the different parts of the image
          cShape = 1
          cPixels = [[y,x]] #Holds pixels of the active part
          complete = False
          count = 0
          direction = None
          while not complete and count<(len(image)*4):
               nextY, nextX, direction = self.expand(image, x, y, focus, direction)
               for s in shape: #Makes sure that pixels are not analyzed twice
                    if s != cShape and ([nextY, nextX] == shape[s]["start"] or [nextY, nextX] == shape[s]["end"]):
                         complete = True

               if not complete:
                    #Check continuity between current pixel and previous pixels
                    #Create a way to adjust the "vision" of comparison (how far back should comparisons go?)
                    try:
                         pixSlope = (nextY - cPixels[-1][0])/(nextX - cPixels[-1][1])
                    except ZeroDivisionError:
                         pixSlope = float('inf')

                    #Catches the case where both slopes are infinity as well as checking how close to parallel the lines are
                    failed = True
                    if shape[cShape]["equation"] == 0 and abs(pixSlope) <= (1-unityLimit):
                         failed = False
                         cPixels.append([nextY, nextX])
                         try:
                              shape[cShape]["equation"] = (nextY - shape[cShape]["start"][0])/(nextX - shape[cShape]["start"][1]) #This makes an imperfect line. Replace with a best fit line (Also, needs to incorporate curves)
                         except ZeroDivisionError:
                              shape[cShape]["equation"] = float('inf') 
                    
                    elif shape[cShape]["equation"] != 0 and (pixSlope == shape[cShape]["equation"] or abs(pixSlope/shape[cShape]["equation"]) >= unityLimit):
                         failed = False
                         cPixels.append([nextY, nextX])
                         try:
                              shape[cShape]["equation"] = (nextY - shape[cShape]["start"][0])/(nextX - shape[cShape]["start"][1]) #This makes an imperfect line. Replace with a best fit line (Also, needs to incorporate curves)
                         except ZeroDivisionError:
                              shape[cShape]["equation"] = float('inf') 

                         
                    if failed == True:
                         shape[cShape]["end"] = [cPixels[-1][0], cPixels[-1][1]]
                         if (shape[cShape]["end"][1] - shape[cShape]["start"][1]) == 0:
                              shape[cShape]["equation"] = float('inf')
                         else:
                              shape[cShape]["equation"] = (shape[cShape]["end"][0] - shape[cShape]["start"][0])/(shape[cShape]["end"][1] - shape[cShape]["start"][1])
                         shape[(len(shape)+1)] = {"start": [nextY, nextX], "end": [nextY, nextX], "equation": 0}
                         cPixels = [[nextY, nextX]]
                         cShape = len(shape)


                    y = nextY
                    x = nextX
                    count += 1

          print(shape)
          newPatt = self.setRelations(shape) #Defines the relations between different parts of the object. At this point, all data concerning the image can be deleted from memory
     
          return newPatt


     def isPOI(self, coords, image, focus):
          if image[coords[1]][coords[0]] > focus:
               return True
          return False

      
     def findPOI(self, image, focus):
          #Scans document to find the first pixel that falls within the focus range
          #Look to see if this can be optimized
          for y in range(0, len(image)):
               for x in range(0, len(image[y])):
                    if image[y][x] > focus:
                         return y, x

          return None, None


     '''
     The function expand will look at the 8 pixels surrounding the pixel coordinates it is given. From there,
     it will first look right, then left, then down, then up. Pixels along borders are chosen over pixels with
     neighbors.
     '''
     def expand(self, image, x, y, focus, previousDirection):
          #Is there a more intelligent way to do this?
          #Fix this - breaks at corners

          #Looking right
          if previousDirection != "left" and (x+1)<len(image[y]):
               right = [[x+1, y+1], [x+1, y], [x+1, y-1]]
               rightPOI = [self.isPOI([x+1, y+1], image, focus), self.isPOI([x+1, y], image, focus), self.isPOI([x+1, y-1], image, focus)]
               if True in rightPOI:
                    if False in rightPOI: #If there are no non-POI, then there are no border pixels to grab
                         if (not rightPOI[0]) and rightPOI[1]:
                              return right[1][1], right[1][0], "right"
                         elif not (rightPOI[0] or rightPOI[1]) and rightPOI[2]:
                              return right[2][1], right[2][0], "right"
                         elif (not rightPOI[2]) and rightPOI[1]:
                              return right[1][1], right[1][0], "right"
                         else:
                              return right[0][1], right[0][0], "right"

          #Looking left
          if previousDirection != "right" and (x-1)>=0:
               left = [[x-1, y+1], [x-1, y], [x-1, y-1]]
               leftPOI = [self.isPOI([x-1, y+1], image, focus), self.isPOI([x-1, y], image, focus), self.isPOI([x-1, y-1], image, focus)]
               if True in leftPOI:
                    if False in leftPOI: #If there are no non-POI, then there are no border pixels to grab
                         if (not leftPOI[0]) and leftPOI[1]:
                              return left[1][1], left[1][0], "left"
                         elif not (leftPOI[0] or leftPOI[1]) and leftPOI[2]:
                              return left[2][1], left[2][0], "left"
                         elif (not leftPOI[2]) and leftPOI[1]:
                              return left[1][1], left[1][0], "left"
                         else:
                              return left[0][1], left[0][0], "left"

          #Looking down
          if previousDirection != "up" and (y-1)>=0:
               down = [[x-1, y-1], [x, y-1], [x+1, y-1]]
               downPOI = [self.isPOI([x-1, y-1], image, focus), self.isPOI([x, y-1], image, focus), self.isPOI([x+1, y-1], image, focus)]
               if True in downPOI:
                    if False in downPOI: #If there are no non-POI, then there are no border pixels to grab
                         if (not downPOI[0]) and downPOI[1]:
                              return down[1][1], down[1][0], "down"
                         elif not (downPOI[0] or downPOI[1]) and downPOI[2]:
                              return down[2][1], down[2][0], "down"
                         elif (not downPOI[2]) and downPOI[1]:
                              return down[1][1], down[1][0], "down"
                         else:
                              return down[0][1], down[0][0], "down"

          #Looking up
          if previousDirection != "down" and (y+1)<len(image):
               up = [[x-1, y+1], [x, y+1], [x+1, y+1]]
               upPOI = [self.isPOI([x-1, y+1], image, focus), self.isPOI([x, y+1], image, focus), self.isPOI([x+1, y+1], image, focus)]
               if True in upPOI:
                    if False in upPOI: #If there are no non-POI, then there are no border pixels to grab
                         if (not upPOI[0]) and upPOI[1]:
                              return up[1][1], up[1][0], "up"
                         elif not (upPOI[0] or upPOI[1]) and upPOI[2]:
                              return up[2][1], up[2][0], "up"
                         elif (not upPOI[2]) and upPOI[1]:
                              return up[1][1], up[1][0], "up"
                         else:
                              return up[0][1], up[0][0], "up"

          return y, x, "Same"



     def setRelations(self, shape): #What criteria are necessary to identify shapes?
          pattern = [0, []] #Format currently follows: [number of parts, list of angles (each element is a list of angles pertaining to a single part)]
          for s1 in shape:
               angles = []
               #Calculates the angle between any two lines (fix this to create a relation between curves)
               for s2 in shape:
                    if s1 != s2:
                         angle = math.atan(shape[s1]["equation"])-math.atan(shape[s2]["equation"])
                         angles.append(angle)
                         
               pattern[1].append(angles)

          pattern[0] = len(pattern[1])
          return pattern
                         

data = makeTestImage()
SBW1 = SimpleBWImage()

def runTest1():
     SBW1.updateChildren(data, "square")
     print(SBW1.children)

dataSet = makeTestData(10)
SBW2 = SimpleBWImage()

def runTest2():
     SBW2.updateChildren(dataSet[0], "square")
     print(SBW2.children)




















          
                         
                         










          
