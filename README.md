# User Guide
## Book Content Rating Project
HCI 584 - By Miranda Frederick 

## Program Requirements

## Program Installation

## How to Use
### Getting Started With APIs
What is an API?

API stands for Application Programming Interface. It allows your application to interact with an external service using a set of rules and protocols. In the case of web APIs, these interactions are usually made through HTTP requests.
Understanding API Requests and Responses

APIs communicate using requests (from your program) and responses (from the API server). Common types of requests include GET (retrieve data), POST (send new data), PUT (update data), and DELETE (remove data).
JSON Format

Most APIs return data in JSON (JavaScript Object Notation) format, which is easy to read and parse in Python using the json library.

### Basic Examples


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
