import streamlit as st
import json
import os

# --- File Handling ---
FILE_NAME = "library.json"

# Load library from file
def load_library():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(FILE_NAME, "w") as file:
        json.dump(library, file, indent=4)

# Initialize session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

# Add a book
def add_book():
    st.header("📚 Add a Book")
    title = st.text_input("Enter Title")
    author = st.text_input("Enter Author")
    year = st.number_input("Enter Publication Year", min_value=0, step=1)
    genre = st.text_input("Enter Genre")
    read_status = st.selectbox("Have you read this book?", ["Yes", "No"])
    link = st.text_input("Enter a Link to the Book (optional)")

    if st.button("Add Book"):
        book = {
            "title": title,
            "author": author,
            "year": int(year),
            "genre": genre,
            "read": read_status == "Yes",
            "link": link
        }
        st.session_state.library.append(book)
        save_library(st.session_state.library)
        st.success("Book added successfully!")

# Remove a book
def remove_book():
    st.header("🗑️ Remove a Book")
    titles = [book['title'] for book in st.session_state.library]
    if not titles:
        st.info("No books to remove.")
        return
    selected_title = st.selectbox("Select a book to remove", titles)
    if st.button("Remove Book"):
        st.session_state.library = [b for b in st.session_state.library if b['title'] != selected_title]
        save_library(st.session_state.library)
        st.success("Book removed successfully!")

# Search for a book
def search_book():
    st.header("🔍 Search for a Book")
    search_by = st.radio("Search by", ["Title", "Author"])
    query = st.text_input("Enter search query")

    if query:
        results = []
        for book in st.session_state.library:
            if search_by == "Title" and query.lower() in book["title"].lower():
                results.append(book)
            elif search_by == "Author" and query.lower() in book["author"].lower():
                results.append(book)

        if results:
            st.subheader("📖 Matching Books:")
            for i, b in enumerate(results, 1):
                st.write(f"{i}. {b['title']} by {b['author']} ({b['year']}) - {b['genre']} - {'Read' if b['read'] else 'Unread'}")
                if b.get("link"):
                    st.markdown(f"[🔗 Link to Book]({b['link']})")
        else:
            st.warning("No matching books found.")

# Display all books
def display_books():
    st.header("📚 All Books")
    if not st.session_state.library:
        st.info("Library is empty.")
    else:
        for i, b in enumerate(st.session_state.library, 1):
            st.write(f"{i}. {b['title']} by {b['author']} ({b['year']}) - {b['genre']} - {'Read' if b['read'] else 'Unread'}")
            if b.get("link"):
                st.markdown(f"[🔗 Link to Book]({b['link']})")

# Show statistics
def show_stats():
    st.header("📊 Library Statistics")
    total = len(st.session_state.library)
    read_books = sum(1 for b in st.session_state.library if b["read"])
    percent_read = (read_books / total * 100) if total else 0

    st.write(f"Total books: {total}")
    st.write(f"Percentage read: {percent_read:.2f}%")

# Sidebar menu
st.sidebar.title("📖 Personal Library Manager")
menu = st.sidebar.radio("Choose an action", [
    "Add a Book",
    "Remove a Book",
    "Search for a Book",
    "Display All Books",
    "Display Statistics"
])

# Call appropriate function
if menu == "Add a Book":
    add_book()
elif menu == "Remove a Book":
    remove_book()
elif menu == "Search for a Book":
    search_book()
elif menu == "Display All Books":
    display_books()
elif menu == "Display Statistics":
    show_stats()
