import json

with open('PythonForDataScience/Data/json_sample03.json') as jsonFile:
    importConfig = json.load(jsonFile)

for elem in importConfig:
    if type(elem)==dict:
        for subelem in elem:
            val=elem[subelem]
#    elif type(elem)==list:
    # loop list
    # continue elif for all the following types
    #     dict
    #     list
    #     str
    #     int
    #     float
    #     True
    #     False
    #     None