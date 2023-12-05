"""
Module: Book Content Rating Application

This module provides the functionality for a book content rating application. It uses tkinter for the GUI, 
requests for API calls, and various other libraries for processing data.

Attributes:
    OPEN_BOOKS_API_URL (str): URL for the Open Library Books API.
    GOOGLE_BOOKS_API_BASE_URL (str): URL for the Google Books API.
    API_ERROR_MESSAGE (str): Default error message for API connection issues.
"""

import tkinter as tk  # Tkinter for GUI components
from tkinter import messagebox, Listbox, Label, Button, Entry, Frame, Text  # Tkinter widgets
import requests  # For making API requests
import urllib.parse  # For URL encoding
from fuzzywuzzy import fuzz  # For string matching
from bs4 import BeautifulSoup  # For HTML parsing
import webbrowser  # For opening URLs in a web browser
from PIL import Image, ImageTk  # For handling images
import io  # For byte stream operations
from collections import namedtuple  # For creating named tuples

# URLs for APIs
OPEN_BOOKS_API_URL = "https://openlibrary.org/search.json"  # URL for Open Library search API
GOOGLE_BOOKS_API_BASE_URL = "https://www.googleapis.com/books/v1/volumes"  # URL for Google Books API

API_ERROR_MESSAGE = "We're having trouble connecting to the system"  # Default API error message

