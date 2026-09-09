import time
from datetime import datetime
from api import request
from config import URLS
from concurrent.futures import ThreadPoolExecutor, as_completed

# Mensagens
def msg(mensagem):

    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    tqdm.write(f"[{timestamp}] {mensagem}")

# Definindo função para obter os dados via chamada API
def get_info(gameId):

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

# Definindo função para requisições multiplas
def multiTheadRequest(gameId,ids):

    results = []
    errors = []

    # Execução da função de requisição, utilizando multithread
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(get_info, gameId): gameId for gameId in ids}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processando jogos"):
            result = future.result()
            if result:
                results.append(result)
            time.sleep(0.1)