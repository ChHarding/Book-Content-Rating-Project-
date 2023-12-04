import tkinter as tk
from tkinter import messagebox, Listbox, Label, Button, Entry, Frame, Text
import requests
import urllib.parse
from fuzzywuzzy import fuzz
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
    Analyzes the description of a book and returns warnings if any keywords are found.
    """
    warnings = []
    for warning_name, warning_keywords in KEYWORD_WARNINGS.items():
        for keyword in warning_keywords:
            if keyword in description.lower() or fuzz.partial_ratio(keyword, description.lower()) > threshold:
                warnings.append(warning_name)
                break
    return warnings

def get_google_books_description_and_img_URL(ISBN):

    google_api_url = f"{GOOGLE_BOOKS_API_BASE_URL}?q=isbn:{ISBN}"

    try:
        response = requests.get(google_api_url)
        response.raise_for_status()  # Raises HTTPError for bad HTTP response
    except requests.RequestException as e:
        messagebox.showerror("Error", f"API Request failed: {e}")
        return "", ""

    data = response.json()
    if "items" not in data:
        print("Unexpected data structure received from Google Books API.")
        return []
    
    try:
        # get description
        description = data["items"][0]["volumeInfo"]["description"]

        # get image url
        image_url = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
        return description, image_url
    except:
        return "", ""

def get_open_books_description(key):
    '''Attempts to get description for an open books key. Returns "" on fail
    '''
    book_url = f"https://openlibrary.org{key}"  
    try:
        response = requests.get(book_url)
        response.raise_for_status()
         
        soup = BeautifulSoup(response.content, 'html.parser')
        work_description = soup.find('div', {'class': 'work-description-content restricted-view'})
        paragraphs = work_description.find_all('p')
    except:
        return "" 

    description = []
    for p in paragraphs:
        description.append(p.text.strip())
    description_str = ' '.join(description)
    return description_str

def search_open_books(title, author=""):
    """
    Search for books in the Open Books API and return a list of results.
    Handles HTTP errors and unexpected data structures gracefully.
    """
    query = {"title": title, "fields": "key, title, author_name, first_publish_year"}
    if author:
        query["author"] = author
    query["limit"] = 10
    try:
        response = requests.get(OPEN_BOOKS_API_URL, params=query)
        response.raise_for_status()
        data = response.json()
        if "docs" not in data:
            print("Unexpected data structure received from Open Books API.")
            return []
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
        messagebox.showerror("Error", f"API Request failed: {e}")
        return []

def search_google_books(title, author=""):
    """
    Search for books in the Google Books API and return a list of results.
    Handles HTTP errors and unexpected data structures gracefully.
    """
    book_title_encoded = urllib.parse.quote(title)
    author_name_encoded = urllib.parse.quote(author)
    google_api_url = f"{GOOGLE_BOOKS_API_BASE_URL}?q=intitle:{book_title_encoded}"
    if author:
        google_api_url += f"+inauthor:{author_name_encoded}"
    google_api_url += "&printType=books&maxResults=10"

    try:
        response = requests.get(google_api_url)
        response.raise_for_status()  # Raises HTTPError for bad HTTP response
        data = response.json()
        if "items" not in data:
            print("Unexpected data structure received from Google Books API.")
            return []

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
        messagebox.showerror("Error", f"API Request failed: {e}")
        return []

def get_book_info(title, author=""):
    """
    Fetches book data (not including the description!) using Google Books and Open Books APIs,
    and returns a combined list of the top 3 unique books from each.
    """
    google_books = search_google_books(title, author)
    open_books = search_open_books(title, author)

    def remove_dups(books):
        # Remove duplicates based on title and author, and limit to top 3 unique results
        seen = set()
        unique_books = []
        for book in books:
            identifier = (book['title'], book['author'])
            if identifier not in seen and len(unique_books) < 3:
                seen.add(identifier)
                unique_books.append(book)

        return unique_books

    google_books_nodup = remove_dups(google_books)
    open_books_nodup = remove_dups(open_books)
    return google_books_nodup + open_books_nodup

def show_book_selection_window(books):
    """
    Shows a window to select a book from the given list with each book option as its own button.
    Text in buttons will wrap if too long.
    """
    selection_window = tk.Toplevel(root)
    selection_window.title("Select a Book")
    selection_window.geometry("500x300")  # Adjust the size as needed

    # Title label
    title_label = tk.Label(selection_window, text="Please select a book:", font=("Arial", 14))
    title_label.pack(pady=(10, 5))

    # Frame for buttons
    buttons_frame = tk.Frame(selection_window)
    buttons_frame.pack(padx=10, pady=5, fill="both", expand=True)

    for book in books:
        book_text = f"{book['title']} By {book['author']}"
        book_button = tk.Button(
            buttons_frame, 
            text=book_text, 
            command=lambda b=book: on_book_selection(b, selection_window),
            wraplength=450,  # Adjust the wraplength as needed
            justify="left",
            anchor="w"
        )
        book_button.pack(pady=2, padx=10, fill='x')

def on_book_selection(book, window):
    """
    Handles the selection of a book when a book button is clicked.
    """
    window.destroy()
    display_selected_book(book)

def display_selected_book(book):
    """
    Displays the selected book's detailed information, including title, author, content warning,
    and clickable purchase link. Calls function to display book photo.
    """
    # Clear existing content and any existing image
    clear_result()

    # Display the detailed information in the text widget
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", "end")
    result_text.insert("1.0", f"Title: {book['title']}\nAuthor: {book['author']}\n")

    # get descriptions
    description = ""
    img_url = ""
    if 'ISBN' in book and book['ISBN']:
        description, img_url = get_google_books_description_and_img_URL(book['ISBN'])
    elif 'key' in book and book['key']:
        description = get_open_books_description(book['key']) # no img URL for open books

    # Fetch and display content warnings
    warnings = analyze_description(description) if description else []
    warning_text = ', '.join(warnings) if warnings else 'None'
    result_text.insert(tk.END, f"Content Warnings: {warning_text}\n")

    # Display clickable purchase link (hyperlink) if available
    if 'link' in book and book['link']:
        hyperlink_text = "Click here to purchase!"
        result_text.insert(tk.END, hyperlink_text, "link")
        result_text.tag_config("link", foreground="blue", underline=1)
        result_text.tag_bind("link", "<Button-1>", lambda e: open_link(book['link']))

    result_text.config(state=tk.DISABLED)

    # Show book image if the URL is available
    if img_url:
        show_book_image(img_url)

def show_book_image(url):
    """
    Downloads and displays the book's cover image from the given URL in the result_frame.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((100, 150), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Clear any existing image labels
        for widget in result_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        # Create a label for the image and display it
        image_label = tk.Label(result_frame, image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection
        image_label.pack()
    except Exception as e:
        print(f"Failed to load image: {e}")

def search_book_ratings():
    """
    Searches for books based on the given title and displays selection window.
    """
    book_title = book_title_entry.get().strip()
    if not book_title:
        messagebox.showerror("Error", "Please enter a book title to search.")
        return

    global books # ;(
    books = get_book_info(book_title)
    if books:
        show_book_selection_window(books)
    else:
        messagebox.showinfo("No Results", "No books found with that title.")

def clear_result():
    """
    Clears the result text and entry fields.
    """
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", "end")
    result_text.config(state=tk.DISABLED)
    book_title_entry.delete(0, tk.END)

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
root.geometry("600x400")  # Adjust the size as necessary

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
result_frame.pack(pady=10, fill='both', expand=True)

# Create label for book information
result_label = tk.Label(result_frame, text="Book Information:")
result_label.pack()

# Create a text widget for displaying book information with content warning rating and author
result_text = tk.Text(result_frame, width=50, height=10, wrap=tk.WORD, state=tk.DISABLED)
result_text.pack()

clear_button = tk.Button(root, text="Clear Result", command=clear_result)
clear_button.pack()

# Create a frame for displaying the book image with a minimum size
image_frame = tk.Frame(root, height=150)
image_frame.pack_propagate(False)  # Prevents the frame from shrinking to fit its contents
image_frame.pack(pady=10, fill='both', expand=True)

# Error handling: wrap the mainloop in a try-except to catch any unexpected exceptions
try:
    root.mainloop()
except Exception as e:
    messagebox.showerror("Unexpected Error", str(e))