# Dictionary of keywords associated with various content warnings
# Each key represents a type of content warning with a list of keywords related to that warning
KEYWORD_WARNINGS = {
    "Animal Abuse": ["animal", "cruelty", "neglect", "harm", "suffering", "mistreatment", "abuse","beating", "starvation", "malnourishment", "torment", "torture", "maltreat",
        "exploit", "kill", "slaughter", "poach", "trap", "experiment", "hunt", "cage","abandon", "discard", "pain", "whip", "shoot", "trap", "confine", "enslave",
        "skin", "fur", "endanger", "bait", "bleed", "choke", "crush", "misuse","overwork", "punish", "scar", "shock", "strangle", "wound", "maim", "disfigure",
        "mutilate", "vivisection", "imprisoned", "lab animal", "chained", "caged","trafficked", "illegal trade", "baiting", "fight", "abusement park", "entertainment",
        "circuses", "rodeo", "farming", "fur trade", "leather", "cosmetic testing","laboratory", "breed", "overbreed", "pet mill", "racing", "gamblers", "breeders",
        "discard", "euthanize", "abandoned", "stray", "wildlife", "marine life","inhumane", "captivity", "illegal hunting", "brutality", "battery", "factory farming",
        "intensive farming", "live transport", "overfishing", "pollution", "habitat destruction","deforestation", "illegal capture", "smuggling", "animal testing", "genetic manipulation",
        "cloning", "forced feeding", "foie gras", "shark finning", "ivory trade", "horn trade","bear bile", "exotic pets", "wildlife trade", "dolphin hunt", "whale hunt", "seal hunt",
        "fur farming", "battery cages", "veal crates", "puppy mills", "cockfight", "dogfight","bullfight", "horse whipping", "elephant ride", "animal performance", "animal hoarding",
        "overpopulation", "negligent care", "physical abuse", "psychological abuse", "overbreeding","debeaking", "tail docking", "ear cropping", "declawing", "force molting", "live bait","animal sacrifice", "roadkill", "pest control", "inhumane slaughter", "live skinning",
        "animal fighting", "dog racing", "horse racing", "animal exploitation", "speciesism","wild capture", "wildlife disruption", "ecosystem damage", "bioaccumulation",
        "toxic testing", "animal abandonment", "zoo captivity", "unsustainable practices","destructive fishing", "bycatch", "animal hoarder", "animal neglect", "animal collector"],
    "Sexual Violence": ["rape", "sexual assault", "molestation", "abuse", "harassment", "exploitation",
        "predator", "stalking", "coercion", "forced", "non-consensual", "trafficking","grooming", "victimization", "indecent", "violence", "aggression", "dominance",
        "power abuse", "lewd", "sex crime", "sexual misconduct", "unwanted advances","inappropriate touch", "intimidation", "survivor", "sexual violence", "sexual threat",
        "sodomy", "non-consent", "predatory", "sexual predator", "date rape", "gang rape","spousal abuse", "marital rape", "child sexual abuse", "incest", "voyeurism",
        "exhibitionism", "sexual humiliation", "sexual slavery", "forced prostitution","sexual exploitation", "sexual coercion", "revenge porn", "upskirt", "peeping tom",
        "statutory rape", "sexual bullying", "cyber harassment", "sextortion", "sexual blackmail",
        "fondling", "indecency", "sexual aggression", "sexual dominance", "rape culture","non-consensual", "nonconsensual", "harassment","grope", "abuse", "forced", "attack", "inappropriate", "unwanted", "exploit", "violate",
        "coerce", "intimidate", "threaten", "predator", "offender", "consent", "groom", "stalk","unsolicited", "touch", "fear", "trauma", "victim", "traumatize", "vulnerable", "invasion",
        "inappropriate", "violation", "indecent", "forceful", "abusive relationship", "manipulation","intimate violence", "uninvited", "molest", "statutory", "silence", "hush", "date rape","drugged", "power", "control", "cyber", "explicit", "sexting", "blackmail", "shaming","exploitation", "revenge porn", "intimate threat", "exposure", "uncomfortable", "unsafe","minor", "child", "elderly", "defenseless"],
    "Body Image/Disordered Eating": ["body image", "eating disorder", "anorexia", "bulimia", "body dysmorphia", "binge","starvation", "diet", "thin", "fat", "overeating", "weight", "obesity", "underweight",
        "purge", "overeating","binge eating", "starvation", "purging", "body shaming", "weight obsession","negative body image", "fat shaming", "dieting", "extreme dieting", "laxative abuse",
        "compulsive eating", "restrictive eating", "body hatred", "thinness", "overexercising","body dissatisfaction", "weight criticism", "calorie counting", "self-starvation",
        "food phobia", "negative self-image", "body comparison", "weight loss","unhealthy body image", "beauty standards", "food guilt",
        "perfectionism in diet", "malnutrition", "underweight", "overweight", "obesity","body negativity", "food obsession", "diet pills", "appetite suppressants",
        "body image distortion", "self-esteem issues", "unrealistic body standards","size zero", "model thin", "skinny ideal", "appearance-focused culture","restriction", "calorie", "fast", "unhealthy", "mirror", "self-worth","appearance", "pressure", "ideal", "size", "dieting", "body shaming", "self-conscious",
        "perfection", "body dissatisfaction", "exercise", "obsession", "orthorexia", "laxatives","diuretics", "body checking", "guilt", "shame", "control", "image", "food fear","compulsive", "scale", "weight gain", "weight loss", "muscle", "toning", "fitness","skinny", "plump", "heavy", "light", "self-esteem", "self-hate", "mirror check","avoidance", "pinch", "measure", "waist", "BMI", "comparison"],
    "Self-Harm/Suicide": ["self-harm", "suicide", "cutting", "overdose", "self-inflict", "end life", "attempt",
        "despair", "self-harm", "self-injury", "cutting", "suicide", "suicidal thoughts", "self-mutilation","self-destructive behavior", "overdose", "self-inflicted", "self-abuse", "harmful behavior","self-punishment", "self-cutting", "self-burning", "suicide attempt", "suicide ideation",
        "self-poisoning", "self-sabotage", "suicidal ideation", "suicidal tendencies", "hanging",
        "jumping", "poisoning", "drowning", "asphyxiation", "suicide note", "suicide plan","fatal injury", "self-inflicted wound", "self-aggression", "self-hatred", "suicide pact",
        "suicide prevention", "cry for help", "self-scarification", "suicide hotline", "suicide crisis","self-strangulation", "lethal means", "death wish", "desperation", "hopelessness",
        "suicide survivor", "fatal self-harm", "suicidal behavior", "suicidal crisis", "suicide watch","suicide risk", "suicide method", "self-inflicted pain", "suicide contagion", "hopelessness", "pain", "wrist", "bleed", "scars", "burn", "jump", "hang","suffocate", "cry", "lonely", "depressed", "worthless", "numb", "lost", "void", "struggle","isolation", "helplessness", "grieve", "self-loathing", "suicidal thoughts", "ideation","death wish", "razor", "pills", "intoxication", "sadness", "sorrow", "self-punishment",
        "self-destructive", "darkness", "emptiness", "rope", "bridge", "height", "firearm","blade", "cutting tool", "gas", "drowning", "substance", "ingest", "alcohol", "method","means", "lethality", "intent", "crisis", "hotline"],
    "Discrimination/Hate Crimes": ["discrimination", "racism", "homophobia", "sexism", "hate crime", "prejudice", "bigotry","intolerance", "xenophobia", "bias", "stereotype", "slur", "discriminate", "marginalize",
        "oppress", "discrimination", "racism", "sexism", "homophobia", "transphobia", "xenophobia",
        "bigotry", "prejudice", "hate crime", "bias", "intolerance", "stereotyping","inequality", "marginalization", "exclusion", "hate speech", "racial profiling",
        "gender discrimination", "sexual orientation discrimination", "religious intolerance","ethnic hatred", "social injustice", "civil rights violation", "racial slur",
        "gender bias", "misogyny", "misandry", "ageism", "ableism", "classism","scapegoating", "victimization", "hateful rhetoric", "sectarian violence",
        "racial violence", "gender-based violence", "ethnocentrism", "cultural discrimination","lynching", "apartheid", "segregation", "genocide", "ethnic cleansing",
        "hate group", "white supremacy", "neo-nazism", "radical extremism", "racial supremacy","gender inequality", "institutional racism", "structural discrimination", "oppression",
        "cultural bias", "social exclusion", "minority oppression", "racial injustice", "gender violence", "racial tension", "cultural clash", "religious persecution","caste discrimination", "social stratification", "hate propaganda", "racial discrimination",
        "ethnic bias", "religious bias", "gender stereotyping", "cultural stereotyping", "minority", "inequality", "unfair", "segregation", "racist", "sexist", "bigot","prejudiced", "hateful", "derogatory", "injustice", "persecute", "isolate", "alienate",
        "ostracize", "scapegoat", "gender bias", "ethnicity", "nationality", "caste", "class","religious", "anti-Semitism", "Islamophobia", "disability", "ageism", "LGBTQ+","gender identity", "transphobia", "colorism", "microaggressions", "supremacy", "radical","extremist", "prejudice", "bias-motivated", "targeted", "offense", "vandalism", "symbol","hate speech", "propaganda"],
    "Violence & Graphic Content": ["violence", "graphic", "gore", "brutal", "vicious", "blood", "wound", "injury", "attack","hurt", "punch", "stab", "hit", "fight", "assault", "battle", "conflict", "terror", "shock","horror", "aggression", "intense", "disturb", "trauma", "frighten", "scar", "fear", "threat","danger", "menace", "brawl", "riot", "massacre", "ambush", "explosive", "bomb", "firearm",
        "weapon", "gunshot",  "violence", "graphic content", "gore", "brutality", "bloodshed", "assault",
        "fighting", "murder", "homicide", "torture", "abuse", "physical attack","warfare", "combat", "mutilation", "graphic injury", "fatal violence", 
        "violent crime", "bloodletting", "gruesome scene", "violent death", "massacre","bloodbath", "carnage", "atrocity", "savagery", "graphic murder", "violent assault",
        "gruesome injury", "sadistic torture", "brutal killing", "violent conflict", "graphic violence", "violent imagery", "vicious attack", "bloody conflict",
        "graphic torture", "violent struggle", "violent aggression", "barbaric acts","graphic killing", "sadistic violence", "graphic depiction", "violent encounter",
        "gruesome detail", "violent retribution", "violent reprisal", "bloody violence","gory scene", "graphic description", "graphic battle", "violent scene", 
        "violence portrayal", "gory detail", "brutal scene", "violent act", "violent behavior","violent clash", "violent uprising", "violent confrontation", "graphic attack""combat", "warfare", "sadism", "torture", "mutilation", "decapitation","beheading", "suffering", "pain", "traumatic", "scarring", "nightmare", "terrorize", "harm","damage", "intimidation", "coercion"],
    "Substance Abuse/Addiction": ["drugs", "drug use", "substance abuse", "narcotics", 
        "overdose", "addiction", "substance abuse", "addiction", "drug abuse", "alcoholism", "drug addiction","alcohol abuse", "overdose", "dependency", "substance use disorder", "drug dependency",
        "narcotics", "intoxication", "withdrawal", "rehabilitation", "sober", "sobriety","substance misuse", "drunk", "high", "addict", "relapse", "detoxification",
        "intervention", "drug rehabilitation", "alcohol dependency", "chemical dependency","opioid crisis", "methamphetamine", "cocaine", "heroin", "prescription drug abuse",
        "illegal drugs", "controlled substances", "substance use", "drug treatment","alcohol treatment", "addiction recovery", "substance dependence", "drug overdose",
        "alcohol overdose", "drug intoxication", "alcohol intoxication", "drug addict","alcohol addict", "drug withdrawal", "alcohol withdrawal", "substance abuse treatment","addiction treatment", "drug rehabilitation center", "alcohol rehabilitation center",
        "substance abuse recovery", "addiction therapy", "substance abuse counseling","drug abuse prevention", "alcohol abuse prevention", "substance addiction","chemical abuse", "addictive behavior", "drug craving", "alcohol craving",
        "substance craving", "drug relapse", "alcohol relapse", "addiction relapse","dependence","heroin", "cocaine", "methamphetamine", "crystal meth", "amphetamine", "speed", "ecstasy", "MDMA","marijuana", "weed", "pot", "cannabis", "THC", "CBD", "psychedelics", "LSD", "acid", "magic mushrooms", "psilocybin","opioids", "opiates", "painkillers", "morphine", "codeine", 
        "benzodiazepines", "valium", "xanax","alcohol", "alcoholism", "drinking", "intoxication", "tobacco", "smoking", "cigarettes", "nicotine", "inhalants", "huffing", "prescription drugs", "pharmaceutical abuse", "caffeine", "energy drinks", "coffee addiction", "anabolic steroids","barbiturates", "sedatives","hallucinogens", "PCP", "ketamine", "binge drinking", "drunk", "hangover","rehab", "rehabilitation", "detox", "withdrawal"],
    "Child Abuse/Domestic Violence": ["child abuse", "domestic violence", "molestation", "beating", "hurt", "neglect","exploit", "trauma", "emotional abuse", "verbal abuse", "physical abuse", "bullying","endanger", "child labor", "trafficking", "kidnap", "abandon", "fear", "threat","intimidate", "victim", "vulnerable", "protective services", "shelter", "coercion",
        "manipulate", "child abuse", "neglect", "maltreatment", "domestic violence", "physical abuse","emotional abuse", "psychological abuse", "sexual abuse", "exploitation", "bullying",
        "harassment", "intimidation", "trauma", "traumatic", "beating", "hitting", "slapping","shaking", "burning", "scalding", "biting", "bruising", "wounding", "injury", "injuries","torture", "assault", "molestation", "incest", "rape", "grooming", "threats", "threatening","screaming", "yelling", "verbal abuse", "coercion", "manipulation", "isolation", "neglecting","abandonment", "starvation", "malnutrition", "withholding care", "medical neglect", "emotional neglect","unsanitary conditions", "unsafe living conditions", "poverty", "homelessness", "drug exposure",
        "alcohol exposure", "custody issues", "legal battles", "restraining order", "protection order","foster care", "adoption issues", "guardianship", "parental rights", "custodial interference",
        "parental kidnapping", "runaway", "missing children", "child exploitation", "child labor","child trafficking", "sex trafficking", "child soldiers", "child marriage", "forced marriage",
        "honor violence", "female genital mutilation", "dowry violence", "acid attacks", "bride burning","spousal abuse", "partner violence", "intimate partner violence", "marital rape", "economic abuse",
        "financial abuse", "control", "power dynamics", "victimization", "victim blaming", "gaslighting","mental health impact", "post-traumatic stress disorder", "anxiety", "depression", "suicidal ideation",
        "self-harm", "substance abuse", "alcoholism", "drug addiction", "escape", "survivor", "resilience","coping mechanisms", "therapy", "counseling", "support groups", "legal action", "law enforcement",
        "social services", "child protective services", "domestic violence shelters", "safe houses","restraining orders", "legal aid", "court cases", "testimony", "witness", "perpetrator", "abuser","predator", "stalking", "cyberstalking", "online harassment", "blackmail", "extortion", "revenge porn",
        "divorce", "separation", "child custody", "visitation rights", "parental alienation", "paternal rights","maternal rights", "family dynamics", "dysfunctional family", "broken home", "family secrets",
        "silence", "denial", "shame", "guilt", "blame", "accusations", "false accusations", "judgment","societal attitudes", "cultural norms", "tradition", "honor", "disgrace", "scandal", "public opinion","media portrayal", "advocacy", "activism", "awareness campaigns", "policy changes", "legislation","protective laws", "child welfare", "human rights", "victim rights", "survivor stories",
        "autobiographical accounts", "biographies", "case studies", "documentaries", "non-fiction","fictional representations", "literary analysis", "sociological studies", "psychological studies",
        "research findings", "statistical data", "data analysis", "academic discourse", "scholarly articles","expert opinions", "testimonials", "personal narratives", "first-hand accounts", "survivor testimonies","healing journey", "recovery process", "rebuilding lives", "empowerment", "strength", "courage",
        "overcoming adversity", "resilience", "hope", "inspiration", "transformation", "growth", "change","new beginnings", "moving forward", "forgiveness", "reconciliation", "peace", "harmony", "healing","closure", "resolution", "justice", "accountability", "consequences", "retribution", "penalties","punishment", "incarceration", "prison", "jail", "legal system", "criminal justice", "law enforcement",
        "police", "detectives", "investigation", "evidence", "proof", "trial", "courtroom", "judge","jury", "verdict", "sentencing", "appeals", "legal battles", "rights", "civil liberties",
        "constitutional rights", "legal representation", "attorneys", "lawyers", "prosecutors","defense attorneys", "legal aid", "pro bono", "advocates", "victim advocates", "counselors",
        "therapists", "psychologists", "psychiatrists", "social workers", "case managers", "support staff","volunteers", "non-profit organizations", "government agencies", "community resources", "hotlines",
        "emergency services", "crisis intervention", "prevention programs", "education", "outreach","public awareness", "campaigns", "fundraising", "donations", "grants", "sponsorships", "partnerships",
        "coalitions", "networks", "conferences", "seminars", "workshops", "training", "certification","professional development", "best practices", "guidelines", "protocols", "standards", "ethics",
        "morals", "values", "beliefs", "attitudes", "perspectives", "opinions", "views", "ideologies","philosophies", "doctrines", "theories", "hypotheses", "assumptions", "prejudices", "biases",
        "stereotypes", "myths", "misconceptions", "misunderstandings", "ignorance", "lack of knowledge","unawareness", "insensitivity", "indifference", "apathy", "lack of empathy", "lack of compassion",
        "lack of understanding", "lack of awareness", "lack of concern", "lack of interest", "lack of involvement","lack of engagement", "lack of commitment", "lack of support", "lack of resources", "lack of funding",
        "lack of access", "barriers", "obstacles", "challenges", "difficulties", "hardships", "struggles","suffering", "pain", "anguish", "agony", "grief", "loss", "mourning", "bereavement", "trauma",
        "traumatic experiences", "shock", "horror", "terror", "fear", "anxiety", "stress", "tension","pressure", "nervousness", "worry", "concern", "apprehension", "dread", "panic", "alarm",
        "desperation", "hopelessness", "helplessness", "vulnerability", "exposure", "risk", "danger","threat", "hazard", "peril", "jeopardy", "insecurity", "uncertainty", "instability", "unpredictability",
        "chaos", "disorder", "disruption", "upheaval", "turmoil", "conflict", "confrontation", "clash","struggle", "fight", "battle", "war", "hostilities", "violence", "aggression", "hostility","antagonism", "animosity", "hatred", "enmity", "rivalry", "competition", "contention", "dispute",
        "argument", "debate", "discussion", "dialogue", "negotiation", "mediation", "arbitration","conciliation", "compromise", "settlement", "agreement", "consensus", "understanding", "reconciliation",
        "resolution", "solution", "outcome", "result", "conclusion", "closure", "finality", "end","termination", "cessation", "conclusion", "completion", "fulfillment", "achievement", "accomplishment",
        "success", "victory", "triumph", "conquest", "dominance", "control", "power", "influence","authority", "leadership", "command", "mastery", "expertise", "skill", "ability", "capability",
        "competence", "proficiency", "knowledge", "understanding", "insight", "wisdom", "intelligence","intellect", "reason", "logic", "rationality", "objectivity", "clarity", "precision", "accuracy","reliability", "trustworthiness", "credibility", "authenticity","dominate", "control", "isolation", "aggressor", "batterer", "offender","assault", "bruise", "injury", "scar", "harm", "abuser", "perpetrator", "childhood trauma","custody", "violation", "power", "intimidation", "dependency", "escape", "survivor","restraint", "punishment", "silent", "witness", "rescue", "report", "intervention","counseling", "therapy", "recovery", "rescue", "guardian", "broken home", "toxic",
        "unsafe","threaten", "menace", "torment", "dysfunctional", "parent", "guardian"],
    "Homicide/Gun Violence": ["murder", "homicide", "gunshot", "shooting", "kill", "death", "assassination", "slaughter","massacre", "victim", "shooter", "gunman", "firearm", "bullet", "weapon", "fatal", "deadly","ambush", "sniper", "gang violence", "drive-by", "murderer", "assailant", "harm", "threat",
        "armed", "pistol", "rifle", "semi-automatic", "assault rifle", "machine gun", "ammo", "ammunition","casualty", "crime scene", "forensic", "detective", "investigation", "vengeance", "revenge",
        "bloodshed", "trigger", "motive", "premeditated", "malice", "aforethought", "victim", "fatal","injury", "intentional", "cold-blooded", "violent", "manslaughter", "execution",     "stray bullet", "fatal shooting", "armed robbery", "terrorist attack", "extremist violence","political assassination", "lynching", "school shooting", "public shooting", "workplace violence",
        "domestic terrorism", "hate crime", "suicidal shooter", "armed conflict", "civil unrest", "riot","mob violence", "paramilitary action", "guerrilla warfare", "tactical operation", "counterterrorism",
        "military assault", "shootout", "execution style", "hitman", "contract killing", "armed assault",
        "war crime", "ethnic cleansing", "genocide", "rebel attack", "insurgency", "militia", "radicalization","extremism", "survivor", "witness", "trauma", "PTSD", "self-defense", "murder plot", "conspiracy",
        "illegal arms", "gun trafficking", "arms dealer", "warlord", "death toll", "fatalities", "body count",
        "bloodbath", "mass murderer", "serial killer", "spree killer", "psychopath", "sociopath", "criminal","felony", "misdemeanor", "law enforcement", "SWAT", "police shooting", "officer-involved shooting",
        "justice", "inquest", "criminal trial", "jury", "verdict", "conviction", "acquittal", "plea bargain","self-incrimination", "testimony", "eyewitness", "forensic evidence", "ballistic", "autopsy", "coroner",
        "crime lab", "DNA evidence", "fingerprint", "crime analyst", "profiling", "criminal psychology","hostage situation", "negotiation", "siege", "barricade", "emergency response", "first responder",
        "crisis management", "public safety", "security breach", "lockdown", "emergency drill", "threat assessment","risk management", "surveillance", "counterintelligence", "intelligence gathering", "undercover operation",
        "stakeout", "raid", "interrogation", "suspect", "informant", "witness protection", "safe house","criminal network", "organized crime", "drug cartel", "mafia", "syndicate", "gang war", "turf war",
        "retaliation", "payback", "blood feud", "code of silence", "omerta", "vigilante", "justice seeker","retribution", "counterstrike", "rebellious", "uprising", "revolt", "anarchy", "chaos", "mayhem",
        "destructive", "catastrophe", "disaster", "atrocity", "brutality", "savagery", "inhumanity","cruelty", "barbarism", "tyranny", "oppression", "persecution", "victimization", "abuse", "exploitation",
        "torture", "mutilation", "disfigurement", "beheading", "execution", "slaughter", "genocide","mass murder", "annihilation", "extermination","crime rate","gang-related", "vendetta", "feud", "hostility", "aggression", "vengeance", "retaliation","bloodthirsty", "gun control", "legislation", "concealed carry", "standoff", "altercation"]
}

