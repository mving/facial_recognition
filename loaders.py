"Insert docstring"
from platform import system
from sys import argv
from os import walk
from cv2 import VideoCapture, CAP_DSHOW

PATH_SPLITTER = "\\" if system() == "Windows" else "/"

def load_cascades(directory="."+PATH_SPLITTER):
    """Loads all xml datasets into a dictionary separated by folder

    Arguments:
    directory -- root directory (default .\\ or ./)

    Returns:
    { "directory1" : ["dataset1.xml", "dataset2.xml", ...],  "directory2" : [...], ... }
    """
    cascades = {}

    for root, _, files in walk(directory):
        files = [root.strip("." + PATH_SPLITTER) + PATH_SPLITTER + f for f in files if ".xml" and "cascade" in f]
        if files:
            cascades.update({root.split(PATH_SPLITTER)[-1] : files})
    return cascades

def count_cameras():
    """Counts cameras availables"""
    i = 0
    while True:
        print(i)
        cam = VideoCapture(i)
        if cam is None or not cam.isOpened():
            print("camera is none")
            break
        i = i + 1
        cam.release()
    return i

def find_museo_image(directory="." + PATH_SPLITTER):
    "Finds museo.jpg"

    allfiles = []
    for root, _, files in walk(directory):
        if "museo.jpg" in files:
            return root.strip("." + PATH_SPLITTER) + PATH_SPLITTER + "museo.jpg"

if __name__ == "__main__":
    print("Runing test routine")

    print("load_cascades()")
    PATH = "." + PATH_SPLITTER
    if len(argv) > 1:
        if argv[1][0] == ".":
            PATH = PATH_SPLITTER.join(argv[0].split(PATH_SPLITTER)[:-1]) + argv[1][1:]
        else:
            PATH = argv[1]

    print("Path = ", PATH)
    print(load_cascades())
    print("Test finished")

    print("count_cameras")
    print("Total cameras: ", count_cameras())
    
    print("Finding museo.jpg")
    print(find_museo_image())
    print("Test finished")
