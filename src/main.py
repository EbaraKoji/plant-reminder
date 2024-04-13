import os

from dotenv import load_dotenv
from slack_sdk.web import WebClient

load_dotenv()

client = WebClient(token=os.environ['SLACK_API_TOKEN'])
response = client.chat_postMessage(
    text="I'm a Slack Bot Created by Ebara! Thank you very much, Mr.Ueda! It's surprisingly yummy YEAHHHHHHH!!!",
    channel='#plant',
)
print(response)
