import math
import itertools

"""
Contains the class Object of Interest, or OOI. This class defines a generalized way to store and analyze images.
"""


class OOI(object):
     """
     Object of Interest (OOI)
     Description: Parent class to image analysis classes. Holds ways to analyze basic patterns.

     Functions
     *alignPatterns: Given two image patterns, returns the best permutation (and the match ratio) of the first pattern which results in the best "match" between the two patterns
     """

     def __init__(self, identifier = None, pattern = None, parents = None, weight = 0, children = None):
          """
          Description: Creates an OOI object

          Parameters
          *identifier: String which will serve as the objects id
          *pattern: Array of elements which defines the attributes of an image
          *parents: Dictionary whose keys are the identifiers of the parent objects and whose values are the parent objects
          *weight: Represents the number of times the pattern has been reinforced, starting with 1 at the pattern's creation
          *children: Dictionary whose keys are the identifiers of the child objects and whose values are the child objects
     
          """
          self.identifier = identifier
          self.weight = weight
          self.parents = parents
          self.children = children
          self.pattern = pattern


     def alignPatterns(self, patt1, patt2):
          """
          Description: Given two image patterns, returns the best match ratio and the permutation of the first pattern that results in this match ratio. This is to account
          for objects which were analyzed in different orientations, resulting in their patterns having slightly different orders.

          Parameters
          *patt1: First pattern to be analyzed
          *patt2: Second pattern to be analyzed
          """
          
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
                              setMatch += abs(as2[j] - 0.000001)/0.000001 #Check to make sure this approximation returns accurate results
                              
                    setRatio = setMatch / weight
                    totalMatch += setRatio

               testRatio = totalMatch / (len(test)+1) #Since the assumption is that the number of parts are the same, their difference is zero
               if abs(testRatio) <= abs(bestRatio):
                    bestRatio = testRatio
                    bestPerm = test

          return bestRatio, bestPerm
               
          
