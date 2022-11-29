# Page for viewing full DF, simulating two events, and viewing data for debugging
# TODO: Better labels/titles/etc.

import streamlit as st
import sqlalchemy
import pandas as pd
from datetime import datetime, timedelta

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

# db connection init
cnxn_str = str('postgresql://Team5:team5@138.26.48.83/Team5DB')
engine = sqlalchemy.create_engine(cnxn_str)

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

def bath_sim():
    """Simulates a bath
    """
    now = datetime.now()
    later = now+timedelta(minutes=+30)
    engine.execute("INSERT INTO events (time, type, status) VALUES (%s, %s, %s)" % (now, "bath", True))
    engine.execute("INSERT INTO events (time, type, status) VALUES (%s, %s, %s)" % (later, "bath", False))
    engine.execute("INSERT INTO water (cost, time) VALUES (%s, %s)" % (.65*30, later))
    engine.execute("INSERT INTO electric (cost, time) VALUES (%s, %s)", (4500/2, later))

def microwave_sim():
    """Simulates a shower
    """
    now = datetime.now()
    later = now+timedelta(minutes=2)
    engine.execute("INSERT INTO events (time, type, status) VALUES (%s, %s, %s)", now, "microwave", True)
    engine.execute("INSERT INTO events (time, type, status) VALUES (%s, %s, %s)", later, "microwave", False)
    engine.execute("INSERT INTO electric (cost, time) VALUES (%s, %s)", (1100/60)*2, later)




# -----------------

# --- PAGE CONTENT ---

with col1:
    st.button("Simulate Bath...", "bath_sim", "Demo: Simulates bath times", bath_sim)

with col2:
    st.button("Simulate Microwave...", 'microwave_sim', "Demo: Simuates microwave usage", microwave_sim)

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