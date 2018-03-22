# RESIP
RElative Spatial Image Processing (RESIP) is an in progress model developed to analyze images based upon the relative shape of the objects within the images. The current heuristic is geared towards simple black and white images, where simple indicates that there is only a single object within the image and that object contains no curves. 

The framework for the Simple BW image processing is created in such a way that other, more complex models can be easily added in. 

The goal of creating this model is to test if a machine learning algorithm can learn the concept behind what distinguishes different shapes from each other. 



### To Do

1. Confirm data output
2. Create a more confident way to determine "completness" of analysis in analyzeImage()
3. Look into ways to adjust model network to be more generalized and adaptable
