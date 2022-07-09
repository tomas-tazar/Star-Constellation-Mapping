import string
import numpy;

def main():
    constArr = []
    validConstellation = False
    
    nameofConst = str(input("Please enter the full name of the constellation or the respective abbreviation: "))
    with open('BSC5.dat', 'r') as data:
        linedata = data.readlines()
        for i in linedata:
            constArr.append(i)
        if nameofConst in constArr:
            print("Valid constellation!")
            validConstellation = True
        else:
            validConstellation = False
    data.close()
    print(constArr)

    if validConstellation == True:
        return nameofConst
    else:
        print("No contellation parsed.")
main()



    