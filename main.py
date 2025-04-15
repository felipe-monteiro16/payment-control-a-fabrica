"""Splitwise API Python Client"""
import json
import os
import sys
from dotenv import load_dotenv
from splitwise import Splitwise
from splitwise.exception import SplitwiseUnauthorizedException


def pause() -> None:
    """Pause the execution of the program until the user presses Enter."""
    input("\nPress Enter to continue...")
    os.system('cls' if os.name == 'nt' else 'clear')


def save_access_token(token: str) -> str:
    """Save the access token to a file."""
    with open("access_token.json", "w", encoding="utf-8") as f:
        json.dump(token, f)


def get_access_token(clt) -> None:
    """Get the access token from the user.
    The user will be redirected to a URL to authorize the application."""

    # Get the authorization URL
    url, oauth_token_secret = clt.getAuthorizeURL()

    # Print the URL to the console
    print("Please visit this URL to authorize the application: ", url)
    oauth_token = url.split("oauth_token=")[-1]
    oauth_verifier = input("Enter the oauth_verifier from the URL: ")
    pause()
    access_token = clt.getAccessToken(
        oauth_token, oauth_token_secret, oauth_verifier
    )
    save_access_token(access_token)


def load_access_token() -> str:
    """Load the access token from a file."""

    # Check if the file exists
    if os.path.exists("access_token.json"):
        with open("access_token.json", "r", encoding="utf-8") as f:
            token = json.load(f)
            return token
    print("Access token file not found.")
    return None


def initialize_client() -> str:
    """Initialize the Splitwise client."""

    # Getting the environment variables from the .env file
    load_dotenv()
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    api_key = os.getenv("API_KEY")

    # Set the Splitwise client
    clt = Splitwise(consumer_key, consumer_secret, api_key=api_key)

    # Check if the environment variables are set
    try:
        clt.getCurrentUser()
    except SplitwiseUnauthorizedException as e:
        print("Unauthorized access. Please set the correct keys on .env file.")
        print(e)
        sys.exit()
    return clt


def check_file_access_token(clt):
    """Check if the access token file exists."""
    if os.path.exists("access_token.json"):
        return True
    print("Access token file not found.")
    print("Let's get a new access token.")
    get_access_token(clt)
    if os.path.exists("access_token.json"):
        return True
    print("Error: Get access token failed.")
    sys.exit()


def verify_access_token(clt):
    """Verify if the access token is valid."""
    try:
        current_user = clt.getCurrentUser()
        print(f" User first name: {current_user.first_name}")
        print("Access token is valid.")
        return True
    except SplitwiseUnauthorizedException as e:
        print("Access token is invalid.")
        print("Error: ", e)
        print("Let's get a new access token.")
        get_access_token(clt)
        if os.path.exists("access_token.json"):
            print("Access token updated successfully.")
            return True
        print("Error: Get access token failed.")
        sys.exit()


def config()-> None:
    """Configure the Splitwise client."""
    # Initialize the Splitwise client
    client = initialize_client()
    print("Client initialized successfully.")

    # Check if the access token file exists
    check_file_access_token(client)

    # Verify if the access token is valid
    verify_access_token(client)

    # Load the access token from the file
    acess_token = load_access_token()
    client.setAccessToken(acess_token)

    print("Access token loaded successfully.")


config()
