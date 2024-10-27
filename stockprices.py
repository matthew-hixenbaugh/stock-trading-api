import requests
from dotenv import load_dotenv
import os

NOTABLE_CHANGE_PERCENT = 5


class StockPrices:

    def __init__(self, *, stock: str):
        self.stock_name = stock
        self.__stock_data = self.__get_from_api()
        self.__stock_prices = self.get_stock_prices()

        two_day_stock_prices = {day: self.__stock_prices[day] for day in list(self.__stock_prices)[:2]}

        (day1, day2) = (list(two_day_stock_prices)[1], list(two_day_stock_prices)[0])
        (day1_closing_price, day2_closing_price) = (float(two_day_stock_prices[day1]['4. close']),
                                                    float(two_day_stock_prices[day2]['4. close']))

        self.__working_date = day1

        closing_difference = day2_closing_price - day1_closing_price
        self.__closing_percent = (closing_difference / day2_closing_price) * 100

    def __get_from_api(self) -> dict:
        load_dotenv()
        alpha_vantage_api_key = os.environ.get("AV_API_KEY")

        alpha_vantage_url = "https://www.alphavantage.co/query"

        parameters = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': self.stock_name,
            'apikey': alpha_vantage_api_key,
            'outputsize': 'compact',
        }

        av_response = requests.get(url=alpha_vantage_url, params=parameters)
        av_response.raise_for_status()
        return av_response.json()

    def get_stock_data(self) -> dict:
        return self.__stock_data

    def get_stock_prices(self) -> dict:
        return self.__stock_data['Time Series (Daily)']

    def get_working_date(self) -> str:
        return self.__working_date

    def has_notable_change(self) -> bool:
        return abs(self.__closing_percent) > NOTABLE_CHANGE_PERCENT
