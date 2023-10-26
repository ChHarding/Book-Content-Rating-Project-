import tkinter as tk
from tkinter import messagebox
import requests
from fuzzywuzzy import fuzz
import urllib.parse

# URLs for APIs
OPEN_BOOKS_API_URL = "https://openlibrary.org/search.json"
GOOGLE_BOOKS_API_BASE_URL = "https://www.googleapis.com/books/v1/volumes"

# Warning keywords
# ... [KEYWORD_WARNINGS dictionary stays the same] ...

def analyze_description(description):
    """
    Analyzes the description of a book and returns warnings if any keywords are found.
    """
    warnings = []
    for warning_name, warning_keywords in KEYWORD_WARNINGS.items():
        for keyword in warning_keywords:
            # Check if the keyword or its fuzzy match is in the description
            if keyword in description.lower() or fuzz.partial_ratio(keyword, description.lower()) > 80:
                warnings.append(warning_name)
                break  # once we've found a match for this warning, move to the next
    return warnings

def search_open_books(title, author=""):
    """
    Search for a book in the Open Books API
    """
    query = {"title": title}
    if author:
        query["author"] = author
    response = requests.get(OPEN_BOOKS_API_URL, params=query)
    if response.status_code == 200:
        data = response.json()
        if data and "docs" in data and len(data["docs"]) > 0:
            return data["docs"][0].get("description", "")
    return ""

def search_google_books(title, author=""):
    """
    Search for a book in the Google Books API
    """
    book_title_encoded = urllib.parse.quote(title)
    author_name_encoded = urllib.parse.quote(author)
    
    # Construct the URL for the Google Books API search
    google_api_url = f"{GOOGLE_BOOKS_API_BASE_URL}?q=intitle:{book_title_encoded}"
    if author:
        google_api_url += f"+inauthor:{author_name_encoded}"

    response = requests.get(google_api_url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["volumeInfo"].get("description", "")
    return ""

def get_book_content_warning(title, author=""):
    """
    Fetches book descriptions using Google Books and Open Books APIs, and returns content warnings based on keywords.
    """
    # Fetch descriptions from APIs
    google_description = search_google_books(title, author)
    open_books_description = search_open_books(title, author)

    # Combine descriptions
    combined_description = f"{google_description} {open_books_description}"

    # Get content warnings from the combined description
    warnings_from_description = analyze_description(combined_description)

    # Construct the rating and reason based on the warnings
    rating = len(warnings_from_description)
    reason = ', '.join(warnings_from_description)

    return rating, reason

def search_book_ratings():
    # Get user input
    book_title = book_title_entry.get()
    author_name = author_entry.get()
    
    # Search for book ratings
    rating, reason = get_book_content_warning(book_title, author_name)
    
    # Update result_text with the information
    result_text.config(state=tk.NORMAL)  # enable editing
    result_text.delete("1.0", "end")  # clear previous content
    result_text.insert("1.0", f"Title: {book_title}\n")
    if author_name:
        result_text.insert(tk.END, f"Author: {author_name}\n")
    result_text.insert(tk.END, f"Rating: {rating}\n")
    if reason:
        result_text.insert(tk.END, f"Reason: {reason}\n")
    
    result_text.config(state=tk.DISABLED)  # disable editing

    book_title_encoded = urllib.parse.quote(book_title)
    author_name_encoded = urllib.parse.quote(author_name)

    google_description = search_google_books(book_title, author_name)
    open_books_description = search_open_books(book_title, author_name)

    # Combine descriptions
    combined_description = f"{google_description} {open_books_description}"

    warnings_from_description = analyze_description(combined_description)

    if warnings_from_description:
        warning_message = '\n'.join(warnings_from_description)
        messagebox.showwarning("Warnings", warning_message)

'''
class MyGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Simple Tkinter GUI")
        self.geometry("400x200")  # Set the initial window size

        # Create a label widget
        label = tk.Label(self, text="Hello, Tkinter!")

        # Pack the label widget to display it
        label.pack(pady=20)  # Adding some vertical padding

if __name__ == "__main__":
    app = MyGUI()
    app.mainloop()
'''
# Create the tkinter window
root = tk.Tk()
root.title("Book Content Warnings")

# Create instructions for the user
instructions_label = tk.Label(root, text="Enter a book title and/or an author's name (optional) to search:")
instructions_label.pack()

# Create input for book title
book_title_label = tk.Label(root, text="Book Title:")
book_title_label.pack()
book_title_entry = tk.Entry(root, width=50)
book_title_entry.pack()

# Create input for author's name
author_label = tk.Label(root, text="Author's Name (optional):")
author_label.pack()
author_entry = tk.Entry(root, width=50)
author_entry.pack()

# Create button to search for book content warning ratings and reason
search_button = tk.Button(root, text="Search Content Warning Rating", command=search_book_ratings)
search_button.pack()

# Create a frame to group result components
result_frame = tk.Frame(root)
result_frame.pack(pady=10)

# Create label for book information
result_label = tk.Label(result_frame, text="Book Information:")
result_label.pack()

# Create a text widget for displaying book information with content warning rating and author
result_text = tk.Text(result_frame, width=50, height=10, wrap=tk.WORD, state=tk.DISABLED)
result_text.pack()

# Create a clear button to clear the result text
clear_button = tk.Button(root, text="Clear Result", command=lambda: result_text.delete("1.0", "end"))
clear_button.pack()

root.mainloop()
