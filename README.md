# API Telegram bot

Every fixed time send request to Yandex API for status.
If status changed send telegram message on your account through Telegram Bot.

## Features

- All token in local storage '.env';
- Console logging;
- In case of critical issue was send message to your Telegram account.


## Installation (for Windows)

Clone repository in your directory
```sh
git clone git@github.com:KuzenkovAG/telegram-bot-yandex.git
```
Install environment
```sh
python -m venv venv
```
Activate it
```sh
source venv/Scripts/activate
```
Install requirements
```sh
pip install -r requirements.txt
```
Create .env
```sh
touch .env
```
Open .env and add information about tokens
```sh
PRACTICUM_TOKEN = YOUR_TOKEN
TELEGRAM_TOKEN = YOUR_TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = YOUR_TELEGRAM_CHAT_ID
```

```sh
python homework.py
```

How to know telegram chat id:
1. Find bot https://t.me/userinfobot;
2. Send any message;
3. It will send your telegram ID.


## License

MIT

**Free Software, Hell Yeah!**