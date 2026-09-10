import pandas as pd
from transform import (
    get_info, 
    msg,
    create_game,
    create_system,
    create_stats,
    create_genre,
    create_developer,
    create_publisher,
    create_region,
    create_rom,
    create_synopsis)
from database import (load_dataframe, get_existing_ids, DB_TABLES)
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

msg("⚡ Fazendo requisição para a API...")
msg(f"🎮 Buscando dados para {len(gameList)} jogos...")

#jogo = get_info(122976)
#print(jogo)



msg("✅ Concluído.")

