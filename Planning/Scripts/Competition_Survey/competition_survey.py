#!/usr/bin/env python
# coding: utf-8

# # Competition Survey
# 
# Analyse important factors from past results of FS Electric competitions

# # Libraries

# In[1]:


import pandas as pd

import os

import matplotlib.pyplot as plt
get_ipython().run_line_magic('config', "InlineBackend.figure_formats = ['svg'] # makes everything svg by default")
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn import preprocessing


# # Importing Results
# PDFs from FS Website

# In[2]:


rel = "data/"
files = os.listdir("./data")


# In[3]:


def read_file(file):
    if( ".csv" == file[-4:] ):
        df = pd.read_csv(rel + file)
        return df


# In[4]:


raw_formula_student = pd.DataFrame()
for file in files:
    if( ".csv" == file[-4:] ):
        raw_formula_student = pd.concat(
            [raw_formula_student, read_file(file)]
        )


# # Data Cleanup

# In[5]:


def cleanup(df):
    df = df.copy()
    df.dropna(inplace=True)
    df.iloc[:, 2:12] = (
        df.iloc[:, 2:12]
        .apply(lambda x: x.str.replace(',', '.'))
        .values.astype(float)
        )
    df[["Car", "Overall Placing"]] = df[["Car", "Overall Placing"]].values.astype('int32')
    df = df.set_index([
        "Competition",
        "City/University"
    ])
    return df

formula_student = raw_formula_student.pipe(cleanup)
formula_student


# # Analysis

# # Overview

# In[6]:


overview = (
    formula_student[["Car", "Overall Scores"]]
    .groupby(
        ["Competition"]
    )
    .agg({
        'Car' : ["count"],
        'Overall Scores' : ["mean", "min", "max"]
    })
    .round(1)
)

overview.plot(title="Competition overview over time", figsize=(6, 6))


overview


# # Importance of Evaluation Components
# Using **correlation**, the components are sorted in descending order of their importance

# In[7]:


(
    formula_student
    .iloc[:, 1:11]
    .corr()
    .rename(columns={"Overall Scores":"Correlation"})
    [["Correlation"]]
    .sort_values("Correlation", ascending=False)
    .iloc[1:, :] # remove the obvious overall scores = 1.00
)


# # Teams with best cost scores
# 
# We can learn how these teams managed to get such good positions

# In[8]:


(
    formula_student[["Cost", "Overall Placing"]]
    .sort_values("Cost", ascending = False)
    .head(10)
    .sort_values("Overall Placing")
)

