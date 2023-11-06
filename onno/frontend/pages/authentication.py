import streamlit as st
from onno.shared.utils.authentication_utils import check_username_exists, hash_password, get_password, check_password
from onno.frontend.helpers.user_utils import initialize_user_info
from onno.shared.utils.database_utils import retrieve_user_info
class Authentication:
    def __init__(self):
        pass
    
    def display(self):
        login_tab, signup_tab = st.tabs(
            ["Log In", "Sign Up"]
        )
        with login_tab:
            st.title("Login")
            username = st.text_input("Username", key='login_username')
            password = st.text_input("Password", key='login_password', type="password")
            if st.button("Login"):
                if check_username_exists(username):
                    if check_password(password, get_password(username)):
                        st.success("Logged In as {}".format(username))
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        st.session_state['user_info'] = retrieve_user_info(username)
                        st.rerun()
                    else:
                        st.error(f"Incorrect Password: {str(hash_password(password))} != {get_password(username)}")
                else:
                    st.error("Username does not exist")

        with signup_tab:
            st.title("Sign Up")
            username = st.text_input("Username", key='signup_username')
            password = st.text_input("Password", key='signup_password', type="password")
            email = st.text_input("Email")
            if st.button("Sign Up"):
                if check_username_exists(username):
                    st.error("Username already exists")
                else:
                    user_info = initialize_user_info(username, hash_password(password), email)
                    st.success("Signed up as {}".format(username))
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state['user_info'] = user_info
                    st.rerun()
