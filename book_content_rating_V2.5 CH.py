import tkinter as tk
from tkinter import messagebox
import requests
from fuzzywuzzy import fuzz
import urllib.parse
from bs4 import BeautifulSoup
import webbrowser
from PIL import Image, ImageTk
import io
from collections import namedtuple

# URLs for APIs
OPEN_BOOKS_API_URL = "https://openlibrary.org/search.json"
GOOGLE_BOOKS_API_BASE_URL = "https://www.googleapis.com/books/v1/volumes"

API_ERROR_MESSAGE = "We're having trouble connecting to the system. Please check your internet connection and try again later."

# Warning keywords
KEYWORD_WARNINGS = {
    "Animal Abuse": ["animal", "cruelty", "neglect", "harm", "suffering", "mistreatment", "abuse","beating", "starvation", "malnourishment", "torment", "torture", "maltreat","exploit", "kill", "slaughter", "poach", "trap", "experiment", "hunt", "cage","abandon", "discard", "pain", "whip", "shoot", "trap", "confine", "enslave",
        "skin", "fur", "endanger", "bait", "bleed", "choke", "crush", "misuse", "overwork","punish", "scar", "shock", "strangle", "wound", "maim", "disfigure", "mutilate","vivisection", "imprisoned", "lab animal", "chained", "caged", "trafficked",
        "illegal trade", "baiting", "fight", "abusement park", "entertainment", "circuses","rodeo", "farming", "fur trade", "leather", "cosmetic testing", "laboratory", "breed","overbreed", "pet mill", "racing", "gamblers", "breeders", "discard", "euthanize","abandoned", "stray", "wildlife", "marine life"],
    "Sexual Violence": ["rape", "molestation", "sexual assault", "non-consensual", "nonconsensual", "harassment","grope", "abuse", "forced", "attack", "inappropriate", "unwanted", "exploit", "violate",
        "coerce", "intimidate", "threaten", "predator", "offender", "consent", "groom", "stalk","unsolicited", "touch", "fear", "trauma", "victim", "traumatize", "vulnerable", "invasion",
        "inappropriate", "violation", "indecent", "forceful", "abusive relationship", "manipulation","intimate violence", "uninvited", "molest", "statutory", "silence", "hush", "date rape","drugged", "power", "control", "cyber", "explicit", "sexting", "blackmail", "shaming","exploitation", "revenge porn", "intimate threat", "exposure", "uncomfortable", "unsafe","minor", "child", "elderly", "defenseless"],
    "Body Image/Disordered Eating": ["body image", "eating disorder", "anorexia", "bulimia", "body dysmorphia", "binge","starvation", "diet", "thin", "fat", "overeating", "weight", "obesity", "underweight",
        "purge", "restriction", "calorie", "fast", "unhealthy", "mirror", "self-worth","appearance", "pressure", "ideal", "size", "dieting", "body shaming", "self-conscious",
        "perfection", "body dissatisfaction", "exercise", "obsession", "orthorexia", "laxatives","diuretics", "body checking", "guilt", "shame", "control", "image", "food fear","compulsive", "scale", "weight gain", "weight loss", "muscle", "toning", "fitness","skinny", "plump", "heavy", "light", "self-esteem", "self-hate", "mirror check","avoidance", "pinch", "measure", "waist", "BMI", "comparison"],
    "Self-Harm/Suicide": ["self-harm", "suicide", "cutting", "overdose", "self-inflict", "end life", "attempt",
        "despair", "hopelessness", "pain", "wrist", "bleed", "scars", "burn", "jump", "hang","suffocate", "cry", "lonely", "depressed", "worthless", "numb", "lost", "void", "struggle","isolation", "helplessness", "grieve", "self-loathing", "suicidal thoughts", "ideation","death wish", "razor", "pills", "intoxication", "sadness", "sorrow", "self-punishment",
        "self-destructive", "darkness", "emptiness", "rope", "bridge", "height", "firearm","blade", "cutting tool", "gas", "drowning", "substance", "ingest", "alcohol", "method","means", "lethality", "intent", "crisis", "hotline"],
    "Discrimination/Hate Crimes": ["discrimination", "racism", "homophobia", "sexism", "hate crime", "prejudice", "bigotry","intolerance", "xenophobia", "bias", "stereotype", "slur", "discriminate", "marginalize",
        "oppress", "minority", "inequality", "unfair", "segregation", "racist", "sexist", "bigot","prejudiced", "hateful", "derogatory", "injustice", "persecute", "isolate", "alienate",
        "ostracize", "scapegoat", "gender bias", "ethnicity", "nationality", "caste", "class","religious", "anti-Semitism", "Islamophobia", "disability", "ageism", "LGBTQ+","gender identity", "transphobia", "colorism", "microaggressions", "supremacy", "radical","extremist", "prejudice", "bias-motivated", "targeted", "offense", "vandalism", "symbol","hate speech", "propaganda"],
    "Violence & Graphic Content": ["violence", "graphic", "gore", "brutal", "vicious", "blood", "wound", "injury", "attack","hurt", "punch", "stab", "hit", "fight", "assault", "battle", "conflict", "terror", "shock","horror", "aggression", "intense", "disturb", "trauma", "frighten", "scar", "fear", "threat","danger", "menace", "brawl", "riot", "massacre", "ambush", "explosive", "bomb", "firearm",
        "weapon", "gunshot", "combat", "warfare", "sadism", "torture", "mutilation", "decapitation","beheading", "suffering", "pain", "traumatic", "scarring", "nightmare", "terrorize", "harm","damage", "intimidation", "coercion"],
    "Substance Abuse/Addiction": ["drugs", "drug use", "substance abuse", "narcotics", 
        "overdose", "addiction", "dependence","heroin", "cocaine", "methamphetamine", "crystal meth", "amphetamine", "speed", "ecstasy", "MDMA","marijuana", "weed", "pot", "cannabis", "THC", "CBD", "psychedelics", "LSD", "acid", "magic mushrooms", "psilocybin","opioids", "opiates", "painkillers", "morphine", "codeine", 
        "benzodiazepines", "valium", "xanax","alcohol", "alcoholism", "drinking", "intoxication", "tobacco", "smoking", "cigarettes", "nicotine", "inhalants", "huffing", "prescription drugs", "pharmaceutical abuse", "caffeine", "energy drinks", "coffee addiction", "anabolic steroids","barbiturates", "sedatives","hallucinogens", "PCP", "ketamine", "binge drinking", "drunk", "hangover","rehab", "rehabilitation", "detox", "withdrawal"],
    "Child Abuse/Domestic Violence": ["child abuse", "domestic violence", "molestation", "beating", "hurt", "neglect","exploit", "trauma", "emotional abuse", "verbal abuse", "physical abuse", "bullying","endanger", "child labor", "trafficking", "kidnap", "abandon", "fear", "threat","intimidate", "victim", "vulnerable", "protective services", "shelter", "coercion",
        "manipulate", "dominate", "control", "isolation", "aggressor", "batterer", "offender","assault", "bruise", "injury", "scar", "harm", "abuser", "perpetrator", "childhood trauma","custody", "violation", "power", "intimidation", "dependency", "escape", "survivor","restraint", "punishment", "silent", "witness", "rescue", "report", "intervention","counseling", "therapy", "recovery", "rescue", "guardian", "broken home", "toxic",
        "unsafe", "threaten", "menace", "torment", "dysfunctional", "parent", "guardian"],
    "Homicide/Gun Violence": ["murder", "homicide", "gunshot", "shooting", "kill", "death", "assassination", "slaughter","massacre", "victim", "shooter", "gunman", "firearm", "bullet", "weapon", "fatal", "deadly","ambush", "sniper", "gang violence", "drive-by", "murderer", "assailant", "harm", "threat",
        "armed", "pistol", "rifle", "semi-automatic", "assault rifle", "machine gun", "ammo", "ammunition","casualty", "crime scene", "forensic", "detective", "investigation", "vengeance", "revenge",
        "bloodshed", "trigger", "motive", "premeditated", "malice", "aforethought", "victim", "fatal","injury", "intentional", "cold-blooded", "violent", "manslaughter", "execution", "crime rate","gang-related", "vendetta", "feud", "hostility", "aggression", "vengeance", "retaliation","bloodthirsty", "gun control", "legislation", "concealed carry", "standoff", "altercation"]
}

def analyze_description(description, threshold=80):
    """
    Analyzes the description of a book and returns warnings if any keywords are found.
    """
    warnings = []
    for warning_name, warning_keywords in KEYWORD_WARNINGS.items():
        for keyword in warning_keywords:
            # Check if the keyword or its fuzzy match is in the description
            if keyword in description.lower() or fuzz.partial_ratio(keyword, description.lower()) > threshold:
                warnings.append(warning_name)
                break  # once we've found a match for this warning, move to the next
    return warnings

def search_open_books(title, author=""):
    """
    Search for a book in the Open Books API
    """
    query = {"title": title}
    if author != '':
        query["author"] = author
    query["fields"] = "key, title, author_name"
    query["limit"] = 1

    response = requests.get(OPEN_BOOKS_API_URL, params=query)
    if response.status_code != 200:
        messagebox.showerror("Error", API_ERROR_MESSAGE)
        return None, None, ""
    data = response.json()
    if data and "docs" in data and len(data["docs"]) > 0:
        key = data["docs"][0]["key"] # ex: '/works/OL45804W' can be used to get to the preview page for this work
        title_  = data["docs"][0]["title"]
        author_lst = data["docs"][0]["author_name"]

        book_url = f"https://openlibrary.org{key}"   
        response = requests.get(book_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        work_description = soup.find('div', {'class': 'work-description-content restricted-view'})
        if work_description is None:
            work_description = soup.find('div', {'class': 'read-more__content'})
        if work_description is None:
            return None, None, f"No description found for {title_}"

        paragraphs = work_description.find_all('p')
        description = []
        for p in paragraphs:
            description.append(p.text.strip())
        description_str = ' '.join(description)

        return title_, author_lst, description_str
    return None, None, ""

def search_google_books(title, author=""):
    """
    Search for a book in the Google Books API and return information along with a purchase link and image thumbnail URL.
    """
    book_title_encoded = urllib.parse.quote(title)
    author_name_encoded = urllib.parse.quote(author)
    
    google_api_url = f"{GOOGLE_BOOKS_API_BASE_URL}?q=intitle:{book_title_encoded}"
    if author != '':
        google_api_url += f"+inauthor:{author_name_encoded}"

    google_api_url += "&printType=books"

    response = requests.get(google_api_url)
    if response.status_code != 200:
        messagebox.showerror("Error", API_ERROR_MESSAGE)
        return None, None, "", "", ""
    
    data = response.json()
    if "items" in data and len(data["items"]) > 0:
        book_info = data["items"][0]["volumeInfo"]
        author_name_lst = book_info.get("authors", [])
        title_ = book_info.get("title", "")
        desc = book_info.get("description", "")
        purchase_link = book_info.get("infoLink", "")
        image_links = book_info.get("imageLinks", {})
        thumbnail_url = image_links.get("thumbnail", "")
        return title_, author_name_lst, desc, purchase_link, thumbnail_url

    return None, None, "", "", ""

def get_book_info(title, author=""):
    """
    Fetches book descriptions using Google Books and Open Books APIs, and returns content warnings based on keywords.
    """
    # Fetch descriptions from APIs
    google_title, google_authors, google_description, purchase_link, thumbnail_url = search_google_books(title, author)   # Adjusted to accept five return values
    print(google_title, google_authors, google_description)
    open_books_title, open_books_authors, open_books_description = search_open_books(title, author)
    print(open_books_title, open_books_authors, open_books_description)

    combined_description = ""

    if google_title is not None: 
        combined_description = google_description

    if open_books_title is not None:
        combined_description = combined_description + " " + open_books_description
    
    if combined_description == "":
        return 0, "No description found for this book.", None, None

    # Get content warnings from the combined description
    warnings_from_description = analyze_description(combined_description)

    # Construct the rating and reason based on the warnings
    rating = len(warnings_from_description)
    reason = ', '.join(warnings_from_description)

    info = namedtuple('info', ['google_title', 'google_authors', 'combined_description',
                               'rating', 'reason', 'purchase_link', 'thumbnail_url'])

    return info(google_title, google_authors,
                combined_description, rating, reason,
                purchase_link, thumbnail_url)

def get_author_info(google_authors, open_books_authors):
    if google_authors:
        return ', '.join(google_authors)
    elif open_books_authors:
        return ', '.join(open_books_authors)
    else:
        return "Unknown"

def show_book_image(url):
    """
    Downloads and displays the book's cover image from the given URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((100, 150), Image.Resampling.LANCZOS)  # Resizing the image
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(result_frame, image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.pack()
    except Exception as e:
        print(f"Failed to load image: {e}")

def search_book_ratings():
    book_title = book_title_entry.get().strip()
    if not book_title:
        messagebox.showerror("Error", "Please enter a book title to search.")
        return
    
    # info is a named tuple!
    info = get_book_info(book_title)
    
    # Format the authors list into a readable string
    author_name = ', '.join(info.google_authors) if info.google_authors else "Unknown"

    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", "end")
    result_text.insert("1.0", f"Title: {info.google_title}\n")
    result_text.insert(tk.END, f"Author: {author_name}\n")
    result_text.insert(tk.END, f"Rating: {info.rating}\n")
    if info.reason:
        result_text.insert(tk.END, f"Reason: {info.reason}\n")
    result_text.config(state=tk.DISABLED)

    for widget in result_frame.winfo_children():
        if isinstance(widget, (tk.Label, tk.Button)):
            widget.destroy()

    if info.thumbnail_url:
        show_book_image(info.thumbnail_url)

    if info.purchase_link:
        purchase_button = tk.Button(result_frame, text="Purchase Book", command=lambda: open_link(info.purchase_link))
        purchase_button.pack()

def clear_result():
    result_text.config(state=tk.NORMAL)  # enable editing
    result_text.delete("1.0", "end")  # clear the content of result_text
    book_title_entry.delete(0, tk.END)  # clear the content of book_title_entry
    result_text.config(state=tk.DISABLED)  # disable editing for result_text

def open_link(url):
    """
    Opens the provided URL in the default web browser.
    """
    webbrowser.open_new(url)
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
instructions_label = tk.Label(root, text="Enter a book title to search.")
instructions_label.pack()

# Create input for book title
book_title_label = tk.Label(root, text="Book Title:")
book_title_label.pack()
book_title_entry = tk.Entry(root, width=50)
book_title_entry.pack()

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

clear_button = tk.Button(root, text="Clear Result", command=clear_result)
clear_button.pack()

# Error handling: wrap the mainloop in a try-except to catch any unexpected exceptions
try:
    root.mainloop()
except Exception as e:
    messagebox.showerror("Unexpected Error", str(e))

root.mainloop()