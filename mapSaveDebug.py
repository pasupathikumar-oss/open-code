import bge.logic as logic
import math
import random
import copy
import bge.render as render
import numpy
import os
cont = logic.getCurrentController()
own = cont.owner
scene = logic.getCurrentScene()
def saveMapToFile(map,fileName):
    with open(fileName, 'w') as saveFile:
        saveFile.write(str(map))
        saveFile.close()
def readFile(fileName):
    fileName = os.path.dirname(os.path.realpath(__file__))+os.sep+"maps"+os.sep+fileName
    print("loading map data from "+str(fileName))
    saveDataString = ""
    with open(fileName) as data:
        for line in data:
            saveDataString+=str(line)
    return ast.literal_eval(saveDataString)

saveMapToFile(logic.expandPath("//"),"/Users/timothy/ROOT.txt")
import os
print("saved file")
#print(readFile("custom.fmp"))
print(logic.expandPath("//"))