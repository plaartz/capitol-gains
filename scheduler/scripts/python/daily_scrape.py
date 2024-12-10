import time
from math import ceil
from requests import post
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
        trades = display_trade_info(driver)

        data = {
            'data': trades,
            'size': -1
        }

        # POST data to our backend
        def recursive_post(rec_data):
            pivot = ceil(len(rec_data) / 2)
            left = rec_data[0:pivot]
            right = rec_data[pivot:]
            left_res = post('http://api:8000/api/core/upload-transactions',json=left, timeout=60)
            if left_res.status_code == 400:
                recursive_post(left)
            right_res = post('http://api:8000/api/core/upload-transactions',json=right, timeout=60)
            if right_res.status_code ==400:
                recursive_post(right)

        response = post('http://api:8000/api/core/upload-transactions',json=data, timeout=60)
        if response.status_code == 400:
            recursive_post(data)
        elif response.status_code != 200:
            print(response.status_code)
            print(response.content)
            exit(1)

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
