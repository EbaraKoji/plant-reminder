from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

weather_icons = {
    'Clear': ':sunny:',
    'Clouds': ':cloud:',
    'Rain': ':rain_cloud:',
    'Snow': ':snowman:',
    'Drizzle': ':closed_umbrella:',
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


def create_formatted_weather_info(current_weather: dict, forecast: dict):
    nl = '\n'
    formatted_weather_info = f"""
小平市の現在の天気
{format_weather_info(parse_weather_info(current_weather))}
小平市の予報
{nl.join([format_weather_info(parse_weather_info(item)) for item in forecast['list'][:5]])}"""
    return formatted_weather_info
