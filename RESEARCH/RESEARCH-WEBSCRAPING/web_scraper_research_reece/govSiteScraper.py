import os
import random
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Paths to the Chrome binary and ChromeDriver
script_dir = os.path.dirname(os.path.realpath(__file__))
chrome_binary_path = os.path.join(
    script_dir,
    "chrome/mac_arm-129.0.6668.100/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")
chrome_driver_path = os.path.join(
    script_dir,
    "chromedriver/mac_arm-129.0.6668.100/chromedriver-mac-arm64/chromedriver")

# Set up Chrome options
chrome_options = Options()
chrome_options.binary_location = chrome_binary_path
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
]
chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

# Initialize WebDriver
driver = webdriver.Chrome(
    service=ChromeService(
        executable_path=chrome_driver_path),
    options=chrome_options)

# Simulate human behavior with random delays


def human_delay(min_delay=2, max_delay=5):
    time.sleep(random.uniform(min_delay, max_delay))

# Scroll to simulate human interaction


def human_scroll(driver):
    scroll_pause_time = random.uniform(0.5, 1.5)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Simulate mouse movement to a specific element


def simulate_mouse_move(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()

# Scrape politician's name from the report


def scrape_politician_name(soup):
    # Look for the <h2> tag with the class 'filedReport'
    h2_tag = soup.find('h2', class_='filedReport')
    if h2_tag:
        # Extract the name in parentheses
        name_start = h2_tag.text.find('(')
        name_end = h2_tag.text.find(')')
        if name_start != -1 and name_end != -1:
            return h2_tag.text[name_start + 1:name_end].strip()
    return "Unknown"

# Scrape report links using BeautifulSoup


def scrape_report_links_from_html(html_content):
    # Base URL for relative links
    base_url = "https://efdsearch.senate.gov"

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    report_links = []
    # Find all <a> tags within <td> tags that have the href attribute
    for a_tag in soup.select('td a[href]'):
        relative_link = a_tag['href']  # Get the href attribute (relative link)
        full_link = base_url + relative_link  # Combine base URL with relative link
        report_links.append(full_link)

    # Write the links to a file
    with open('report_links.txt', 'w') as file:
        for link in report_links:
            file.write(link + '\n')

    return report_links

# Function to scrape stock transactions from each report page


def scrape_transactions(report_url):
    driver.get(report_url)
    human_delay(2, 5)
    human_scroll(driver)

    # Get the page source for BeautifulSoup parsing
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Scrape the politician's name
    politician_name = scrape_politician_name(soup)

    wait = WebDriverWait(driver, 20)
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        rows = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        transactions = []
        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, 'td')
                transaction_data = {
                    'Politician': politician_name,  # Add politician's name here
                    'Transaction Date': cells[1].text,
                    'Owner': cells[2].text,
                    'Ticker': cells[3].text,
                    'Asset Name': cells[4].text,
                    'Asset Type': cells[5].text,
                    'Transaction Type': cells[6].text,
                    'Amount': cells[7].text,
                    'Comment': cells[8].text if len(cells) > 8 else "--"
                }
                transactions.append(transaction_data)
            except NoSuchElementException:
                print("Error extracting data from a row.")
        return transactions
    except TimeoutException:
        print("Timed out waiting for the transactions table to load.")
        return None

# Function to scrape report links and stock trades for periodic
# transaction reports


def scrape_report_links_and_transactions(search_url, from_date, to_date):
    driver.get(search_url)
    wait = WebDriverWait(driver, 20)

    try:
        wait.until(EC.presence_of_element_located((By.ID, 'agree_statement')))
        agree_checkbox = driver.find_element(By.ID, 'agree_statement')
        if not agree_checkbox.is_selected():
            agree_checkbox.click()
        human_delay(1, 3)

        # Select periodic transaction report checkbox
        periodic_checkbox = driver.find_element(
            By.CSS_SELECTOR, 'input[value="11"]')
        if not periodic_checkbox.is_selected():
            periodic_checkbox.click()

        from_date_element = driver.find_element(By.ID, 'fromDate')
        to_date_element = driver.find_element(By.ID, 'toDate')

        from_date_element.clear()
        from_date_element.send_keys(from_date)
        to_date_element.clear()
        to_date_element.send_keys(to_date)

        human_delay(2, 4)
        submit_button = driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]')
        simulate_mouse_move(driver, submit_button)
        submit_button.click()
        human_scroll(driver)

        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))

        # Get the page source and extract links using BeautifulSoup
        page_source = driver.page_source
        report_links = scrape_report_links_from_html(page_source)

        all_transactions = []
        for link in report_links:
            transactions = scrape_transactions(link)
            if transactions:
                all_transactions.extend(transactions)

        # Save to a file
        transactions_file_path = os.path.join(
            script_dir, "stock_transactions.txt")
        with open(transactions_file_path, "w") as file:
            for transaction in all_transactions:
                file.write(f"{transaction}\n")

        return all_transactions
    except TimeoutException:
        print("Timed out waiting for search form or results.")
        return None


# Main Execution Flow
search_url = "https://efdsearch.senate.gov/search/home/"
from_date = "10/02/2024"
to_date = "10/09/2024"

# Scrape stock transactions using Selenium
transactions_data = scrape_report_links_and_transactions(
    search_url, from_date, to_date)

# Close the browser after scraping
driver.quit()

# Print extracted transactions
if transactions_data:
    for transaction in transactions_data:
        print(transaction)
