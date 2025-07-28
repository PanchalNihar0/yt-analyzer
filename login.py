
import time
from streamlit_option_menu import option_menu
import home,profile,history
import streamlit as st

from db import (
    login_user, register_user, create_user_table, create_analysis_table,
    fetch_user_history
)

# Initialize tables
create_user_table()
create_analysis_table()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# Signup Page
def signup():
    st.subheader("🔐 Signup")
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    if st.button("Create Account"):
        if not username or not password:
            st.warning("Username and password required.")
        else:
            try:
                register_user(username, password)
                st.success("Account created! Please log in.")
            except:
                st.error("Error during registration. Username may already exist.")

# Login Page
def login():
    st.subheader("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")

# Logged-in Dashboard
def dashboard():
    
    # st.sidebar.header("MENU")
    class MultiApp:
        def __init__(self):
            self.apps=[]
        def add_app(self,title,function):
            self.apps.append({
                "title" : title,
                "function" : function} )
        def run():
            with st.sidebar:
                app = option_menu(
                    menu_title='MENU',
                    options=['home','profile','history'],
                    menu_icon='chat-text-fill',
                    default_index=0
                    ) # type: ignore
            if app=='home':
                home.app()
            if app== 'profile':
                profile.app()
            if app=='history':
                history.app()
        run()
 # type: ignore
    # st.sidebar.button('Profile')
    # st.sidebar.button('History')
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.experimental_rerun()

# Main UI
if st.session_state.logged_in:
    dashboard()
else:
    st.title("🧑‍💻 Login & Signup with MySQL")
    menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

    if menu == "Signup":
        signup()
    else:
        login()


