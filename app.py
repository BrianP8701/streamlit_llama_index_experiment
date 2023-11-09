import streamlit as st
from onno import *
from onno.frontend.utils.database_utils import Database

st.session_state['DATABASE'] = Database(st.secrets['GOOGLE_FIREBASE_KEY'], st.secrets['GOOGLE_SERVICE_ACCOUNT_KEY'])
if not 'logged_in' in st.session_state:
    auth = Authentication()
    auth.display()
else:
    st.sidebar.title("Onno")
    selection = st.sidebar.radio('', ["Data", "Chatbot", 'Settings'])

    if selection == "Data":
        data_webpage = Data()
        data_webpage.display()
