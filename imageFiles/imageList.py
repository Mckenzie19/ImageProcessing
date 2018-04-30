import os

fileNames = [f for f in os.listdir(os.path.dirname(os.path.realpath("imageList.py"))) if (os.path.isfile(f) and (".jpg" in f))]
