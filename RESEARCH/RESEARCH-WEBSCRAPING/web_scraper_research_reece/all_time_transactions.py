import csv
import logging
import os
import random
import re
import time
import uuid
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Ensure log and output directory exists
LOG_DIRECTORY = 'web_scraper'
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

# Set up logging to both file and console
logger = logging.getLogger('all_time_scrape')
logger.setLevel(logging.INFO)

# Create file handler which logs even debug messages
fh = logging.FileHandler(os.path.join(LOG_DIRECTORY, 'all_time_scrape.log'))
fh.setLevel(logging.INFO)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handlers to logger
logger.addHandler(fh)
logger.addHandler(ch)


def setup_driver():
    """
    Set up and return a Selenium WebDriver with specified options.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run headless for automation
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    # Optional: Randomize user-agent for stealth
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        " AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64)"
        " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0)"
        " Gecko/20100101 Firefox/89.0",
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

    # Using webdriver_manager to automatically handle the driver
    try:
        service = ChromeService(ChromeDriverManager().install())
        web_driver = webdriver.Chrome(service=service, options=chrome_options)
        return web_driver
    except WebDriverException as e:
        logger.error("Error setting up WebDriver: %s", e)
        raise


def human_delay(min_delay=2, max_delay=5):
    """
    Simulate human-like delay between actions.
    """
    time.sleep(random.uniform(min_delay, max_delay))


def scrape_report_links_from_html(html_content):
    """
    Parse HTML content and extract all report links.
    """
    base_url = "https://efdsearch.senate.gov"
    soup = BeautifulSoup(html_content, 'html.parser')
    report_links = []

    for a_tag in soup.select('td a[href]'):
        relative_link = a_tag['href']
        full_link = base_url + relative_link
        report_links.append(full_link)

    return report_links


def clean_senator_name(raw_name):
    """
    Clean and parse the senator's name into first name, middle initial, and last name.
    """
    # Remove titles like "The Honorable" from the beginning
    raw_name = re.sub(
        r'^(The Honorable\s+)',
        '',
        raw_name,
        flags=re.IGNORECASE).strip()

    # Remove any text in parentheses (e.g., "(Former Senator)")
    name_without_parentheses = re.sub(r'\([^)]*\)', '', raw_name).strip()

    # Split the name into parts
    name_parts = name_without_parentheses.strip().split()

    # Assign first name, middle initial, and last name
    if len(name_parts) >= 3:
        first_name = name_parts[0]
        middle_initial = name_parts[1][0] if len(name_parts[1]) == 1 else ''
        last_name = ' '.join(name_parts[2:])
    elif len(name_parts) == 2:
        first_name = name_parts[0]
        middle_initial = ''
        last_name = name_parts[1]
    else:
        first_name = name_parts[0] if name_parts else ''
        middle_initial = ''
        last_name = ''

    return first_name.strip(), middle_initial.strip(), last_name.strip()


def parse_asset_details(asset_name_field):
    """
    Parse the 'Asset Name' field and extract asset details.
    """
    details = {}
    # Split the field by newlines
    lines = asset_name_field.strip().split('\n')
    # The first line is the Asset Name
    details['Asset Name'] = lines[0].strip()
    for line in lines[1:]:
        line = line.strip()
        # Match Rate/Coupon
        rate_match = re.match(r'Rate/Coupon:\s*(.+)', line)
        if rate_match:
            details['Rate/Coupon'] = rate_match.group(1)
        # Match Matures
        matures_match = re.match(r'Matures:\s*(.+)', line)
        if matures_match:
            details['Maturity Date'] = matures_match.group(1)
        # Match Company
        company_match = re.match(r'Company:\s*(.+)', line)
        if company_match:
            details['Company'] = company_match.group(1)
        # Match Description
        description_match = re.match(r'Description:\s*(.+)', line)
        if description_match:
            details['Description'] = description_match.group(1)
    return details


def parse_amount_range(amount_str):
    """
    Parse the 'Amount' field and return minimum and maximum amounts.
    """
    # Remove '$' and commas
    amount_str = amount_str.replace('$', '').replace(',', '')
    # Split by ' - ' to get min and max
    if ' - ' in amount_str:
        min_amount_str, max_amount_str = amount_str.split(' - ')
        try:
            min_amount = int(min_amount_str)
            max_amount = int(max_amount_str)
        except ValueError:
            min_amount = max_amount = 0
    else:
        try:
            min_amount = max_amount = int(amount_str)
        except ValueError:
            min_amount = max_amount = 0
    return min_amount, max_amount


def scrape_transactions(web_driver, report_url):
    """
    Scrape stock transactions from a single report page.
    """
    try:
        web_driver.get(report_url)
        human_delay(2, 5)

        # Wait for the table to appear on the page
        wait = WebDriverWait(web_driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        page_source = web_driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract senator's name and clean it
        senator_name_tag = soup.find('h2', class_='filedReport')
        raw_senator_name = senator_name_tag.get_text(
            separator=' ', strip=True) if senator_name_tag else "Unknown"
        first_name, middle_initial, last_name = clean_senator_name(
            raw_senator_name)

        # Ensure proper capitalization
        first_name = first_name.title()
        middle_initial = middle_initial.upper()
        last_name = last_name.title()

        rows = web_driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        transactions = []

        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, 'td')

                # Parse Ticker
                ticker_text = cells[3].text.strip()
                if ticker_text == '--':
                    ticker = None
                else:
                    ticker = [
                        t.strip() for t in re.split(
                            r'[\n,]+', ticker_text)]
                    if len(ticker) == 1:
                        ticker = ticker[0]

                # Parse Transaction Date
                transaction_date_str = cells[1].text.strip()
                transaction_date = datetime.strptime(
                    transaction_date_str, '%m/%d/%Y').strftime('%Y-%m-%d')

                # Parse Amount
                amount_str = cells[7].text.strip()
                min_amount, max_amount = parse_amount_range(amount_str)

                # Parse Asset Details
                asset_details = parse_asset_details(cells[4].text)

                # Standardize Asset Type
                raw_asset_type = cells[5].text.strip()
                asset_type_mapping = {
                    'Municipal Security': 'Municipal Security',
                    'Non-Public Stock': 'Private Stock',
                    'Other Securities': 'Other Securities',
                    'Stock': 'Stock',
                    # Add other mappings as needed
                }
                standardized_asset_type = asset_type_mapping.get(
                    raw_asset_type, raw_asset_type)

                # Generate Transaction ID
                transaction_id = str(uuid.uuid4())

                transaction_data = {
                    'Transaction ID': transaction_id,
                    'First Name': first_name,
                    'Middle Initial': middle_initial,
                    'Last Name': last_name,
                    'Transaction Date': transaction_date,
                    'Owner': cells[2].text.strip().title(),
                    'Ticker': ticker,
                    'Asset Type': standardized_asset_type,
                    'Transaction Type': cells[6].text.strip(),
                    'Amount Range': amount_str,
                    'Amount Min': min_amount,
                    'Amount Max': max_amount,
                    'Comment': cells[8].text.strip() if len(cells) > 8 else "--"}

                # Update with asset details
                transaction_data.update(asset_details)

                transactions.append(transaction_data)
            except (NoSuchElementException, ValueError) as e:
                logger.error(
                    "Error extracting data from row in %s: %s", report_url, e)

        return transactions
    except TimeoutException:
        logger.info(
            "No table found on %s. Skipping page (likely image-based content).",
            report_url)
        return []
    except WebDriverException as e:
        logger.error("WebDriver error while scraping %s: %s", report_url, e)
        return []


def apply_filters(web_driver):
    """
    Apply filters on the search page for scraping.
    """
    try:
        # Agree to statement checkbox
        agree_checkbox = web_driver.find_element(By.ID, 'agree_statement')
        if not agree_checkbox.is_selected():
            agree_checkbox.click()
        human_delay(1, 3)

        # Select periodic transaction report checkbox
        periodic_checkbox = web_driver.find_element(
            By.CSS_SELECTOR, 'input[value="11"]')
        if not periodic_checkbox.is_selected():
            periodic_checkbox.click()

        # Set the date range filter (from 01/01/2012 to today)
        from_date_element = web_driver.find_element(By.ID, 'fromDate')
        to_date_element = web_driver.find_element(By.ID, 'toDate')

        from_date_element.clear()
        from_date_element.send_keys("01/01/2012")
        to_date_element.clear()
        to_date_element.send_keys("")

        # Submit the form
        submit_button = web_driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        human_delay(2, 4)
    except (NoSuchElementException, WebDriverException) as e:
        logger.error("Error applying filters: %s", e)


def scrape_all_transactions(web_driver, search_url):
    """
    Scrape all stock transactions from the search URL with pagination.
    """
    try:
        web_driver.get(search_url)
        apply_filters(web_driver)

        all_report_links = []
        current_page = 1

        while True:
            logger.info("Collecting report links from page %s...", current_page)

            # Wait for the report table to load
            wait = WebDriverWait(web_driver, 30)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))

            # Scrape the report links from the page
            page_source = web_driver.page_source
            report_links = scrape_report_links_from_html(page_source)
            logger.info("Found %s report links on page %s.", len(report_links), current_page)
            all_report_links.extend(report_links)

            # Find the pagination element
            try:
                next_button = web_driver.find_element(By.ID, 'filedReports_next')
                if 'disabled' in next_button.get_attribute('class'):
                    logger.info("Reached last page. Stopping pagination.")
                    break
                else:
                    web_driver.execute_script("arguments[0].click();", next_button)
                    logger.info(
                        "Clicked 'Next' button. Moving to page %s...",
                        current_page + 1)
                    human_delay(2, 5)
                    current_page += 1
            except NoSuchElementException:
                logger.error("'Next' button not found on page %s.", current_page)
                break
            except WebDriverException as e:
                logger.error(
                    "Error during pagination on page %s: %s", current_page, e)
                break

        logger.info("Total reports collected: %s", len(all_report_links))

        # Now, process each report link
        all_transactions = []
        unique_transactions = set()

        for index, link in enumerate(all_report_links, start=1):
            logger.info("Scraping report %s/%s: %s", index, len(all_report_links), link)
            transactions = scrape_transactions(web_driver, link)
            if transactions:
                for transaction in transactions:
                    # Create a unique key for the transaction
                    transaction_key = (
                        transaction['First Name'],
                        transaction['Last Name'],
                        transaction['Transaction Date'],
                        transaction.get('Asset Name', ''),
                        transaction['Transaction Type'],
                        transaction['Amount Range']
                    )
                    if transaction_key not in unique_transactions:
                        unique_transactions.add(transaction_key)
                        all_transactions.append(transaction)
                    else:
                        logger.info("Duplicate transaction found: %s", transaction_key)
            else:
                logger.warning("No transactions found for %s.", link)
            human_delay(1, 3)  # Optional delay between reports

        logger.info("Successfully scraped %s transactions.", len(all_transactions))
        return all_transactions
    except (TimeoutException, WebDriverException) as e:
        logger.error("Error during scraping: %s", e)
        return None


def write_transactions_to_csv(transactions, file_path):
    """
    Write the list of transactions to a CSV file at the specified path.
    """
    fieldnames = [
        'Transaction ID',
        'First Name',
        'Middle Initial',
        'Last Name',
        'Transaction Date',
        'Owner',
        'Ticker',
        'Asset Name',
        'Company',
        'Description',
        'Rate/Coupon',
        'Maturity Date',
        'Asset Type',
        'Transaction Type',
        'Amount Range',
        'Amount Min',
        'Amount Max',
        'Comment'
    ]
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for transaction in transactions:
                writer.writerow(transaction)
        logger.info(
            "Successfully wrote %s transactions to %s.", len(transactions), file_path)
    except IOError as e:
        logger.error("IO error writing transactions to CSV file: %s", e)
    except csv.Error as e:
        logger.error("CSV error writing transactions to CSV file: %s", e)
    except Exception as e:  # Final catch-all, if necessary
        logger.error("Unexpected error writing transactions to CSV file: %s", e)


# Main Execution Flow
if __name__ == '__main__':
    logger.info("Starting stock transactions scrape for all time...")

    # Setup WebDriver
    driver = setup_driver()

    # URL for Senate EFD search
    SEARCH_URL = "https://efdsearch.senate.gov/search/home/"

    # Scrape all stock transactions using pagination
    transactions_data = scrape_all_transactions(web_driver=driver, search_url=SEARCH_URL)

    # Write transactions to CSV file after scraping
    if transactions_data:
        transactions_file_path = os.path.join(
            LOG_DIRECTORY, "all_stock_transactions.csv")
        write_transactions_to_csv(transactions_data, transactions_file_path)
    else:
        logger.info("No transactions found.")

    # Close the browser after scraping
    driver.quit()

    # Log results
    if transactions_data:
        logger.info(
            "Scraping complete. %s transactions found.", len(transactions_data))
    else:
        logger.info("No transactions found.")
