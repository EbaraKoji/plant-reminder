import os

from dotenv import load_dotenv
from slack_sdk.web import WebClient

load_dotenv()

client = WebClient(token=os.environ['SLACK_API_TOKEN'])
response = client.api_test()
print(response)
