import json
import re
import time
from math import ceil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from requests import post


def setup_driver() -> webdriver.Chrome:
    """
    Set up the Selenium WebDriver with Chrome in headless mode.
    
    :return: WebDriver instance
    """
    options = Options()
    options.add_argument('--headless') # Run Chrome in headless mode for faster performance
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def check_agree_and_redirect(driver: webdriver.Chrome) -> None:
    """
    Check the 'agree_statement' checkbox and wait for the page to redirect.

    :param driver: Selenium WebDriver instance
    """
    agree_checkbox = driver.find_element(By.ID, 'agree_statement')
    if not agree_checkbox.is_selected():
        agree_checkbox.click()
    time.sleep(1)

# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
def apply_filter(driver: webdriver.Chrome, filters: dict) -> None:
    """
    Applies filters to the periodic transaction reports 
    depending on what user wants to input/filter by.
    
    Args:
    driver (webdriver): Selenium WebDriver instance.
    filters: A dictionary of optional filter inputs from the user.
    """
    periodic_transactions_checkbox = driver.find_element(
        By.XPATH,
        '//input[@type="checkbox" and @id="reportTypes" and @value="11"]'
    )
    if not periodic_transactions_checkbox.is_selected():
        periodic_transactions_checkbox.click()
        time.sleep(1)

    if filters['first_name'] != '':
        first_name = driver.find_element(By.ID, 'firstName')
        first_name.clear()
        first_name.send_keys(filters['first_name'])
        time.sleep(1)

    if filters['last_name'] != '':
        last_name = driver.find_element(By.ID, 'lastName')
        last_name.clear()
        last_name.send_keys(filters['last_name'])
        time.sleep(1)

    if filters['senator']:
        senator_checkbox = driver.find_element(
            By.XPATH,
            '//input[@type="checkbox" and @value="1"]'
        )
        if not senator_checkbox.is_selected():
            senator_checkbox.click()
            time.sleep(1)
        if filters['senator_state'] != 'All States':
            senator_select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "senatorFilerState"))
            )
            senator_state = Select(senator_select_element)
            senator_state.select_by_visible_text(filters['senator_state'])
            time.sleep(1)

    if filters['candidate']:
        candidate_checkbox = driver.find_element(
            By.XPATH,
            '//input[@type="checkbox" and @value="4"]'
        )
        if not candidate_checkbox.is_selected():
            candidate_checkbox.click()
            time.sleep(1)
        if filters['candidate_state'] != 'All States':
            candidate_select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "candidateFilerState"))
            )
            candidate_state = Select(candidate_select_element)
            candidate_state.select_by_visible_text(filters['candidate_state'])
            time.sleep(1)

    if filters['former_senator']:
        former_senator_checkbox = driver.find_element(
            By.XPATH,
            '//input[@type="checkbox" and @value="5"]'
        )
        if not former_senator_checkbox.is_selected():
            former_senator_checkbox.click()
            time.sleep(1)

    if filters['from_date'] != '':
        from_date = driver.find_element(By.ID, 'fromDate')
        from_date.clear()
        from_date.send_keys(filters['from_date'])
        time.sleep(1)

    if filters['to_date'] != '':
        if filters['from_date'] == '':
            # pylint: disable=broad-exception-raised
            raise Exception('Must also enter in a start date')
        to_date = driver.find_element(By.ID, 'toDate')
        to_date.clear()
        to_date.send_keys(filters['to_date'])
        time.sleep(1)

    search_report_button = driver.find_element(
        By.XPATH,
        """//button[@type="submit" 
            and contains(@class, "btn-primary") 
            and contains(text(), "Search Reports")]"""
        )
    search_report_button.click()

    time.sleep(1)

def format_table_contents(data: list) -> None:
    """
    Format data and send data to be updated in the database

    :param data: a comma separated list of transactions where each 
                 list contains the transaction details
    """
    all_transactions = []
    for row in data:
        transaction_number = int(row[0])
        transaction_date_string = row[1]
        format_str = '%m/%d/%Y'
        transaction_date = datetime.strptime(transaction_date_string, format_str)
        transaction_date = transaction_date.strftime('%Y-%m-%d')
        owner = row[2]
        ticker = row[3]
        asset_name = row[4]
        asset_type = row[5]
        transaction_type = row[6]
        if transaction_type != 'Purchase':
            transaction_type = 'Sale'
        amount_range = row[7]
        comment = row[8]
        if ticker == '--' or asset_type not in ['Stock' , 'Stock Option']:
            continue
        all_transactions.append({
            'transaction_number': transaction_number,
            'ticker': ticker.split('\n'),
            'owner': owner,
            'stock_name': asset_name.split('\n'),
            'transaction_date': transaction_date,
            'transaction_type': transaction_type,
            'transaction_amount': amount_range,
            'comment': comment
        })
    return all_transactions


def extract_table_contents(driver: webdriver.Chrome) -> list:
    """
    Extracts all the contents of a table on the current page.
    
    Args:
    driver (webdriver): Selenium WebDriver instance.
    
    Returns:
    list: A list of dictionaries representing each row in the table.
    """
    # Wait for the table to be present on the page
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//table'))
    )

    rows = table.find_elements(By.XPATH, './/tbody/tr')

    table_contents = []

    for row in rows:
        columns = row.find_elements(By.TAG_NAME, 'td')
        column_texts = [col.text.strip() for col in columns]

        table_contents.append(column_texts)
    table_contents = format_table_contents(table_contents)
    return table_contents

