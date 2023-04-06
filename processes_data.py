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
    
#times
def return_teams_stats(infos: pd.DataFrame()) -> list:
    teams_stats = infos.loc["teams"]["info"]
    return teams_stats

#participantes
def return_participants(infos: pd.DataFrame()) -> list:
    participants = infos.loc["participants"]["info"]
    #colocar mais metodos para escolher um ou outro participante aqui?
    return participants

#salvando os participantes em um DataFrame. Vou usar o infos para não ficar mudando o tipo de dado que as funções recebem
def participants_data_frame(infos: pd.DataFrame()) -> pd.DataFrame:
    all_infos = return_participants(infos)
    df = pd.DataFrame(all_infos)
    return df

def participants_challenges(infos: pd.DataFrame()) -> pd.DataFrame:
    all_infos = return_participants(infos)
    df = pd.DataFrame(all_infos)
    challenges = df.loc[:,["summonerName", "challenges"]]
    return challenges 



infos = json_loader("SiriusPuroMalte", "BR1_2490895250")
participants_challenges(infos)
