# services/waha.py

import requests

class Waha:
    def __init__(self):
        self.__api_url = 'http://waha:3000'

    def send_message(self, chat_id, message):
        url = f'{self.__api_url}/api/sendText'
        headers = {'Content-Type': 'application/json'}
        payload = {
            'session': 'default',
            'chatId': chat_id,
            'text': message,
        }
        try:
            response = requests.post(url=url, json=payload, headers=headers, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erro em send_message: {e}")

    def start_typing(self, chat_id):
        url = f'{self.__api_url}/api/startTyping'
        headers = {'Content-Type': 'application/json'}
        payload = {
            'session': 'default',
            'chatId': chat_id,
        }
        try:
            response = requests.post(url=url, json=payload, headers=headers, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erro em start_typing: {e}")

    def stop_typing(self, chat_id):
        url = f'{self.__api_url}/api/stopTyping'
        headers = {'Content-Type': 'application/json'}
        payload = {
            'session': 'default',
            'chatId': chat_id,
        }
        try:
            response = requests.post(url=url, json=payload, headers=headers, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erro em stop_typing: {e}")

    def seg(self, chat_id):
        autorizados = {
            "5521982390569@c.us"
        }
        return "aut" if chat_id in autorizados else "not"
