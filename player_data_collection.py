import get_match_data as api
import json
import glob
import pandas as pd

def pegar_x_partidas_de_player(player_name, numero_de_partidas):
    summoner = api.get_summoner_by_name(player_name)
    matches_id = api.get_matches_ids(summoner, numero_de_partidas)
    list_of_matches = []
    for id in matches_id:
        game = api.get_all_match_data(id)
        list_of_matches.append(game)
    
    return list_of_matches

#preciso de uma função para buscar apenas os campeões que o player jogo
def get_champs_played_in_list_of_matches(player_name, list_of_matches):
    summoner = api.get_summoner_by_name(player_name)
    player_id = summoner['puuid']
    #deve conter o campeão como chave,numero de matches jogados, quantidade de vitórias
    champions_played = {}
    for game in list_of_matches:
        #print(game['participants'])
        for participant in game['info']["participants"]:
            if participant['puuid'] == player_id:
                #dois casos, se o champion já foi lido, ou se não foi
                if participant["championName"] in champions_played:
                    if participant["win"]:
                        current_values = champions_played[participant["championName"]]
                        current_values[0] = current_values[0] + 1
                        current_values[1] = current_values[1] + 1
                        champions_played[participant["championName"]] = current_values #[Numero de matches, Vitorias]
                    else:
                        current_values = champions_played[participant["championName"]]
                        current_values[0] = current_values[0] + 1 #aumentando só o numero de partidas jogadas
                        champions_played[participant["championName"]] = current_values #[Numero de matches, Vitorias]
                else:                    
                    if participant["win"]:
                        champions_played[participant["championName"]] = [1, 1] #[Numero de matches, Vitorias]
                    else:
                        champions_played[participant["championName"]] = [1, 0]
                break
    
    return champions_played

#função para pegar os campeões mais jogados de um conjunto de partidas armazenados em csv em uma pasta
#pelo padrão dessa aplicação, player_name é também o nome da pasta
def search_for_champs_played_in_folder_of_matches(player_name):
    #ler cada um dos arquivos
    #folder_path = '/path/to/folder'

    # create a list of file paths matching the pattern '*.csv' in the folder
    file_paths = glob.glob(player_name + '/*.json')

    #ler o campeão que o player jogou
    #deve conter o campeão como chave,numero de matches jogados, quantidade de vitórias
    champions_played = {}
    for game_id in file_paths:

        with open(game_id, 'r') as f:
            game = json.load(f)
        
        for participant in game['info']["participants"]:
            if participant["summonerName"] == player_name:
                #dois casos, se o champion já foi lido, ou se não foi
                if participant["championName"] in champions_played:
                    if participant["win"]:
                        champions_played[participant["championName"]]["Partidas"] += 1
                        champions_played[participant["championName"]]["Vitorias"] += 1
                    else:
                        champions_played[participant["championName"]]["Partidas"] += 1
                else:                    
                    if participant["win"]:
                        champions_played[participant["championName"]] = {"Partidas": 1, "Vitorias": 1}
                    else:
                        champions_played[participant["championName"]] = {"Partidas": 1, "Vitorias": 0}
                
                break
    
    #fazendo o winrate (vitorias/partidas)*100
    for champion, stats in champions_played.items():
        partidas = stats["Partidas"]
        vitorias = stats["Vitorias"]
        winrate = vitorias/partidas*100
        champions_played[champion]["Winrate"] = winrate
    #devolver em um formato usavél
    file_name = player_name + "_champions_played.json" #salvando em json, talvez seja o formato mais usavel
    with open(file_name, 'w') as fp:
        json.dump(champions_played, fp)


#list_of_matches = pegar_x_partidas_de_player(summoner, 100)
#salvar os dados de todo mundo em arquivos locais, pra n precisar ficar acessando a api
def get_match_data_from_list_of_players(list_of_players, number_of_matchs_to_record):
    for player in list_of_players:
        player_uuid = api.get_summoner_by_name(player)
        ids_of_matches = api.get_matches_ids(player_uuid, number_of_matchs_to_record)
        api.get_all_data_from_match_ids(ids_of_matches, player)
        print("Salvo {} matches do player {}".format(number_of_matchs_to_record, player))


o_conselho = ["BruselsPuroMalte", "F1dget Spinner", "ILLEOI", "Kandriel", "Uchisori"]
alcoolatras = ["CachaçaCorote", "CachaçaYpióca", "samarula", "Lokal Enjoyer", "gira pica de mel", "CachaçaSeleta"]
cyber_seniors = ["sNowayBr", "Kuhaku", "KÄT CHUP", "h J", "DaviPirado"]
#get_match_data_from_list_of_players(cyber_seniors, 50)
#for player in cyber_seniors:
 #   search_for_champs_played_in_folder_of_matches(player)
search_for_champs_played_in_folder_of_matches("h J")