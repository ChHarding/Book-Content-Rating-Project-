import tkinter as tk
from tkinter import messagebox
import requests
from fuzzywuzzy import fuzz
import urllib.parse

# CH I added a few more keywords by asking ChatGPT for this:
'''
I'm trying to develop a set of words that could indicate that a text might deserve a content warning about Substance Abuse/Addiction. Please give me at least 100 words and make sure that you cover cases where a "bad" word might occur slightly differently based on it grammatical context e.g. I would want not just drug but also drugged, drugs, drug's, etc.
'''
# There's probably a better way to do hone in on what I say about grammatical context
# if you want to spend some time to find out how grammar people call this 
# properly (stemming? lemmatization? I don't know)

# Dictionary for keyword-based content warnings
KEYWORD_WARNINGS = {
    "Animal Abuse": ["animal", "cruelty", "neglect", "harm", "suffering"],
    "Sexual Violence": ["rape", "molestation", "sexual assault", "non-consensual", "nonconsensual"],
    "Body Image/Disordered Eating": ["body image", "eating disorder", "anorexia", "bulimia", "body dysmorphia"],
    "Self-Harm/Suicide": ["self-harm", "suicide", "cutting", "overdose", "self-inflict"],
    "Discrimination/Hate Crimes": ["discrimination", "racism", "homophobia", "sexism", "hate crime", "prejudice"],
    "Violence & Graphic Content": ["violence", "graphic", "gore", "brutal", "vicious"],
    "Substance Abuse/Addiction": ["Addiction", "Addict", "Addicted", "Addictive", "Substance abuse", "Substance use", "Substance misuse", "Substance dependency", "Drug", "Drugs", "Drug's", "Drug use", "Drug misuse", "Drug dependency", "Drugged", "Drugging", "Druggie", "Druggist", "Narcotic", "Narcotics", "Opiate", "Opiates", "Opium", "Heroin", "Cocaine", "Crack cocaine", "Methamphetamine", "Meth", "Methadone", "MDMA", "Ecstasy", "Prescription drugs", "Over-the-counter drugs", "OTC drugs", "Pharmaceutical", "Pill", "Pills", "Medication", "Overdose", "High", "Stoned", "Junkie", "Dope", "Doping", "Doper", "Needle", "Syringe", "Injection", "Inject", "Shooting up", "Substance use disorder", "Substance dependence", "Chemical dependency", "Alcoholic", "Alcoholism", "Booze", "Boozer", "Binge drinking", "Intoxication", "Drunk", "Drunkenness", "Alcohol abuse", "Alco", "Party drugs", "Designer drugs", "Gateway drugs", "Synthetic drugs", "Hallucinogens", "Psychedelics", "LSD", "Acid", "Magic mushrooms", "Psilocybin", "Marijuana", "Cannabis", "Weed", "Pot", "420", "Joint", "Blunt", "Mary Jane", "Grass", "Hashish", "Methadone", "Painkillers", "Barbiturates", "Sedatives", "Tranquilizers", "Benzos", "Xanax", "Valium", "Ativan", "Ritalin", "ADHD medication", "Fentanyl", "Vicodin", "Oxycodone", "Percocet", "Codeine", "Codependency", "Relapse", "Recovery", "Rehabilitation", "Sober", "Sobriety", "12-step program", "Detox", "Withdrawal", "Craving", "Tolerance", "Peer pressure", "Enabling", "Recovery center", "Drug testing", "Abstain", "Trigger", "Gateway drug", "DARE (Drug Abuse Resistance Education)", "Substance treatment", "Rehab facility", "Opioid epidemic", "Alcohol withdrawal", "Alcohol poisoning", "Fetal alcohol syndrome", "Recovery community", "Harm reduction", "Sober living", "Substance counseling", "NA (Narcotics Anonymous)", "AA (Alcoholics Anonymous)", "Dual diagnosis", "Controlled substance", "Relapse prevention", "Suboxone", "Naloxone", "Narcan", "Euphoria", "Self-medication", "Gateway behavior"],
    "Child Abuse/Domestic Violence": ["child abuse", "domestic violence", "molestation", "beating", "hurt"],
    "Homicide/Gun Violence": ["murder", "homicide", "gunshot", "shooting", "kill", "death"]
}

def analyze_description(description):
    detected_warnings = []
    description_lower = description.lower()

    for warning, keywords in KEYWORD_WARNINGS.items():
        for keyword in keywords:
            if fuzz.partial_ratio(keyword, description_lower) > 80:  # Here, 80 is the threshold for matching. Adjust as necessary.
                detected_warnings.append(warning) # Ch should remove duplicates
                break

    return detected_warnings

def search_book_ratings():
    book_title = book_title_entry.get()
    author_name = author_entry.get()
    
    if book_title == '': # CH more explicit
        messagebox.showerror("Error", "Please enter a book title.")
        return

    # CH: not sure if Google books cares if there are spaces in the title
    # but it's best practice to convert "weird" URL chars into sth like %20
    # for spaces
    book_title = urllib.parse.quote(book_title)


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