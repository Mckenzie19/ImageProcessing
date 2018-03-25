import math
import itertools
from .ooi import *

'''
This file contains the class SimpleBWImage, which is a subclass of the OOI class. A Simple Black and White Image
is characterized by having only a single object, where the object contains grayscale colors and is continous (the object does
not have any breaks in its outline/shape).

Current Heuristics:
*Information given on the image is in a 2x2 array
*Color information is on a scale from 0 to 1, with 0 being white and 1 being black
*Object does not have any curves

'''

class SimpleBWImage(OOI):
     """
     Simple Black and White Image (SimpleBWImage)

     Description: Classifies and analyzes images that are given to it in array form.

     Functions
     *identifyImage: Identifies the type of object within a given image
     *updateChildren: Updates the pattern of the child whose name is given, or identifies which child's pattern should be updated
     *analyzeImage: Creates a pattern based upon a given image
     *isPOI: Identifies whether or not a given pixel is a pixel of interest
     *findPOI: Finds the "first" pixel of interest in an image, moving from left to right, top to bottom
     *expand: Given the current pixel position and the previous direction expanded, finds the next adjacent POI
     *setRelations: Given a list of parts (the "shape"), returns a pattern
     """

     def __init__(self, identifier = None, pattern = None, parents = None, weight = 0, children = None):
          """
          Description: Creates a SimpleBWImage object

          Parameters
          *identifier: String used to identify the object
          *pattern: An array that contains the pattern which identifies the object as unique
          *parents: Dictionary whose keys are the identifiers of the parent objects and whose values are the parent objects
          *weight: Represents the number of times the pattern has been reinforced, starting with 1 at the pattern's creation
          *children: Dictionary whose keys are the identifiers of the child objects and whose values are the child objects
          
          """
          super(SimpleBWImage, self).__init__(identifier, pattern, parents, weight, children)
          

     def identifyImage(self, image, focus = 0.5, unityLimit = 0.9, proxRatio = 0.8):
          """
          Description: Given an image, will return the child that best matches the image's pattern, given the best match is within the proximity ratio

          Parameters
          *image: Array containing the pixel data
          *focus: Value which defines the lowest pixel value that is considered "interesting"
          *unityLimit: Value that defines when pixels are considered continuous and when they are considered to be a new part
          *proxRatio: Value that defines when the image pattern and child pattern are a "match"
          
          """
          
          imagePattern = self.analyzeImage(image, focus, unityLimit)
          bestRatio = 0.0
          bestChild = None
          #Determines which child best matches the pattern given
          for child in self.children:
               #Returns the difference between the two patterns, as well as the child pattern which created this ratio
               matchRatio, childPattern = self.alignPatterns(self.children[child].pattern, imagePattern)
               if matchRatio <= bestRatio:
                    bestRatio = matchRatio
                    bestChild = child

          if bestRatio <= (1-proxRatio):
               return bestChild, bestRatio
          else:
               return None, 0.0


     def updateChildren(self, image, childName, focus = 0.5, unityLimit = 0.9):
          """
          Description: Given an image, either updates the pattern of the child whose identifier is childName or creates a new child

          Parameters
          *image: Array containing the image data
          *childName: Identifier of child whose pattern will be updated
          *focus: Defines which pixels are "interesting" and which are not
          *unityLimit: Defines when pixels are considered continuous and when they are not
          """
          
          imagePattern = self.analyzeImage(image, focus, unityLimit)
          if self.children == None:
               newChild = SimpleBWImage(childName, imagePattern, {self.identifier: self}, 1)
               self.children = {childName: newChild}
          elif childName not in self.children:
               #Currently using objects to store information. Find a way to generalize this.
               newChild = SimpleBWImage(childName, imagePattern, {self.identifier: self}, 1)
               self.children[childName] = newChild
          else:
               self.children[childName].weight += 1 #Increases weight of pattern by 1
          
               matchRatio, IMAngles = self.alignPatterns(imagePattern, self.children[childName].pattern)
               #Assuming number of parts is the same
               for i in range(len(IMAngles)):
                    for j in range(len(IMAngles[i])):
                         try:
                              diffRatio = (self.children[childName].pattern[i+1][j] - IMAngles[i][j]) / abs(IMAngles[i][j])
                         except ZeroDivisionError:
                              diffRatio = (self.children[childName].pattern[i+1][j] - 0.000001) / 0.000001
                              
                         self.children[childName].pattern[i+1][j] += (self.children[childName].pattern[i+1][j]*(diffRatio/self.children[childName].weight)) #Change the angle by the percent difference in angles divided by the total weight of the pattern 

               
          return
          

     def analyzeImage(self, image, focus, unityLimit):
          """
          Description: Given an image, returns a pattern which defines the image

          Parameters
          *image: Array containing the pixel data
          *focus: Defines which pixels are "interesting"
          *unityLimit: Defines which pixels are continuous
          """
          
          y, x = self.findPOI(image, focus)
          shape = [[(y,x),(y,x), None]] #Holds information on the different parts of the image
          cShape = 0
          #Can we just save the previous pixel instead of all of the pixels in the current part?
          cPixels = [(y,x)] #Holds pixels of the active part
          complete = False
          count = 0
          direction = None
          
          while not complete and count<(len(image)*10): #Extra condition to make sure no infinite loops at the moment. FIXME
               nextY, nextX, direction = self.expand(image, x, y, focus, direction)
               for s in range(len(shape)): #Makes sure that pixels are not analyzed twice
                    if s != cShape and ((nextY, nextX) == shape[s][0] or (nextY, nextX) == shape[s][1]):
                         complete = True
                    
               failed = True
               if not complete:
                    #Check continuity between current pixel and previous pixels
                    #Create a way to adjust the "vision" of comparison (how far back should comparisons go?)
                    try:
                         pixSlope = (nextY - cPixels[-1][0])/(nextX - cPixels[-1][1])
                    except ZeroDivisionError:
                         pixSlope = float('inf') #Vertical Lines

                    #Checks if the slope between the current pixel and the previous pixel match the total slope of the current part
                    if shape[cShape][2] == None:
                         failed = False
                    elif shape[cShape][2] == 0 and abs(pixSlope) <= unityLimit:
                         failed = False
                    elif shape[cShape][2] == float('inf') or shape[cShape][2] != 0:
                         
                         if pixSlope == shape[cShape][2]:
                              failed = False
                         elif (shape[cShape][2] == float('inf')) and (pixSlope >= (1-unityLimit)*((cPixels[-1][0]-0.99999*shape[cShape][0][0])/(cPixels[-1][1] - 0.99999*shape[cShape][0][1]))):
                              failed = False
                         elif ((pixSlope-shape[cShape][2])/abs(shape[cShape][2]) <= unityLimit):
                              failed = False
                      
               if failed or complete:
                    shape[cShape][1] = (cPixels[-1][0], cPixels[-1][1])
                    if (shape[cShape][1][1] - shape[cShape][0][1]) == 0:
                         shape[cShape][2] = float('inf')
                    else:
                         shape[cShape][2] = (shape[cShape][1][0] - shape[cShape][0][0])/(shape[cShape][1][1] - shape[cShape][0][1])
                    if not complete:
                         shape.append([(y, x), (nextY, nextX), None])
                         cPixels = [(y, x), (nextY, nextX)]
                         cShape = len(shape)-1
               else:
                    cPixels.append((nextY, nextX))
                    try:
                         shape[cShape][2] = (nextY - shape[cShape][0][0])/(nextX - shape[cShape][0][1]) #This makes an imperfect approximation. Replace with a best fit line (Also, needs to incorporate curves)
                    except ZeroDivisionError:
                         shape[cShape][2] = float('inf')

                         
               y = nextY
               x = nextX
               count += 1

          newPatt = self.setRelations(shape) #Defines the relations between different parts of the object. At this point, all data concerning the image can be deleted from memory

          return newPatt


     def isPOI(self, pixelVal, focus):
          """
          Description: Given the value of a pixel and the focus value, determines of the pixel is a "Pixel of Interest"

          Parameters
          *pixelVal: Value of the pixel
          *focus: Defines the lowest value that a pixel can have and still be "interesting"
          """
          if pixelVal > focus:
               return True
          return False

      
     def findPOI(self, image, focus):
          """
          Description: Scans the image array from left-to-right, top-to-bottom in order to find a POI

          Parameters
          *image: Array containing pixel data
          *focus: Defines which pixels are interesting and which are not
          """
          for y in range(0, len(image)):
               for x in range(0, len(image[y])):
                    if image[y][x] > focus:
                         return y, x

          return None, None


     def expand(self, image, x, y, focus, prevDir):
          """
          Description: Given the current position, finds the next adjacent POI, looking first right, then left, then down, then up.

          Parameters
          *image: Array containing pixel data
          *(x, y): Index values of the current pixel position
          *focus: Defines what is a POI and what is not
          *preDir: Holds a string that indicates which direction the function previously expanded
          """

          #Looking right
          if (x+1)<len(image[y]):
               right = [[x+1, y+1], [x+1, y], [x+1, y-1]]
               rightPOI = [(prevDir != "ul") and self.isPOI(image[y+1][x+1], focus), (prevDir != "l") and self.isPOI(image[y][x+1], focus), (prevDir != "dl") and self.isPOI(image[x+1][y-1], focus)]
               if True in rightPOI:
                    if False in rightPOI: #If there are no non-POI, then there are no border pixels to grab
                         if (not rightPOI[0]) and rightPOI[1]:
                              return right[1][1], right[1][0], "r"
                         elif not (rightPOI[0] or rightPOI[1]) and rightPOI[2]:
                              return right[2][1], right[2][0], "ur"
                         elif (not rightPOI[2]) and rightPOI[1]:
                              return right[1][1], right[1][0], "r"
                         else:
                              return right[0][1], right[0][0], "dr"

          #Looking left
          if (x-1)>=0:
               left = [[x-1, y+1], [x-1, y], [x-1, y-1]]
               leftPOI = [(prevDir != "ur") and self.isPOI(image[y+1][x-1], focus), (prevDir != "r") and self.isPOI(image[y][x-1], focus), (prevDir != "dr") and self.isPOI(image[y-1][x-1], focus)]
               if True in leftPOI:
                    if False in leftPOI: #If there are no non-POI, then there are no border pixels to grab
                         if (not leftPOI[0]) and leftPOI[1]:
                              return left[1][1], left[1][0], "l"
                         elif not (leftPOI[0] or leftPOI[1]) and leftPOI[2]:
                              return left[2][1], left[2][0], "ul"
                         elif (not leftPOI[2]) and leftPOI[1]:
                              return left[1][1], left[1][0], "l"
                         else:
                              return left[0][1], left[0][0], "dl"

          #Looking down
          if (y-1)>=0:
               down = [[x-1, y+1], [x, y+1], [x+1, y+1]]
               downPOI = [(prevDir != "ur") and self.isPOI(image[y+1][x-1], focus), (prevDir != "u") and self.isPOI(image[y+1][x], focus), (prevDir != "ul") and self.isPOI(image[y+1][x+1], focus)]
               if True in downPOI:
                    if False in downPOI: #If there are no non-POI, then there are no border pixels to grab
                         if (not downPOI[0]) and downPOI[1]:
                              return down[1][1], down[1][0], "d"
                         elif not (downPOI[0] or downPOI[1]) and downPOI[2]:
                              return down[2][1], down[2][0], "dr"
                         elif (not downPOI[2]) and downPOI[1]:
                              return down[1][1], down[1][0], "d"
                         else:
                              return down[0][1], down[0][0], "dl"

          #Looking up
          if (y+1)<len(image):
               up = [[x-1, y-1], [x, y-1], [x+1, y-1]]
               upPOI = [(prevDir != "dr") and self.isPOI(image[y-1][x-1], focus), (prevDir != "d") and self.isPOI(image[y-1][x], focus), (prevDir != "dl") and self.isPOI(image[y-1][x+1], focus)]
               if True in upPOI:
                    if False in upPOI: #If there are no non-POI, then there are no border pixels to grab
                         if (not upPOI[0]) and upPOI[1]:
                              return up[1][1], up[1][0], "u"
                         elif not (upPOI[0] or upPOI[1]) and upPOI[2]:
                              return up[2][1], up[2][0], "ur"
                         elif (not upPOI[2]) and upPOI[1]:
                              return up[1][1], up[1][0], "u"
                         else:
                              return up[0][1], up[0][0], "ul"

          return y, x, prevDir


     def setRelations(self, shape): #What criteria are necessary to identify shapes?
          """
          Description: Given a shape (list of parts), determines the relationships between the parts and stores those relations in a pattern

          Parameters
          *shape: Contains the parts of an analyzed object
          """
          
          pattern = [len(shape)] #Format currently follows: [number of parts, list of angles (each element is a list of angles pertaining to a single part)]
          for s1 in range(len(shape)):
               angleSet = []
               #Calculates the angle between any two lines (fix this to create a relation between curves)
               for s2 in range(len(shape)):
                    if s1 != s2:
                         angle = math.atan(shape[s1][2])-math.atan(shape[s2][2])
                         angleSet.append(angle)
                         
               pattern.append(angleSet)

          return pattern
                         

















          
                         
                         










          
