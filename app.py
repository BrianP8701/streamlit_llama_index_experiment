import streamlit as st
from onno import *

if not 'logged_in' in st.session_state:
    auth = Authentication()
    auth.display()
else:
    st.sidebar.title("Nav")
    selection = st.sidebar.radio('', ["Temp", "Data", "Chatbot", 'Settings'])

    if selection == "Temp":
        temp = Temp()
        temp.display()
    elif selection == "Data":
        data_webpage = Data()
        data_webpage.display()
