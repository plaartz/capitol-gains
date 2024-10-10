import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

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
    print('success')
    return driver


def check_agree_and_redirect(driver):
    """
    Check the 'agree_statement' checkbox and wait for the page to redirect.

    :param driver: Selenium WebDriver instance
    """
    print('gets here')
    agree_checkbox = driver.find_element(By.ID, 'agree_statement')
    if not agree_checkbox.is_selected():
        agree_checkbox.click()
    time.sleep(5)


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
        time.sleep(5)
        print('works')

    finally:
        driver.quit()


if __name__ == '__main__':
    main()

