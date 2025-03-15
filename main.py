import streamlit as st
import pymongo

# MongoDB Connection (Local)
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "LibraryDB"
COLLECTION_NAME = "books"

# Connect to Local MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Load books from MongoDB
def load_library():
    return list(collection.find({}, {"_id": 0}))  # Hide MongoDB _id field

# Add a new book to MongoDB
def add_book(title, genre, year, author, read):
    book = {
        "Title": title,
        "Genre": genre,
        "Publication Year": year,
        "Author": author,
        "Read": read
    }
    collection.insert_one(book)
    st.success(f"Added book: {title}")

# Delete books (removes first 'count' books)
def delete_books(count):
    all_books = list(collection.find().limit(count))  # Get N books
    if len(all_books) < count:
        st.error("Not enough books to delete!")
    else:
        for book in all_books:
            collection.delete_one({"Title": book["Title"]})  # Delete by Title
        st.success(f"Deleted {count} books!")

# Streamlit UI
def main():
    st.set_page_config(page_title="Personal Library Manager", layout="wide")

    st.sidebar.title("📖 Navigation")
    page = st.sidebar.radio("Go to", ["View Library", "Add Book", "Delete Books"])

    if page == "View Library":
        st.title("📚 Your Library")
        library = load_library()
        if library:
            for book in library:
                st.write(f"**Title:** {book['Title']}, **Genre:** {book['Genre']}, **Year:** {book['Publication Year']}, **Author:** {book['Author']}, **Read:** {book['Read']}")
        else:
            st.write("No books found!")

    elif page == "Add Book":
        st.title("➕ Add a New Book")
        title = st.text_input("Title")
        genre = st.text_input("Genre")
        year = st.number_input("Publication Year", min_value=1000, max_value=2100, step=1)
        author = st.text_input("Author")
        read = st.checkbox("Have you read this book?")
        if st.button("Add Book"):
            if title and author:
                add_book(title, genre, year, author, read)
            else:
                st.error("Title and Author are required!")

    elif page == "Delete Books":
        st.title("🗑️ Delete Books")
        delete_count = st.number_input("How many books to delete?", min_value=1, step=1)
        if st.button("Delete Books"):
            delete_books(delete_count)

if __name__ == "__main__":
    main()