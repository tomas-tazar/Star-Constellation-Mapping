import os
import sys
import math
import svgwrite
starArr = []
availableConstellations = ["And", "Cap","Col", "Dra", "Lac", "Mus", "Psc", "Tau", "Ant", "Car", "Com", "Eql", "Leo", "Nor", "Pup", "Tel", "Aps", "Cas", "CrA" ,"Eri", "Lep", "Oct", "Pyx", "TrA", "Aql", "Cen", "CrB", "For", "Lib", "Oph","Ret", "Tri", "Aqr", "Cep", "Crt", "Gem", "LMi", "Ori", "Scl", "Tuc", "Ara","Cet", "Cru", "Lup", "Pav", "Sco", "UMa", "Ari", "Cha", "Crv", "Her", "Lyn", "Peg", "Sct", "UMi", "Aur", "Cir", "CVn","Hor", "Lyr","Per", "Ser","Vel", "Boo","CMa","Cyg","Hya","Men","Phe","Sex","Vir", "Cae","CMi","Del","Hyi","Mic","Pic","Sge","Vol","Cam","Cnc","Dor","Ind","Mon","PsA","Sgr", "Vul"]

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

choose = str(input("Welcome to the Star Constellation Mapper, would you like to display a list of possible constellation inputs? \n[y/n]: "))
if (choose == 'y'):
    print("\n", availableConstellations, '\n')
elif (choose == 'n'):
    pass
else:
    sys.exit(1)

nameofConst = str(input("Please enter the respective abbreviation of the constellation that you want to map: "))
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
        
        try: #https://en.wikipedia.org/wiki/Color_index
            if (colourB - colourV) < float(-0.02):
                colour = '#c0cfff'
            elif(colourB - colourV) < float(-0.30):
                colour = '#50a0ff'
            elif(colourB - colourV) < float(-0.33):
                colour = '#7070ff'
            elif (colourB - colourV) > float(0):
                colour = '#cfffff'
            elif(colourB - colourV) > float(0.30):
                colour = '#fcfcfc'
            elif(colourB - colourV) > float(0.58):
                colour = '#efffdf'
            elif(colourB - colourV) > float(0.81):
                colour = '#ffff7f'
            elif(colourB - colourV) > float(1.40):
                colour = '#ff7f7f'

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
dwg.add(dwg.rect(insert=(0, 0), size=(2000, 2000), fill='black'))

for Star in starArr:
    fcoordX = (Star.x - minY) / (maxX - minX)
    fcoordY = (Star.y - minY) / (maxY - minY)
    resX = (1-fcoordX) * (500)
    resY = (1-fcoordY) * (500)
    dwg.add(dwg.circle(center=(resX, resY), r=max(1,5-Star.magnitude), stroke='none', fill=Star.colour))
    dwg.save()

'''
try:
    file_handle = open("SVGs", 'w')
except IOError as e:
    print(str(e))
    exit(1)

file_handle.write(str(dwg))
'''

if lenOfStarArray != 0:
    print('\nSuccess! \nCheck your folder for the SVG image output!')
    cont = str(input("\nWould you like to map another constellation? [y/n]: "))
    if cont == 'y':
        os.system('python "main.py"')
    else:
        print("Goodbye!")
        sys.exit(0)

        
            





