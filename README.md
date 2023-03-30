# API Telegram bot for check homework status

Evry fixed time(can be adjusted) send request to API for checking homework status.
If status changed send telegram message on your account through Telegram Bot.

## Features

- All token storaged in local storage env.
- Console logging.
- In case of critical issue was send message to Telegram account.


## Installation

Install the dependencies.

```sh
git clone ...
python3 -m venv venv
pip install -r requirements.txt
```

## Tokens

Create .env file in directory
```sh
touch .env
```
Open .env and add 3 rows
```sh
PRACTICUM_TOKEN = YOUR_TOCEN
TELEGRAM_TOKEN = YOUR_TELEGRAM_TOCEN
TELEGRAM_CHAT_ID = YOUR_CHAT_ID
```

## License

MIT

**Free Software, Hell Yeah!**