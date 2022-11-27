# Main/Landing page, showing floor plan and interactable toggles
# TODO: Change toggles to push to db
# TODO: Add all buttons, seperate into on/off?
# TODO: Add thermostat control
# TODO: Better labels/titles/etc.

import streamlit as st
import plotly.express as px

# --- CONFIG/SETUP ---

st.set_page_config("Home Page/Sensors", ":house:", "wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

col1, col2 = st.columns([3,1])

# --------------------

# --- FUNCTIONS ---

def door_front_tog():
    st.session_state.door_front = not st.session_state.door_front

def door_back_tog():
    st.session_state.door_back = not st.session_state.door_back

def door_garage_out_tog():
    st.session_state.door_garage_out = not st.session_state.door_garage_out

def door_garage_one_tog():
    st.session_state.door_garage_one = not st.session_state.door_garage_one

def door_garage_two_tog():
    st.session_state.door_garage_two = not st.session_state.door_garage_two

# -----------------

# --- PAGE CONTENT ---
col1.header("Floor Plan:")
with col1:
    st.image('https://cdn.discordapp.com/attachments/1015265506657325098/1041452290663526480/2482a951fb4671796bc6aff788a71049.png')

col2.header("Sensor Controllers:")
with col2:
    # Contains buttons to toggle doors, lights, tv, thermostat, etc.

    # Front Door
    st.button("door_front", "door_front_btn", "Click to open/close the front door", door_front_tog)
    if 'door_front' not in st.session_state:
        st.session_state.door_front = False
    st.write('Toggle status: ', st.session_state.door_front)

    # Back Door
    st.button("door_back", "door_back_btn", "Click to open/close the back door", door_back_tog)
    if 'door_back' not in st.session_state:
        st.session_state.door_back = False
    st.write('Toggle status: ', st.session_state.door_back)

    # door_garage_out
    st.button("door_garage_out", "door_garage_out_btn", "Click to open/close the door_garage_out door", door_garage_out_tog)
    if 'door_garage_out' not in st.session_state:
        st.session_state.door_garage_out = False
    st.write('Toggle status: ', st.session_state.door_garage_out)

    # door_garage_one
    st.button("door_garage_one", "door_garage_one_btn", "Click to open/close the door_garage_one door", door_garage_one_tog)
    if 'door_garage_one' not in st.session_state:
        st.session_state.door_garage_one = False
    st.write('Toggle status: ', st.session_state.door_garage_one)

    # door_garage_two
    st.button("door_garage_two", "door_garage_two_btn", "Click to open/close the door_garage_two door", door_garage_two_tog)
    if 'door_garage_two' not in st.session_state:
        st.session_state.door_garage_two = False
    st.write('Toggle status: ', st.session_state.door_garage_two)
# --------------------