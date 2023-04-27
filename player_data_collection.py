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
#retorna apenas os campeões mais relevantes, definidos pela medida de relevância
def search_for_champs_played_in_folder_of_matches(player_name):
    # create a list of file paths matching the pattern '*.csv' in the folder
    file_paths = glob.glob(player_name + '/*.json')

    #ler o campeão que o player jogou
    #deve conter o campeão como chave,numero de matches jogados, quantidade de vitórias, media de gold por minuto,
    #  media de dano por minuto, placar de visão e visionScoreAdvantageLaneOpponent, teamDamagePercentage, damageTakenOnTeamPercentage
    #damageDealtToObjectives
    champions_played = {}

    #o que fazer com os jogos que o player ficou AFK? A API não salva alguns dados caso eles não tenham existido
    tempo_minimo_de_jogo = 600 #10 minutos, para n considerar partidas onde alguém ficou AFK
    for game_id in file_paths:

        with open(game_id, 'r') as f:
            game = json.load(f)
        
        #preciso checar se o game foi remake
        if game["info"]["gameDuration"] >= tempo_minimo_de_jogo:
            
            for participant in game['info']["participants"]:
                if participant["summonerName"] == player_name:
                    #dois casos, se o champion já foi lido, ou se não foi
                    if participant["championName"] in champions_played:
                        if participant["win"]:
                            champions_played[participant["championName"]]["Partidas"] += 1
                            champions_played[participant["championName"]]["Vitorias"] += 1
                        else:
                            champions_played[participant["championName"]]["Partidas"] += 1
                        
                        #somando a um valor já existente. Se a chave não existir, será que considera 0 pelo +=?
                        champions_played[participant["championName"]]["Gold por Minuto"] += participant["challenges"]["goldPerMinute"]
                        #dano por minuto
                        champions_played[participant["championName"]]["Dano por Minuto"] += participant["challenges"]["damagePerMinute"]
                        #visionScore
                        champions_played[participant["championName"]]["Placar de Visão"] += participant["visionScore"]
                        #visionScoreAdvantageLaneOpponent //Algumas partidas mais antigas não tem esse dado!
                        #champions_played[participant["championName"]]["Vantagem de Visão"] += participant["challenges"]["visionScoreAdvantageLaneOpponent"]
                        #teamDamagePercentage
                        champions_played[participant["championName"]]["Porcentagem de Dano do Time"] += participant["challenges"]["teamDamagePercentage"]
                        #damageTakenOnTeamPercentage
                        champions_played[participant["championName"]]["Porcentagem de Tankada do time"] += participant["challenges"]["damageTakenOnTeamPercentage"]
                        #damageDealtToObjectives Dar um jeito de fazer isso em porcentagem do time também, para manter a comparação
                        champions_played[participant["championName"]]["Dano a Objetivos"] += participant["damageDealtToObjectives"]
                    else:                    
                        if participant["win"]:
                            champions_played[participant["championName"]] = {"Partidas": 1, "Vitorias": 1}
                        else:
                            champions_played[participant["championName"]] = {"Partidas": 1, "Vitorias": 0}
                    
                        #adicionando a chave "gold por minuto" se não houver
                        champions_played[participant["championName"]]["Gold por Minuto"] = participant["challenges"]["goldPerMinute"]
                        #dano por minuto
                        champions_played[participant["championName"]]["Dano por Minuto"] = participant["challenges"]["damagePerMinute"]
                        #visionScore
                        champions_played[participant["championName"]]["Placar de Visão"] = participant["visionScore"]
                        #visionScoreAdvantageLaneOpponent //Algumas partidas mais antigas não tem esse dado!
                        #champions_played[participant["championName"]]["Vantagem de Visão"] = participant["challenges"]["visionScoreAdvantageLaneOpponent"]
                        #teamDamagePercentage
                        champions_played[participant["championName"]]["Porcentagem de Dano do Time"] = participant["challenges"]["teamDamagePercentage"]
                        #damageTakenOnTeamPercentage
                        champions_played[participant["championName"]]["Porcentagem de Tankada do time"] = participant["challenges"]["damageTakenOnTeamPercentage"]
                        #damageDealtToObjectives Dar um jeito de fazer isso em porcentagem do time também, para manter a comparação
                        champions_played[participant["championName"]]["Dano a Objetivos"] = participant["damageDealtToObjectives"]
                        
                    break
        
    #fazendo o winrate (vitorias/partidas)*100 e outras medias
    for champion, stats in champions_played.items():
        champions_played[champion]["Winrate"] = stats["Vitorias"] / stats["Partidas"] * 100
        champions_played[champion]["Gold por Minuto"] = stats["Gold por Minuto"]/ stats["Partidas"]
        champions_played[champion]["Dano por Minuto"] = stats["Dano por Minuto"]/stats["Partidas"]
        champions_played[champion]["Placar de Visão"] = stats["Placar de Visão"]/stats["Partidas"]
        #champions_played[champion]["Vantagem de Visão"] = stats["Vantagem de Visão"]/stats["Partidas"]
        champions_played[champion]["Porcentagem de Dano do Time"] = stats["Porcentagem de Dano do Time"]/stats["Partidas"]
        champions_played[champion]["Porcentagem de Tankada do time"] = stats["Porcentagem de Tankada do time"]/stats["Partidas"]
        champions_played[champion]["Dano a Objetivos"] = stats["Dano a Objetivos"]/stats["Partidas"]
    
    medida_de_relevância = 3 #palpite inicial, 4 é mais ou menos 8% das partidas do player, 3 é 6%
    champions_relevantes = {} #devolver apenas campeões com que jogou mais do que a medida de relevância
    for champion in champions_played.keys():
        if champions_played[champion]["Partidas"] >= medida_de_relevância:
            champions_relevantes[champion] = champions_played[champion]

    #devolver em um formato usavél
    file_name = player_name + "_dossie.json" #salvando em json, talvez seja o formato mais usavel
    with open(file_name, 'w') as fp:
        json.dump(champions_relevantes, fp)


#list_of_matches = pegar_x_partidas_de_player(summoner, 100)
#salvar os dados de todo mundo em arquivos locais, pra n precisar ficar acessando a api
def get_match_data_from_list_of_players(list_of_players, number_of_matchs_to_record):
    for player in list_of_players:
        player_uuid = api.get_summoner_by_name(player)
        ids_of_matches = api.get_matches_ids(player_uuid, number_of_matchs_to_record)
        api.get_all_data_from_match_ids(ids_of_matches, player)
        print("Salvo {} matches do player {}".format(number_of_matchs_to_record, player))

#preciso de uma função que vá criando um indice com os ids de partidas, baseado no tempo. Atualizar a database só com infos novas
#a api da riot só aceita valores em Epoch
def get_list_of_matchs_based_on_time(player, data_em_epoch):
    player_uuid = api.get_summoner_by_name(player)
    api.get_matches_ids_to_csv_starting_in_date(player_uuid, data_em_epoch)

