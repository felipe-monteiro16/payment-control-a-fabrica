from dotenv import load_dotenv
import os

load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
api_key = os.getenv("API_KEY")
print(consumer_key, consumer_secret, api_key) # prints the value of the secret key