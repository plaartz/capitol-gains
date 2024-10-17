import time
import datetime
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

def setup_driver() -> webdriver.Chrome:
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


def check_agree_and_redirect(driver: webdriver.Chrome) -> None:
    """
    Check the 'agree_statement' checkbox and wait for the page to redirect.

    :param driver: Selenium WebDriver instance
    """
    agree_checkbox = driver.find_element(By.ID, 'agree_statement')
    if not agree_checkbox.is_selected():
        agree_checkbox.click()
    time.sleep(1)


def filter(driver: webdriver.Chrome, filters: dict) -> None:
    """
    Applies filters to the periodic transaction reports depending on what user wants to input/filter by.
    
    Args:
    driver (webdriver): Selenium WebDriver instance.
    filters: A dictionary of optional filter inputs from the user.
    """
    periodic_transactions_checkbox = driver.find_element(By.XPATH, '//input[@type="checkbox" and @id="reportTypes" and @value="11"]')
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
        senator_checkbox = driver.find_element(By.XPATH, '//input[@type="checkbox" and @value="1"]')
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
        candidate_checkbox = driver.find_element(By.XPATH, '//input[@type="checkbox" and @value="4"]')
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
        former_senator_checkbox = driver.find_element(By.XPATH, '//input[@type="checkbox" and @value="5"]')
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
            raise Exception('Must also enter in a start date')
        to_date = driver.find_element(By.ID, 'toDate')
        to_date.clear()
        to_date.send_keys(filters['to_date'])
        time.sleep(1)
    
    search_report_button = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "btn-primary") and contains(text(), "Search Reports")]')
    search_report_button.click()

    time.sleep(1)


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
        print(column_texts)
    print()
    return table_contents


def display_trade_info(driver: webdriver.Chrome) -> list:
    """
    Iterates through all rows in the table for each page, clicks on the periodic transaction link, and extracts information for today's stock transactions.

    :param driver: Selenium WebDriver instance
    """
    wait = WebDriverWait(driver, 10)
    all_trade_information = []
    # Iterate while there are still pages to get reports from
    while True:
        try:
            rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
            time.sleep(1)
            for index in range(len(rows)):
                try:
                    # Re-locate rows for each iteration to avoid stale references
                    rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
                    row = rows[index]

                    cols = row.find_elements(By.TAG_NAME, 'td')
                    first_name = cols[0].text.strip()
                    last_name = cols[1].text.strip()
                    office = cols[2].text.strip()
                    report_type = cols[3]
                    date_filed = cols[4].text.strip()
                    format_str = '%m/%d/%Y'
                    datetime_object = datetime.datetime.strptime(date_filed, format_str)

                    link = row.find_element(By.XPATH, './/a[@href]')
                    href = link.get_attribute('href')

                    transaction_information = (first_name, last_name, office, href, datetime_object)

                    # Click the link
                    driver.execute_script("window.open(arguments[0], '_blank');", href)

                    # Switch to the new tab
                    driver.switch_to.window(driver.window_handles[1])

                    time.sleep(1)

                    # Skip reports that aren't in the correct format (e.g. are images)
                    try:
                        periodic_transaction_report_image = driver.find_element(By.XPATH, '//img[@alt="filing document"]')
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)
                        continue
                    except NoSuchElementException as e:
                        # Wait for the page to load if the report isn't an image
                        wait.until(
                            EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Periodic Transaction Report")]'))  # Adjust the header based on your page
                        )
                    all_trade_information.append(transaction_information)
                    extract_table_contents(driver)

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                    # Wait for the original table to reload
                    time.sleep(1)

                except NoSuchElementException as e:
                    print('No entries')
                    break
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
        filters['from_date'] = '09/01/2013'
        filters['to_date'] = '10/08/2024'
        filter(driver, filters)
        trades = display_trade_info(driver)

    finally:
        driver.quit()


if __name__ == '__main__':
    main()

