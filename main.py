import os
import player_data_collection as pdc
import get_match_data as gmd
import composite_functions as fun


primeiro_de_marco_2023 = 1677639600
primeiro_de_fevereiro_2023 = 1675209600
#alguns nomes de invocador foram alterados, ou estão incorretors, dando um erro NoneType, e a mensagem Summoner with that ridiculous name not found
#para não ter que rodar tudo de novo, criei dois conjuntos de vetores, e fui comentando
alcoolatras = ["CachaçaCorote", "CachaçaYpióca", "samarula", "Lokal Enjoyer", "GoróSeuRoberto", "CachaçaSeleta"]
#alcoolatras = []
byte_b = ["TuniKrime", "Allora", "ASW Frajola", "xXVitoReisXx"]
#byte_b = []
cyber_seniors = ["sNowayBr", "Kuhaku", "KÄT CHUP", "h J", "DaviPirado"]
#cyber_seniors = []
estrelas = ["BolianiNouli", "Linus501512", "Yo Megumy S2", "Egirl Rolezeira", "GatinhaArisca", "Anonineteen"]
#estrelas = ["GatinhaArisca", "Anonineteen"]
grito = ["Quaglietta", "James The 7th", "C0UL0BRE", "ANICIO", "Jose Ze"]
#grito = []
o_conselho = ["BruselsPuroMalte", "F1dget Spinner", "ILLEOI", "Kandriel", "Uchisori", "GodKira678", "Mach4jhin"]
#o_conselho = []
soca_fofo =  ["Cachorro", "Brunocc31", "WarWickSocaFofo", "CJotaa"]
#soca_fofo = []
tropa = ["Lar1nhacs", "OMT Emisu", "Brockadorr", "aninhaclarasc", "A Thresh Talker", "Nidhogg30"]
#tropa = []

times = {
    "Alcoolatras Anonimos": alcoolatras,
    "Byte Brawlers": byte_b,
    "Cyber Seniors": cyber_seniors,
    "Estrelas Negras": estrelas,
    "Grito": grito,
    "O Conselho": o_conselho,
    "Soca Fofo": soca_fofo,
    "Tropa do Guarda Chuva": tropa
}

#get_match_data_from_list_of_players(cyber_seniors, 50)
# for player in alcoolatras:
#    search_for_champs_played_in_folder_of_matches(player)
#search_for_champs_played_in_folder_of_matches("h J")

#procurando a lista de partidas que cada jogador listado jogou
# for time in times.values():
#     for player in time:
#         print("Pegando partidas de: ", player)
#         pdc.get_list_of_matchs_based_on_time(player, primeiro_de_fevereiro_2023)

#lendo o id dos matches da pasta
data_folder = "dados_dos_times_corujão"
path = os.getcwd()
data_folder_path = os.path.join(path, data_folder)

# fun.adicionar_ID_partidas_em_csv_para_time("O Conselho", o_conselho, data_folder, primeiro_de_fevereiro_2023)

# fun.atualizar_partidas_de_todos_jogadores(times, data_folder)

for time in times:
    pasta_do_time = os.path.join(data_folder_path, time)
    for player in times[time]:
        print("Criando o dossie de ", player)
        summoner_infos = gmd.get_summoner_by_name(player)
        fun.search_for_champs_played_in_folder_of_matches(player, summoner_infos["puuid"], pasta_do_time)
                
                