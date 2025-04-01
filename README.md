# Payment Control - A Fábrica
The main goal is to automate payments made at the Fábrica.

# Setups
After cloning the repository, follow the steps below to setup and run the project properly.

### Requirements
This project uses Poetry for dependency management. Make sure Poetry is installed on your machine. If you don't have installed, you can do it with:

```
pip install poetry
```

Then, install depencencies by running:

```
poetry install
```
### File `.env`

In the project root, create an `.env` file to store the Splitwise API keys.

The `.env` file have to contain this following environment variables.

```
CONSUMER_KEY=consumer_key_here
CONSUMER_SECRET=consumer_secret_here
API_KEY=api_key_here
```

