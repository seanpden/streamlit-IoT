# Page for viewing full DF, simulating two events, and viewing data for debugging
# TODO: Implement simulation buttons
# TODO: Better labels/titles/etc.

import streamlit as st
import sqlalchemy
import pandas as pd

# --- CONFIG/SETUP ---

st.set_page_config("Events Page", ":bulb:", "wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

col3, col4, col5, col6 = st.columns([1, 1, 1, 1])

# --------------------

# --- FUNCTIONS ---
cnxn_str = str('postgresql://Team5:team5@138.26.48.83/Team5DB')
engine = sqlalchemy.create_engine(cnxn_str)
# engine = engine.raw_connection()

# @st.cache
def get_water():
    return pd.DataFrame(pd.read_sql(sql='SELECT * FROM water', con=engine)).sort_values(by=['time'])

# @st.cache
def get_electric():
    return pd.DataFrame(pd.read_sql(sql='SELECT * FROM electric', con=engine)).sort_values(by=['time'])

# @st.cache
def get_events():
    return pd.DataFrame(pd.read_sql(sql='SELECT * FROM events', con=engine)).sort_values(by=['time'])

# @st.cache
def get_hvac():
    return pd.DataFrame(pd.read_sql(sql='SELECT * FROM hvac', con=engine)).sort_values(by=['time'])

# -----------------

# --- PAGE CONTENT ---

with col1:
    st.button("Simulate Bath...", "bath_sim", "Demo: Simulates bath times")

with col2:
    st.button("Simulate Microwave...", 'microwave_sim', "Demo: Simuates microwave usage")

with col3:
    st.subheader("HVAC table")
    hvac = get_hvac()
    st.dataframe(hvac)

with col4:
    st.subheader("Events table")
    events = get_events()
    st.dataframe(events)

with col5:
    st.subheader("Electric table")
    electric = get_electric()
    st.dataframe(electric)

with col6:
    st.subheader("Water table")
    water = get_water()
    st.dataframe(water)

# --------------------