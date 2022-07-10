import csv
import pandas as pd
import math
starArr = []

class Star:
    def __init__(self, name, magnitude, asc, declination):
        self.name = name
        self.magnitude = magnitude
        self.asc = asc
        self.declination = declination

nameofConst = str(input("Please enter the full name of the constellation or the respective abbreviation: "))
with open('bsc5.dat', 'r') as data:
    for linedata in data.readlines():
        if linedata[11:14] == nameofConst:
            name = nameofConst
        else:
            continue

        try:
            magnitude = float(linedata[102:107])
        except:
            ValueError
            print("magnitude not present, star will be invalid!")
            continue

        asc = [float(x) for x in linedata[75:83]]
        declination = [float(i) for i in linedata[83:90]]
        starArr.append(Star(name,magnitude,asc,declination))

outputMsg = len(starArr)
if outputMsg == 0:
    print("There were no stars of your input found in the Yale Bright Star Catalog.")
else:
    print('Returning star objects: \n', starArr)

        
            





