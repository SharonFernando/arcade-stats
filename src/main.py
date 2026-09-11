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
from database import (load_dataframe, get_existing_ids)
from config import (LIST, STATS, DB_TABLES)

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

jogo = get_info(122976)

df_jogos = pd.DataFrame(jogo,index=[0])

game = create_game(df_jogos)
print(game)

systems = create_system(df_jogos)
print(systems)

#stats = create_stats(df_jogos)
#print(stats)

genre = create_genre(df_jogos)
print(genre)

developer = create_developer(df_jogos)
print(developer)

publisher = create_publisher(df_jogos)
print(publisher)

region = create_region(df_jogos)
print(region)

#rom = create_rom(df_jogos)
#print(rom)

synopsis = create_synopsis(df_jogos)
print(synopsis)

msg("✅ Concluído.")

