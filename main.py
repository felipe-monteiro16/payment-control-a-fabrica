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


def load_access_token(clt) -> str:
    """Check if the access token file exists, verify if the access token is valid,
    and load the access token from the file."""
    # Check if the access token file exists
    check_file_access_token(clt)

    # Load the access token from the file
    try:
        with open("access_token.json", "r", encoding="utf-8") as f:
            token = json.load(f)
            clt.setAccessToken(token)
            # Verify if the access token is valid
            verify_access_token(clt)
    except json.JSONDecodeError as e:
        print("Load access token failed.")
        print(f"Error: {e}")
        print("Delete the access token file and try again.\n")
        sys.exit()
    return token


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
        print("Unauthorized access. Please set the correct keys on .env file.\n")
        print(e)
        sys.exit()
    print("\nEnvironment variables loaded successfully.\n")
    print("Client initialized successfully.\n")
    return clt


def check_file_access_token(clt):
    """Check if the access token file exists."""
    if os.path.exists("access_token.json"):
        print("Access token file found.\n")
        return True
    print("Access token file not found.")
    print("Let's get a new access token.\n")
    get_access_token(clt)
    if os.path.exists("access_token.json"):
        return True
    print("Error: Get access token failed.\n")
    sys.exit()


def verify_access_token(clt):
    """Verify if the access token is valid."""
    try:
        current_user = clt.getCurrentUser()
        print(f" User name: {current_user.first_name}")
    except SplitwiseUnauthorizedException as e:
        print("Access token is invalid.")
        print(f"Error: {e}\n")
        print("Let's get a new access token.\n")
        get_access_token(clt)
        if os.path.exists("access_token.json"):
            print("Access token updated successfully.\n")
            return True
        print("Error: Get access token failed.\n")
        sys.exit()
    print("Access token is valid.\n")
    return True


def config()-> None:
    """Configure the Splitwise client."""
    # Initialize the Splitwise client
    client = initialize_client()

    # Load the access token from the file
    access_token = load_access_token(client)
    client.setAccessToken(access_token)

    print("Access token loaded successfully.\n")


config()
