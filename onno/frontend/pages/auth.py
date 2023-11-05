import streamlit as st
from onno.shared.utils.auth import check_username_exists, hash_password, save_user_info, get_password, check_password

class Auth:
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
                    user_info = {
                        'username': username,
                        'password': hash_password(password),
                        'email': email
                    }
                    save_user_info(username, user_info)
                    st.success("Signed up as {}".format(username))
                    st.session_state['logged_in'] = True
                    st.rerun()
