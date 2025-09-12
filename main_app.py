import os
import time
import streamlit as st
from datetime import datetime
from auth import register_user, login_user
from database import (
    setup_document_collection, process_files_to_collection, 
    query_documents, list_my_chats, generate_chat_title,
    get_user_uploads_dir, get_file_paths_from_uploads
)
from utils import inject_custom_css, is_valid_email
from file_processing import read_file_content

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    st.error("Error: API_KEY not found.")
    st.stop()

# Initialize AI21 client
from ai21 import AI21Client
from ai21.models.chat import ChatMessage
client = AI21Client(api_key=api_key)

# Initialize MongoDB
from pymongo import MongoClient
try:
    mongo_client = MongoClient(os.getenv("MONGO_URI"))
    db = mongo_client["intern_data"]
    collection = db["chat_collection"]
    users_collection = db["users_collection"]
except Exception as e:
    st.error(f"MongoDB Connection Error: {e}")
    st.stop()

# ChromaDB Configuration
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
CHROMA_TENANT = os.getenv("CHROMA_TENANT")
CHROMA_DB = os.getenv("CHROMA_DB")

# Initialize ChromaDB
import chromadb
try:
    if CHROMA_API_KEY:
        chroma_client = chromadb.CloudClient(
            api_key=CHROMA_API_KEY,
            database=CHROMA_DB
        )
    else:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
