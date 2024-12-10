# pylint: disable=too-many-branches, too-many-locals, too-many-statements

from os import environ
from sys import stderr
from math import ceil
from datetime import date, datetime, timedelta
import json
from collections import deque
from time import sleep

from requests import post, get

STRUCT = {
    "ticker":"ticker",
    "price":"close",
    "date":'datetime'
}
API_URL_TIME ="https://api.twelvedata.com/time_series"
API_URL_EOD = "https://api.twelvedata.com/eod"
PER_MINUTE = 8

API_KEY = environ.get("STOCK_API_KEY")


STOCKS = [
    {"ticker":"AAPL","date_range":1},
    {"ticker":"MSFT","date_range":2},
    {"ticker":"AVGO","date_range":10},
    {"ticker":"NSC","date_range":5},
    {"ticker":"GOOG","date_range":6},
    {"ticker":"TSLA","date_range":3},
    {"ticker":"META","date_range":9},
    {"ticker":"NSC","date_range":2},
    {"ticker":"META","date_range":2},
    {"ticker":"NSC","date_range":2},
    ]

def fetch_data() -> list:
    """
    This method takes calls the backend to receive a list of stocks that it needs to have updated.
    It then calls another api to fetch the stock prices needed and resends them to the backend to
    be persisted in the database.

    @return     Returns a list of stock prices to a given date for each stock that was requested.
    """
    def parse_date(date_range: int) -> tuple[date, date]:
        now = datetime.now()
        days_ago = now - timedelta(days=date_range - 1)
        return days_ago.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")

    # Fetch needed tickers from our backend
    response = get('http://api:8000/api/core/fetch-stock-ids',timeout=60).json()

    data = {}
    stocks = response["stocks"]

    eod_queue = deque()
    time_series_queue = deque()
    """
    [
        {
            "ticker": "AAPL",
            "date_range": 1-365

        }
    ]
    """
    # Parse whether we can use a simple eod api call or a time_series api call
    for stock in sorted(
        stocks,
        key=lambda x: x["date_range"] if "date_range" in x else -1,
        reverse=True):
        # stock in time_series doesnt work curr
        if stock["ticker"] in eod_queue or stock in time_series_queue:
            continue
        if "date_range" not in stock:
            # Add struct for bad date_range calls
            # Potentially just fetch eod
            continue
        if stock["date_range"] == 1:
            eod_queue.append(stock["ticker"])
        elif stock["date_range"] > 1:
            start_date, end_date = parse_date(stock["date_range"])
            time_series_queue.append({
                "ticker":stock["ticker"],
                "start_date":start_date,
                "end_date":end_date,
                "date_range":stock["date_range"]
            })

    # every minute we can fetch 8 stocks starting with time series

    while len(time_series_queue):
        iteration = [time_series_queue.popleft() for _ in range(PER_MINUTE) if time_series_queue]
        symbol_str = ",".join([symbol["ticker"] for symbol in iteration])
        earliest_date = sorted(iteration, key=lambda x: x["start_date"])[0]["start_date"]

        #pylint: disable=line-too-long
        iteration_response = get(
            f'{API_URL_TIME}?apikey={API_KEY}&symbol={symbol_str}&interval=1day&start_date={earliest_date}&country=United States',
            timeout=60
        )
        if iteration_response.status_code in [429,500]:
            for item in iteration:
                time_series_queue.append(item)
            continue
        res = iteration_response.json()

        if len(iteration) > 1:
            for ticker in res.keys():
                if res[ticker]["status"] != "ok":

                    print(res[ticker])
                    continue # Potentially do more here
                data[ticker] = {
                    "ticker": ticker,
                    "prices": [
                        {
                            "price":price["close"], 
                            "date":price["datetime"]
                        } for price in res[ticker]["values"]]
                }
        else:
            if res["status"] == "ok":
                ticker = res["meta"]["symbol"]
                data[ticker] = {
                    "ticker": ticker,
                    "prices": [
                        {
                            "price": price["close"],
                            "date": price["datetime"]
                        } for price in res["values"]
                    ]
                }


        # Potentially do some more preprocessing to only have actual needed dates from `iteration`
        # tickers since they could be different we are just batch requesting

        if len(eod_queue) or len(time_series_queue):
            sleep(60)

        # Find a better implementation that allows to continue parsing until the api call
        # is ready

    while len(eod_queue):
        iteration = [eod_queue.popleft() for _ in range(PER_MINUTE) if eod_queue]
        symbol_str = ",".join(iteration)

        #pylint: disable=line-too-long
        iteration_response = get(f'{API_URL_EOD}?apikey={API_KEY}&symbol={symbol_str}&country=United States', timeout=60)
        if iteration_response.status_code in [429,500]:
            for item in iteration:
                time_series_queue.append(item)
            continue
        res = iteration_response.json()

        if len(iteration) > 1:
            for ticker in res.keys():
                data[ticker] = {
                    "ticker": ticker,
                    "prices": [
                        {
                            "price":res[ticker]["close"],
                            "date": res[ticker]["datetime"]
                        }
                    ]
                }
        else:
            ticker = res["symbol"]
            data[ticker] = {
                "ticker": res["symbol"],
                "prices": [
                    {
                        "price":res["close"],
                        "date": res["datetime"]
                    }
                ]
            }
        if len(eod_queue):
            sleep(60)

    return data


