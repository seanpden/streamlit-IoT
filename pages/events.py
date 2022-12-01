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
    # return pd.DataFrame(pd.read_sql(sql='SELECT week_of_year, SUM(usage::FLOAT) AS sum_of_usage FROM new_water GROUP BY week_of_year ORDER BY week_of_year ASC', con=engine))
    return pd.DataFrame(pd.read_sql(sql='SELECT * FROM water', con=engine)).sort_values(by=['time'])

# @st.cache
def get_electric():
    # return pd.DataFrame(pd.read_sql(sql='SELECT week_of_year, SUM(usage::FLOAT) AS sum_of_usage FROM new_electric GROUP BY week_of_year ORDER BY week_of_year ASC', con=engine))
    return pd.DataFrame(pd.read_sql(sql='SELECT * FROM electric', con=engine)).sort_values(by=['time'])

# @st.cache
def get_events():
    return pd.DataFrame(pd.read_sql(sql='SELECT * FROM events', con=engine)).sort_values(by=['time'])

# @st.cache
def get_hvac():
    # return pd.DataFrame(pd.read_sql(sql='SELECT week_of_year, AVG(interiortemp::FLOAT) AS mean_of_temp FROM new_hvac GROUP BY week_of_year ORDER BY week_of_year ASC', con=engine))
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


# # NEW TABLE CREATION, IGNORE

# def new_hvac_sql():
#     hvac = pd.DataFrame(pd.read_sql(sql='SELECT * FROM hvac', con=engine)).sort_values(by=['time'])
#     hvac['day_of_month'] = pd.DatetimeIndex(hvac['time']).day
#     hvac['month'] = pd.DatetimeIndex(hvac['time']).month
#     hvac['year'] = pd.DatetimeIndex(hvac['time']).year
#     hvac['day_of_year'] = pd.DatetimeIndex(hvac['time']).day_of_year
#     hvac['day_of_week'] = pd.DatetimeIndex(hvac['time']).weekday
#     hvac['week_of_year'] = pd.to_datetime(hvac['time']).dt.isocalendar().week
#     hvac.to_sql(name='new_hvac', con=engine, if_exists='fail')

# def new_water_sql():
#     water = pd.DataFrame(pd.read_sql(sql='SELECT * FROM water', con=engine)).sort_values(by=['time'])
#     water['usage'] = water['cost'].replace('[\$,]', '', regex=True).astype(float)
#     water['real_cost'] = (water['usage']*0.00336)
#     water['day_of_month'] = pd.DatetimeIndex(water['time']).day
#     water['month'] = pd.DatetimeIndex(water['time']).month
#     water['year'] = pd.DatetimeIndex(water['time']).year
#     water['day_of_year'] = pd.DatetimeIndex(water['time']).day_of_year
#     water['day_of_week'] = pd.DatetimeIndex(water['time']).weekday
#     water['week_of_year'] = pd.to_datetime(water['time']).dt.isocalendar().week
#     water.to_sql(name='new_water', con=engine, if_exists='fail')

# def new_electric_sql():
#     electric = pd.DataFrame(pd.read_sql(sql='SELECT * FROM electric', con=engine)).sort_values(by=['time'])
#     electric['usage'] = electric['cost'].replace('[\$,]', '', regex=True).astype(float)
#     electric['real_cost'] = ((electric['usage']*(1/1000))*0.12)
#     electric['day_of_month'] = pd.DatetimeIndex(electric['time']).day
#     electric['month'] = pd.DatetimeIndex(electric['time']).month
#     electric['year'] = pd.DatetimeIndex(electric['time']).year
#     electric['day_of_year'] = pd.DatetimeIndex(electric['time']).day_of_year
#     electric['day_of_week'] = pd.DatetimeIndex(electric['time']).weekday
#     electric['week_of_year'] = pd.to_datetime(electric['time']).dt.isocalendar().week
#     electric.to_sql(name='new_electric', con=engine, if_exists='fail')

# def new_events_sql():
#     events = pd.DataFrame(pd.read_sql(sql='SELECT * FROM events', con=engine)).sort_values(by=['time'])
#     events['day_of_month'] = pd.DatetimeIndex(events['time']).day
#     events['month'] = pd.DatetimeIndex(events['time']).month
#     events['year'] = pd.DatetimeIndex(events['time']).year
#     events['day_of_year'] = pd.DatetimeIndex(events['time']).day_of_year
#     events['day_of_week'] = pd.DatetimeIndex(events['time']).weekday
#     events['week_of_year'] = pd.to_datetime(events['time']).dt.isocalendar().week
#     events.to_sql(name='new_events', con=engine, if_exists='fail')

def get_new_hvac():
    return pd.DataFrame(pd.read_sql(sql='SELECT * FROM new_hvac', con=engine))
def get_new_water():
    return pd.DataFrame(pd.read_sql(sql='SELECT * FROM new_water', con=engine))
def get_new_electric():
    return pd.DataFrame(pd.read_sql(sql='SELECT * FROM new_electric', con=engine))
def get_new_events():
    return pd.DataFrame(pd.read_sql(sql='SELECT * FROM new_events', con=engine))

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


# st.button('hvac insert columns', 'hvac_btn', 'new db table test', new_hvac_sql)
foobar = get_new_hvac()
st.dataframe(foobar)

# st.button('water insert columns', 'water_btn', 'new db table test', new_water_sql)
foobar = get_new_water()
st.dataframe(foobar)

# st.button('electric insert columns', 'electric_btn', 'new db table test', new_electric_sql)
foobar = get_new_electric()
st.dataframe(foobar)

# st.button('events insert columns', 'events_btn', 'new db table test', new_events_sql)
foobar = get_new_events()
st.dataframe(foobar)

# --------------------