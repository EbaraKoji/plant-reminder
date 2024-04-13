import os
from typing import Literal

import requests
from dotenv import load_dotenv

load_dotenv()


def fetch_weather_info(city_name: str, type: Literal['weather', 'forecast']):
    url = f"https://api.openweathermap.org/data/2.5/{type}" \
        f"?q={city_name}&units=metric&appid={os.environ['OPEN_WEATHER_API_KEY']}"
    res = requests.get(url)
    return res.json()
