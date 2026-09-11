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

roms = gameList[["id","rom"]].dropna(subset=['id']).drop_duplicates(subset=['id'])

msg("⚡ Fazendo requisição para a API...")
msg(f"🎮 Buscando dados para {len(gameList)} jogos...")

jogo = get_info(122976)

df_games = pd.DataFrame(jogo,index=[0])
roms['id'] = roms['id'].astype(int)
df_games['gameId'] = df_games['gameId'].astype(int)
df_games = df_games.merge(roms, left_on='gameId', right_on='id', how='left')

print(df_games)

game = create_game(df_games)
print(game)

systems = create_system(df_games)
print(systems)

stats = create_stats(statsList)
print(stats)

genre = create_genre(df_games)
print(genre)

developer = create_developer(df_games)
print(developer)

publisher = create_publisher(df_games)
print(publisher)

region = create_region(df_games)
print(region)

rom = create_rom(df_games)
print(rom)

synopsis = create_synopsis(df_games)
print(synopsis)

msg("✅ Concluído.")