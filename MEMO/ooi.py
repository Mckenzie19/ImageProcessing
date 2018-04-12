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

          if type(patt1[0]) == type(1) or type(patt2[0]) == type(1): #Checks if the patterns contain nested tuples
               match = 0
               if (patt2[0] - patt1[0]) == 0:
                    pass
               elif patt1[0] != 0:
                    match = abs(patt2[0] - patt1[0])/abs(patt1[0])
               else:
                    match = abs(patt2[0] - 0.000001)/0.000001
                    
               return patt1, ratio

          else: #Permutates the given array and recursively finds the best match
               lowestRatio = float('inf')
               bestPerm = None
               for testPerm in itertools.permuations(patt1[1:]):
                    permRatio = 0
                    perm = []
                    for i in range(len(patt1)-1):
                         partPerm, partRatio = alignPatterns(testPerm[i], patt2[i+1])
                         permRatio += partMatch
                         perm += partPerm

                    permRatio = parmRatio/len(patt1) #Assumed number of parts is the same

                    if abs(permRatio) <= abs(lowestRatio):
                         lowestRatio = permRatio
                         bestPerm = perm

               return bestPerm, lowestRatio
          
