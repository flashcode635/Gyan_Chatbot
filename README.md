**Gyan Chatbot - AI-Powered Document Intelligence Platform**

**Project Overview**

Gyan Chatbot is an advanced AI-powered document assistant that enables users to interact with their documents through natural language conversations. The platform combines cutting-edge AI capabilities with robust document processing to deliver intelligent responses based on both general knowledge and specific document content. 

**Key Features**

1:- Dual Chat Modes: Switch between global knowledge and document-specific conversations

2:- Multi-Format Document Support: Process TXT, PDF, DOCX, JSON, and XLSX files

3:- Intelligent Semantic Search: AI-powered document querying using vector embeddings

4:- Secure Authentication System: User registration and login with MongoDB storage

5:- Persistent Chat History: Complete conversation history maintained across sessions

6:- Modern UI/UX: Custom-designed Streamlit interface with responsive layout

**gyan-chatbot/Folder structure**

├── main_app.py             # Primary application controller

├── auth.py                 # User authentication management

├── database.py             # Database operations & vector storage

├── file_processing.py      # Multi-format document processing

├── utils.py                # Utilities & UI customization

├── .env                    # Environment configuration

├── requirements.txt        # Dependency management

└── script_python_2         # Main script file


**Installation Guide**

1.Prerequisites

2.Python 3.8 or higher

3.MongoDB Atlas account or local MongoDB instance

4.AI21 Studio API key

**Step-by-Step Setup**


**1.Install required dependencies**


pip install -r requirements.txt

**2.Configure environment variables**

Create a .env file with the following variables:

env

1.API_KEY=your_ai21_api_key_here

2.MONGO_URI=your_mongodb_connection_string

3.CHROMA_API_KEY=your_chromadb_api_key

4.CHROMA_TENANT=your_chromadb_tenant

5.CHROMA_DB=your_chromadb_database_name

**3.Launch the application**

streamlit run main_app.py

**Architecture Overview**

![image alt](https://github.com/rishi991072/Gyan_Chatbot/blob/04f23387204caf8f143e3b1718296bfae7e9963d/Screenshot%20(23).png)



**Advanced Features**

1.Chat History: Access previous conversations from the sidebar

2.Document Management: View, manage, and delete uploaded files

3.Mode Switching: Seamlessly transition between global and local modes

4.Session Persistence: Your data remains available across sessions

**Technical Implementation****

**Core Technologies**

1.AI21 Studio Jamba Model: Advanced language processing capabilities

2.Streamlit Framework: Responsive web application interface

3.MongoDB: Scalable data storage for users and chat history

4.ChromaDB: Efficient vector storage for semantic search

5.Document Processing Libraries: PyPDF2, python-docx, openpyxl

**Performance Optimization**

1.Efficient Chunking: 800-character optimal document segmentation

2.Smart Vectorization: Semantic embedding for accurate retrieval

3.Session Management: Efficient state handling for smooth user experience

4.Error Handling: Comprehensive exception management throughout

**API Integration**

1.The application integrates with the following services:

2.AI21 Studio API: For advanced language model capabilities

3.MongoDB Atlas: For cloud-based data storage

4.ChromaDB: For vector storage and similarity search

**UI Images**

![image alt](https://github.com/rishi991072/Gyan_Chatbot/blob/1dd486878a985bedc30e5efca367e451b41fcb59/Screenshot%20(18).png)

![image alt](https://github.com/rishi991072/Gyan_Chatbot/blob/f83be4935517df16195edc6fb095f44364a2f28b/Screenshot%20(22).png)

**Gyan Chatbot - Transforming document interaction through AI intelligence. 🚀**
















