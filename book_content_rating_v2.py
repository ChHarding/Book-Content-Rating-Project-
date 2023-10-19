import tkinter as tk
from tkinter import messagebox
import requests

# Content warning keyword themes and their associated lists
CONTENT_WARNING_KEYWORDS = {
    "Animal Abuse": ["animal", "abuse", "cruelty", "harm"],
    "Sexual Violence": ["rape", "sexual assault", "molest", "sexual violence"],
    "Body Image/Disordered Eating": ["body image", "eating disorder", "anorexia", "bulimia", "body dysmorphia", "diet"],
    "Self-Harm/Suicide": ["self-harm", "suicide", "cutting", "self-inflict"],
    "Discrimination/Hate Crimes": ["discrimination", "hate crime", "racism", "sexism", "prejudice"],
    "Violence & Graphic Content": ["violence", "graphic", "gore", "explicit", "brutal"],
    "Substance Abuse/Addiction": ["drug", "addiction", "alcohol", "substance abuse", "intoxication"],
    "Child Abuse/Domestic Violence": ["child abuse", "domestic violence", "molest", "beat"],
    "Homicide/Gun Violence": ["homicide", "gun violence", "murder", "shoot", "death"]
}

# Function to search for book content warning ratings and reason using the Google Books and Open Library APIs
def search_book_ratings():
    book_title = book_title_entry.get()
    author_name = author_entry.get()
    
    if not book_title:
        messagebox.showerror("Error", "Please enter a book title.")
        return

    # URLs for both APIs
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{book_title}"
    open_library_api_url = f"https://openlibrary.org/search.json?title={book_title}"

    if author_name:
        google_books_api_url += f"+inauthor:{author_name}"
        open_library_api_url += f"&author={author_name}"

    try:
        warnings_detected = []

        # Fetch from Google Books API
        google_books_response = requests.get(google_books_api_url)
        google_books_data = google_books_response.json()

        if "items" in google_books_data:
            description = google_books_data["items"][0]["volumeInfo"].get("description", "")
            for warning, keywords in CONTENT_WARNING_KEYWORDS.items():
                for keyword in keywords:
                    if keyword.lower() in description.lower():
                        warnings_detected.append(warning)
                        break

        # Fetch from Open Library API
        open_library_response = requests.get(open_library_api_url)
        open_library_data = open_library_response.json()

        if "docs" in open_library_data and len(open_library_data["docs"]) > 0:
            subjects = open_library_data["docs"][0].get("subject", [])
            for warning, keywords in CONTENT_WARNING_KEYWORDS.items():
                for keyword in keywords:
                    if any(keyword.lower() in subject.lower() for subject in subjects):
                        warnings_detected.append(warning)
                        break

        # Display the results
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", "end")

        if warnings_detected:
            result_text.insert("1.0", f"Content Warnings for {book_title}:\n\n")
            for warning in warnings_detected:
                result_text.insert(tk.END, f"- {warning}\n")
        else:
            result_text.insert("1.0", "No content warnings detected for this book.")

        result_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", str(e))



# Please use a class for the GUI, it'll make things easier when it gets more complex
'''
import tkinter as tk

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
root.title("Book Content Warning Ratings GUI")

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