def analyze_description(description, threshold=80):
    """
    Analyzes a book description to identify potential content warnings based on predefined keywords.

    This function checks each keyword in the KEYWORD_WARNINGS dictionary against the given book 
    description. If a keyword matches or has a partial fuzzy match above the specified threshold,
    the corresponding warning is included in the result.

    Args:
        description (str): The book description to be analyzed.
        threshold (int, optional): The threshold for fuzzy matching (default is 80).

    Returns:
        list: A list of warning types that match keywords found in the description.

    Raises:
        ValueError: If the description is not provided or is not a string.
    """

    # Validate input description
    if not isinstance(description, str):
        raise ValueError("Description must be a string.")

    warnings = []  # Initialize a list to store matching warnings

    # Iterate over each warning type and its associated keywords
    for warning_name, warning_keywords in KEYWORD_WARNINGS.items():
        # Check each keyword in the current warning type
        for keyword in warning_keywords:
            # Check if keyword is in description or matches fuzzily above threshold
            if keyword in description.lower() or fuzz.partial_ratio(keyword, description.lower()) > threshold:
                warnings.append(warning_name)  # Add warning type to list
                break  # Stop checking more keywords in the same warning type

    return warnings  # Return the list of found warnings

def get_google_books_description_and_img_URL(ISBN):
    """
    Retrieves the description and thumbnail image URL of a book from the Google Books API using its ISBN.

    This function makes a request to the Google Books API and extracts the book description and 
    thumbnail image URL if available. If the API request fails or the data is not found, it returns empty strings.

    Args:
        ISBN (str): The International Standard Book Number (ISBN) of the book.

    Returns:
        tuple: A tuple containing the book description and image URL. Returns empty strings if data is not found or on error.

    Raises:
        tk.messagebox.showerror: If the API request fails, an error message box is displayed.
    """

    google_api_url = f"{GOOGLE_BOOKS_API_BASE_URL}?q=isbn:{ISBN}"  # Construct the API URL

    try:
        response = requests.get(google_api_url)  # Send a request to the Google Books API
        response.raise_for_status()  # Raises HTTPError for bad HTTP response
    except requests.RequestException as e:
        messagebox.showerror("Error", f"API Request failed: {e}")  # Display error message on request failure
        return "", ""

    data = response.json()  # Parse the JSON response
    if "items" not in data:
        print("Unexpected data structure received from Google Books API.")  # Log unexpected data structure
        return "", ""

    try:
        description = data["items"][0]["volumeInfo"]["description"]  # Extract the book description
        image_url = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]  # Extract the image URL
        return description, image_url
    except:
        return "", ""  # Return empty strings if extraction fails


