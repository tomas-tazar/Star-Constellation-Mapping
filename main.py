import os
import sys
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

asc0sum = sum([Star.asc for Star in starArr])
declination0sum = sum([Star.declination for Star in starArr])

x, y = [None]*lenOfStarArray, [None]*lenOfStarArray


try:
    asc0 = asc0sum / lenOfStarArray
except ZeroDivisionError:
    print("Unable to add star from constellation! It it likely the name of the constellation you entered is invalid.")
    sys.exit(1)

try:
    declination0 = declination0sum / lenOfStarArray
except ZeroDivisionError:
    print("Unable to add star from constellation! It it likely the name of the constellation you entered is invalid.")
    sys.exit(1)

for i, Star in enumerate(starArr):
    x[i], y[i] = Star.calculateCoordinates(asc0, declination0)

minX, maxX, minY, maxY = min(x), max(x), min(y), max(y)
aspectratio = 0.8

width = 500
height = 500

with open('{:s}.svg'.format(name), 'w') as fileoutput:
    print('<?xml version="1.0" encoding="utf-8"?>', file=fileoutput)
    print('<svg xmlns="http://www.w3.org/2000/svg"', file=fileoutput)
    print('xmlns:xlink="http://www.w3.org/1999/xlink"', file=fileoutput)
    print('width="{:d}" height="{:d}" style="background: #000000">'.format(width, height), file=fileoutput)
    for Star in starArr:
        rx = (Star.x - minX) / (maxX - minX)
        ry = (Star.y - minY) / (maxY - minY)
        cx = (1-rx) * (width)
        cy = (1-ry) * (height)
        print('<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}"'' stroke="none" fill="#ffffff" name="{name:s}"/>'.format(cx=cx, cy=cy, r=max(1,5-Star.magnitude), name=Star.name), file=fileoutput)
    print('</svg>', file=fileoutput)

if lenOfStarArray != 0:
    print('\nSuccess! \nCheck your folder for the SVG image output!')
    cont = str(input("Would you like to map another constellation? [y/n]: "))
    if cont == 'y':
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    else:
        print("Goodbye!")
        sys.exit(0)

        
            





