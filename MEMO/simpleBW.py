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

     def __init__(self, identifier = None, pattern = None, parents = None, weight = 0, children = None, focus = 0.5, unityLimit = 0.9, proxRatio = 0.9):
          """
          Description: Creates a SimpleBWImage object

          Parameters
          *identifier: String used to identify the object
          *pattern: An array that contains the pattern which identifies the object as unique
          *parents: Dictionary whose keys are the identifiers of the parent objects and whose values are the parent objects
          *weight: Represents the number of times the pattern has been reinforced, starting with 1 at the pattern's creation
          *children: Dictionary whose keys are the identifiers of the child objects and whose values are the child objects
          *focus: Value which defines the lowest pixel value that is considered "interesting"
          *unityLimit: Value that defines when pixels are considered continuous and when they are considered to be a new part
          *proxRatio: Value that defines when the image pattern and child pattern are a "match"
          
          """
          super(SimpleBWImage, self).__init__(identifier, pattern, parents, weight, children)
          self.focus = focus
          self.unityLimit = unityLimit
          self.proxRatio = proxRatio
          

     def identifyImage(self, image):
          """
          Description: Given an image, will return the child that best matches the image's pattern, given the best match is within the proximity ratio

          Parameters
          *image: Array containing the pixel data

          """
          
          imagePattern = self.analyzeImage(image)
          #print("Image Pattern (Identify Image): ", imagePattern)
          bestRatio = 0.0
          bestChild = None
          #Determines which child best matches the pattern given
          for child in self.children:
               #Returns the difference between the two patterns, as well as the child pattern which created this ratio
               childPattern, diffRatio = self.alignPatterns(self.children[child].pattern, imagePattern)
               if diffRatio <= bestRatio:
                    bestRatio = diffRatio
                    bestChild = child

          if bestRatio <= (1-self.proxRatio):
               return bestChild, bestRatio
          else:
               return None, 1.0


     def updateChildren(self, image, childName):
          """
          Description: Given an image, either updates the pattern of the child whose identifier is childName or creates a new child

          Parameters
          *image: Array containing the image data
          *childName: Identifier of child whose pattern will be updated
          
          """
          
          imagePattern = self.analyzeImage(image)
          if self.children == None:
               newChild = SimpleBWImage(childName, imagePattern, {self.identifier: self}, 1)
               self.children = {childName: newChild}
          elif childName not in self.children:
               #Currently using objects to store information. Find a way to generalize this.
               newChild = SimpleBWImage(childName, imagePattern, {self.identifier: self}, 1)
               self.children[childName] = newChild
          else:
               self.children[childName].weight += 1 #Increases weight of pattern by 1

               #print("\n\nImage Pattern (Update Children): ", imagePattern)
               #print("Child Pattern (Update Children): ", self.children[childName].pattern)
               IMPatt, ratio = self.alignPatterns(imagePattern, self.children[childName].pattern)
               self.children[childName].pattern, ratio = self.updatePattern(self.children[childName].pattern, IMPatt)

          return



     def updatePattern(self, childPatt, IMPatt):
          #print("\nChild Pattern: ", childPatt)
          #print("Image Pattern: ", IMPatt)

          #Assuming childPatt type will match IMPatt type
          if type(childPatt[1]) in [type(1.0), type(1)]:
               if (childPatt[1] - IMPatt[1]) == 0:
                    agreement = 1
               elif IMPatt[1] == 0:
                    agreement = 0
               else:
                    agreement = 1 - abs((childPatt[1] - IMPatt[1])/IMPatt[1])

               newWeight = ((childPatt[0]+IMPatt[0])/2)*(agreement)
               newValue = (childPatt[1] + IMPatt[1])/2

               return (newWeight, newValue), agreement

          else:
               totAgreement = 0
               values = []
               for val in range(len(childPatt)-1):
                    newVal, agreement = self.updatePattern(childPatt[val+1], IMPatt[val+1])
                    values.append(newVal)
                    totAgreement += agreement
                    #print("Calculated Values: ", values)
                    #print("Total Agreement: ", totAgreement)

               agreementRatio = totAgreement / len(values)
               newWeight = abs(((childPatt[0] + IMPatt[0])/2)*agreementRatio)
               pattern = [newWeight] + values

               return pattern, agreementRatio



     def analyzeImage(self, image):
          """
          Description: Given an image, returns a pattern which defines the image

          Parameters
          *image: Array containing the pixel data
          
          """
          
          y, x = self.findPOI(image)
          shape = [[(y,x),(y,x), None]] #Holds information on the different parts of the image
          cShape = 0
          #Can we just save the previous pixel instead of all of the pixels in the current part?
          cPixels = [(y,x)] #Holds pixels of the active part
          complete = False
          count = 0
          nextState = None
          
          while not complete and count<(len(image)*10): #Extra condition to make sure no infinite loops at the moment. FIXME
               nextY, nextX, nextState = self.expand(image, x, y, nextState)
               #print("\n\n(Y, X): ", (y, x))
               #print("(NextY, NextX): ", (nextY, nextX))
               #print("Expansion Direction: ", direction)
               
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

                    #print("Pixel Slope: ", pixSlope)
                    #print("Part Slope: ", shape[cShape][2])
                    #Checks if the slope between the current pixel and the previous pixel match the total slope of the current part
                    if shape[cShape][2] == None:
                         failed = False
                    elif shape[cShape][2] == 0 and abs(pixSlope) <= self.unityLimit:
                         failed = False
                    elif shape[cShape][2] == float('inf') or shape[cShape][2] != 0:
                         if pixSlope == shape[cShape][2]:
                              failed = False
                         elif (shape[cShape][2] == float('inf')) and (pixSlope >= (1-self.unityLimit)*((cPixels[-1][0]-0.99999*shape[cShape][0][0])/(cPixels[-1][1] - 0.99999*shape[cShape][0][1]))):
                              failed = False
                         elif (abs((pixSlope-shape[cShape][2])/shape[cShape][2]) <= self.unityLimit):
                              failed = False

               #print("Breaks Continuity: ", failed)     
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

          #print("\nShape: ", shape)
          #print("Pattern: ", newPatt)

          return newPatt


     def isPOI(self, y, x, image):
          """
          Description: Given the value of a pixel and the focus value, determines of the pixel is a "Pixel of Interest". Also checks
          to make sure that desired coordinates for the pixel are within the scope of the image.

          Parameters
          *y, x: Coordinates of the pixel to be tested
          *image: Array of pixel values
          """
          if (y < 0) or (y >= len(image)):
               return False
          elif (x < 0) or (x >= len(image[y])):
               return False
          elif image[y][x] > self.focus:
               return True
          return False

      
     def findPOI(self, image):
          """
          Description: Scans the image array from left-to-right, top-to-bottom in order to find a POI

          Parameters
          *image: Array containing pixel data
          """
          for y in range(0, len(image)):
               for x in range(0, len(image[y])):
                    if image[y][x] > self.focus:
                         return y, x

          return None, None


     def expand(self, image, x, y, currentS = None):
          """
          Description: Given the current position, finds the next adjacent POI, looking first right, then left, then down, then up.

          Parameters
          *image: Array containing pixel data
          *(x, y): Index values of the current pixel position
          *currentS: The current state, which indicates the order in which pixels should be checked
          """
          states = {'U': [(y-1, x), (y-1, x+1)], 'R': [(y, x+1), (y+1, x+1)], 'D': [(y+1, x), (y+1, x-1)], 'L': [(y, x-1), (y-1, x-1)]}
          if currentS == None:
               currentS = ['U', 'R', 'D', 'L']

          prevPix = (states[currentS[-1]][1], len(currentS)-1) #Obtains the value of the "last" pixel checked and its state
          for s in range(len(currentS)):
               for pix in states[currentS[s]]:
                    if (not self.isPOI(prevPix[0][0], prevPix[0][1], image)) and self.isPOI(pix[0], pix[1], image):
                         nextState = currentS[s:]+currentS[0:s]
                         return pix[0], pix[1], nextState
                    elif (self.isPOI(prevPix[0][0], prevPix[0][1], image) and (not self.isPOI(pix[0], pix[1], image))):
                         nextState = currentS[prevPix[1]:]+currentS[0:prevPix[1]]
                         return prevPix[0][0], prevPix[0][1], nextState                    
                    else:
                         prevPix = (pix, s)

          return None, None, None         
          


     def setRelations(self, shape): #What criteria are necessary to identify shapes?
          """
          Description: Given a shape (list of parts), determines the relationships between the parts and stores those relations in a pattern

          Parameters
          *shape: Contains the parts of an analyzed object
          """
          
          pattern = [1, (1, float(len(shape)))] #Format currently follows: [number of parts, list of angles (each element is a list of angles pertaining to a single part)]
          for s1 in range(len(shape)):
               relationSet = [1]
               #Calculates the angle between any two lines (fix this to create a relation between curves)
               for s2 in range(len(shape)):
                    if s1 != s2:
                         angle = abs(math.atan(shape[s1][2])-math.atan(shape[s2][2]))
                         len1 = (((shape[s1][0][0]-shape[s1][1][0])**2)+((shape[s1][0][1]-shape[s1][1][1])**2))**(1/2)
                         len2 = (((shape[s2][0][0]-shape[s2][1][0])**2)+((shape[s2][0][1]-shape[s2][1][1])**2))**(1/2)
                         relLength = abs(len1-len2)/len1
                         relationSet.append([1, (1, angle),(1, relLength)])
                         
               pattern.append(relationSet)

          return pattern
                         

















          
                         
                         










          
