#!/usr/bin/env python
# coding: utf-8

# In[1]:


import plotly.express as px
import plotly.graph_objs as go

import plotly.io as pio
pio.templates.default = "ggplot2"
pio.renderers.default = "notebook"


# In[ ]:


import pandas as pd

#Create a public URL
#https://docs.google.com/spreadsheets/d/0Ak1ecr7i0wotdGJmTURJRnZLYlV3M2daNTRubTdwTXc/edit?usp=sharing

#get spreadsheets key from url
gsheetkey = "0Ak1ecr7i0wotdGJmTURJRnZLYlV3M2daNTRubTdwTXc"

#sheet name
sheet_name = 'Sheet 1'

url=f'https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=xlsx'
df = pd.read_excel(url,sheet_name=sheet_name)
print(df)

