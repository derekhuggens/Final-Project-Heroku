#!/usr/bin/env python
# coding: utf-8

# ## Machine Learning Model: Neural Network

# In[1]:


# Import our dependencies
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,OneHotEncoder
import pandas as pd
import tensorflow as tf

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


# ### Split and scale data

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


# In[17]:


len(X_train[0])


# ### Compile, Train and Evaluate the Model

# In[18]:


# Define the model - deep neural net, i.e., the number of input features and hidden nodes for each layer.
number_input_features = len(X_train[0])
hidden_nodes_layer1 = 320
hidden_nodes_layer2 = 160

nn = tf.keras.models.Sequential()

# First hidden layer
nn.add(tf.keras.layers.Dense(units=hidden_nodes_layer1, input_dim=number_input_features, activation="relu"))

# Second hidden layer
nn.add(tf.keras.layers.Dense(units=hidden_nodes_layer2, activation="relu"))

# Output layer
nn.add(tf.keras.layers.Dense(units=1, activation="sigmoid"))

# Check the structure of the model
nn.summary()


# In[19]:


# Import checkpoint dependencies
import os
from tensorflow.keras.callbacks import ModelCheckpoint

# Define the checkpoint path and filenames
os.makedirs("checkpoints/",exist_ok=True)
checkpoint_path = "checkpoints/weights.{epoch:02d}.hdf5"


# In[20]:


# Compile the model
nn.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])


# In[21]:


# Create a callback that saves the model's weights every 10 epochs
cp_callback = ModelCheckpoint(
    filepath=checkpoint_path,
    verbose=1,
    save_weights_only=True,
    save_freq=240)


# In[22]:


# Train the model
fit_model = nn.fit(X_train_scaled,y_train,epochs=100, callbacks=[cp_callback])


# In[23]:


# Evaluate the model using the test data
model_loss, model_accuracy = nn.evaluate(X_test_scaled,y_test,verbose=2)
print(f"Loss: {model_loss}, Accuracy: {model_accuracy}")


# In[24]:


# Export our model to HDF5 file
nn.save("AutoInsuranceClaims.h5")


# In[ ]:




