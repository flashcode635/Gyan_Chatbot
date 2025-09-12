import re
import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.2rem;
        color: #3b82f6;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .sidebar-header {
        font-size: 1.5rem;
        color: #3b82f6;
        margin-bottom: 1rem;
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Logo styling */
    .logo {
        font-size: 2rem;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .small-logo {
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .new-chat-btn {
        background-color: #94a3b8;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.5rem;
        width: 100%;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .new-chat-btn:hover {
        background-color: #b2beb5;
    }
    
    /* Chat bubbles */
    .chat-bubble-user {
        background-color: #dbeafe;
        padding: 1rem;
        border-radius: 1rem 1rem 0 1rem;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #bfdbfe;
    }
    
    .chat-bubble-assistant {
        background-color: #f1f5f9;
        padding: 1rem;
        border-radius: 1rem 1rem 1rem 0;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    /* Typing animation */
    .typing-animation {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #64748b;
        margin: 0 2px;
        animation: typing 1.4s infinite ease-in-out both;
    }
    .typing-animation:nth-child(1) {
        animation-delay: -0.32s;
    }
    .typing-animation:nth-child(2) {
        animation-delay: -0.16s;
    }
    @keyframes typing {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    /* Chat history */
    .chat-history-item {
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 0.25rem 0;
        cursor: pointer;
        transition: background-color 0.2s;
        border: 1px solid #e2e8f0;
        background-color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .chat-history-item:hover {
        background-color: #eff6ff;
        border-color: #93c5fd;
    }
    
    /* Delete button */
    .delete-btn {
        background: none;
        border: none;
        color: #ef4444;
        cursor: pointer;
        font-size: 0.9rem;
        padding: 0.2rem;
        border-radius: 0.25rem;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
    }
    .delete-btn:hover {
        background-color: #fee2e2;
    }
    
    /* Mode selector */
    .mode-selector {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
        gap: 0.5rem;
    }
    .mode-btn {
        flex: 1;
        padding: 0.5rem;
        text-align: center;
        border: 1px solid #d1d5db;
        border-radius: 0.5rem;
        cursor: pointer;
        background-color: #f9fafb;
        transition: all 0.2s;
    }
    .mode-btn.active {
        background-color: #94a3b8;
        color: white;
        border-color: #94a3b8;
    }
    .mode-btn:hover:not(.active) {
        background-color: #e5e7eb;
    }
    
    /* Logo and user info */
    .logo-container {
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 1rem;
        border: 1px solid #bae6fd;
    }
    
    .user-info {
        padding: 0.75rem;
        background-color: #f8fafc;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    /* File delete button */
    .file-delete-btn {
        background: none;
        border: none;
        color: #64748b;
        cursor: pointer;
        font-size: 1rem;
        padding: 0.25rem;
        border-radius: 0.25rem;
    }
    .file-delete-btn:hover {
        color: #ef4444;
        background-color: #fee2e2;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Performance optimizations */
    .stApp > div {
        will-change: transform;
    }
    </style>
    """, unsafe_allow_html=True)

def generate_user_id(users_collection):
    last_user = users_collection.find_one(sort=[("created_at", -1)])
    if not last_user:
        return "USR0001"
    last_id = last_user["user_id"]
    last_num = int(last_id[3:])
    return f"USR{last_num+1:04d}"

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)