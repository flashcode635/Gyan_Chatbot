# 🚀 Vigyan Chatbot - AI-Powered Document Intelligence Platform

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=flat&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</div>

## 📋 Project Overview

Vigyan Chatbot is an advanced AI-powered document assistant that enables natural language interactions with your documents. The platform combines cutting-edge AI with robust document processing to deliver intelligent, context-aware responses.

## ✨ Key Features

- **🤖 Dual Chat Modes** - Seamlessly switch between global knowledge and document-specific conversations
- **📄 Multi-Format Support** - Process TXT, PDF, DOCX, JSON, and XLSX files with ease
- **🔍 Semantic Search** - AI-powered document querying using advanced vector embeddings
- **🔒 Secure Authentication** - Robust user registration and login system with MongoDB storage
- **🔄 Persistent History** - Complete conversation history maintained across sessions
- **🎨 Modern UI/UX** - Clean, responsive interface built with Streamlit

## 📁 Project Structure

```
Vigyan-chatbot/
├── main_app.py             # Primary application controller
├── auth.py                 # User authentication management
├── database.py             # Database operations & vector storage
├── file_processing.py      # Multi-format document processing
├── utils.py                # Utilities & UI customization
├── .env                    # Environment configuration
├── requirements.txt        # Dependency management
└── script_python_2         # Main script file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account or local MongoDB instance
- AI21 Studio API key

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   - Copy `.env.sample` to `.env`
   - Update with your API keys and configuration

3. **Launch Application**
   ```bash
   streamlit run main_app.py
   # If the above doesn't work, try:
   # python -m streamlit run main_app.py
   ```

## 🏗️ Architecture Overview

![Architecture Diagram](https://github.com/rishi991072/Vigyan_Chatbot/blob/04f23387204caf8f143e3b1718296bfae7e9963d/Screenshot%20(23).png)

## ⚡ Advanced Features

- **🗂️ Document Management** - Upload, view, and manage your documents
- **🔄 Session Persistence** - Your data remains available across sessions
- **🌐 Mode Switching** - Toggle between global and document-specific modes
- **📊 Chat Analytics** - Track and analyze your conversation history

## 🛠️ Technical Stack

### Core Technologies

- **🤖 AI21 Studio Jamba Model** - Advanced language processing
- **🌐 Streamlit** - Responsive web application framework
- **🗄️ MongoDB** - Scalable data storage
- **🔍 ChromaDB** - Efficient vector storage for semantic search
- **📄 Document Processing** - PyPDF2, python-docx, openpyxl

### Performance Optimizations

- **⚡ Efficient Chunking** - 800-character optimal document segmentation

2.Smart Vectorization: Semantic embedding for accurate retrieval

3.Session Management: Efficient state handling for smooth user experience

4.Error Handling: Comprehensive exception management throughout

**API Integration**

1.The application integrates with the following services:

2.AI21 Studio API: For advanced language model capabilities

3.MongoDB Atlas: For cloud-based data storage

4.ChromaDB: For vector storage and similarity search

**UI Images**

![image alt](https://github.com/rishi991072/Vigyan_Chatbot/blob/1dd486878a985bedc30e5efca367e451b41fcb59/Screenshot%20(18).png)

![image alt](https://github.com/rishi991072/Vigyan_Chatbot/blob/f83be4935517df16195edc6fb095f44364a2f28b/Screenshot%20(22).png)

**Vigyan Chatbot - Transforming document interaction through AI intelligence. 🚀**
















