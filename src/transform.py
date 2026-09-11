import time
from datetime import datetime
from api import request
from config import URLS
from database import get_existing_ids
from concurrent.futures import ThreadPoolExecutor, as_completed

# Mensagens
def msg(mensagem):

    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return print(f"[{timestamp}] {mensagem}")


# Função para obter os dados via chamada API
def get_info(gameId, gameList):

    existing_ids = get_existing_ids(
        "game", 
        "id"
    )

    ids_to_request = gameList[
        ~gameList['id'].isin(existing_ids)
    ]

    for id in ids_to_request:

        try:

            # Requisições de informações de jogos
            game = request(URLS['games'], gameId)['jeu']

            # Informações dos jogos
            gameId = game.get('id', '')
            gameName = next((g.get('text') for g in game.get('noms', []) if isinstance(g, dict)), '')
            systemId = game.get('systeme', {}).get('id', '')
            systemName = game.get('systeme', {}).get('text', '')
            publisherId = game.get('editeur', {}).get('id', '')
            publisherName = game.get('editeur', {}).get('text', '')
            developerId = game.get('developpeur', {}).get('id', '')
            developerName = game.get('developpeur', {}).get('text', '')
            genreId = next((g.get('id') for g in game.get('genres', []) if isinstance(g, dict)), '')
            genreName = next((n.get('text') for g in game.get('genres', []) if isinstance(g, dict) for n in g.get('noms', []) if isinstance(n, dict) and n.get('langue') == 'pt'), '')
            regionId = next((regionId for rom in game.get('roms', []) if isinstance(rom, dict) for regionId in rom.get('regions', {}).get('regions_id', [])),'')
            regionShortname = next((r for rom in game.get('roms', []) if isinstance(rom, dict) for r in rom.get('regions', {}).get('regions_shortname', [])),'')
            regionFullname = next((r for rom in game.get('roms', []) if isinstance(rom, dict) for r in rom.get('regions', {}).get('regions_pt', [])),'')
            gameReleaseDate = next((d.get('text') for d in game.get('dates', []) if isinstance(d, dict)), '')
            synopsis = next((s.get('text') for s in game.get('synopsis', []) if isinstance(s, dict) and s.get('langue') == 'pt'), '')
            
            system = request(URLS['systems'], systemId)['systemes']

            # Informações dos sistemas
            systemCompany = next((item.get('compagnie') for item in system if item.get('id') == int(systemId)),'')
            systemType = next((item.get('type') for item in system if item.get('id') == int(systemId)),'')
            systemReleaseYear = next((item.get('datedebut') for item in system if item.get('id') == int(systemId)),'')

            return{
                'gameId': gameId,
                'gameName': gameName,
                'systemId': systemId,
                'systemName': systemName,
                'systemCompany': systemCompany,
                'systemType': systemType,
                'systemReleaseYear': systemReleaseYear,
                'publisherId': publisherId,
                'publisherName': publisherName,
                'developerId': developerId,
                'developerName': developerName,
                'genreId': genreId,
                'genreName': genreName,
                'regionId': regionId,
                'regionShortname': regionShortname,
                'regionFullname': regionFullname,
                'gameReleaseDate' : gameReleaseDate,
                'synopsis': synopsis
            }
        
        except request.exceptions.RequestException as e:

            msg(f"❌ Erro no ID {gameId}: {e}")


# Criar dataframe dos jogos
def create_game(df_gamelist):
    game = df_gamelist[
        [
            'gameId',
            'gameName',
            'systemId',
            'genreId',
            'developerId',
            'publisherId',
            'regionId',
            'gameReleaseDate'
        ]
    ]

    game.columns = [
        'id',
        'name',
        'systemId',
        'genreId',
        'developerId',
        'publisherId',
        'regionId',
        'releaseDate'
    ]

    return game


# Criar dataframe dos sistemas
def create_system(df_gamelist):
    system = df_gamelist[
        [
            'systemId',
            'systemName',
            'systemCompany',
            'systemType',
            'systemReleaseYear'
        ]
    ]

    system.columns = [
        'id',
        'name',
        'company',
        'type',
        'releaseYear'
    ]
    
    return system


# Criar dataframe dos status
def create_stats(df_stats):
    stats = df_stats[
        [
            'id',
            'game_id',
            'start_time',
            'end_time',
            'playtime'
        ]
    ]

    stats.columns = [
            'id',
            'gameId',
            'startTime',
            'endTime',
            'playTime'
    ]

    return stats


# Criar dataframe dos desenvolvedores
def create_developer(df_gamelist):
    developer = df_gamelist[
        [
            'developerId',
            'developerName'
        ]
    ]

    developer.columns = [
            'id',
            'name'
        ]
    
    return developer


# Criar dataframe das editoras
def create_publisher(df_gamelist):
    publisher = df_gamelist[
        [
            'publisherId',
            'publisherName'
        ]
    ]

    publisher.columns = [
            'id',
            'name'
        ]
    
    return publisher


# Criar dataframe dos gêneros
def create_genre(df_gamelist):
    genre = df_gamelist[
        [
            'genreId',
            'genreName'
        ]
    ]

    genre.columns = [
            'id',
            'name'
        ]

    return genre


# Criar dataframe das roms
def create_rom(df_gamelist):
    rom = df_gamelist[
        [
            'id',
            'rom',
            'systemId'
        ]
    ]

    rom.columns = [
        'gameId',
        'fileName',
        'systemId'
    ]

    return rom


# Criar dataframe das regiões
def create_region(df_gamelist):
    region = df_gamelist[
        [
            'regionId',
            'regionShortname',
            'regionFullname'
        ]
    ]

    region.columns = [
            'id',
            'shortName',
            'fullName'
        ]

    return region


# Criar dataframe das sinopses
def create_synopsis(df_gamelist):
    synopsis = df_gamelist[
        [
            'gameId',
            'synopsis'
        ]
    ]

    synopsis.columns = [
        'gameId',
        'text'
    ]

    return synopsis


# Definindo função para requisições multiplas
def multiTheadRequest(gameId, ids, gameList):

    msg(f'🎮 Buscando informação para o id {gameId}...')

    results = []

    # Execução da função de requisição, utilizando multithread
    with ThreadPoolExecutor(max_workers=5) as executor:

        futures = {
            executor.submit(get_info, gameId, gameList): gameId
            for gameId in ids
        }

        for future in as_completed(futures):
            gameId = futures[future]

            try:
                result = future.result()

                if result:
                    results.append(result)

            except Exception as e:
                msg(f"❌ Erro no jogo {gameId}: {e}")

    return