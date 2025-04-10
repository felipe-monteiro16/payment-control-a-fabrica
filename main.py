"""Splitwise API Python Client"""
import json
import os
from dotenv import load_dotenv
from splitwise import Splitwise
from splitwise.exception import SplitwiseUnauthorizedException


def pause() -> None:
    """Pause the execution of the program until the user presses Enter."""
    input("\nPress Enter to continue...")
    os.system('cls' if os.name == 'nt' else 'clear')


def get_access_token() -> None:
    """Get the access token from the user.
    The user will be redirected to a URL to authorize the application."""

    # Get the authorization URL
    url, oauth_token_secret = client.getAuthorizeURL()

    # Print the URL to the console
    print("Please visit this URL to authorize the application: ", url)
    oauth_token = url.split("oauth_token=")[-1]
    oauth_verifier = input("Enter the oauth_verifier from the URL: ")
    pause()
    access_token = client.getAccessToken(
        oauth_token, oauth_token_secret, oauth_verifier
    )
    save_access_token(access_token)


def save_access_token(token: str) -> str:
    """Save the access token to a file."""
    with open("access_token.json", "w", encoding="utf-8") as f:
        json.dump(token, f)


def load_access_token() -> str:
    """Load the access token from a file."""

    # Check if the file exists
    if os.path.exists("access_token.json"):
        with open("access_token.json", "r", encoding="utf-8") as f:
            token = json.load(f)
            return token
    else:
        print("Access token file not found.")
        return None


def initialize_client() -> str:
    """Initialize the Splitwise client."""

    # Getting the environment variables from the .env file
    load_dotenv()
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    api_key = os.getenv("API_KEY")

    # Check if the environment variables are set
    if not consumer_key or not consumer_secret or not api_key:
        print("Please set the environment variables. More details on README.md")
        return None

    # Set the Splitwise client
    clt = Splitwise(consumer_key, consumer_secret, api_key=api_key)
    return clt


# Initialize the Splitwise client
client = initialize_client()
if client is not None:
    print("Client initialized successfully.")

    # Check if the access token file exists
    if os.path.exists("access_token.json"):
        acess_token = load_access_token()
        client.setAccessToken(acess_token)
    else:
        get_access_token()
else:
    print("Client initialization failed.")


# Usage example


try:
    # Get the current user
    current_user = client.getCurrentUser()
    print("User ID: ", current_user.id)
    print("User Name: ", current_user.first_name)



except SplitwiseUnauthorizedException as e:
    print("Access token is invalid.")
    print("Error: ", e)

    # Reauthorize the application
    get_access_token()
    print("Access token updated successfully.")
    print("Please run the program again.")
    pause()
