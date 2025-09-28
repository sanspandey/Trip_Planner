import streamlit as st 
import requests
import os
from dotenv import load_dotenv
from agent import plan_trip

load_dotenv()

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Trip Planner", page_icon="✈️")

if "token" not in st.session_state:
    st.session_state.token = None
if "email" not in st.session_state:
    st.session_state.email = None

st.title("AI Trip Planner Menu")

page = st.sidebar.radio(
    "Go to",
    ["Home", "SignUP", "Login", "Plan a Trip"]
)

if page.lower() == "signup":
    st.header("Create an Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        try:
            resp = requests.post(
                f"{API_URL}/auth/signup",
                json={"email": email, "password": password},
                timeout=10
            )
            try:
                data = resp.json()
            except ValueError:
                st.error(f"server returned non-JSON: {resp.text}")
                data = {}
                
            if resp.status_code == 201:
                st.success(data.get('message',"Account Created!"))
            else:
                st.error(data.get("detail","sighnup failed"))
        except Exception as e:
            st.error(f"Request Failed: {e}")

elif page.lower() == 'login':
    st.header("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button('Login'):
        try:
            resp = requests.post(
                f"{API_URL}/auth/login",
                json={"email": email, "password": password},
                timeout=10
            )
            try:
                data = resp.json()
            except ValueError:
                st.error(f"Server returned non-JSON : {resp.text}")
                data = {}
                
            if resp.status_code == 200:
                st.session_state.token = True
                st.session_state.email = email
                st.success(data.get("message", "Login Successful"))
            else:
                st.error(data.get("detail","Login Failed"))
        except Exception as e:
            st.error(f"Request Failed: {e}")

elif page == "Plan a Trip":
    st.header("AI Trip Planner")
    if not st.session_state.token:
        st.warning("Please log in first")
    else:
        destination = st.text_input("Destination (city/country)")
        days = st.number_input("Number of Days", min_value=1)
        preferences = st.text_input("Your Preferences (food, adventure, culture)")
        if st.button("Generate plan"):
            with st.spinner("Talking to AI..."):
                itinerary = plan_trip(destination, int(days), preferences)
            st.subheader("Your Trip Planner")
            st.markdown(itinerary)

else:
    st.title("Welcome to the AI Trip Planner")
    st.write("Use the menu sidebar to sign up and create your dream trip")
