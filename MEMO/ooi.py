import math
import itertools


class OOI(object): #ObjectOfInterest

     def __init__(self, identifier = None, pattern = None, parents = None, weight = 0, children = None):
          self.identifier = identifier
          self.weight = weight
          self.parents = parents #Parents and Children should follow the form: {identifier: object}
          self.children = children
          self.pattern = pattern


     def getPattern(self):
          return self.pattern



     #Takes in two patterns, and returns the permuatation of the first pattern that results in the most agreement between the elements
     #Patterns given to function with format: [number of parts, angleSet1, angleSet2, ..., angleSetN], where angleSetN is a list of angles pertaining to a specific part
     #Currently assumes that each angle set has the same number of parts - FIX THIS
     #Assumes each element is either a list or a float
     def alignPatterns(self, patt1, patt2):
          bestRatio = float('inf')
          bestPerm = None
          #Since number of parts will currently be assumed to be the same, only need to check permutations of one of the angleSets
          for test in itertools.permutations(patt1[1:]):
               totalMatch = 0
               for i in range(len(test)):
                    as1 = test[i]
                    as2 = patt2[i+1]
                    setMatch = 0
                    weight = len(as1)
                    for j in range(weight):
                         if as2[j] == as1[j]: #Difference is zero
                             pass 
                         elif as1[j] != 0:
                              setMatch += abs(as2[j] - as1[j])/abs(as1[j])
                         else:
                              setMatch += abs(as2[j] - 0.000001)/0.000001 #Check to make sure this is an okay approximation
                              
                    setRatio = setMatch / weight
                    totalMatch += setRatio

               testRatio = totalMatch / (len(test)+1) #Since the assumption is that the number of parts are the same, their difference is zero
               if abs(testRatio) <= abs(bestRatio):
                    bestRatio = testRatio
                    bestPerm = test

          return bestRatio, bestPerm
               
          
