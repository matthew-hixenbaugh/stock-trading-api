import requests
from dotenv import load_dotenv
import os


class NewsReport:

    def __init__(self, *, date: str, query: str):

        self.__working_date = date
        self.__query = query
        self.__news_data = self.__get_from_api()

    def __get_from_api(self) -> dict:
        load_dotenv()
        api_key = os.environ.get("NEWSAPI_API_KEY")

        url = "https://newsapi.org/v2/everything"

        parameters = {
            'q': self.__query,
            'from': self.__working_date,
            'sortBy': 'popularity',
            'apiKey': api_key,
            'language': 'en',
            'searchIn': 'title',
        }

        news_response = requests.get(url=url, params=parameters)
        news_response.raise_for_status()

        return news_response.json()

    def get_article_titles(self) -> list:
        news_list = self.__news_data['articles']
        top_three = news_list[:3]

        top_three_titles = [article['title'] for article in top_three]

        return top_three_titles