def get_open_books_description(key):
    """
    Retrieves the book description from the Open Library website using a given key.

    This function constructs a URL for the Open Library page of the book using the provided key,
    then sends an HTTP request to get the page content. It parses the HTML to find the book's description. 
    The description is extracted as text from paragraph elements and returned as a single string.

    Args:
        key (str): The unique key for the book on the Open Library website.

    Returns:
        str: The book description as a single string. Returns an empty string if the description
        is not found or if there's an error during the request or parsing process.
    """

    book_url = f"https://openlibrary.org{key}"  # Construct the URL for the book on Open Library

    try:
        response = requests.get(book_url)  # Send a request to the Open Library website
        response.raise_for_status()  # Raises HTTPError for bad HTTP response

        soup = BeautifulSoup(response.content, 'html.parser')  # Parse the HTML content

        work_description = soup.find('div', {'class': 'work-description-content restricted-view'})
        # Check if work description is present
        if not work_description:
            return ""  # Return an empty string if the description is not found

        paragraphs = work_description.find_all('p')  # Extract all paragraph elements

        description = []
        for p in paragraphs:
            description.append(p.text.strip())  # Strip and append each paragraph's text
        description_str = ' '.join(description)  # Join all paragraph texts into a single string
        return description_str
    except:
        return ""  # Return an empty string in case of any exception during the process


