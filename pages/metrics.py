# Page for data dashboard...
# Scorecards for: Elec. usage/cost, water usage/cost
# Graphs for: elec. usage/cost over time, water usage/cost over time
# TODO: BETTER FORMAT, more scorecards?
# TODO: MORE LABELS

import streamlit as st
import meteostat as ms
from datetime import datetime
import plotly.express as px
import sqlalchemy
import pandas as pd
import numpy as np

# --- CONFIG/SETUP ---

st.set_page_config("Metrics", ":bar_chart:", "wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,2])
col4, col5= st.columns([1,1])

# --------------------

# --- FUNCTIONS ---

cnxn_str = str('postgresql://Team5:team5@138.26.48.83/Team5DB')
engine = sqlalchemy.create_engine(cnxn_str)

# @st.cache
def get_water():
    # df[df.columns[1:]] = df[df.columns[1:]].replace('[\$,]', '', regex=True).astype(float)
    water = pd.DataFrame(pd.read_sql(sql='SELECT * FROM water', con=engine)).sort_values(by=['time']).drop(columns=['id'])
    # water['month'] = pd.DatetimeIndex(water['time']).month_name()
    water['month'] = pd.DatetimeIndex(water['time']).month
    water['usage'] = water['cost'].replace('[\$,]', '', regex=True).astype(float)
    water['real_cost'] = (water['usage']*0.00336)
    return water.groupby(['month']).sum()

# @st.cache
def get_electric():
    electric = pd.DataFrame(pd.read_sql(sql='SELECT * FROM electric', con=engine)).sort_values(by=['time']).drop(columns=['id'])
    # electric['month'] = pd.DatetimeIndex(electric['time']).month_name()
    electric['month'] = pd.DatetimeIndex(electric['time']).month
    electric['usage'] = electric['cost'].replace('[\$,]', '', regex=True).astype(float)
    electric['real_cost'] = ((electric['usage']*(1/1000))*0.12)
    return electric.groupby(['month']).sum()

# @st.cache
def get_events(grouped=None, stat=None):
    events = pd.DataFrame(pd.read_sql(sql='SELECT * FROM events', con=engine)).sort_values(by=['time'])
    events['month'] = pd.DatetimeIndex(events['time']).month_name()
    return events.groupby(['month'])

# @st.cache
def get_hvac():
    hvac = pd.DataFrame(pd.read_sql(sql='SELECT * FROM hvac', con=engine)).sort_values(by=['time'])
    hvac['month'] = pd.DatetimeIndex(hvac['time']).month
    return hvac.groupby(['month']).mean()

# -----------------

# --- PAGE CONTENT ---

water = get_water()

st.sidebar.header("Filters here...")
month = st.sidebar.multiselect(
    "Which month number to select?",
    options=water.index.unique(),
    default=water.index[0]
)

water_select = water.query(
    "month == @month"
)

elec = get_electric()

elec_select = elec.query(
    "month == @month"
)

hvac = get_hvac()

with col1:
    st.metric(f"Water Cost: {month}", f"${(water_select['real_cost'].sum()):.2f}", f"Water usage (gallons): ~{water_select['usage'].sum():.0f}", delta_color="off")

with col2:
    st.metric(f"Electric Cost: {month}", f"${(elec_select['real_cost'].sum()):.2f}", f"Electric usage (watts): ~{elec_select['usage'].sum():.0f}", delta_color="off")

with col3:
    # st.text("Interior/Exterior Farenheit vs. Month Number")
    st.write(px.line(hvac, x=hvac.index, y=[hvac['interiortemp'], hvac['exteriortemp']]).update_layout(title="Interior/Exterior temp vs. Time"))

with col4:
    st.write(px.line(elec, x=elec.index, y=[elec['usage'], elec['real_cost']]).update_layout(title="Electricity usage and cost vs. Time"))

with col5:
    st.write(px.line(water, x=water.index, y=[water['usage'], water['real_cost']]).update_layout(title="Water usage and cost vs. Time"))

# --------------------