import streamlit as st

def register_user(users_collection, generate_user_id_func):
    with st.form("register_form"):
        st.subheader("Register New Account")
        username = st.text_input("Name")
        email = st.text_input("Email").lower()
        
        submitted = st.form_submit_button("Register")
        
        if submitted:
            if not username or not email:
                st.error("All fields are required!")
                return None, None
            
            from utils import is_valid_email
            if not is_valid_email(email):
                st.error("Invalid email format!")
                return None, None
            
            if users_collection.find_one({"email": email}):
                st.error("Email already exists. Please login.")
                return None, None
            
            # Pass the users_collection to the function
            user_id = generate_user_id_func(users_collection)
            
            from datetime import datetime
            users_collection.insert_one({
                "user_id": user_id,
                "username": username,
                "email": email,
                "created_at": datetime.now()
            })
            
            from database import get_user_uploads_dir
            user_uploads_dir = get_user_uploads_dir(user_id)
            
            st.success(f"Registered successfully! User ID: {user_id}")
            return user_id, True
    
    return None, None

def login_user(users_collection):
    with st.form("login_form"):
        st.subheader("Login to Your Account")
        email = st.text_input("Email").lower()
        user_id_input = st.text_input("User ID").upper()
        
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if not email or not user_id_input:
                st.error("Both fields are required!")
                return None, None
            
            user = users_collection.find_one({"email": email, "user_id": user_id_input})
            if not user:
                st.error("Email or User ID not found!")
                return None, None
            
            st.success(f"Welcome back, {user['username']}!")
            return user["user_id"], False
    
    return None, None