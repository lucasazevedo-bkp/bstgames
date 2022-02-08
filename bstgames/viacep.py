import json
import requests


def get_address(code):
    url = f'https://viacep.com.br/ws/{code}/json/'
    request = requests.get(url)
    if request.status_code == 200:
        response = json.loads(request.text)
        if 'erro' not in response:
            return response