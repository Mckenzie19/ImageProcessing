# MEMO

MEmory MOdels (MEMO) contains the models used as the "memory" of the Learning AGent (LAG). The current data structures only account for Simple Black and White Images, but will contain more complex models later on.

### To Do

1. ~~Confirm basic data output~~
2. Updates to Expansion function broke analyzeImage continuity checks - IN PROGRESS
3. Adjust shape analysis to store part distance relations (rectangles vs squares) (NOTE: Should each element in a pattern contain its own weight? Ex. Triangle patterns would have a high weight on the number of parts (3), but not on the angle values)
4. Look into making pattern analysis / alignments recursive?
5. Create a more confident way to determine "completness" of analysis in analyzeImage()
6. Look into ways to adjust model network to be more generalized and adaptable