def search_open_books(title, author=""):
    """
    Searches for books in the Open Books API using the provided title and author.

    This function constructs a query with the specified title and author (if provided),
    then sends an HTTP request to the Open Books API. The results are parsed and formatted
    into a list of dictionaries, each containing details about a book.

    Args:
        title (str): The title of the book to search for.
        author (str, optional): The author of the book to refine the search. Defaults to an empty string.

    Returns:
        list: A list of dictionaries, where each dictionary contains information about a book
        (title, author, release date, and key). Returns an empty list if no data is found or on error.

    Raises:
        tk.messagebox.showerror: Displays an error message box if the API request fails.
    """

    query = {"title": title, "fields": "key, title, author_name, first_publish_year"}  # Define query parameters
    if author:
        query["author"] = author  # Add author to the query if provided
    query["limit"] = 10  # Set the result limit to 10

    try:
        response = requests.get(OPEN_BOOKS_API_URL, params=query)  # Send the request to Open Books API
        response.raise_for_status()  # Check for HTTP errors

        data = response.json()  # Parse the JSON response
        if "docs" not in data:
            print("Unexpected data structure received from Open Books API.")  # Log unexpected data structure
            return []

        # Process and return the search results
        return [
            {
                "title": doc.get("title", ""),
                "author": ', '.join(doc.get("author_name", [])),
                "release_date": doc.get("first_publish_year", ""),
                "key": doc.get("key", ""),
            }
            for doc in data["docs"]
        ]
    except requests.RequestException as e:
        messagebox.showerror("Error", f"API Request failed: {e}")  # Display error message on request failure
        return []  # Return an empty list on error


