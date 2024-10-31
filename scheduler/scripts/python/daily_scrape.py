import time
from test_scrape import setup_driver, check_agree_and_redirect, apply_filter, display_trade_info

def main():
    """
    Main function to set up WebDriver, perform search, scrape results, and save to CSV.
    """
    driver = setup_driver()

    # pylint: disable=duplicate-code
    try:
        # Navigate past agree statement page
        url = 'https://efdsearch.senate.gov/search/home/'
        driver.get(url)
        check_agree_and_redirect(driver)
        today_date = time.strftime("%m/%d/%Y", time.localtime())
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
        filters['from_date'] = today_date
        filters['to_date'] = today_date
        apply_filter(driver, filters)
        display_trade_info(driver)

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
