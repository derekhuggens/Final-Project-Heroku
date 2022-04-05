# import dependencies
import pandas as pd
import json

# read in .csv to a pandas DataFrame
df = pd.read_csv (r'C:\Users\Derek\My Drive\School\UCF\Bootcamp\Class Folder\Final-Project-\EDA\insurance_claims.csv')

# convert DataFrame object into a JSON string.
df.to_json (r'C:\Users\Derek\My Drive\School\UCF\Bootcamp\Class Folder\Final-Project-\EDA\insurance_claims.json', orient="table")


