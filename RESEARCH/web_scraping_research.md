# Research Report
Web Scraping Government Website
### Summary of Work
I looked through old notes from CS 220 and CS 320 about web scraping, including BeautifulSoup and Selenium, and how to use these tools in order to navigate a website and extract the contents of the website. I also looked up youtube videos and old projects with examples of how they worked (including specific methods used), and the output of those code chunks. BeautifulSoup and Selenium also have documentation that I read through that explained more in detail about some of the functions we can use to navigate the web.
### Motivation
Our project is meant to scrape the government website provided to us for the stock trade information that we will be using to populate our database and display for on our application. Relates to #35.
### Time Spent
300 minutes (about 270 minutes doing research, roughly 30 minutes writing this report)
### Results

##### BeautifulSoup
BeautifulSoup is a Python library used for parsing HTML and XML documents. It creates a parse tree for parsed pages and provides Pythonic methods for searching, navigating, and modifying the parse tree.

Strengths:
- Fast and lightweight for static HTML scraping
- Easy-to-use API for navigating the document tree
- Supports different parsers

Limitations:
- Can't handle dynamic JavaScript content (requires a fully-rendered page)
- Not designed for interacting with web forms, handling cookies, or controlling the browser (that's where Selenium comes in)

##### Selenium
Selenium is a tool for browser automation. It lets you interact with web pages, simulates user behavior, and extracts dynamic content that you wouldn't be able to do with other scraping tools

Strengths:
- Handles JavaScript-rendered content by simulating a full web browser (like Chrome)
- Can interact with forms, buttons, and other page elements like a normal person would
- Useful for scraping websites where content is loaded dynamically or when you need to interact with the website in order to load data.

Limitations:
- Slower than using libraries like BeautifulSoup alone, since it renders entire web pages
- Requires a WebDriver for specific browsers
- More resource-intensive since it simulates a browser

### How Web Scraping Works
Web scraping using Selenium and BeautifulSoup generally follows these steps:

1. Accessing the Website
- Selenium uses WebDrivers to simulate a real user accessing a webpage.
- After loading the page, Selenium can perform actions like clicking buttons, submitting forms, or scrolling
2. Extracting HTML Content
- Once the webpage is fully loaded (including JavaScript content), Selenium can capture the full page source (HTML) and pass it to BeautifulSoup for parsing.
3. Parsing HTML with BeautifulSoup
- BeautifulSoup parses the static or dynamic HTML provided by Selenium.
- It offers methods like find(), find_all(), or CSS selectors for extracting elements like headings, paragraphs, links, tables, etc.
- These elements are what we are going to either be storing inside of our database or interacting with to naviagte to the page we want where the information is located
4. Data Extraction and Storage
- The extracted data is cleaned and structured.
- The data can be stored in various formats, such as CSV, JSON, or directly into databases like MySQL or MongoDB (in our case we're going to be directly putting the info into the database).

### Sources
<!--list your sources and link them to a footnote with the source url-->
- BeautifulSoup[^1]
- Selenium[^2]
- CS 320 Gitlab Folder about Selenium[^3]
- CS 220 Website containing BeautifulSoup Lecture[^4]
- CS 220 BeautifulSoup lecture files[^5]
[^1]: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
[^2]: https://selenium-python.readthedocs.io/getting-started.html#simple-usage
[^3]: https://git.doit.wisc.edu/cdis/cs/courses/cs320/s24/-/blob/main/lecture_material/11-web-1
[^4]: https://cs220.cs.wisc.edu/f23/schedule.html
[^5]: https://canvas.wisc.edu/courses/374263/files/folder/Mikes_Lecture_Notes/Lec31_Web_3

