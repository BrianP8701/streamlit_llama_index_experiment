import streamlit as st

def initialize_user_info(username: str, hashed_password: str, email: str):
    user_info = {
        'username': username,
        'password': hashed_password,
        'email': email,
        'libraries': {}
    }
    st.session_state['DATABASE'].save_user_info(username, user_info)
    st.session_state['DATABASE'].create_folder(f'users/{username}/libraries/')
    return user_info

def create_new_empty_library(username: str, library_name: str):
    st.session_state['DATABASE'].create_folder(f'users/{username}/libraries/{library_name}/raw/')
    st.session_state['DATABASE'].create_folder(f'users/{username}/libraries/{library_name}/text/')
    