def main() -> None:
    """
    Calls the needed apis and methods to properly update stock prices for the backend
    """
    # Get the data from 3rd party api
    data = fetch_data()

    # Transform the data
    data = {
        "data": data,
        "size": -1
    }

    # POST data to our backend
    def recursive_post(rec_data):
        if len(rec_data["data"]) > 1:
            pivot = ceil(len(rec_data["data"]) / 2)
            left = {key: rec_data["data"][key] for key in list(rec_data["data"].keys())[:pivot]}
            right = {key: rec_data["data"][key] for key in list(rec_data["data"].keys())[pivot:]}
            # pylint: disable=line-too-long
            left_res = post('http://api:8000/api/core/upload-stock-prices',json={"data": left, "size": -1}, timeout=60)
            if left_res.status_code == 400:
                recursive_post({"data":left})
            # pylint: disable=line-too-long
            right_res = post('http://api:8000/api/core/upload-stock-prices',json={"data": right, "size": -1}, timeout=60)
            if right_res.status_code == 400:
                recursive_post({"data":right})
        else:
            key = list(rec_data["data"].keys())[0]
            pivot = ceil(len(rec_data["data"][key]["prices"]) / 2)

            left = rec_data["data"][key]["prices"][:pivot]
            right = rec_data["data"][key]["prices"][pivot:]

            left_data = {
                "data": {
                    key: {
                        "ticker": key,
                        "prices": left
                    }
                },
                "size": -1
            }
            right_data = {
                "data": {
                    key: {
                        "ticker": key,
                        "prices": right
                    }
                },
                "size": -1
            }
            # pylint: disable=line-too-long
            left_res = post('http://api:8000/api/core/upload-stock-prices',json=left_data, timeout=60)
            if left_res.status_code == 400:
                recursive_post(left_data)
            # pylint: disable=line-too-long
            right_res = post('http://api:8000/api/core/upload-stock-prices',json=right_data, timeout=60)
            if right_res.status_code == 400:
                recursive_post(right_data)



    response = post('http://api:8000/api/core/upload-stock-prices',json=data, timeout=60)
    if response.status_code == 400:
        recursive_post(data)
    elif response.status_code != 200:
        print(f'Error uploading stocks on date {date.today().strftime("%Y-%m-%d")}, \
              writing to backup json file for manual upload',file=stderr)
        # pylint: disable=line-too-long
        with open(f'/scheduler/backup/{date.today().strftime("%Y-%m-%d")}.json','w+',encoding='utf-8') as f:
            json.dump(data, f,indent=2)

        exit(1)

if __name__ == "__main__":
    main()
