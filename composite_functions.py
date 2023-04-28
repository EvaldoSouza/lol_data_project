#Arquivo contendo as funções combinadas, realizando tarefas mais complexas (Requisitar varias infos para API, separando dados, etc)
import json
import os
import glob
import get_match_data as gmd
import player_data_collection as pdc
#get_match_data_from_list_of_players(cyber_seniors, 50)
# for player in alcoolatras:
#    search_for_champs_played_in_folder_of_matches(player)
#search_for_champs_played_in_folder_of_matches("h J")

#procurando a lista de partidas que cada jogador listado jogou
# for time in times.values():
#     for player in time:
#         print("Pegando partidas de: ", player)
#         pdc.get_list_of_matchs_based_on_time(player, primeiro_de_fevereiro_2023)

#Essa função recebe como paramentros um dicionário contendo um dicionário com os times e a lista de players, e uma data inicial
#a partir da qual pegar os matches de cada jogador de cada time. Essa data tem que ser em segundos Epoch
#A função irá pegar o nome do player, criar um arquivo com o id de todas as partidas que o player jogou até esse dia inicial
#E então irá consultar a API da Riot para pegar todos os dados dessa partida, salvando em uma pasta com o nome do jogador
def atualizar_partidas_de_todos_jogadores(times, data_folder, dia_inicial_em_epoch):
    for time in times.values():
        for player in time:
            print("Pegando partidas de: ", player)
            pdc.get_list_of_matchs_based_on_time(player, dia_inicial_em_epoch)

    #data_folder = "dados_dos_times_corujão" #nome da pasta para armazenar
    path = os.getcwd()
    data_folder_path = os.path.join(path, data_folder)

    for time in times:
        time_folder = os.path.join(os.path.abspath(data_folder_path), time)
        
        if not os.path.exists(time_folder):
            os.makedirs(time_folder)
        
        os.chdir(time_folder)
        for player in times[time]:
        #print(os.getcwd())
        #print(os.listdir(os.getcwd()))
            lista_matches = player + "_matches.csv"
            player_folder_exists = os.path.exists(player)
            #os dados de cada partida são salvos em uma pasta com o nome do jogador
            if player_folder_exists:
                with open(lista_matches, "r") as file: 
                    contents = [ partida.strip() for partida in file]
                    #print( contents)
                    for partida in contents:
                        if not os.path.exists(partida):
                            print("Salvando partida {} de {}".format(partida, player))
                            gmd.store_match_data(gmd.get_all_match_data(partida), player)
                        else:
                            print("!!Partida {} já existe!!".format(partida))
            else:
                with open(lista_matches, "r") as file:
                    contents = [ partida.strip() for partida in file]
                    #print( contents)
                    #get_all_match_data já cria uma pasta caso ela não exista
                    for partida in contents:
                        print("Salvando partida {} de {}".format(partida, player))
                        gmd.store_match_data(gmd.get_all_match_data(partida), player)


#função para pegar os campeões mais jogados de um conjunto de partidas armazenados em csv em uma pasta
#pelo padrão dessa aplicação, player_name é também o nome da pasta
#retorna apenas os campeões mais relevantes, definidos pela medida de relevância
def search_for_champs_played_in_folder_of_matches(player_name):
    # create a list of file paths matching the pattern '*.csv' in the folder
    file_paths = glob.glob(player_name + '/*.json')#pegar um caminho melhor

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

    #preciso organizar os campeões, ou criar uma lista com os mais jogados primeiro
    champions_relevantes_em_ordem = dict(sorted(champions_relevantes.items(), key = lambda x: x[1]["Partidas"], reverse=True))
    #devolver em um formato usavél
    file_name = player_name + "_dossie.json" #salvando em json, talvez seja o formato mais usavel
    with open(file_name, 'w') as fp:
        json.dump(champions_relevantes_em_ordem, fp)