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

    def calculateCoordinates(self, asc0, declination0):
        deltaAsc = self.asc - asc0
        self.x = math.cos(self.declination) * math.sin(deltaAsc)
        self.y = math.sin(self.declination) * math.cos(declination0) - math.cos(self.declination) * math.cos(deltaAsc) * math.sin(declination0)

        return self.x, self.y

nameofConst = str(input("Please enter the full name of the constellation or the respective abbreviation: "))
with open('bsc5.dat', 'r') as data:
    for linedata in data.readlines():
        if linedata[11:14] == nameofConst:
            name = nameofConst
        else:
            continue

        try:
            magnitude = float(linedata[102:107])
        except ValueError:
            print("magnitude is not a valid value, star will be invalid!")
            continue

        ascHour, ascMin, ascSec = [float(x) for x in (linedata[75:77], linedata[77:79], linedata[79:83])]
        declinationHour, declinationMin, declinationSec = [float(i) for i in (linedata[83:86], linedata[86:88], linedata[88:90])]

        asc = math.radians((ascHour + ascMin/60 + ascSec/3600) * 15.)
        declination = math.radians(declinationHour + declinationMin/60 + declinationSec/3600)

        starArr.append(Star(name,magnitude,asc,declination))

lenOfStarArray = len(starArr)

sumAscension = sum([Star.asc for Star in starArr])
sumDeclination = sum([Star.declination for Star in starArr])
asc0 = sumAscension / lenOfStarArray
declination0 = sumDeclination / lenOfStarArray
x, y = [None]*lenOfStarArray, [None]*lenOfStarArray

for i, Star in enumerate(starArr):
    x[i], y[i] = Star.calculateCoordinates(asc0, declination0)

minX, maxX, minY, maxY = min(x), max(x), min(y), max(y)


lenOfStarArray = len(starArr)
if lenOfStarArray == 0:
    print("There were no stars of your input found in the Yale Bright Star Catalog.")
else:
    print('Returning star objects: \n', starArr)

        
            





