import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

def setup_driver():
    """
    Set up the Selenium WebDriver with Chrome in headless mode.
    
    :return: WebDriver instance
    """
    options = Options()
    options.headless = True # Run Chrome in headless mode for faster performance
    service = Service(ChromeDriverManager().install())
    # Errors out on driver line since chromium isn't installed on cs lab machines
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def check_agree_and_redirect(driver):
    """
    Check the 'agree_statement' checkbox and wait for the page to redirect.

    :param driver: Selenium WebDriver instance
    """
    agree_checkbox = driver.find_element(By.ID, 'agree_statement')
    if not agree_checkbox.is_selected():
        agree_checkbox.click()
    time.sleep(1)


# def get_periodic_transactions_for_date_range(driver, start_date, end_date):
#     """
#     Navigates to the periodic transactions reports for a range of dates to populate database.

#     :param driver: Selenium WebDriver instance
#     :param start_date: the earliest date we want to get the transactions from
#     :Param from_date: the latest date we want to get the transactions from
#     """
#     from_date = driver.find_element(By.ID, 'fromDate')
#     to_date = driver.find_element(By.ID, 'toDate')
#     from_date.clear()
#     to_date.clear()

#     periodic_transactions_checkbox = driver.find_element(By.XPATH, '//input[@type="checkbox" and @id="reportTypes" and @value="11"]')
#     if not periodic_transactions_checkbox.is_selected():
#         periodic_transactions_checkbox.click()

#     from_date.send_keys(start_date)
#     to_date.send_keys(end_date)

#     search_report_button = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "btn-primary") and contains(text(), "Search Reports")]')
#     search_report_button.click()

#     time.sleep(1)


def filter(driver, filters):
    """
    Applies filters to the periodic transaction reports depending on what user wants to input/filter by.
    
    Args:
    driver (webdriver): Selenium WebDriver instance.
    filters: A dictionary of optional filter inputs from the user.
    """
    periodic_transactions_checkbox = driver.find_element(By.XPATH, '//input[@type="checkbox" and @id="reportTypes" and @value="11"]')
    if not periodic_transactions_checkbox.is_selected():
        periodic_transactions_checkbox.click()

    if filters['first_name'] != '':
        first_name = driver.find_element(By.ID, 'firstName')
        first_name.clear()
        first_name.send_keys(filters['first_name'])

    if filters['last_name'] != '':
        last_name = driver.find_element(By.ID, 'lastName')
        last_name.clear()
        last_name.send_keys(filters['last_name'])

    if filters['senator']:
        senator_checkbox = driver.find_element(By.XPATH, '//input[@type="checkbox" and @value="1"]')
        if not senator_checkbox.is_selected():
            senator_checkbox.click()
        if filters['senator_state'] != 'All States':
            senator_select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "senatorFilerState"))
            )
            senator_state = Select(senator_select_element)
            senator_state.select_by_visible_text(filters['senator_state'])

    if filters['candidate']:
        candidate_checkbox = driver.find_element(By.XPATH, '//input[@type="checkbox" and @value="4"]')
        if not candidate_checkbox.is_selected():
            candidate_checkbox.click()
        if filters['candidate_state'] != 'All States':
            candidate_select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "candidateFilerState"))
            )
            candidate_state = Select(candidate_select_element)
            candidate_state.select_by_visible_text(filters['candidate_state'])

    if filters['former_senator']:
        former_senator_checkbox = driver.find_element(By.XPATH, '//input[@type="checkbox" and @value="5"]')
        if not former_senator_checkbox.is_selected():
            former_senator_checkbox.click()
    
    if filters['from_date'] != '':
        from_date = driver.find_element(By.ID, 'fromDate')
        from_date.clear()
        from_date.send_keys(filters['from_date'])

    if filters['to_date'] != '':
        to_date = driver.find_element(By.ID, 'toDate')
        to_date.clear()
        to_date.send_keys(filters['to_date'])
    
    search_report_button = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "btn-primary") and contains(text(), "Search Reports")]')
    search_report_button.click()

    time.sleep(1)


def extract_table_contents(driver):
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
        print(column_texts)
    print()
    return table_contents


def display_trade_info(driver):
    """
    Iterates through all rows in the table, clicks on the periodic transaction link, and extracts information for today's stock transactions.

    :param driver: Selenium WebDriver instance
    """
    rows = driver.find_elements(By.XPATH, '//table/tbody/tr')

    for index in range(len(rows)):
        try:
            # Re-locate rows for each iteration to avoid stale references
            rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
            row = rows[index]

            link = row.find_element(By.XPATH, './/a[@href]')
            href = link.get_attribute('href')

            # Click the link
            driver.execute_script("window.location.href = arguments[0];", href)

            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Periodic Transaction Report")]'))  # Adjust the header based on your page
            )

            extract_table_contents(driver)

            driver.back()

            # Wait for the original table to reload
            time.sleep(1)

        except NoSuchElementException as e:
            print('No entries')
            break
        except Exception as e:
            print(f"Error processing row {index + 1}: {e}")


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
        filters['first_name'] = 'S'
        filters['senator'] = True
        filters['from_date'] = '09/01/2024'
        filters['to_date'] = '09/19/2024'
        filter(driver, filters)
        display_trade_info(driver)

    finally:
        driver.quit()


if __name__ == '__main__':
    main()

