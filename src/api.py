import requests
from config import (
    DEVID,
    DEVPASSWORD,
    SSID,
    SSPASSWORD
)

# Definindo função para chamada API
def request(url, gameId):

    PARAMS={
        'devid': DEVID,
        'devpassword': DEVPASSWORD,
        'ssid': SSID,
        'sspassword': SSPASSWORD,
        'gameid': gameId,
        'output': 'json'
    }

    try:

        response = requests.get(
            url = url,
            params=PARAMS,
            timeout=30
        )

        return response.json()['response']
    
    except:

        return response.raise_for_status()







