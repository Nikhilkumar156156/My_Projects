with open('D:\Python\Project_cur\Currency.txt') as f:
    lines = f.readlines()

currencyDict = {}

for line in lines:
    parsed = line.split("\t")
    currencyDict[parsed[0]] = parsed[1]
    

amount = int(input("Enter the amount to be converted in other currencies:"))

for item in currencyDict.keys():
    print(item)

convertin = input("Enter the currency you want to convert:")


print(f"{amount} inr is same as {float(currencyDict[convertin])*amount} {convertin}")