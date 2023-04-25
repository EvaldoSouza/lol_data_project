from riotwatcher import LolWatcher, ApiError
import csv
import pandas as pd
from utility_funcs import *

# golbal variables
api_key = 'RGAPI-46b7fdd6-0ac8-4fc1-8988-b645ef5a4c9a' #NÃO DEIXAR NO GITHUB!!!!
watcher = LolWatcher(api_key)
my_region = 'br1'

#chamar primeiro para pegar os dados do invocador
def get_summoner_by_name(summoner):
    try:
        me = watcher.summoner.by_name(my_region, summoner)
        return me
    except ApiError as err:
        if err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')

#pega apenas o id do match
def get_matches_ids(summoner_info, number_of_matches): #
    try:
        my_matches = watcher.match.matchlist_by_puuid(my_region, summoner_info['puuid'], count= number_of_matches) #achar um jeito de pesquisar por outras infos
        return my_matches
    except ApiError as err:
        if err.response.status_code == 404:
            print('Summoner with this puuid not found')

#salva os ids dos matches em um csv
def get_matches_ids_to_csv(summoner_info, number_of_matches): #
    try:
        my_matches = watcher.match.matchlist_by_puuid(my_region, summoner_info['puuid'], count= number_of_matches) #achar um jeito de pesquisar por outras infos
        filename = summoner_info['name'] + '_matches.csv'
        df = pd.DataFrame(my_matches)
        #salvando para csv
        df.to_csv(str(filename))
    except ApiError as err:
        if err.response.status_code == 404:
            print('Summoner with this puuid not found')
    
    
#pegando todas as informações da partida, e retornando cru
def get_all_match_data(match_id):
    try:
        match_detail = watcher.match.by_id(my_region, match_id)
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        else:
            raise
    
    return match_detail

#armazenando todas as informações cruas de uma lista de partidas
#primeiro, criar uma função que armazena os dados em json. Cada partida vai ser um json
def store_match_data(match_detail, summoner):
    filename = str(match_detail['metadata']['matchId']) + ".json"
    df = pd.DataFrame(match_detail)
    #criando a pasta do summoner
    folder_path = str(summoner)
    make_folder_if_inexistent(folder_path)
    #salvando para csv
    df.to_json(folder_path +"/"+ str(filename))

#pegar a lista de partidas que vou armazenar
def read_list_of_matches(list_of_matches_csv):
    rows = read_csv(list_of_matches_csv)
    ids_of_matchs = []
    #rows é uma lista, onde cada posição é uma linha da tabela de matchs. O id dos matchs está na coluna "0"(zero)
    for match in rows:
        ids_of_matchs.append(match["0"])
    return ids_of_matchs

#função que recebe uma lista de ids de matchs e salva os jogos
def get_all_data_from_match_ids(ids_of_matches, summoner):
    for id in ids_of_matches:
        store_match_data(get_all_match_data(id), summoner)  

#função para ler um csv com os ids e salvar os jogos
def get_all_data_from_ids_in_csv(list_of_matches_csv, summoner):
    ids = read_list_of_matches(list_of_matches_csv)

    for id in ids:
        store_match_data(get_all_match_data(id), summoner)
