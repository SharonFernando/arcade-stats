import pandas as pd
from transform import get_info, msg
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

#for game in gameList['id']:
#    print(game)

print(msg("teste"))

#jogo = get_info(122976)
#print(jogo)