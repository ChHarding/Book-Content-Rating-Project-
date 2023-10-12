import tkinter as tk
from tkinter import messagebox
import requests
from fuzzywuzzy import fuzz

# Dictionary for keyword-based content warnings
KEYWORD_WARNINGS = {
    "Animal Abuse": ["animal", "cruelty", "neglect", "harm", "suffering"],
    "Sexual Violence": ["rape", "molestation", "sexual assault", "non-consensual", "nonconsensual"],
    "Body Image/Disordered Eating": ["body image", "eating disorder", "anorexia", "bulimia", "body dysmorphia"],
    "Self-Harm/Suicide": ["self-harm", "suicide", "cutting", "overdose", "self-inflict"],
    "Discrimination/Hate Crimes": ["discrimination", "racism", "homophobia", "sexism", "hate crime", "prejudice"],
    "Violence & Graphic Content": ["violence", "graphic", "gore", "brutal", "vicious"],
    "Substance Abuse/Addiction": ["drug", "addiction", "alcohol", "substance abuse", "opioid", "narcotic"],
    "Child Abuse/Domestic Violence": ["child abuse", "domestic violence", "molestation", "beating", "hurt"],
    "Homicide/Gun Violence": ["murder", "homicide", "gunshot", "shooting", "kill", "death"]
}

def analyze_description(description):
    detected_warnings = []
    description_lower = description.lower()

    for warning, keywords in KEYWORD_WARNINGS.items():
        for keyword in keywords:
            if fuzz.partial_ratio(keyword, description_lower) > 80:  # Here, 80 is the threshold for matching. Adjust as necessary.
                detected_warnings.append(warning)
                break

    return detected_warnings

def search_book_ratings():
    book_title = book_title_entry.get()
    author_name = author_entry.get()
    
    if not book_title:
        messagebox.showerror("Error", "Please enter a book title.")
        return

    # Create a URL for the Google Books API search
    api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{book_title}"
    
    if author_name:
        api_url += f"+inauthor:{author_name}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()

            if "items" in data and len(data["items"]) > 0:
                book = data["items"][0]
                title = book["volumeInfo"]["title"]
                authors = book["volumeInfo"].get("authors", [])
                author = ", ".join(authors) if authors else "Unknown"
                maturity_rating = book["volumeInfo"].get("maturityRating", "Not Rated")
                description = book["volumeInfo"].get("description", "No description available.")

                warnings_from_description = analyze_description(description)
                if warnings_from_description:
                    extended_warning = f"R (Discretion Advised) - Reasons: {', '.join(warnings_from_description)}"
                else:
                    extended_warning = {
                        "MATURE": f"R (Discretion Advised) - General Mature Content",
                        "NOT_MATURE": "G (For Everyone)"
                    }.get(maturity_rating, "Not Rated")

                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", "end")
                result_text.insert("1.0", f"Title: {title}\nAuthor: {author}\nContent Warning Rating: {extended_warning}\n\nDescription:\n{description}")
                result_text.config(state=tk.DISABLED)
            else:
                result_text.config(state=tk.NORMAL)
                result_text.delete("1.0", "end")
                result_text.insert("1.0", "No results found for the given criteria.")
                result_text.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "Unable to fetch book information. Please try again later.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

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