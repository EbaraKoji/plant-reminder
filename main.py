import os

from dotenv import load_dotenv
from slack_sdk.web import WebClient

from src.weather import fetch_weather_info
from src.format_weather import create_formatted_weather_info


def remind_watering():
    load_dotenv()

    city_name = 'Kodaira'
    try:
        client = WebClient(token=os.environ['SLACK_API_TOKEN'])
        current_weather = fetch_weather_info(city_name, type='weather')
        assert int(current_weather['cod']) == 200
        forecast = fetch_weather_info(city_name, type='forecast')
        assert int(forecast['cod']) == 200  # XXX: weatherでは数値だが、forecastでは文字列型で返ってくる!

        formatted_weather_info = create_formatted_weather_info(current_weather, forecast)
        client.chat_postMessage(
            text='リマインダー: 水やり\n' + formatted_weather_info,
            channel='#plant',
        )

    except BaseException as e:
        client.chat_postMessage(
            text=f"Failed to log reminder. \nError: {e}",
            channel='#times-ebara',
        )


if __name__ == '__main__':
    remind_watering()
