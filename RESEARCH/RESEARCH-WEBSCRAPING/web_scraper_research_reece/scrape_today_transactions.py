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
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Ensure log and output directory exists
LOG_DIRECTORY = "web_scraper"
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

# Set up logging to both file and console
logger = logging.getLogger("scrape_today_transactions")
logger.setLevel(logging.INFO)

# Create file handler which logs even debug messages
fh = logging.FileHandler(os.path.join(LOG_DIRECTORY, "daily_scrape.log"))
fh.setLevel(logging.INFO)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handlers to logger
logger.addHandler(fh)
logger.addHandler(ch)


def setup_driver():
    """
    Set up and return a Selenium WebDriver with specified options.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless for automation
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # Optional: Randomize user-agent for stealth
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/94.0.4606.61 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) "
        "Gecko/20100101 Firefox/89.0",
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

    # Using webdriver_manager to automatically handle the driver
    try:
        service = ChromeService(ChromeDriverManager().install())
        web_driver = webdriver.Chrome(service=service, options=chrome_options)
        return web_driver
    except TimeoutException as e:
        logger.error("Error setting up WebDriver: %s", e)
        raise
    except WebDriverException as e:
        logger.error("WebDriverException occurred: %s", e)
        raise


def human_delay(min_delay=2, max_delay=5):
    """
    Simulate human-like delay between actions.

    Args:
        min_delay (int, optional): Minimum delay in seconds. Defaults to 2.
        max_delay (int, optional): Maximum delay in seconds. Defaults to 5.
    """
    time.sleep(random.uniform(min_delay, max_delay))


def scrape_report_links_from_html(html_content):
    """
    Parse HTML content and extract all report links.

    Args:
        html_content (str): HTML content of the page.

    Returns:
        list: List of full report URLs.
    """
    base_url = "https://efdsearch.senate.gov"
    soup = BeautifulSoup(html_content, "html.parser")
    report_links = []

    for a_tag in soup.select("td a[href]"):
        relative_link = a_tag["href"]
        full_link = base_url + relative_link
        report_links.append(full_link)

    return report_links


def clean_senator_name(raw_name):
    """
    Clean and parse the senator's name into first name, middle initial, and last name.

    Args:
        raw_name (str): Raw name string.

    Returns:
        tuple: (first_name, middle_initial, last_name)
    """
    # Remove titles like "The Honorable" from the beginning
    raw_name = re.sub(r"^(The Honorable\s+)", "", raw_name, flags=re.IGNORECASE).strip()

    # Remove any text in parentheses (e.g., "(Former Senator)")
    name_without_parentheses = re.sub(r"\([^)]*\)", "", raw_name).strip()

    # Split the name into parts
    name_parts = name_without_parentheses.strip().split()

    # Assign first name, middle initial, and last name
    if len(name_parts) >= 3:
        first_name = name_parts[0]
        middle_initial = name_parts[1][0] if len(name_parts[1]) == 1 else ""
        last_name = " ".join(name_parts[2:])
    elif len(name_parts) == 2:
        first_name = name_parts[0]
        middle_initial = ""
        last_name = name_parts[1]
    else:
        first_name = name_parts[0] if name_parts else ""
        middle_initial = ""
        last_name = ""

    return first_name.strip(), middle_initial.strip(), last_name.strip()


def parse_asset_details(asset_name_field):
    """
    Parse the 'Asset Name' field and extract asset details.

    Args:
        asset_name_field (str): Asset name string containing details.

    Returns:
        dict: Parsed asset details.
    """
    details = {}
    # Split the field by newlines
    lines = asset_name_field.strip().split("\n")
    # The first line is the Asset Name
    details["Asset Name"] = lines[0].strip()
    for line in lines[1:]:
        line = line.strip()
        # Match Rate/Coupon
        rate_match = re.match(r"Rate/Coupon:\s*(.+)", line)
        if rate_match:
            details["Rate/Coupon"] = rate_match.group(1)
        # Match Matures
        matures_match = re.match(r"Matures:\s*(.+)", line)
        if matures_match:
            details["Maturity Date"] = matures_match.group(1)
        # Match Company
        company_match = re.match(r"Company:\s*(.+)", line)
        if company_match:
            details["Company"] = company_match.group(1)
        # Match Description
        description_match = re.match(r"Description:\s*(.+)", line)
        if description_match:
            details["Description"] = description_match.group(1)
    return details


def parse_amount_range(amount_str):
    """
    Parse the 'Amount' field and return minimum and maximum amounts.

    Args:
        amount_str (str): Amount string, e.g., "$1,000 - $5,000" or "$3,000".

    Returns:
        tuple: (min_amount, max_amount)
    """
    # Remove '$' and commas
    amount_str = amount_str.replace("$", "").replace(",", "")
    # Split by ' - ' to get min and max
    if " - " in amount_str:
        min_amount_str, max_amount_str = amount_str.split(" - ")
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


def scrape_transactions(local_driver, report_url):
    """
    Scrape stock transactions from a single report page.

    Args:
        local_driver (webdriver.Chrome): Selenium WebDriver instance.
        report_url (str): URL of the report page.

    Returns:
        list: List of transaction dictionaries.
    """
    local_driver.get(report_url)
    human_delay(2, 5)

    # Wait for the table to appear on the page
    wait = WebDriverWait(local_driver, 20)
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        page_source = local_driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract senator's name and clean it
        senator_name_tag = soup.find("h2", class_="filedReport")
        raw_senator_name = (
            senator_name_tag.get_text(separator=" ", strip=True)
            if senator_name_tag
            else "Unknown"
        )
        first_name, middle_initial, last_name = clean_senator_name(raw_senator_name)

        # Ensure proper capitalization
        first_name = first_name.title()
        middle_initial = middle_initial.upper()
        last_name = last_name.title()

        rows = local_driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        transactions = []

        for row in rows:
            try:
                cells = row.find_elements(By.TAG_NAME, "td")

                # Parse Ticker
                ticker_text = cells[3].text.strip()
                if ticker_text == "--":
                    ticker = None
                else:
                    ticker = [t.strip() for t in re.split(r"[\n,]+", ticker_text)]
                    if len(ticker) == 1:
                        ticker = ticker[0]

                # Parse Transaction Date
                transaction_date_str = cells[1].text.strip()
                transaction_date = datetime.strptime(
                    transaction_date_str, "%m/%d/%Y"
                ).strftime("%Y-%m-%d")

                # Parse Amount
                amount_str = cells[7].text.strip()
                min_amount, max_amount = parse_amount_range(amount_str)

                # Parse Asset Details
                asset_details = parse_asset_details(cells[4].text)

                # Standardize Asset Type
                raw_asset_type = cells[5].text.strip()
                asset_type_mapping = {
                    "Municipal Security": "Municipal Security",
                    "Non-Public Stock": "Private Stock",
                    "Other Securities": "Other Securities",
                    "Stock": "Stock",
                    # Add other mappings as needed
                }
                standardized_asset_type = asset_type_mapping.get(
                    raw_asset_type, raw_asset_type
                )

                # Generate Transaction ID
                transaction_id = str(uuid.uuid4())

                transaction_data = {
                    "Transaction ID": transaction_id,
                    "First Name": first_name,
                    "Middle Initial": middle_initial,
                    "Last Name": last_name,
                    "Transaction Date": transaction_date,
                    "Owner": cells[2].text.strip().title(),
                    "Ticker": ticker,
                    "Asset Type": standardized_asset_type,
                    "Transaction Type": cells[6].text.strip(),
                    "Amount Range": amount_str,
                    "Amount Min": min_amount,
                    "Amount Max": max_amount,
                    "Comment": cells[8].text.strip() if len(cells) > 8 else "--",
                }

                # Update with asset details
                transaction_data.update(asset_details)

                transactions.append(transaction_data)
            except (
                TimeoutException,
                ValueError,
                AttributeError,
                WebDriverException,
            ) as e:
                logger.error("Error extracting data from row in %s: %s", report_url, e)

        return transactions
    except TimeoutException:
        logger.error(
            "Timed out waiting for the transactions table to load in %s.", report_url
        )
        return []
    except (WebDriverException, Exception) as e:
        logger.error("WebDriver error while scraping %s: %s", report_url, e)
        return []


def apply_filters(local_driver):
    """
    Apply filters on the search page for scraping today's transactions.

    Args:
        local_driver (webdriver.Chrome): Selenium WebDriver instance.
    """
    try:
        # Agree to statement checkbox
        agree_checkbox = local_driver.find_element(By.ID, "agree_statement")
        if not agree_checkbox.is_selected():
            agree_checkbox.click()
        human_delay(1, 3)

        # Select periodic transaction report checkbox
        periodic_checkbox = local_driver.find_element(
            By.CSS_SELECTOR, 'input[value="11"]'
        )
        if not periodic_checkbox.is_selected():
            periodic_checkbox.click()

        # Set the date range filter (today's date)
        today = datetime.now().strftime("%m/%d/%Y")
        from_date_element = local_driver.find_element(By.ID, "fromDate")
        to_date_element = local_driver.find_element(By.ID, "toDate")

        from_date_element.clear()
        from_date_element.send_keys(today)
        to_date_element.clear()
        to_date_element.send_keys(today)

        # Submit the form
        submit_button = local_driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        submit_button.click()
        human_delay(2, 4)
    except (TimeoutException, WebDriverException) as e:
        logger.error("Error applying filters: %s", e)
    except Exception as e:  # Optional catch-all, with pylint disable
        logger.error("Unexpected error applying filters: %s", e)
        raise  # Re-raise to not silently fail


def scrape_today_transactions(local_driver, search_url):
    """
    Scrape today's stock transactions from the search URL with pagination.

    Args:
        local_driver (webdriver.Chrome): Selenium WebDriver instance.
        search_url (str): URL for Senate EFD search.

    Returns:
        list: List of transaction dictionaries.
    """
    local_driver.get(search_url)
    try:
        apply_filters(local_driver)

        all_transactions = []
        unique_transactions = set()

        # Wait for the report table to load
        wait = WebDriverWait(local_driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))

        # Scrape the report links from the page
        page_source = local_driver.page_source
        report_links = scrape_report_links_from_html(page_source)

        # Scrape transactions for each report link
        for index, link in enumerate(report_links, start=1):
            logger.info("Scraping report %d/%d: %s", index, len(report_links), link)
            transactions = scrape_transactions(local_driver, link)
            if transactions:
                for txn_record in transactions:
                    # Create a unique key for the transaction
                    transaction_key = (
                        txn_record["First Name"],
                        txn_record["Last Name"],
                        txn_record["Transaction Date"],
                        txn_record.get("Asset Name", ""),
                        txn_record["Transaction Type"],
                        txn_record["Amount Range"],
                    )
                    if transaction_key not in unique_transactions:
                        unique_transactions.add(transaction_key)
                        all_transactions.append(txn_record)
                    else:
                        logger.info("Duplicate transaction found: %s", transaction_key)
            else:
                logger.warning("No transactions found for %s.", link)
            human_delay(1, 3)  # Optional delay between reports

        # Save today's transactions to a CSV file
        transactions_file_path = os.path.join(
            LOG_DIRECTORY, f"stock_transactions_{datetime.now().strftime('%Y%m%d')}.csv"
        )

        # Write transactions to CSV
        if all_transactions:
            write_transactions_to_csv(all_transactions, transactions_file_path)

        logger.info("Successfully scraped %d transactions.", len(all_transactions))
        return all_transactions
    except TimeoutException:
        logger.error("Timed out waiting for the reports table to load.")
        return []
    except (WebDriverException, Exception) as e:
        logger.error("Error during scraping: %s", e)
        return []


def write_transactions_to_csv(transactions, file_path):
    """
    Write the list of transactions to a CSV file at the specified path.

    Args:
        transactions (list): List of transaction dictionaries.
        file_path (str): Path to the output CSV file.
    """
    fieldnames = [
        "Transaction ID",
        "First Name",
        "Middle Initial",
        "Last Name",
        "Transaction Date",
        "Owner",
        "Ticker",
        "Asset Name",
        "Company",
        "Description",
        "Rate/Coupon",
        "Maturity Date",
        "Asset Type",
        "Transaction Type",
        "Amount Range",
        "Amount Min",
        "Amount Max",
        "Comment",
    ]
    try:
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for txn_record in transactions:
                writer.writerow(txn_record)
        logger.info(
            "Successfully wrote %d transactions to %s.", len(transactions), file_path
        )
    except Exception as e:
        logger.error("Error writing transactions to CSV file: %s", e)


# Main Execution Flow
if __name__ == "__main__":
    logger.info("Starting stock transactions scrape for today...")

    # Setup WebDriver
    driver = setup_driver()

    # URL for Senate EFD search
    SEARCH_URL = "https://efdsearch.senate.gov/search/home/"

    # Scrape today's stock transactions
    transactions_data = scrape_today_transactions(driver, SEARCH_URL)

    # Close the browser after scraping
    driver.quit()

    # Log and print results
    if transactions_data:
        logger.info("Scraping complete. %d transactions found.", len(transactions_data))
        for txn in transactions_data:
            print(txn)
    else:
        logger.info("No transactions found.")
