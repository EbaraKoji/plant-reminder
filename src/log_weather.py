import os
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from slack_sdk.web import WebClient

from weather import fetch_weather_info

load_dotenv()

weather_icons = {
    'Clear': ':sunny:',
    'Clouds': ':cloud:',
    'Rain': ':rain_cloud:',
    'Snow': ':snowman:',
}


@dataclass
class WeatherInfo:
    time: datetime
    weather_icon: str
    temp: float
    humidity: float


def parse_weather_info(item: dict, current=False):
    if current is True:
        time = datetime.now(tz=ZoneInfo('Asia/Tokyo'))
    else:
        time = datetime.fromtimestamp(item['dt'], tz=ZoneInfo('Asia/Tokyo'))
    weather_icon = weather_icons[item['weather'][0]['main']]
    temp = round(item['main']['temp'], 1)
    humidity = item['main']['humidity']
    return WeatherInfo(time=time, weather_icon=weather_icon, temp=temp, humidity=humidity)


def format_weather_info(weather_info: WeatherInfo):
    return f"{weather_info.time.strftime('%m/%d %H:%M')}  " \
        f"{weather_info.weather_icon}  {weather_info.temp}°C  " \
        f"湿度:{weather_info.humidity}%"


# with open('data/current_weather.json', 'r') as f:
#     current_weather = json.loads(f.read())

# with open('data/forecast.json', 'r') as f:
#     forecast = json.loads(f.read())

current_weather = fetch_weather_info(city_name='Kodaira', type='weather')
assert int(current_weather['cod']) == 200
forecast = fetch_weather_info(city_name='Kodaira', type='forecast')
assert int(forecast['cod']) == 200   # XXX: weatherでは数値だが、forecastでは文字列型で返ってくる!

nl = '\n'
formatted_weather_info = f"""
小平市の現在の天気
{format_weather_info(parse_weather_info(current_weather))}
小平市の予報
{nl.join([format_weather_info(parse_weather_info(item)) for item in forecast['list'][:3]])}
"""

# print(formatted_weather_info)

client = WebClient(token=os.environ['SLACK_API_TOKEN'])
response = client.chat_postMessage(
    text=formatted_weather_info,
    channel='#times-ebara',
)
print(response)
