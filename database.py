import os
import re
import uuid
from pathlib import Path
from datetime import datetime
import streamlit as st  # Added this import

def get_user_uploads_dir(user_id):
    """Get user-specific uploads directory path"""
    user_dir = Path(f"./uploads/user_{user_id}")
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

def get_file_paths_from_uploads(user_id):
    """Get all file paths from user-specific uploads directory"""
    user_uploads_dir = get_user_uploads_dir(user_id)
    files = list(user_uploads_dir.glob("*"))
    return [str(f) for f in files if f.is_file()]

def setup_document_collection(chroma_client, user_id):
    """Setup ChromaDB collection with documents for specific user"""
    collection_name = f"user_{user_id}_documents"
    
    try:
        collection = chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={"user_id": user_id, "created_at": datetime.now().isoformat()}
        )
        return collection
    except Exception as e:
        st.error(f"Error in document setup: {e}")
        return None

def process_files_to_collection(file_paths, collection, user_id):
    """Process files and add to ChromaDB collection"""
    from file_processing import read_file_content
    
    documents = []
    metadatas = []
    ids = []
    
    for file_path in file_paths:
        content = read_file_content(file_path)
        if content:
            sentences = re.split(r'(?<=[.!?]) +', content)
            chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) < 800:
                    current_chunk += sentence + " "
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence + " "
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({
                    "source": file_path, 
                    "chunk_index": i,
                    "user_id": user_id,
                    "filename": os.path.basename(file_path),
                    "file_type": os.path.splitext(file_path)[1]
                })
                ids.append(f"{user_id}_{os.path.basename(file_path)}_{i}_{uuid.uuid4().hex[:6]}")
    
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        st.success(f"Added {len(documents)} document chunks from {len(file_paths)} files!")
    else:
        st.warning("No valid content found in provided files!")
    
    return collection

def query_documents(question, collection, n_results=3):
    """Query documents using ChromaDB"""
    try:
        results = collection.query(
            query_texts=[question],
            n_results=n_results
        )
        
        if results and results['documents'] and results['documents'][0]:
            relevant_content = "\n\n".join([
                f" Source: {results['metadatas'][0][i].get('filename', 'Unknown')}\n"
                f"Content: {doc}\n"
                for i, doc in enumerate(results['documents'][0])
            ])
            return relevant_content
        else:
            return "No relevant information found in documents."
    
    except Exception as e:
        st.error(f"Error querying documents: {e}")
        return "Error searching documents."

def list_my_chats(collection, user_id):
    chats = list(collection.find({"user_id": user_id}).sort("timestamp", -1))
    return chats

def generate_chat_title(first_message):
    """Generate a title from the first message"""
    if not first_message:
        return "New Chat"
    
    # Clean the message and truncate
    clean_msg = re.sub(r'[^\w\s]', '', first_message)
    words = clean_msg.split()
    
    if len(words) <= 5:
        title = clean_msg
    else:
        title = " ".join(words[:5]) + "..."
    
    return title[:40]