#pegar um json de uma pasta específica e separar seus dados
import pandas as pd
import datetime
#pegando o json. Considera que o json foi armazenado em uma pasta com o nome do summoner
def json_loader(summoner, match_id):
    path_name = str(summoner)+ "/" + str(match_id) + ".json"
    infos = pd.read_json(path_name)
    return infos

#separando os dados
#data da partida
def game_creation_time(infos: pd.DataFrame()) -> str:
    time_in_unix = infos.loc["gameCreation"]["info"]
    time_in_unix = time_in_unix / 1000 #o tempo está em milisegundos, e não em segundos, como pede a proxima função
    date = datetime.datetime.fromtimestamp(time_in_unix)
    return date.strftime("%d-%m-%Y %H:%M:%S")

#gametype. Se for ARAM é pra ignorar
def return_game_type(infos: pd.DataFrame()) -> str:
    game_type = infos.loc["gameType"]["info"]
    return game_type
    
#times, todos os status 
def return_teams_stats(infos: pd.DataFrame()) -> list:
    teams_stats = infos.loc["teams"]["info"]
    return teams_stats

#participantes
def return_participants_list(infos: pd.DataFrame()) -> list:
    participants = infos.loc["participants"]["info"]
    #colocar mais metodos para escolher um ou outro participante aqui?
    return participants

#salvando os participantes em um DataFrame. Vou usar o infos para não ficar mudando o tipo de dado que as funções recebem
def participants_data_frame(infos: pd.DataFrame()) -> pd.DataFrame:
    all_infos = return_participants_list(infos)
    df = pd.DataFrame(all_infos)
    return df

def participants_challenges(infos: pd.DataFrame()) -> pd.DataFrame:
    all_infos = return_participants_list(infos)
    df = pd.DataFrame(all_infos)
    challenges = df.loc[:,["summonerName", "challenges"]]
    return challenges 

#usar infos ou usar o df dos participants já? Usando infos para ficar consistente com as outras
def did_summoner_win(summoner, infos: pd.DataFrame()) -> bool:
    participants = return_participants_list(infos) 
    participants_df = pd.DataFrame(participants)
    win_stats = participants_df.loc[:,["summonerName", "win"]]
    did_win = win_stats.loc[win_stats['summonerName'] == summoner, 'win'].iloc[0]
    return did_win

#retornandos campeos jogados na partida
def participants_champs(infos: pd.DataFrame()) -> pd.DataFrame:
    all_infos = return_participants_list(infos)
    df = pd.DataFrame(all_infos)
    champion_name = df.loc[:,["summonerName", "championName"]]
    return pd.DataFrame(champion_name) 

#retornando o KDA e o champ
def participants_champs_KDA(infos: pd.DataFrame) -> pd.DataFrame:
    all_infos = return_participants_list(infos)
    df = pd.DataFrame(all_infos)
    columns = ['summonerName', 'championName', 'kills', 'deaths', 'assists']
    result_df = df.loc[:, columns]
    return result_df

def participants_lane(infos: pd.DataFrame) -> pd.DataFrame:
    all_infos = return_participants_list(infos)
    df = pd.DataFrame(all_infos)
    lane = df.loc[:,["summonerName", "lane"]]
    return pd.DataFrame(lane)

#retorna os item em código
#TODO linkar com o json que contem os nomes e afim de cada item
def participants_champs_items(infos: pd.DataFrame) -> pd.DataFrame:
    all_infos = return_participants_list(infos)
    df = pd.DataFrame(all_infos)
    champ_items = df.loc[:, ["summonerName", "championName", "itemsPurchased","item0",
    "item1",
    "item2",
    "item3",
    "item4",
    "item5",
    "item6"]]
    return pd.DataFrame(champ_items)

def vision_stats(infos: pd.DataFrame) -> pd.DataFrame:
    all_infos = return_participants_list(infos)
    df = pd.DataFrame(all_infos)
    vision = df.loc[:,["summonerName", "visionScore", "visionWardsBoughtInGame", "wardsKilled", "wardsPlaced"]]
    return pd.DataFrame(vision)

def combat_stats(infos: pd.DataFrame()) -> pd.DataFrame:
    all_infos = return_participants_list(infos)
    df = pd.DataFrame(all_infos)
    combat_df = df[["summonerName",
                    "championId",
                    "championName",
                    "timeCCingOthers",
                    "totalDamageDealt",
                    "totalDamageDealtToChampions",
                    "totalDamageShieldedOnTeammates",
                    "totalDamageTaken",
                    "physicalDamageDealt",
                    "physicalDamageDealtToChampions",
                    "physicalDamageTaken",
                    "magicDamageDealt",
                    "magicDamageDealtToChampions",
                    "magicDamageTaken",
                    "totalHeal",
                    "totalHealsOnTeammates",
                    "totalMinionsKilled",
                    "totalTimeCCDealt",
                    "totalTimeSpentDead",
                    "totalUnitsHealed",
                    "trueDamageDealt",
                    "trueDamageDealtToChampions",
                    "trueDamageTaken"]]
    return pd.DataFrame(combat_df)

import pandas as pd

def participants_gold(infos: pd.DataFrame) -> pd.DataFrame:
    all_infos = return_participants_list(infos)
    df = pd.DataFrame(all_infos)
    gold_info = df.loc[:, ["summonerName", "championId",
                    "championName", "goldEarned", "goldSpent"]]
    return pd.DataFrame(gold_info)


infos = json_loader("SiriusPuroMalte", "BR1_2490895250")
#did_summoner_win("SiriusPuroMalte", infos)


