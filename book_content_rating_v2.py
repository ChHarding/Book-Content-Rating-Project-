import tkinter as tk
from tkinter import messagebox
import requests

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Search for Book Content Warnings")
        self.api_handler = APIHandler()

        self.init_components()

    def init_components(self):
        self.label1 = tk.Label(self, text="Book Title")
        self.label1.pack(pady=10)

        self.book_title_entry = tk.Entry(self)
        self.book_title_entry.pack(pady=10)

        self.label2 = tk.Label(self, text="Author")
        self.label2.pack(pady=10)

        self.author_entry = tk.Entry(self)
        self.author_entry.pack(pady=10)

        self.search_button = tk.Button(self, text="Search", command=self.search_book_ratings)
        self.search_button.pack(pady=10)

        self.clear_button = tk.Button(self, text="Clear result", command=self.clear_results)
        self.clear_button.pack(pady=10)

        self.result_text = tk.Text(self, height=10, width=50)
        self.result_text.pack(pady=10)

    def search_book_ratings(self):
        book_title = self.book_title_entry.get()
        author_name = self.author_entry.get()

        warnings_detected = self.api_handler.get_content_warnings_for_book(book_title, author_name)

        for warning in warnings_detected:
            self.result_text.insert(tk.END, warning + "\n")

    def clear_results(self):
        self.result_text.delete("1.0", "end")


class APIHandler:
    def __init__(self):
        self.analyzer = ContentWarningAnalyzer()

    def get_content_warnings_for_book(self, book_title, author_name):
        description = self.get_description_from_google_books(book_title, author_name)
        subjects = self.get_subjects_from_open_library(book_title, author_name)

        warnings_detected = []
        warnings_detected.extend(self.analyzer.analyze_text(description))
        warnings_detected.extend(self.analyzer.analyze_text(subjects))

        return list(set(warnings_detected))

    def get_description_from_google_books(self, book_title, author_name):
        # This is just a placeholder; you'll need to handle actual API requests and parsing here
        return "Sample description from Google Books for {} by {}".format(book_title, author_name)

    def get_subjects_from_open_library(self, book_title, author_name):
        # This is just a placeholder; you'll need to handle actual API requests and parsing here
        return "Sample subjects from Open Library for {} by {}".format(book_title, author_name)


class ContentWarningAnalyzer:
    def __init__(self):
        self.content_warning_keywords = {
        # Content warning keyword themes and their associated lists
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
        
        "Self-Harm/Suicide": [ "self-harm", "suicide", "cutting", "overdose", "self-inflict", "end life", "attempt",
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
        
        "Violence & Graphic Content": ["violence", "graphic", "gore", "explicit", "brutal"],
        "Substance Abuse/Addiction": ["drug", "addiction", "alcohol", "substance abuse", "intoxication"],
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
        
        "Homicide/Gun Violence": [ "murder", "homicide", "gunshot", "shooting", "kill", "death", "assassination", "slaughter",
        "massacre", "victim", "shooter", "gunman", "firearm", "bullet", "weapon", "fatal", "deadly",
        "ambush", "sniper", "gang violence", "drive-by", "murderer", "assailant", "harm", "threat",
        "armed", "pistol", "rifle", "semi-automatic", "assault rifle", "machine gun", "ammo", "ammunition",
        "casualty", "crime scene", "forensic", "detective", "investigation", "vengeance", "revenge",
        "bloodshed", "trigger", "motive", "premeditated", "malice", "aforethought", "victim", "fatal",
        "injury", "intentional", "cold-blooded", "violent", "manslaughter", "execution", "crime rate",
        "gang-related", "vendetta", "feud", "hostility", "aggression", "vengeance", "retaliation",
        "bloodthirsty", "gun control", "legislation", "concealed carry", "standoff", "altercation"]
}
    def analyze_text(self, text):
        detected_warnings = []

        for warning, keywords in self.content_warning_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    detected_warnings.append(warning)
                    break  

        return detected_warnings


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()