except Exception as e:
    st.error(f"ChromaDB Error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Gyan Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def generate_user_id(users_collection):
    """Generate a new user ID"""
    last_user = users_collection.find_one(sort=[("created_at", -1)])
    if not last_user:
        return "USR0001"
    last_id = last_user["user_id"]
    last_num = int(last_id[3:])
    return f"USR{last_num+1:04d}"

def main():
    inject_custom_css()
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "is_new" not in st.session_state:
        st.session_state.is_new = False
    if "mode" not in st.session_state:
        st.session_state.mode = "global"
    if "doc_collection" not in st.session_state:
        st.session_state.doc_collection = None
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = []
    if "chat_title" not in st.session_state:
        st.session_state.chat_title = "New Chat"
    if "show_more_chats" not in st.session_state:
        st.session_state.show_more_chats = False
    if "file_uploader_key" not in st.session_state:
        st.session_state.file_uploader_key = 0
    
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown("""
        <div class="logo">GC</div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown('<h1 class="main-header">Gyan Chatbot</h1>', unsafe_allow_html=True)
    
    # Authentication
    if not st.session_state.user_id:
        auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])
        
        with auth_tab1:
            user_id, is_new = login_user(users_collection)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.is_new = is_new
                st.rerun()
        
        with auth_tab2:
            user_id, is_new = register_user(users_collection, generate_user_id)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.is_new = is_new
                st.rerun()
        
        return
    
    # Sidebar
    with st.sidebar:
        
        st.markdown("""
        <div style='display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-bottom: 1.5rem;'>
            <div class="small-logo">GC</div>
            <h2 style='margin: 0; color: #3b82f6; font-size: 1.5rem;'>Gyan Chatbot</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Display user info
        user_info = users_collection.find_one({"user_id": st.session_state.user_id})
        if user_info:
            st.markdown(f'<div class="user-info">', unsafe_allow_html=True)
            st.write(f"👤 **{user_info['username']}**")
            st.write(f"🆔 `{st.session_state.user_id}`")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            st.session_state.current_chat = []
            st.session_state.chat_title = "New Chat"
            st.rerun()
        
        # Mode Selector
        st.subheader("Chat Mode")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌍 Global", use_container_width=True, 
                        type="primary" if st.session_state.mode == "global" else "secondary"):
                st.session_state.mode = "global"
                st.rerun()
        with col2:
            if st.button("📁 Local", use_container_width=True, 
                        type="primary" if st.session_state.mode == "local" else "secondary"):
                st.session_state.mode = "local"

                if st.session_state.doc_collection is None:
                    st.session_state.doc_collection = setup_document_collection(
                        chroma_client, st.session_state.user_id
                    )
                st.rerun()
        
        # Document Management for Local Mode
        if st.session_state.mode == "local":
            st.subheader("Document Management")
            
            # File uploader
            uploaded_files = st.file_uploader(
                "Upload documents", 
                type=["txt", "pdf", "docx", "json", "xlsx"],
                accept_multiple_files=True,
                key=f"file_uploader_{st.session_state.file_uploader_key}"
            )
            
            if uploaded_files:
                user_uploads_dir = get_user_uploads_dir(st.session_state.user_id)
                file_paths = []
                
                for uploaded_file in uploaded_files:
                    # Save uploaded file to user-specific directory
                    file_path = user_uploads_dir / uploaded_file.name
                    
                    # Handle duplicate files
                    counter = 1
                    while file_path.exists():
                        name, ext = os.path.splitext(uploaded_file.name)
                        file_path = user_uploads_dir / f"{name}_{counter}{ext}"
                        counter += 1
                    
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    file_paths.append(str(file_path))
                
                # Process files to collection
                if st.session_state.doc_collection:
                    st.session_state.doc_collection = process_files_to_collection(
                        file_paths, st.session_state.doc_collection, st.session_state.user_id
                    )
                    st.session_state.file_uploader_key += 1  # Reset uploader
                else:
                    st.error("Document collection not initialized!")
            
            # Show uploaded files
            existing_files = get_file_paths_from_uploads(st.session_state.user_id)
            if existing_files:
                st.subheader("Your Files")
                for file_path in existing_files:
                    file_name = os.path.basename(file_path)
                    file_size = os.path.getsize(file_path) / 1024  # Size in KB
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.text(f"{file_name}")
                    with col2:
                        st.text(f"{file_size:.1f} KB")
                    with col3:
                        if st.button("❌", key=f"delete_{file_name}"):
                            try:
                                os.remove(file_path)
                                st.success(f"Deleted {file_name}")
                                time.sleep(1)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting file: {e}")
        
        # Chat History
        st.subheader("Chat History")
        chats = list_my_chats(collection, st.session_state.user_id)
        
        if chats:
            # Limit to 5 chats unless show more is enabled
            display_chats = chats if st.session_state.show_more_chats or len(chats) <= 5 else chats[:5]
            
            for chat in display_chats:
                chat_id = str(chat["_id"])
                title = chat.get("title", "Untitled")
                timestamp = chat.get("timestamp", datetime.now())
                time_str = timestamp.strftime("%d %b %H:%M")
                mode_emoji = "📁" if chat.get("mode") == "local" else "🌍"
                
                # Create container for chat item with delete button on right
                chat_col1, chat_col2 = st.columns([5, 1])
                
                with chat_col1:
                    
                    if st.button(f"{mode_emoji} {title} - {time_str}", key=f"load_{chat_id}", use_container_width=True):
                        st.session_state.current_chat = chat.get("chat", [])
                        st.session_state.chat_title = title
                        st.rerun()
                
                with chat_col2:
                    
                    if st.button("❌", key=f"delete_{chat_id}", help="Delete this chat", use_container_width=True):
                        collection.delete_one({"_id": chat["_id"]})
                        st.success("Chat deleted!")
                        time.sleep(1)
                        st.rerun()
            
            # Show more/less button
            if len(chats) > 5:
                if st.session_state.show_more_chats:
                    if st.button("Show Less", use_container_width=True):
                        st.session_state.show_more_chats = False
                        st.rerun()
                else:
                    if st.button("Show More", use_container_width=True):
                        st.session_state.show_more_chats = True
                        st.rerun()
        else:
            st.info("No chat history yet. Start a new conversation!")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.is_new = False
            st.session_state.mode = "global"
            st.session_state.doc_collection = None
            st.session_state.current_chat = []
            st.session_state.chat_title = "New Chat"
            st.session_state.show_more_chats = False
            st.rerun()
    
    # Main chat area
    st.subheader(st.session_state.chat_title)
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.current_chat:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-bubble-user">🧑 {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-assistant">🤖 {message["content"]}</div>', unsafe_allow_html=True)
    
    
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        
        st.session_state.current_chat.append({"role": "user", "content": user_input})
        
        if len(st.session_state.current_chat) == 1:  # 
            st.session_state.chat_title = generate_chat_title(user_input)
        
        with chat_container:
            st.markdown(f'<div class="chat-bubble-user">🧑 {user_input}</div>', unsafe_allow_html=True)
        
        if st.session_state.mode == "local" and st.session_state.doc_collection:
        
            with st.spinner("Searching in your documents..."):
                relevant_doc_content = query_documents(user_input, st.session_state.doc_collection)
            
            if relevant_doc_content and "No relevant information" not in relevant_doc_content:
                context_prompt = f"""Based ONLY on the following document content:

{relevant_doc_content}

Answer this question: {user_input}

If the document doesn't contain the exact answer, say "I don't have information about this in my documents". Do not use any external knowledge."""
                
                messages = [ChatMessage(role="user", content=context_prompt)]
            else:
                messages = [ChatMessage(role="user", content=user_input)]
        else:
            
            messages = []
            for msg in st.session_state.current_chat:
                messages.append(ChatMessage(role=msg["role"], content=msg["content"]))
        
        with chat_container:
            typing_placeholder = st.empty()
            typing_placeholder.markdown(
                '<div class="chat-bubble-assistant">🤖 <span class="typing-animation"></span><span class="typing-animation"></span><span class="typing-animation"></span></div>', 
                unsafe_allow_html=True
            )
        
        try:
            
            response = client.chat.completions.create(
                messages=messages,
                model="jamba-large",
                max_tokens=250,
                temperature=0.1 if st.session_state.mode == "local" else 0.3,
                top_p=0.9
            )
            
            answer = response.choices[0].message.content
            
            typing_placeholder.empty()
            st.markdown(f'<div class="chat-bubble-assistant">🤖 {answer}</div>', unsafe_allow_html=True)
            
        
            st.session_state.current_chat.append({"role": "assistant", "content": answer})
            
            
            if len(st.session_state.current_chat) == 2:  
                collection.insert_one({
                    "user_id": st.session_state.user_id,
                    "title": st.session_state.chat_title,
                    "chat": st.session_state.current_chat,
                    "timestamp": datetime.now(),
                    "mode": st.session_state.mode
                })
        
        except Exception as e:
            typing_placeholder.empty()
            st.error(f"AI API error: {e}")
            if st.session_state.mode == "local" and 'relevant_doc_content' in locals() and relevant_doc_content and "No relevant information" not in relevant_doc_content:
                fallback_msg = f"Here's what I found in your documents:\n\n{relevant_doc_content[:1000]}{'...' if len(relevant_doc_content) > 1000 else ''}"
                st.markdown(f'<div class="chat-bubble-assistant">🤖 {fallback_msg}</div>', unsafe_allow_html=True)
                st.session_state.current_chat.append({"role": "assistant", "content": fallback_msg})

if __name__ == "__main__":
    main()