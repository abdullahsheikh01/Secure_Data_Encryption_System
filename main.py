import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import configparser

st.set_page_config(
    page_title="Store Your Data Securely"
)

def login():
    config  = configparser.ConfigParser()
    config.read("config.ini")
    user_name : str = st.text_input("Enter Your User Name")
    entered_pass = st.text_input("Enter Your Password: ",type="password")
    correct_pass = config["credentials"]["password"]
    correct_user_name = config["credentials"]["username"]
    if st.button("Login"):
        if entered_pass == correct_pass and user_name==correct_user_name:
            st.success("You Login!")
        else:
            st.error("Incorrect Password!")

def store_data():
    st.subheader("Store Your Data Securely")
    user_name : str = st.text_input("Write Your username",autocomplete="off")
    pass_key : str = st.text_input("Enter Your Pass Key",type="password",autocomplete="off")
    data : str = st.text_area("Enter Your Data")
    if st.button("Store"):
        for _ in st.session_state.stored_data:
            if pass_key and data and user_name:
                st.session_state.stored_data[user_name] = {
                    "pass_key" : hashlib.sha256(pass_key.encode()).hexdigest(),
                    "data" : st.session_state.f.encrypt(data.encode('utf-8'))
                }
        else:
            st.error("Please fill all fields:")

def retrieve_data():
    st.subheader("Retrieve Your Data: ")
    user_name : str = st.text_input("Enter Your Username: ")
    pass_keyy : str = st.text_input("Enter Your Passkey of Data: ",type="password",autocomplete="off") 
    if st.button("Retrieve"):
        process = False
        for key in st.session_state.stored_data:
            if key==user_name:
                process = True
                break
            else:
                process = False
        if pass_keyy and process:
            if st.session_state.stored_data[user_name]["pass_key"]==hashlib.sha256(pass_keyy.encode()).hexdigest():
                st.subheader("Your Data: ")
                a = st.session_state.f.decrypt(st.session_state.stored_data[user_name]["data"])
                st.write(a.decode())
        else:
            st.error("Your Passkey or Username is Wrong")

key : bytes = Fernet.generate_key()

if "f" not in st.session_state:
    st.session_state.f = Fernet(key)

st.markdown("# Welcome to Secure Data Encrytion System! by [Abdullah Shaikh](https://www.linkedin.com/in/abdullah-shaikh-29699b302/)")
option : str = st.selectbox("Select ",["Home","Store Data","Retrieve Data","Login"])

if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

if option == "Store Data":
    store_data()
elif option == "Retrieve Data":
    retrieve_data()
elif option == "Login":
    login()