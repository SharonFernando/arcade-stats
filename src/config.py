import os
from dotenv import load_dotenv

load_dotenv()

# URLs para requisições
URLS={
    'games' : 'https://api.screenscraper.fr/api2/jeuInfos.php',
    'systems': 'https://api.screenscraper.fr/api2/systemesListe.php'
}

# Dados para API
DEVID = os.getenv('devid')
DEVPASSWORD = os.getenv('devpassword')
SSID = os.getenv('ssid')
SSPASSWORD = os.getenv('sspassword')

# Dados banco de dados
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')
NAME = os.getenv('DB_NAME')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')

# Arquivos
LIST = "gamelist.csv"
STATS = "stats.csv"