# pylint: disable=too-many-locals
def display_trade_info(driver: webdriver.Chrome) -> list:
    """
    Iterates through all rows in the table for each page, 
    clicks on the periodic transaction link, 
    and extracts information for all stock transactions.

    :param driver: Selenium WebDriver instance
    """
    wait = WebDriverWait(driver, 10)
    all_trade_information = []
    # Iterate while there are still pages to get reports from
    while True:
        try:
            rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
            time.sleep(1)
            for index, row in enumerate(rows):
                try:
                    # Re-locate rows for each iteration to avoid stale references
                    empty_row = driver.find_elements(By.CLASS_NAME, 'dataTables_empty')

                    # No results, so exit
                    if empty_row:
                        break

                    rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
                    row = rows[index]

                    cols = row.find_elements(By.TAG_NAME, 'td')

                    first_and_middle_name = cols[0].text.strip().split()
                    if len(first_and_middle_name) > 1:
                        middle_initial = first_and_middle_name[1]
                    else:
                        middle_initial = ''
                    first_name = first_and_middle_name[0]
                    last_name = cols[1].text.strip()
                    office = cols[2].text.strip()
                    date_filed = cols[4].text.strip()
                    format_str = '%m/%d/%Y'
                    date_received = datetime.strptime(date_filed, format_str)
                    date_received = date_received.strftime('%Y-%m-%d')

                    link = row.find_element(By.XPATH, './/a[@href]')
                    href = link.get_attribute('href')

                    # Click the link
                    driver.execute_script("window.open(arguments[0], '_blank');", href)

                    # Switch to the new tab
                    driver.switch_to.window(driver.window_handles[1])

                    time.sleep(1)

                    # Skip reports that aren't in the correct format (e.g. are images)
                    try:
                        _ = driver.find_element(
                            By.XPATH,
                            '//img[@alt="filing document"]'
                        )
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)
                        continue
                    except NoSuchElementException:
                        # Wait for the page to load if the report isn't an image
                        wait.until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    '//h1[contains(text(), "Periodic Transaction Report")]'
                                )
                            )
                        )
                    match = re.search(r"\((.*?)\)", office)
                    filer_type = match.group(1)

                    table_info = extract_table_contents(driver)

                    transaction_information = {
                        'first_name': first_name, 
                        'middle_initial': middle_initial,
                        'last_name': last_name,
                        'filer_type': filer_type,
                        'date_received': date_received
                    }
                    transaction_information['transactions'] = table_info

                    all_trade_information.append(transaction_information)

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                    # Wait for the original table to reload
                    time.sleep(1)

                except NoSuchElementException:
                    print('No entries')
                    break
                # pylint: disable=broad-except
                except Exception as e:
                    print(f"Error processing row {index + 1}: {e}")

            # Click the next button to get the next page of reports if the button isn't disabled
            next_button = driver.find_element(By.ID, 'filedReports_next')
            time.sleep(1)

            if 'disabled' in next_button.get_attribute('class'):
                print("Next button is disabled. No more pages to process.")
                break

            next_button.click()
            print('moving to next page')

            # Wait for the new page to load
            wait.until(EC.staleness_of(next_button))
            time.sleep(1)

        except NoSuchElementException:
            print('Next button not found or no more pages to process.')
            break
        # pylint: disable=broad-except
        except Exception as e:
            print(f"Error while processing pages: {e}")
            break
    return all_trade_information


def main():
    """
    Main function to set up WebDriver, perform search, scrape results, and save to CSV.
    """
    driver = setup_driver()

    try:
        # Navigate past agree statement page
        url = 'https://efdsearch.senate.gov/search/home/'
        driver.get(url)
        check_agree_and_redirect(driver)
        filters = {
            'first_name': '',
            'last_name': '',
            'senator': False,
            'senator_state': 'All States',
            'candidate': False,
            'candidate_state': 'All States',
            'former_senator': False,
            'from_date': '',
            'to_date': ''
        }
        filters['from_date'] = '01/01/2015'
        filters['to_date'] = time.strftime("%m/%d/%Y", time.localtime())
        apply_filter(driver, filters)
        trades = display_trade_info(driver)

        data = {
            'data': trades,
            'size': -1
        }

        # POST data to our backend
        def recursive_post(rec_data):
            pivot = ceil(len(rec_data['data']) / 2)
            left = rec_data["data"][0:pivot]
            right = rec_data["data"][pivot:]
            # pylint: disable=line-too-long
            left_res = post('http://api:8000/api/core/upload-transactions',json={'data':left, 'size': -1}, timeout=60)
            if left_res.status_code == 400:
                recursive_post({'data':left, 'size': -1})
            # pylint: disable=line-too-long
            right_res = post('http://api:8000/api/core/upload-transactions',{'data':right, 'size': -1}, timeout=60)
            if right_res.status_code == 400:
                recursive_post({'data':right, 'size': -1})

        response = post('http://api:8000/api/core/upload-transactions',json=data, timeout=60)
        if response.status_code == 400:
            recursive_post(data)
        elif response.status_code != 200:
            with open('/scheduler/backup/full_scrape.json','w+') as f:
                json.dump(data, f, indent=2)
            print(response.status_code)
            print(response.content)
            exit(1)

    finally:
        driver.stop_client()
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
