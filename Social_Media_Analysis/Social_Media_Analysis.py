#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import matplotlib as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objs as go

import plotly.io as pio
pio.templates.default = "ggplot2"
pio.renderers.default = "notebook"


# In[2]:


gsheetkey = "1kax9m1FKah7cWPwylxhdJSyqF5eVALjgRbxyPuPg7g0"
sheet_name = 'Social_Media_Analysis'
url= f'https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=xlsx'

sheet = pd.read_excel(url, sheet_name = sheet_name)


# In[3]:


df = (
    sheet
    .resample('M', on='Date')
    .count()
    [["Platform"]]
    .reset_index()
    .rename(columns={"Platform":"Count"})
)

df["Date"] = df["Date"].dt.strftime('%Y-%m')


# In[4]:


sets = [
    df[(df["Date"] <= "2022-01")],
    df[(df["Date"] >= "2022-01") & (df["Date"] <= "2022-06")],
    df[df["Date"] >= "2022-06"]
]


# In[5]:


fig = go.Figure().update_layout(
  # Title and Subtitle
  title =
  	"Monthly Social Media Posts" +
  	"<br><sup>" + "Higher is better" + "</sup>",
  title_x = 0.08, #left-align

  # axes titles
  xaxis_title = "Time",
  yaxis_title = "Number of Posts",
    
  # legend
  showlegend = True,
  legend = dict(
  	orientation = 'h',
    
    # positioning
    yanchor = "bottom",
    y = 1,
    xanchor = "left",
    x = 0
  )
).update_xaxes(
    range = [df["Date"].iloc[0], df["Date"].iloc[-1]]
).update_yaxes(
    range = [0, 1.1 * df["Count"].max()]
)

fig.add_trace(go.Scattergl(
    x = sets[0]["Date"],
    y = sets[0]["Count"],
    name = "Before Joining",
    mode = "lines"
    )
)

fig.add_trace(go.Scattergl(
    x = sets[1]["Date"],
    y = sets[1]["Count"],
    name = "After Joining",
    visible='legendonly',
    mode = "lines"
    )
)

fig.add_trace(go.Scattergl(
    x = sets[2]["Date"],
    y = sets[2]["Count"],
    name = "Without",
    visible='legendonly',
    mode = "lines"
    )
)


fig.show(config = dict(
      doubleClickDelay = 400, # (ms) affects the single click delay; default = 300ms
      displayModeBar = False,
      showTips = False
))


# In[6]:


fig.write_html("social_media_analysis_plotly.html",
               full_html=False,
               include_plotlyjs = "../../../backend/plugins/plotly/plotly-basic.min.js",
               config = dict(
                 doubleClickDelay = 400, # (ms) affects the single click delay; default = 300ms
                 displayModeBar = False,
                 showTips = False
               )
              )

