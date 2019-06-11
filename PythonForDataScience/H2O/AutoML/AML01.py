import h2o
from h2o.automl import H2OAutoML

h2o.init()

df_train = h2o.import_file('PythonForDataScience/Data/titanic.csv')

x = df_train.columns
y = "Survived"
x.remove(y)

df_train[y] = df_train[y].asfactor()
df_train.describe()     # required only to check out the data. Remove for production.
aml = H2OAutoML(max_runtime_secs=30)
aml.train(x = x, y = y, training_frame=df_train)

leader = aml.leader

leader
leaderboard = aml.leaderboard
leaderboard.head()