def search_google_books(title, author=""):
    """
    Searches for books in the Google Books API using the provided title and optionally the author.

    This function constructs a URL for querying the Google Books API with the specified title and author,
    sends an HTTP request, and parses the response. The results are formatted into a list of dictionaries,
    each containing details about a book.

    Args:
        title (str): The title of the book to search for.
        author (str, optional): The author of the book to refine the search. Defaults to an empty string.

    Returns:
        list: A list of dictionaries, where each dictionary contains information about a book
        (title, author, release date, link, and ISBN). Returns an empty list if no data is found or on error.

    Raises:
        tk.messagebox.showerror: Displays an error message box if the API request fails.
    """

    book_title_encoded = urllib.parse.quote(title)  # URL-encode the book title
    author_name_encoded = urllib.parse.quote(author)  # URL-encode the author name
    google_api_url = f"{GOOGLE_BOOKS_API_BASE_URL}?q=intitle:{book_title_encoded}"  # Construct the API URL

    if author:
        google_api_url += f"+inauthor:{author_name_encoded}"  # Add author to the query if provided

    google_api_url += "&printType=books&maxResults=10"  # Append parameters for print type and max results

    try:
        response = requests.get(google_api_url)  # Send the request to Google Books API
        response.raise_for_status()  # Check for HTTP errors

        data = response.json()  # Parse the JSON response
        if "items" not in data:
            print("Unexpected data structure received from Google Books API.")  # Log unexpected data structure
            return []

        # Process and return the search results
        return [
            {
                "title": item.get("volumeInfo", {}).get("title", ""),
                "author": ', '.join(item.get("volumeInfo", {}).get("authors", [])),
                "release_date": item.get("volumeInfo", {}).get("publishedDate", ""),
                "link": item.get("volumeInfo", {}).get("infoLink", ""),
                "ISBN": item.get("volumeInfo", {}).get("industryIdentifiers", [{}])[0].get("identifier", ""), # CH
            }
            for item in data["items"]
        ]
    except requests.RequestException as e:
        messagebox.showerror("Error", f"API Request failed: {e}")  # Display error message on request failure
        return []  # Return an empty list on error


