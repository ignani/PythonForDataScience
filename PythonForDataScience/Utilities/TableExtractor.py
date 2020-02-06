import csv
import re

def loadCsv(file):
    lines=csv.reader(open(r'{}'.format(file)))
    dataSet=list(lines)

    #replacing multiple spaces with ','
    for i in range(len(dataSet)):
        if(len(dataSet[i])==1):
            dataSet[i]=(re.sub('\s\s+',',',dataSet[i][0])).split(',')

    #removing blank items
    for i in dataSet:
        for j in i:
            if(j==""):
                i.remove(j)

    dataSet.append([])
    dataSet.append([])

    result=[]
    i=0
    while i<(len(dataSet)-1):
        if(len(dataSet[i+1])-len(dataSet[i])<2 and len(dataSet[i])>2):
            table=[]
            while(dataSet[i]!=[]):
                if(len(dataSet[i])==1):
                    dataSet[i-1].append(dataSet[i][0])
                else:
                    table.append(dataSet[i])
                i+=1
            result.append(table)
        else:
            while(dataSet[i]!=[]):
                i+=1
        i+=1

    for tab in result:
        for row in tab:
            print(row)
        print("\n")

def main():
    loadCsv('sample.csv')

main()