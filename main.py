from dotenv import load_dotenv
import os
from splitwise import Splitwise
#import logging


def pause():
    input("\nPress Enter to continue...")
    os.system('cls' if os.name == 'nt' else 'clear')


# Getting the environment variables from the .env file
load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
api_key = os.getenv("API_KEY")

# Initialize the Splitwise client
client = Splitwise(consumer_key, consumer_secret, api_key=api_key)

# Get the authorization URL
url, oauth_token_secret = client.getAuthorizeURL()

# Print the URL to the console
print("Please visit this URL to authorize the application: ", url)
oauth_token = input("Enter the oauth_token from the URL: ")
oauth_verifier = input("Enter the oauth_verifier from the URL: ")
pause()


# Get the access token
access_token = client.getAccessToken(
    oauth_token, oauth_token_secret, oauth_verifier
    )
current_user = client.getCurrentUser()
print("Access token: ", access_token)
print("Current user: ", current_user)