def get_book_info(title, author=""):
    """
    Fetches book data (excluding descriptions) from Google Books and Open Books APIs,
    returning a combined list of the top 3 unique books from each source.

    The function searches both APIs for books matching the title and author, removes duplicates,
    and limits the results to the top 3 unique entries from each API based on title and author.

    Args:
        title (str): The title of the book to search for.
        author (str, optional): The author of the book to refine the search. Defaults to an empty string.

    Returns:
        list: A combined list of dictionaries, each containing information about a book from
        either Google Books or Open Books APIs. Limited to the top 3 unique books from each source.
    """

    google_books = search_google_books(title, author)  # Fetch book data from Google Books API
    open_books = search_open_books(title, author)  # Fetch book data from Open Books API

    def remove_dups(books):
        """
        Helper function to remove duplicate books based on title and author.
        Limits the result to the top 3 unique books.

        Args:
            books (list): A list of book dictionaries.

        Returns:
            list: A list of unique book dictionaries.
        """
        seen = set()  # Set to keep track of seen (title, author) tuples
        unique_books = []  # List to store unique books
        for book in books:
            identifier = (book['title'], book['author'])  # Create a unique identifier for each book
            if identifier not in seen and len(unique_books) < 3:
                seen.add(identifier)  # Add identifier to seen set
                unique_books.append(book)  # Add book to unique list

        return unique_books

    # Apply duplicate removal to both API results and combine them
    google_books_nodup = remove_dups(google_books)
    open_books_nodup = remove_dups(open_books)
    return google_books_nodup + open_books_nodup


def show_book_selection_window(books):
    """
    Displays a window allowing the user to select a book from a list.

    This function creates a new window with buttons for each book in the provided list. Each button,
    when clicked, will trigger the on_book_selection function with the corresponding book's data.

    Args:
        books (list): A list of dictionaries, each containing information about a book.

    Note:
        Text in buttons will wrap if too long. The function assumes the existence of a Tkinter root window.
    """

    selection_window = tk.Toplevel(root)  # Create a new top-level window on the existing Tkinter root
    selection_window.title("Select a Book")
    selection_window.geometry("500x300")  # Set the window size

    # Create and place a title label in the window
    title_label = tk.Label(selection_window, text="Please select a book:", font=("Arial", 14))
    title_label.pack(pady=(10, 5))

    # Frame to contain book selection buttons
    buttons_frame = tk.Frame(selection_window)
    buttons_frame.pack(padx=10, pady=5, fill="both", expand=True)

    # Create a button for each book in the list
    for book in books:
        book_text = f"{book['title']} By {book['author']}"
        book_button = tk.Button(
            buttons_frame, 
            text=book_text, 
            command=lambda b=book: on_book_selection(b, selection_window),
            wraplength=450,  # Wrap text if it's too long
            justify="left",
            anchor="w"
        )
        book_button.pack(pady=2, padx=10, fill='x')  # Pack each button into the frame


def on_book_selection(book, window):
    """
    Handles the event when a book is selected from the selection window.

    Closes the selection window and displays detailed information about the selected book.

    Args:
        book (dict): A dictionary containing information about the selected book.
        window (tk.Toplevel): The selection window to be closed upon selection.
    """

    window.destroy()  # Close the selection window
    display_selected_book(book)  # Call function to display the selected book's details


def display_selected_book(book):
    """
    Displays the selected book's detailed information, including title, author, content warnings,
    and a clickable link for purchase. Also, calls a function to display the book's image if available.

    Args:
        book (dict): A dictionary containing information about the selected book.
    """

    clear_result()  # Clear existing content and any existing image

    # Display book title and author
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", "end")
    result_text.insert("1.0", f"Title: {book['title']}\nAuthor: {book['author']}\n")

    # Fetch and display book description and image URL (if available)
    description, img_url = "", ""
    if 'ISBN' in book and book['ISBN']:
        description, img_url = get_google_books_description_and_img_URL(book['ISBN'])
    elif 'key' in book and book['key']:
        description = get_open_books_description(book['key'])  # No image URL for open books

    # Display content warnings based on the book's description
    warnings = analyze_description(description) if description else []
    warning_text = ', '.join(warnings) if warnings else 'None'
    result_text.insert(tk.END, f"Content Warnings: {warning_text}\n")

    # Display a clickable purchase link (hyperlink) if available
    if 'link' in book and book['link']:
        hyperlink_text = "Click here to purchase!"
        result_text.insert(tk.END, hyperlink_text, "link")
        result_text.tag_config("link", foreground="blue", underline=1)
        result_text.tag_bind("link", "<Button-1>", lambda e: open_link(book['link']))

    result_text.config(state=tk.DISABLED)  # Disable editing of the text widget

    # Display book image if the URL is available
    if img_url:
        show_book_image(img_url)

