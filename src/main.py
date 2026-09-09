import pandas as pd
from transform import get_info
from config import (LIST, STATS)

# lendo os arquivos
gameList = pd.read_csv(LIST)
statsList = pd.read_csv(STATS)

gameList = gameList[
    [
    "id",
    "playcount",
    "gametime",
    "lastplayed",
    "releasedate",
    "rom"
    ]
]

jogo = get_info(122976)
print(jogo)