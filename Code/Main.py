#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pymongo


# In[7]:


import json
from pymongo import MongoClient

mongo_uri = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=<AppName>"
database_name = "Project_puma_data"

files_and_collections = {
    "C:/<file-path>/1_puma_financial_health_metrics.json": "financial_health_metrics",
    "C:/<file-path>/2_puma_race_and_ethnicity.json": "race_and_ethnicity",
    "C:/<file-path>/SNAP+Meal+Gap+-+2020+data.json": "snap_meal_gap"
}

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]

for file_path, collection_name in files_and_collections.items():
    with open(file_path, "r") as file:
        data = json.load(file)
        collection = db[collection_name]
        result = collection.insert_many(data)
        print(f"Inserted {len(result.inserted_ids)} documents into the collection '{collection_name}'.")

# Close the MongoDB connection
client.close()


# In[8]:


import pandas as pd
from pymongo import MongoClient

# MongoDB connection details
mongo_uri = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=<AppName>"
database_name = "Project_puma_data"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]

# List of collections to fetch
collection_names = ["financial_health_metrics", "race_and_ethnicity", "snap_meal_gap"]

# Dictionary to hold data from each collection
dataframes = {}

for collection_name in collection_names:
    collection = db[collection_name]
    data = list(collection.find())
    df = pd.DataFrame(data)
    dataframes[collection_name] = df
    print(f"Loaded {len(df)} records from collection '{collection_name}'.")

# Close MongoDB connection
client.close()


# In[9]:



snap_data = dataframes["snap_meal_gap"]
puma_race = dataframes["race_and_ethnicity"]
puma_financial = dataframes["financial_health_metrics"]

# Extracting county names from the countystate column in SNAP data
snap_data['County'] = snap_data['countystate'].str.extract(r'^(.*?),')
snap_counties = snap_data['County'].str.strip().unique()

# Filtering rows in PUMA race dataset where puma10_name contains county names
puma_race_filtered = puma_race[puma_race['puma10_name'].str.contains('|'.join(snap_counties), case=False, na=False)]

# Filtering rows in PUMA financial dataset where puma10_name contains county names
puma_financial_filtered = puma_financial[puma_financial['puma10_name'].str.contains('|'.join(snap_counties), case=False, na=False)]


# In[ ]:




