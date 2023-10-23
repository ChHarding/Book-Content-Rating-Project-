import tkinter as tk
from tkinter import messagebox
import requests
from fuzzywuzzy import fuzz
import urllib.parse

# Dictionary for keyword-based content warnings
KEYWORD_WARNINGS = {
    "Animal Abuse": [ "animal", "cruelty", "neglect", "harm", "suffering", "mistreatment", "abuse",
        "beating", "starvation", "malnourishment", "torment", "torture", "maltreat",
        "exploit", "kill", "slaughter", "poach", "trap", "experiment", "hunt", "cage",
        "abandon", "discard", "pain", "whip", "shoot", "trap", "confine", "enslave",
        "skin", "fur", "endanger", "bait", "bleed", "choke", "crush", "misuse", "overwork",
        "punish", "scar", "shock", "strangle", "wound", "maim", "disfigure", "mutilate",
        "vivisection", "imprisoned", "lab animal", "chained", "caged", "trafficked",
        "illegal trade", "baiting", "fight", "abusement park", "entertainment", "circuses",
        "rodeo", "farming", "fur trade", "leather", "cosmetic testing", "laboratory", "breed",
        "overbreed", "pet mill", "racing", "gamblers", "breeders", "discard", "euthanize",
        "abandoned", "stray", "wildlife", "marine life"],
    "Sexual Violence": ["rape", "molestation", "sexual assault", "non-consensual", "nonconsensual", "harassment",
        "grope", "abuse", "forced", "attack", "inappropriate", "unwanted", "exploit", "violate",
        "coerce", "intimidate", "threaten", "predator", "offender", "consent", "groom", "stalk",
        "unsolicited", "touch", "fear", "trauma", "victim", "traumatize", "vulnerable", "invasion",
        "inappropriate", "violation", "indecent", "forceful", "abusive relationship", "manipulation",
        "intimate violence", "uninvited", "molest", "statutory", "silence", "hush", "date rape",
        "drugged", "power", "control", "cyber", "explicit", "sexting", "blackmail", "shaming",
        "exploitation", "revenge porn", "intimate threat", "exposure", "uncomfortable", "unsafe",
        "minor", "child", "elderly", "defenseless"],
    "Body Image/Disordered Eating": ["body image", "eating disorder", "anorexia", "bulimia", "body dysmorphia", "binge",
        "starvation", "diet", "thin", "fat", "overeating", "weight", "obesity", "underweight",
        "purge", "restriction", "calorie", "fast", "unhealthy", "mirror", "self-worth",
        "appearance", "pressure", "ideal", "size", "dieting", "body shaming", "self-conscious",
        "perfection", "body dissatisfaction", "exercise", "obsession", "orthorexia", "laxatives",
        "diuretics", "body checking", "guilt", "shame", "control", "image", "food fear",
        "compulsive", "scale", "weight gain", "weight loss", "muscle", "toning", "fitness",
        "skinny", "plump", "heavy", "light", "self-esteem", "self-hate", "mirror check",
        "avoidance", "pinch", "measure", "waist", "BMI", "comparison"],
    "Self-Harm/Suicide": ["self-harm", "suicide", "cutting", "overdose", "self-inflict", "end life", "attempt",
        "despair", "hopelessness", "pain", "wrist", "bleed", "scars", "burn", "jump", "hang",
        "suffocate", "cry", "lonely", "depressed", "worthless", "numb", "lost", "void", "struggle",
        "isolation", "helplessness", "grieve", "self-loathing", "suicidal thoughts", "ideation",
        "death wish", "razor", "pills", "intoxication", "sadness", "sorrow", "self-punishment",
        "self-destructive", "darkness", "emptiness", "rope", "bridge", "height", "firearm",
        "blade", "cutting tool", "gas", "drowning", "substance", "ingest", "alcohol", "method",
        "means", "lethality", "intent", "crisis", "hotline"],
    "Discrimination/Hate Crimes": ["discrimination", "racism", "homophobia", "sexism", "hate crime", "prejudice", "bigotry",
        "intolerance", "xenophobia", "bias", "stereotype", "slur", "discriminate", "marginalize",
        "oppress", "minority", "inequality", "unfair", "segregation", "racist", "sexist", "bigot",
        "prejudiced", "hateful", "derogatory", "injustice", "persecute", "isolate", "alienate",
        "ostracize", "scapegoat", "gender bias", "ethnicity", "nationality", "caste", "class",
        "religious", "anti-Semitism", "Islamophobia", "disability", "ageism", "LGBTQ+",
        "gender identity", "transphobia", "colorism", "microaggressions", "supremacy", "radical",
        "extremist", "prejudice", "bias-motivated", "targeted", "offense", "vandalism", "symbol",
        "hate speech", "propaganda"],
    "Violence & Graphic Content": ["violence", "graphic", "gore", "brutal", "vicious", "blood", "wound", "injury", "attack",
        "hurt", "punch", "stab", "hit", "fight", "assault", "battle", "conflict", "terror", "shock",
        "horror", "aggression", "intense", "disturb", "trauma", "frighten", "scar", "fear", "threat",
        "danger", "menace", "brawl", "riot", "massacre", "ambush", "explosive", "bomb", "firearm",
        "weapon", "gunshot", "combat", "warfare", "sadism", "torture", "mutilation", "decapitation",
        "beheading", "suffering", "pain", "traumatic", "scarring", "nightmare", "terrorize", "harm",
        "damage", "intimidation", "coercion"],
    "Substance Abuse/Addiction": ["drugs", "drug use", "substance abuse", "narcotics", 
        "overdose", "addiction", "dependence","heroin", "cocaine", "methamphetamine", "crystal meth", 
        "amphetamine", "speed", "ecstasy", "MDMA","marijuana", "weed", "pot", "cannabis", "THC", "CBD", 
        "psychedelics", "LSD", "acid", "magic mushrooms", "psilocybin","opioids", "opiates", "painkillers", "morphine", "codeine", 
        "benzodiazepines", "valium", "xanax","alcohol", "alcoholism", "drinking", "intoxication", 
        "tobacco", "smoking", "cigarettes", "nicotine", 
        "inhalants", "huffing", "prescription drugs", "pharmaceutical abuse", 
        "caffeine", "energy drinks", "coffee addiction", 
        "anabolic steroids","barbiturates", "sedatives","hallucinogens", "PCP", "ketamine", 
        "binge drinking", "drunk", "hangover","rehab", "rehabilitation", "detox", "withdrawal"],
    "Child Abuse/Domestic Violence": ["child abuse", "domestic violence", "molestation", "beating", "hurt", "neglect",
        "exploit", "trauma", "emotional abuse", "verbal abuse", "physical abuse", "bullying",
        "endanger", "child labor", "trafficking", "kidnap", "abandon", "fear", "threat",
        "intimidate", "victim", "vulnerable", "protective services", "shelter", "coercion",
        "manipulate", "dominate", "control", "isolation", "aggressor", "batterer", "offender",
        "assault", "bruise", "injury", "scar", "harm", "abuser", "perpetrator", "childhood trauma",
        "custody", "violation", "power", "intimidation", "dependency", "escape", "survivor",
        "restraint", "punishment", "silent", "witness", "rescue", "report", "intervention",
        "counseling", "therapy", "recovery", "rescue", "guardian", "broken home", "toxic",
        "unsafe", "threaten", "menace", "torment", "dysfunctional", "parent", "guardian"],
    "Homicide/Gun Violence": ["murder", "homicide", "gunshot", "shooting", "kill", "death", "assassination", "slaughter",
        "massacre", "victim", "shooter", "gunman", "firearm", "bullet", "weapon", "fatal", "deadly",
        "ambush", "sniper", "gang violence", "drive-by", "murderer", "assailant", "harm", "threat",
        "armed", "pistol", "rifle", "semi-automatic", "assault rifle", "machine gun", "ammo", "ammunition",
        "casualty", "crime scene", "forensic", "detective", "investigation", "vengeance", "revenge",
        "bloodshed", "trigger", "motive", "premeditated", "malice", "aforethought", "victim", "fatal",
        "injury", "intentional", "cold-blooded", "violent", "manslaughter", "execution", "crime rate",
        "gang-related", "vendetta", "feud", "hostility", "aggression", "vengeance", "retaliation",
        "bloodthirsty", "gun control", "legislation", "concealed carry", "standoff", "altercation"]
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
root.title("Book Content Warning")

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
search_button = tk.Button(root, text="Search for Content Warning", command=search_book_ratings)
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