def show_book_image(url):
    """
    Downloads and displays the book's cover image from the provided URL.

    The function sends a request to the given URL to fetch the image data. It then creates
    a thumbnail of the image and displays it in a label within the result_frame. Handles errors
    gracefully and prints an error message if the image fails to load.

    Args:
        url (str): The URL of the image to be displayed.
    """

    try:
        response = requests.get(url)  # Send request to download the image
        response.raise_for_status()  # Check for HTTP errors

        image_data = response.content  # Get image data from response
        image = Image.open(io.BytesIO(image_data))  # Open image from byte data
        image.thumbnail((100, 150), Image.Resampling.LANCZOS)  # Create a thumbnail of the image

        photo = ImageTk.PhotoImage(image)  # Convert image to PhotoImage for Tkinter

        # Clear any existing image labels in the result frame
        for widget in result_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        # Create and pack a new label with the image
        image_label = tk.Label(result_frame, image=photo)
        image_label.image = photo  # Keep a reference to prevent garbage collection
        image_label.pack()  # Display the label in the result frame
    except Exception as e:
        print(f"Failed to load image: {e}")  # Print error message if image loading fails


def search_book_ratings():
    """
    Initiates a search for books based on the entered title in the search field.

    This function retrieves the title from the book_title_entry widget, checks if it's not empty,
    and then calls get_book_info to fetch book data. It displays the book selection window if books
    are found or shows a message if no books are found.

    Globals:
        books (list): A global list to store book data.

    Note:
        This function makes use of a global 'books' variable to store the search results.
    """

    book_title = book_title_entry.get().strip()  # Get and strip the book title from the entry widget
    if not book_title:
        messagebox.showerror("Error", "Please enter a book title to search.")  # Show error if title is empty
        return

    global books  # Reference the global 'books' variable
    books = get_book_info(book_title)  # Fetch book data using the entered title

    if books:
        show_book_selection_window(books)  # Show book selection window if books are found
    else:
        messagebox.showinfo("No Results", "No books found with that title.")  # Inform if no books are found


def clear_result():
    """
    Clears the displayed results in the text widget and the book title entry field.

    This function is used to reset the content of the result text widget and the book title
    entry field, essentially clearing previous search results and inputs. It makes the text
    widget temporarily editable to clear its contents and then disables it again to prevent
    user edits.
    """

    result_text.config(state=tk.NORMAL)  # Enable editing of the result text widget
    result_text.delete("1.0", "end")  # Clear all content from the result text widget
    result_text.config(state=tk.DISABLED)  # Disable editing of the result text widget

    book_title_entry.delete(0, tk.END)  # Clear the content of the book title entry field


def open_link(url):
    """
    Opens a URL in the user's default web browser.

    This function is typically used for opening a hyperlink clicked by the user, such as a link
    to a book's purchase page. It uses the webbrowser module to open the URL in the default browser.

    Args:
        url (str): The URL to be opened in the web browser.
    """

    webbrowser.open_new(url)  # Open the URL in a new window of the default browser

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
# Create the tkinter main window
root = tk.Tk()
root.title("Book Content Warnings")
root.geometry("600x400")  # Set the initial window size

# Create a label to provide instructions for the user
instructions_label = tk.Label(root, text="Enter a book title to search.")
instructions_label.pack()

# Create a label and entry widget for inputting the book title
book_title_label = tk.Label(root, text="Book Title:")
book_title_label.pack()
book_title_entry = tk.Entry(root, width=50)  # Wide entry field for book title input
book_title_entry.pack()

# Create a button to initiate the search for book content warning ratings
search_button = tk.Button(root, text="Search Content Warning Rating", command=search_book_ratings)
search_button.pack()

# Create a frame to group the result display components
result_frame = tk.Frame(root)
result_frame.pack(pady=10, fill='both', expand=True)  # Padded and set to fill available space

# Create a label to indicate the book information display area
result_label = tk.Label(result_frame, text="Book Information:")
result_label.pack()

# Create a text widget for displaying the book information along with content warning rating
result_text = tk.Text(result_frame, width=50, height=10, wrap=tk.WORD, state=tk.DISABLED)
result_text.pack()  # Text widget is initially disabled for editing

# Create a button to clear the displayed result
clear_button = tk.Button(root, text="Clear Result", command=clear_result)
clear_button.pack()

# Create a frame to display the book image with a fixed minimum height
image_frame = tk.Frame(root, height=150)
image_frame.pack_propagate(False)  # Prevents the frame from shrinking smaller than its contents
image_frame.pack(pady=10, fill='both', expand=True)  # Padded and set to fill available space

# Error handling: wrap the main event loop in a try-except block
try:
    root.mainloop()  # Start the Tkinter event loop
except Exception as e:
    messagebox.showerror("Unexpected Error", str(e))  # Show an error message in case of exceptions