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

In the project root, create an `.env` file to store the Splitwise API keys, you can get these keys from the project administrators.

The `.env` file have to contain this following environment variables.

```
CONSUMER_KEY=consumer_key_here
CONSUMER_SECRET=consumer_secret_here
API_KEY=api_key_here
```

After these steps, your project will be ready to run.

# Running the project

To get the access of the `Splitwise API`, it will be need to do some steps on first run.

In the project root, open the terminal and run:
```
poetry run main.py
```

Temporary: If it gets error, try:
```
poetry run main.py --no-root
```

### First Running


After running, on browser, open the link that appeared on terminal and authorize the access.

After authorizing, click on the text:

`Click to show out of band authentication information`

Copy the `oauth_verifier` that appears:

```
params[:oauth_verifier] is <oauth_verifier_here>
``` 

And paste on terminal.

The tokens will be saved on `access_token.json` file. If these tokens expire, you'll need to do this process again to keep the acess of the `Splitwise API`.

Done!