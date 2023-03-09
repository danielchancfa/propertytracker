

import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import datetime

import streamlit as st
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.title('China Property Data Tracker')
st.markdown('''
This is a minimum viable product (MVP) app to show the latest china property transaction trend. I scraped data from 4 source:

Offical Data (scrape data from 1/1/2020 - 7/3/2023):

1. 深圳市住房和建设局 http://zjj.sz.gov.cn/xxgk/ztzl/pubdata/index.html 
2. 武汉市住房和建设局 http://fgj.wuhan.gov.cn/xxgk/xxgkml/sjfb/mrxjspfcjtjqk/

P.S. Offical Data is up to 7/3/2023

Platform Data (scape all listing in 100 pages):
\n

3. 深圳链家网 https://sz.lianjia.com/
4. 武汉链家网 https://wh.lianjia.com/

P.S.  Historical Platform Data is not available
\n

Data is supposed to updated daily automatically by schedule . 
Only data in ShenZhen and WuHun was scraped for demo purpose.
''')
st.title('Instruction')
st.markdown('Please select **:red[data]** on the left side bar')

st.header('Data')
st.markdown("""
Full set of data can be found in https://github.com/danielchancfa/propertytracker

Offical Data: 
1. SZOffical.csv 
2. WHOffical.csv

liangjia Data: 
1. 20230308lianjiaSZ.csv
2. 20230309lianjiaSZ.csv 
3. 20230308lianjiaWH.csv 
4. 20230309lianjiaWH.csv
""")