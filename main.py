def main():
    constArr = []
    validConstellation = False
    
    nameofConst = str(input("Please enter the full name of the constellation or the respective abbreviation: "))
    with open('bsc5.dat', 'r') as data:
        linedata = data.readlines()
        for line in linedata:
            constArr.append(line)
        if nameofConst in constArr:
            validConstellation = True
        else:
            validConstellation = False
    data.close()

    if validConstellation == True:
        indexMatch = constArr.index(nameofConst)
        

    else:
        print("No contellation parsed.")
main()