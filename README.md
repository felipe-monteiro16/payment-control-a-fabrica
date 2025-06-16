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

In the project root, create an `.env` file to store the Splitwise keys, Mercado Pago API token, Whatsapp API keys, you can get these keys from the project administrators.

The `.env` file have to contain these following Splitwise environment variables.

```
# SPLITWISE KEYS
CONSUMER_KEY=consumer_key_here
CONSUMER_SECRET=consumer_secret_here
API_KEY=api_key_here

# MERCADO PAGO TOKEN
ACCESS_TOKEN=mercado_pago_access_token_here

# WHATSAPP KEYS
WHATSAPP_PHONE_NUMBER_ID=your_whatsapp_phone_number_id_here
WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token_here
```

And the Mercado Pago Access Token:

```
ACCESS_TOKEN=mercado_pago_access_token_here
```

After these steps, your project will be ready to run.


# Running the project

### First Running

To get the access of the `Splitwise API`, it will be need to do some steps on first run.

In the project root, open the terminal and run:
```
poetry run python main.py get-users
```

Temporary: If it gets an error, try:
```
poetry run python main.py get-users --no-root
```

After running, on browser, open the link that appeared on terminal and authorize the access.

After authorizing, click on the text:

`Click to show out of band authentication information`

Copy the `oauth_verifier` that appears:

```
params[:oauth_verifier] is <oauth_verifier_here>
``` 

Paste on terminal and press ENTER.

The tokens will be saved on `access_token.json` file. If these tokens expire, you'll need to do this process again to keep the access of the `Splitwise API`.

Done! If everything went well, will have appeared the `users list` on terminal.

## Commands

To run the project, use `poetry run` followed by `python main.py` and the desired command.

For more information, use:
```
poetry run python main.py --help
```

### Command List

* `get-users`: Get all users from Splitwise API.

    Usage example:
    ```
    poetry run python main.py get-users
    ```
    The users name and ID will be displayed.

* `get-user-debts`: Get user debts from the last month by ID.

    Usage example:
    ```
    poetry run python main.py get-user-debts USER-ID
    ```
    If the user has debts, the name and amount of the debt will be displayed.

* `get-payment-link`: Get the payment link for the given user_id.

    Usage example:
    ```
    poetry run python main.py get-payment-link USER-ID
    ```
    The payment link and the items table will be displayed.

* `send-payment-link`: Get user debts, create a Mercado Pago payment link, and send it to the user via WhatsApp.

    Usage example:
    ```
    poetry run python main.py send-payment-link USER-ID
    ```
    The payment link will be sent to the user.

* `create-user-debts`: Create user debts in Splitwise from a CSV file.

    Usage example:
    ```
    poetry run python main.py create-user-debts --path data_access/src/debts.csv --description "Expense description"
    ```
    The debts will be created in Splitwise and shown in the CLI.

* `get-paid-debts`: Verify paid users (via Mercado Pago) and send payments to Splitwise.

    Usage example:
    ```
    poetry run python main.py get-paid-debts
    ```
    Paid users will be processed and their payments sent to Splitwise.
