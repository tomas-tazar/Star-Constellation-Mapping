import csv
import pandas as pd
constArr = pd.array

class Star:
    def __init__(self, name, position, magnitude):
        self.name = name
        self.position = position
        self.magnitude = magnitude

def main():
    nameofConst = str(input("Please enter the full name of the constellation or the respective abbreviation: "))
    constArr = pd.read_csv('bsc5.dat', nrows=5)
    print(constArr)

    if nameofConst in constArr:
        for nameofConst in constArr:
            indexMatch = constArr.index(nameofConst)
            newStar = Star(indexMatch[1], indexMatch[2], indexMatch[3])
            indexMatch += 1
            print("Returning star objects.")
            print(newStar)
            return newStar            
    else:
        print("No constellation found.")
main()



