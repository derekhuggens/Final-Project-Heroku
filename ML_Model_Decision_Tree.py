#!/usr/bin/env python
# coding: utf-8

# ## Machine Learning Model: Decision Trees

# In[1]:


# Import our dependencies
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,OneHotEncoder
import pandas as pd
from path import Path
from sklearn import tree
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# Python SQL toolkit and Object Relational Mapper dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql, connect, Error

from config import db_password

import warnings
warnings.filterwarnings('ignore')


# ### Loading data

# In[2]:


# Query to extract data from insurance_claims table in Postgres
# Code adapted from https://pynative.com/python-postgresql-select-data-from-table/

# Create a global string for the PostgreSQL db name
db_name = "insurance_fraud_db"

# Connect to an existing database
connection = psycopg2.connect(user="postgres",
                              password=db_password,
                              host="127.0.0.1",
                              port="5432",
                              database=db_name)

# Create a cursor to perform database operations
cursor = connection.cursor()

# Executing a SQL query
cursor.execute("SELECT * FROM insurance_claims")

# Fetch result
record = cursor.fetchall()

# Close connections
cursor.close()
connection.close()


# In[3]:


# Query to extract column headers from insurance_claims table in Postgres
# Code adabpted from https://kb.objectrocket.com/postgresql/
# "Get The Column Names From A PostgreSQL Table with the Psycopg2 Python Adapter"

try:
    # declare a new PostgreSQL connection object
    conn = psycopg2.connect(user="postgres",
                              password=db_password,
                              host="127.0.0.1",
                              port="5432",
                              database=db_name)

except Exception as err:
    print ("psycopg2 connect() ERROR:", err)
    conn = None
    
# define a function that gets the column names from a PostgreSQL table
def get_columns_names(table):

    # declare an empty list for the column names
    columns = []

    # declare cursor objects from the connection    
    col_cursor = conn.cursor()

    # Select string for query to get column names
    col_names_str = "SELECT column_name FROM information_schema.columns WHERE table_name = 'insurance_claims' ORDER BY ordinal_position"

    try:
        sql_object = sql.SQL(
            # pass SQL statement to sql.SQL() method
            col_names_str
        ).format(
            # pass the identifier to the Identifier() method
            sql.Identifier( table )
        )

        # execute the SQL string to get list with col names in a tuple
        col_cursor.execute( sql_object )

        # get the tuple element from the liast
        col_names = ( col_cursor.fetchall() )

        # iterate list of tuples and grab first element
        for tup in col_names:

            # append the col name string to the list
            columns += [ tup[0] ]

        # close the cursor object to prevent memory leaks
        col_cursor.close()

    except Exception as err:
        print ("get_columns_names ERROR:", err)

    # return the list of column names
    return columns

# if the connection to PostgreSQL is valid
if conn != None:

    # pass a PostgreSQL string for the table name to the function
    columns = get_columns_names( "insurance_claims" )


# In[4]:


# Insert data and column headers into DataFrame
insurance_df = pd.DataFrame(record, columns=columns)
insurance_df.head()


# ### Preprocess the dataset

# In[5]:


insurance_df.dtypes


# In[6]:


insurance_df.nunique()


# In[7]:


# Drop the columns with many distinct values (some have 900+)
insurance_df.drop(columns=["policy_number", "policy_bind_date", "insured_zip", "incident_location", "incident_date"], inplace=True)
insurance_df.head()


# In[8]:


# Convert policy_annual_premium column values from object to float
insurance_df["policy_annual_premium"] = insurance_df["policy_annual_premium"].astype(float, errors = 'raise')
insurance_df.dtypes


# In[9]:


# Replace the fraud_reported column values Y and N with 0 and 1
insurance_df = insurance_df.replace({'fraud_reported': {'Y': 1, 'N': 0}})
insurance_df.head()


# In[ ]:





# ### Convert categorical variables with OneHotEncoding

# In[10]:


# Split our preprocessed data for target array and OneHotEncoder
y = insurance_df["fraud_reported"].values
X_df = insurance_df.drop(["fraud_reported"],1)


# In[11]:


# Generate our categorical variable lists
X_cat = X_df.dtypes[X_df.dtypes == "object"].index.tolist()


# In[12]:


# Check the number of unique values in each column
X_df[X_cat].nunique()


# In[13]:


# Create a OneHotEncoder instance
enc = OneHotEncoder(sparse=False)

# Fit and transform the OneHotEncoder using the categorical variable list
encode_df = pd.DataFrame(enc.fit_transform(X_df[X_cat]))

# Add the encoded variable names to the dataframe
encode_df.columns = enc.get_feature_names_out(X_cat)
encode_df.head()


# In[14]:


# Merge one-hot encoded features and drop the originals
X_df = X_df.merge(encode_df,left_index=True,right_index=True)
X_df = X_df.drop(X_cat,1)
X_df.head()


# ### Split and scale the data

# In[15]:


# Set variable for our features array
X = X_df.values

# Split the preprocessed data into a training and testing dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=78)


# In[16]:


# Creating StandardScaler instance
scaler = StandardScaler()

# Fitting Standard Scaller
X_scaler = scaler.fit(X_train)

# Scaling data
X_train_scaled = X_scaler.transform(X_train)
X_test_scaled = X_scaler.transform(X_test)


# ### Fit the Decision Tree model

# In[17]:


# Creating the decision tree classifier instance
model = tree.DecisionTreeClassifier()

# Fitting the model
model = model.fit(X_train_scaled, y_train)

# Making predictions using the testing data
predictions = model.predict(X_test_scaled)


# ### Model Evaluation

# In[18]:


# Calculating the confusion matrix
cm = confusion_matrix(y_test, predictions)
cm_df = pd.DataFrame(
    cm, index=["Actual 0", "Actual 1"], columns=["Predicted 0", "Predicted 1"]
)

# Calculating the accuracy score
acc_score = accuracy_score(y_test, predictions)


# In[19]:


# Displaying results
print("Confusion Matrix")
display(cm_df)
print(f"Accuracy Score : {acc_score}")
print("Classification Report")
print(classification_report(y_test, predictions))


# In[ ]:




