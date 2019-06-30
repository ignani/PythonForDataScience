import json

# Import the config data into json object
with open('PythonForDataScience/Data/json_sample02.json') as f:
    importConfig = json.load(f)

def find(element, json):
    keys = element.split('.')
    rv = json
    for key in keys:
        rv = rv[key]
    return rv

for x in importConfig:
    a = x


# find('quiz.sport',importConfig)
for key,value in importConfig:
    print(key + '-' + value)
    print("The key and value are ({}) = ({})".format(key, value))

for song in importConfig:
    # now song is a dictionary
    for attribute, value in song.iteritems():
        print(attribute, value) # example usage

for (k, v) in importConfig.items():
   print("Key: " + k)
   print("Value: " + str(v))

find('Name',importConfig)
importConfig.itervalues()