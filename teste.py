import get_match_data as api
import json
summoner = 'gira pica de mel'

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
    champions_played = []
    for game in list_of_matches:
        #print(game['participants'])
        for participant in game['info']["participants"]:
            if participant['puuid'] == player_id:
                champions_played.append(participant["championName"])
                break
    
    return champions_played

list_of_matches = pegar_x_partidas_de_player(summoner, 10)

champions_played = get_champs_played_in_list_of_matches(summoner, list_of_matches)
print(champions_played)
