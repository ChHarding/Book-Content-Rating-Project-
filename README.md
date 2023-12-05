# User Guide
## Book Content Rating Project
HCI 584 - By Miranda Frederick 

## About 
The purpose of this program is to provide users with content warnings for books. Nine content areas are evaluated for each book searched by the user (listed below). If the content is present in the book information within the search engine, the category is included in the warning section of the search results. To assist with accuracy, after searching for a title, users are presented with a list of search results to choose from. Once they select the correct book, users receive the book description, author name, appropriate content warnings, a photo of the book cover, and a link to purchase the book online in the search results box. All information is subject to availability. 

## Program Requirements
### Python Version:
Python 3.7 or higher. This is essential as the syntax and libraries used may not be compatible with older versions.

### External Libraries:
#### 'requests': 
This library is used for making HTTP requests to APIs.

#### Pillow (PIL): 
Required for image processing tasks, particularly for handling book cover images.

#### tkinter: 
Should be available by default in Python for GUI creation. If not, it might need separate installation depending on the operating system.

#### fuzzywuzzy: 
Used for string matching operations.

#### beautifulsoup4: 
Necessary for HTML parsing when fetching data from websites.

#### python-Levenshtein: 
An optional but recommended dependency for fuzzywuzzy for faster string matching.


## Program Installation
Prior to using, the environment needs to be set up to run the program. 

### First, Install Python:
Ensure Python 3.7 or higher is installed on your system. You can download it from the official Python website.

### Second, Install Required Libraries:
Open a terminal or command prompt.
Navigate to the project's root directory.
Run the following command to install all required packages:

pip install requests Pillow fuzzywuzzy beautifulsoup4 python-Levenshtein


## How to Use
### Getting Started With APIs
#### What is an API?

API stands for Application Programming Interface. It allows your application to interact with an external service using a set of rules and protocols. In the case of web APIs, these interactions are usually made through HTTP requests.
Understanding API Requests and Responses

APIs communicate using requests (from your program) and responses (from the API server). Common types of requests include GET (retrieve data), POST (send new data), PUT (update data), and DELETE (remove data).
JSON Format

Most APIs return data in JSON (JavaScript Object Notation) format, which is easy to read and parse in Python using the json library.

### Basic Examples
#### Making a Simple API Request
Start with a basic GET request to fetch data. For example, retrieving a book's information from Google Books API:

import requests

response = requests.get("https://www.googleapis.com/books/v1/volumes?q=title:1984")
book_data = response.json()
print(book_data)

#### Parsing API Responses
Learn to parse JSON responses to extract useful information:

title = book_data['items'][0]['volumeInfo']['title']
authors = book_data['items'][0]['volumeInfo']['authors']
print(f"Title: {title}, Authors: {authors}")

#### Using Parameters with API Requests
Make a more complex request by adding parameters to your API call:

params = {
    'q': 'title:To Kill a Mockingbird',
    'maxResults': 2
}
response = requests.get("https://www.googleapis.com/books/v1/volumes", params=params)
data = response.json()
for book in data['items']:
    print(book['volumeInfo']['title'])

#### Handling API Errors
It's important to handle potential errors in API requests:

if response.status_code == 200:
    # Process successful response
else:
    print(f"Error: {response.status_code}")

### API Tips for Beginners
#### Read the API Documentation: 
Before using any API, read its documentation to understand its usage limits, available endpoints, required parameters, and the data format it returns.

#### Experiment in Small Steps: 
Start with simple requests, understand the response, and then gradually add more complexity like error handling, headers, and query parameters.

#### Use API Testing Tools: 
Tools like Postman can be helpful for testing API requests and responses before coding them.

### How to Run This Application 
#### Installing Python:
1. Download Python: Visit the official Python website and download the latest version of Python (at least Python 3.7 or higher).
2. Run Installer: Open the downloaded installer. Ensure you check the option "Add Python 3.x to PATH" to make Python accessible from the command line.
3. Verify Installation: Open your command line (Command Prompt on Windows, Terminal on macOS and Linux) and type python --version. You should see the Python version number if the installation was successful.
   
#### Setting Up a Development Environment:
1. Choose an IDE/Editor: While you can use any text editor, an Integrated Development Environment (IDE) like PyCharm, Visual Studio Code, or Thonny can be more helpful. These IDEs provide features like syntax highlighting, code completion, and easier debugging.
2. Install an IDE: Download and install your chosen IDE following the instructions on its respective website.

##### Note:
Ensure that the working directory (the directory from which you run the script) is the root folder of the project. This is important for the script to correctly locate and import any dependencies or additional modules.

Internet Connection: Ensure you have an active internet connection during the installation process.

Permission Issues: If you encounter permission errors on macOS or Linux, try adding sudo at the beginning of the installation command. On Windows, run the command prompt as an administrator.

Python PATH: If Python commands aren’t recognized, it’s likely an issue with the PATH environment variable. Revisit the Python installer and ensure you select the option to add Python to PATH.

For more advanced configuration or troubleshooting, please refer to the developer's guide or contact the creator for support. 


## Known Issues
### Common Errors and Fixes
#### API Connection Failure:
Error Message: "API Request failed"
Fix: Check internet connection. Ensure that the API service (Google Books, Open Library) is not down. If using a developer key, verify that it is valid and has not exceeded its usage limits.

#### Unexpected Data Structure from API:
Error Message: "Unexpected data structure received from [API Name]"
Fix: This is likely due to changes in the API's response format. Users should report this issue for further investigation.

#### Image Loading Failure:
Error Message: Printed in the console, not shown to the user directly.
Fix: Verify the internet connection. If the issue persists, the problem might be with the image source or URL format.

#### No Books Found:
Error Message: "No books found with that title."
Fix: Ensure the book title is correctly spelled. Try including the author's name for a more precise search.

### Caveats and Limitations
#### Rate Limiting: 
Both APIs may have rate limits. Excessive requests in a short period might temporarily block access.

#### Incomplete Data: 
Sometimes, the APIs might return incomplete data (e.g., missing author or publication year).

#### No Image URLs: 
Open Library API may not always provide image URLs for book covers.

## Awknowledgements 

Thank you to our professor, Chris Harding, for his guidance and assistance throughout the semester on my first Python project. In addition, thank you to the friends who acted as testers for me throughout the semester and acted as my first users!
