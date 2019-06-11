import h2o

h2o.init()

df = h2o.import_file('PythonForDataScience/Data/beers.csv')
