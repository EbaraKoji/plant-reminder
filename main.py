import os

import functions_framework
from dotenv import load_dotenv
from slack_sdk.web import WebClient

from src.format_weather import create_formatted_weather_info
from src.weather import fetch_weather_info


@functions_framework.cloud_event
def remind_watering(cloud_event):
    load_dotenv()

    city_name = 'Kodaira'
    channel = '#plant'
    debug_channel = '#times-ebara'

    try:
        client = WebClient(token=os.environ['SLACK_API_TOKEN'])

        # send debug message to debug channel if debug_topic is published
        attributes = cloud_event.data['message'].get('attributes', {})
        debug_enabled = attributes.get('debug') == 'true'

        current_weather = fetch_weather_info(city_name, type='weather')
        assert int(current_weather['cod']) == 200
        forecast = fetch_weather_info(city_name, type='forecast')
        assert int(
            forecast['cod']) == 200  # XXX: weatherでは数値だが、forecastでは文字列型で返ってくる!

        formatted_weather_info = create_formatted_weather_info(current_weather, forecast)

        if debug_enabled:
            client.chat_postMessage(
                text=f'DEBUG: {debug_enabled}\nリマインダー: 水やり\n{formatted_weather_info}\n\n水やりをしてくれた人は、このメッセージに:white_check_mark:でリアクションしてください!',
                channel=debug_channel,
            )
            return

        client.chat_postMessage(
            text=f'リマインダー: 水やり\n{formatted_weather_info}\n\n水やりをしてくれた人は、このメッセージに:white_check_mark:でリアクションしてください!',
            channel=channel,
        )

    except BaseException as e:
        client.chat_postMessage(
            text=f"Failed to log reminder. \nError: {e}",
            channel=debug_channel,
        )
