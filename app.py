import streamlit as st
from onno import *

if st.session_state['logged_in'] == None:
    auth = Auth()
    auth.display()
else:
    st.sidebar.title("Nav")
    selection = st.sidebar.radio('', ["Data", "Chatbot", 'Settings', 'Temp'])

    if selection == "Temp":
        temp = Temp()
        temp.display()
    elif selection == "Data":
        data_webpage = Data()
