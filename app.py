import streamlit as st
from onno import *

if not 'logged_in' in st.session_state:
    auth = Authentication()
    auth.display()
else:
    st.sidebar.title("Onno")
    selection = st.sidebar.radio('', ["Data", "Chatbot", 'Settings'])

    if selection == "Data":
        data_webpage = Data()
        data_webpage.display()
