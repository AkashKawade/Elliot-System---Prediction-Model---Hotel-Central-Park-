#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import pandas as pd

# Define the start and end dates
start_date = "01-01-2023"
end_date = "28-02-2023"

# API URL (Fetching all data)
url = "https://render-ivuy.onrender.com/data"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Ensure Date column is in datetime format
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

    # Convert start and end dates to datetime
    start_date = pd.to_datetime(start_date, format="%d-%m-%Y")
    end_date = pd.to_datetime(end_date, format="%d-%m-%Y")

    # Filter DataFrame by date range
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    print(filtered_df)

except requests.exceptions.RequestException as e:
    print("Error fetching data:", e)


# In[ ]:





# In[ ]:




