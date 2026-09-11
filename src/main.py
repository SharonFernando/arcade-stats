import pandas as pd
from database import load_dataframe
from transform import (
    msg,
    create_game,
    create_system,
    create_stats,
    create_genre,
    create_developer,
    create_publisher,
    create_region,
    create_rom,
    create_synopsis,
    multiTheadRequest
)
from config import (
    LIST, 
    STATS, 
    DB_TABLES
)

# lendo os arquivos
gameList = pd.read_csv(LIST)
statsList = pd.read_csv(STATS)

roms = gameList[["id","rom"]].dropna(subset=['id']).drop_duplicates(subset=['id'])

msg("⚡ Fazendo requisição para a API...")
msg(f"🎮 Buscando dados para {len(roms)} jogos...")

for rom in roms['id'][:2]:
    jogo = multiTheadRequest(rom, roms['id'], roms)

df_games = pd.DataFrame(jogo,index=[0])

roms['id'] = roms['id'].astype(int)
df_games['gameId'] = df_games['gameId'].astype(int)
df_games = df_games.merge(roms, left_on='gameId', right_on='id', how='left')

game = create_game(df_games)
load_dataframe(game, DB_TABLES['game'])

systems = create_system(df_games)
load_dataframe(systems, DB_TABLES['system'])

stats = create_stats(statsList)
load_dataframe(stats, DB_TABLES['stats'])

genre = create_genre(df_games)
load_dataframe(genre, DB_TABLES['genre'])

developer = create_developer(df_games)
load_dataframe(developer, DB_TABLES['developer'])

publisher = create_publisher(df_games)
load_dataframe(publisher, DB_TABLES['publisher'])

region = create_region(df_games)
load_dataframe(region, DB_TABLES['region'])

rom = create_rom(df_games)
load_dataframe(rom, DB_TABLES['rom'])

synopsis = create_synopsis(df_games)
load_dataframe(synopsis, DB_TABLES['synopsis'])

msg("✅ Concluído.")