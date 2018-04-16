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

          #print("\nPattern 1: ", patt1)
          #print("Pattern 2: ", patt2)

          if type(patt1) in [type(1.0), type(1)]: #Checks if the patterns contain nested tuples

               ratio = 0
               if type(patt2) not in [type(1.0), type(1)]:
                    ratio = float('inf')
               elif (patt2 - patt1) == 0:
                    pass
               elif patt1 != 0:
                    ratio = abs(patt2 - patt1)/abs(patt1)
               else:
                    ratio = abs(patt2 - 0.0000001)/0.0000001
                    
               return patt1, ratio

          else: #Permutates the given array and recursively finds the best match
               lowestRatio = float('inf')
               bestPerm = None
               for testPerm in itertools.permutations(patt1[1:]):
                    #print("Permutation: ", testPerm)
                    totRatio = 0
                    totPerm = [((patt1[0]+patt2[0])/2)]
                    for i in range(len(testPerm)):
                         if type(testPerm[i]) != type(patt2[i+1]):
                              totRatio = float('inf')
                              totPerm.append(testPerm)
                              break
                         partPerm, partRatio = self.alignPatterns(testPerm[i], patt2[i+1])
                         totRatio += partRatio
                         totPerm.append(partPerm)

                    averageRatio = totRatio/len(testPerm)
                    if averageRatio <= lowestRatio:
                         lowestRatio = averageRatio
                         bestPerm = totPerm

               return bestPerm, lowestRatio




          
          
