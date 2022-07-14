import os
import sys
import math
import svgwrite
starArr = []
availableConstellations = []

class Star:
    def __init__(self, name, magnitude, asc, declination, colour):
        self.name = name
        self.magnitude = magnitude
        self.asc = asc
        self.declination = declination
        self.colour = colour

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
            continue
        
        try:
            colourB = float(linedata[102:107])
            colourV = float(linedata[180:184])
            colourR = float(linedata[185:190])     
        except (NameError, ValueError):
            colour = '#FFFFFF'
            
        ascHour, ascMin, ascSec = [float(x) for x in (linedata[75:77], linedata[77:79], linedata[79:83])]
        declinationHour, declinationMin, declinationSec = [float(i) for i in (linedata[83:86], linedata[86:88], linedata[88:90])]
        
        try:
            if (colourB - colourV) < float(0):
                if (colourB - colourV) < float(-3):
                    colour = '#000dff'
                    if(colourB - colourV) < float(-10):
                        colour = '#050dfc'
                else:
                    colour = '#6e72ba'

            if (colourB - colourV) > float(0):
                if(colourB - colourV) > float(3):
                    colour = '#fcfcfc'
                else:
                    colour = '#e4e4ed'
            
            '''
            if (colourV - colourR) < float(-10):
                if(colourV - colourR) < float(-100):
                    colour = '#c2802b'
                    if(colourV - colourR) < float(-160):
                        colour = '#d44317'
                else:
                    colour = '#c2b82b'
            '''
            
        except (NameError, ValueError):
            colour = '#FFFFFF'   

        asc = math.radians((ascHour + ascMin/60 + ascSec/3600) * 15.)
        declination = math.radians(declinationHour + declinationMin/60 + declinationSec/3600)

        starArr.append(Star(name,magnitude,asc,declination,colour))

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


dwg = svgwrite.Drawing('{:s}.svg'.format(nameofConst), profile='full')
dwg.add(dwg.rect(insert=(0, 0), size=(1200, 1200), fill='black'))

for Star in starArr:
    fcoordX = (Star.x - minY) / (maxX - minX)
    fcoordY = (Star.y - minY) / (maxY - minY)
    resX = (1-fcoordX) * (500)
    resY = (1-fcoordY) * (500)
    dwg.add(dwg.circle(center=(resX, resY), r=max(1,5-Star.magnitude), stroke='none', fill=Star.colour))
    dwg.save()

if lenOfStarArray != 0:
    print('\nSuccess! \nCheck your folder for the SVG image output!')
    cont = str(input("Would you like to map another constellation? [y/n]: "))
    if cont == 'y':
        os.system('python "main.py"')
    else:
        print("Goodbye!")
        sys.exit(0)

        
            





