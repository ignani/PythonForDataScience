"""
Remove : https://medium.com/analytics-vidhya/gentle-introduction-to-automl-from-h2o-ai-a42b393b4ba2

In this example, we are going to predict whether or not a loan will be paid by the customer.
The data available for us to do this prediction is given below:

Variable            Description
Loan_ID             - Unique Loan ID
Gender              - Male/ Female
Married             - Applicant married (Y/N)
Dependents          - Number of dependents
Education           - Applicant Education (Graduate/ Under Graduate)
Self_Employed       - Self employed (Y/N)
ApplicantIncome     - Applicant income
CoapplicantIncome   - Coapplicant income
LoanAmount          - Loan amount in thousands
Loan_Amount_Term    - Term of loan in months
Credit_History      - credit history meets guidelines
Property_Area       - Urban/ Semi Urban/ Rural
Loan_Status         - Loan approved (Y/N)

"""
import h2o
from h2o.automl import H2OAutoML

h2o.init()

df_train = h2o.import_file('PythonForDataScience/Data/LoanPredictionIII_train.csv')
df_train.head()

# Let’s check the datatypes with .describe() method.
df_train.describe()

# Now we have to separate the features and target variables. AutoML functions take features and the target in x and y variables.
y = "Loan_Status"
x = ['Gender','Married','Education','ApplicantIncome','LoanAmount', 'CoapplicantIncome','Loan_Amount_Term','Credit_History','Property_Area']

# As you can see in this example, the datatype of our target variable — Loan_Status is of type enum.
# If it's referred as int type, then you must change the data type to enum.
df_train[y] = df_train[y].asfactor()
# Note: Failing to change the data type makes AutoML think this is a regression problem which comes at a great cost if you are running models for 10+ hours.

# Great! Now we are ready to fire up the AutoML
# Set the values for max_runtime_secs and/or max_models to set explicit time or number-of-model limits on your run.
# The model will train on the parameters provided. For this tutorial, let us use 10 models and a maximum runtime of about 2 mins.
aml = H2OAutoML(max_models = 10, max_runtime_secs=120, seed = 1)
aml.train(x = x, y = y, training_frame = df_train)

# Once the model is trained, you can access the Leaderboard.
# The leader model is stored at aml.leader and the leaderboard is stored at aml.leaderboard.
# The leaderboard stores the snapshot of the top models.
# The top models are usually the stacked ensembles as they can easily outperform a single trained model.
# To view the entire leaderboard, specify the rows argument of the head() method as the total number of rows:
lb = aml.leaderboard
lb.head()
lb.head(rows=lb.nrows) # Entire leaderboard

# Prediction and Saving the model
# You could use the best leader model to make prediction. This can be done by using the following command:
df_test = h2o.import_file('PythonForDataScience/Data/LoanPredictionIII_test.csv')
prediction = aml.predict(df_test)

# The next step would be to save the trained model.
# There are two ways to save the leader model — binary format and MOJO format.
# If you’re taking your leader model to production, then it is suggested to use MOJO format since it’s optimized for production use.
h2o.save_model(aml.leader, path = "PythonForDataScience/Models/Loan_Pred_Model_III_shaz13")