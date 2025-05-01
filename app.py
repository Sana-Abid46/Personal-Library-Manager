import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# Set page config with better styling
st.set_page_config(
    page_title="Islamic Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .stSelectbox>div>div>select {
        border-radius: 5px;
    }
    .stNumberInput>div>div>input {
        border-radius: 5px;
    }
    .stTextArea>div>div>textarea {
        border-radius: 5px;
    }
    .css-1d391kg {
        padding: 1rem;
        border-radius: 5px;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for books if not exists
if 'books' not in st.session_state:
    if os.path.exists("library.json"):
        try:
            with open("library.json", "r", encoding='utf-8') as f:
                st.session_state.books = json.load(f)
        except json.JSONDecodeError:
            st.error("Error: Invalid library file. Starting with empty library.")
            st.session_state.books = []
    else:
        st.session_state.books = []

def save_library():
    """Save the library to a JSON file."""
    with open("library.json", "w", encoding='utf-8') as f:
        json.dump(st.session_state.books, f, indent=4, ensure_ascii=False)

# Sidebar for adding new books and navigation
with st.sidebar:
    st.title("Islamic Library Manager")
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["📚 Library", "➕ Add Book", "📊 Statistics", "⚙️ Settings"]
    )

# Main content area
if page == "📚 Library":
    st.title("📚 Islamic Library")
    
    # Search and filter section
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("🔍 Search books", placeholder="Search by title, author, or genre")
    with col2:
        search_type = st.selectbox("Search by", ["Title", "Author", "Genre"])
    with col3:
        read_filter = st.selectbox("Status", ["All", "Read", "Unread"])
    
    # Filter books based on search and status
    filtered_books = st.session_state.books
    if search_term:
        if search_type == "Title":
            filtered_books = [book for book in filtered_books if search_term.lower() in book["title"].lower()]
        elif search_type == "Author":
            filtered_books = [book for book in filtered_books if search_term.lower() in book["author"].lower()]
        else:
            filtered_books = [book for book in filtered_books if search_term.lower() in book["genre"].lower()]
    
    if read_filter != "All":
        filtered_books = [book for book in filtered_books if book["read"] == (read_filter == "Read")]
    
    # Display books in a table with better formatting
    if filtered_books:
        df = pd.DataFrame(filtered_books)
        df['read'] = df['read'].map({True: '✅ Read', False: '📖 Unread'})
        df = df.rename(columns={
            'title': 'Title',
            'author': 'Author',
            'year': 'Year',
            'genre': 'Genre',
            'read': 'Status',
            'description': 'Description'
        })
        
        # Add action buttons for each book
        df['Actions'] = '📝 Edit | ❌ Delete'
        
        # Display the table with better styling
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Title": st.column_config.TextColumn("Title", width="large"),
                "Author": st.column_config.TextColumn("Author", width="medium"),
                "Year": st.column_config.NumberColumn("Year", width="small"),
                "Genre": st.column_config.TextColumn("Genre", width="medium"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Description": st.column_config.TextColumn("Description", width="large"),
                "Actions": st.column_config.TextColumn("Actions", width="medium")
            }
        )
    else:
        st.info("No books found matching your criteria.")

elif page == "➕ Add Book":
    st.title("➕ Add New Book")
    
    # Add book form with better layout
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Title", placeholder="Enter book title")
        author = st.text_input("Author", placeholder="Enter author name")
        year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
    with col2:
        genre = st.text_input("Genre", placeholder="Enter genre")
        read_status = st.selectbox("Read Status", ["Unread", "Read"])
        description = st.text_area("Description", placeholder="Enter book description", height=100)
    
    if st.button("Add Book", type="primary"):
        if title and author:
            new_book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "description": description,
                "read": read_status == "Read",
                "added_date": datetime.now().strftime("%Y-%m-%d")
            }
            st.session_state.books.append(new_book)
            save_library()
            st.success("Book added successfully!")
        else:
            st.error("Please fill in at least title and author.")

elif page == "📊 Statistics":
    st.title("📊 Library Statistics")
    
    if st.session_state.books:
        total_books = len(st.session_state.books)
        read_books = sum(1 for book in st.session_state.books if book["read"])
        percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
        
        # Display statistics in cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", total_books)
        with col2:
            st.metric("Books Read", read_books)
        with col3:
            st.metric("Reading Progress", f"{percentage_read:.1f}%")
        
        # Genre distribution
        st.subheader("Genre Distribution")
        genre_counts = pd.DataFrame(st.session_state.books)['genre'].value_counts()
        st.bar_chart(genre_counts)
        
        # Reading progress over time
        st.subheader("Reading Progress")
        if 'added_date' in st.session_state.books[0]:
            df = pd.DataFrame(st.session_state.books)
            df['added_date'] = pd.to_datetime(df['added_date'])
            df = df.sort_values('added_date')
            df['cumulative_read'] = df['read'].cumsum()
            st.line_chart(df.set_index('added_date')['cumulative_read'])
    else:
        st.info("No books in the library yet.")

elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    
    st.subheader("Backup & Restore")
    if st.button("Export Library"):
        with open("library_backup.json", "w", encoding='utf-8') as f:
            json.dump(st.session_state.books, f, indent=4, ensure_ascii=False)
        st.success("Library exported successfully!")
    
    uploaded_file = st.file_uploader("Import Library", type=['json'])
    if uploaded_file is not None:
        try:
            imported_books = json.load(uploaded_file)
            st.session_state.books = imported_books
            save_library()
            st.success("Library imported successfully!")
        except:
            st.error("Invalid file format. Please upload a valid JSON file.")
    
    st.subheader("Appearance")
    theme = st.selectbox("Theme", ["Light", "Dark"])
    st.info("Theme changes will take effect after restarting the app.")