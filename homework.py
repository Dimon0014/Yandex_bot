import logging
import os
import requests
import sys
import telegram
import time

from exceptions import ApiAnswerError, HomeworkError
from dotenv import load_dotenv
from http import HTTPStatus
from logging import Formatter, StreamHandler
from typing import Dict

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

EXPECTED_RESPONSE_KEYS = ('homeworks', 'current_date')


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(handler)


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

ERROR_HAPPENED: Dict[type, bool] = {}


def check_tokens():
    """If variable absent - exit program."""
    mandatory_variables = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
    }
    for name, variable in mandatory_variables.items():
        if not variable:
            message = f'Absent mandatory variable {name}'
            logger.critical(message)
            raise TypeError(message)


def send_message(bot, message):
    """Send message to telegram."""
    try:
        logger.debug(f'Start send message - {message}.')
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug('Message successfully sent.')
    except Exception as error:
        logger.error(error, exc_info=True)


def get_api_answer(timestamp):
    """Receive JSON answer from Practicum API."""
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except requests.RequestException:
        raise ApiAnswerError('Error in receiving response.')
    status = response.status_code
    if status != HTTPStatus.OK:
        raise ApiAnswerError(
            f'{ENDPOINT} unavailable. Status code - {status}'
        )
    return response.json()


def check_response(response):
    """Check type of response, available keys."""
    if isinstance(response, dict):
        response_keys = response.keys()
    else:
        raise TypeError('Object response should be have type dict.')
    for key in EXPECTED_RESPONSE_KEYS:
        if key not in response_keys:
            raise TypeError(f'Nessesary key - {key}, absent in responce.')
    for key in response_keys:
        if key not in EXPECTED_RESPONSE_KEYS:
            raise TypeError(f'Response have unexpected key - {key}.')
    if not isinstance(response.get('homeworks'), list):
        raise TypeError('Homeworks should be have type list.')


def parse_status(homework):
    """Check status of homework."""
    if 'homework_name' in homework.keys():
        homework_name = homework.get('homework_name')
    else:
        raise HomeworkError('Key "homework_name" absent in dict "homework"')
    status = homework.get('status')
    verdict = HOMEWORK_VERDICTS.get(status)
    if not verdict:
        raise HomeworkError(f'Unexpected homework status {status}')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def get_current_time():
    """Receive current time as integer."""
    return int(time.time())


def main():
    """Main program logic."""
    check_tokens()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = get_current_time()

    while True:
        try:
            response = get_api_answer(timestamp)
            logger.debug(f'Received response {response}.')
            check_response(response)
            homeworks = response.get('homeworks')
            if homeworks:
                logger.debug(f'Response have homeworks {homeworks}.')
                message = parse_status(homeworks[0])
                send_message(bot, message)
                timestamp = get_current_time()
        except Exception as error:
            logger.error(error, exc_info=True)
            if not ERROR_HAPPENED.get(type(error)):
                send_message(bot, f'Сбой в работе программы: {error}.')
                ERROR_HAPPENED[type(error)] = True
        try:
            time.sleep(RETRY_PERIOD)
        except KeyboardInterrupt:
            logger.debug('Stop program.')
            exit()


if __name__ == '__main__':
    logger.debug('Program started.')
    main()
