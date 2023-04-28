import os
import player_data_collection as pdc
import get_match_data as gmd


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
estrelas = ["Bolianinouli", "Linus501512", "Yo Megumy S2", "Egirl Rolezeira", "GatinhaArisca", "Anonineteen"]
#estrelas = ["GatinhaArisca", "Anonineteen"]
grito = ["Quaglietta", "James The 7th", "C0UL0BRE", "ANICIO", "Jose Ze"]
#grito = []
o_conselho = ["BruselsPuroMalte", "F1dget Spinner", "ILLEOI", "Kandriel", "Uchisori"]
#o_conselho = []
soca_fofo =  ["Cachorro", "Brunocc31", "WarWickSocaFofo", "CJotaa"]
#soca_fofo = []
tropa = ["Lar1nhacs", "OMT Emisu", "Brockadorr", "aninhaclarasc", "A Thresh Talker ", "Nidhogg30"]
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

for time in times:
    time_folder = os.path.join(os.path.abspath(data_folder_path), time)
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
                    partida_file = partida + ".json"
                    #print(os.path.join(time_folder,player, partida_file))
                    #print(os.path.isfile(os.path.join(time_folder,player, partida_file)))
                    if not os.path.isfile(os.path.join(time_folder,player, partida_file)):
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
    
        
           

            
#contents agora contem uma lista com os matchs que o player jogou
#preciso pegar os dados desse match SE não estiver na pasta com o nome do jogador

                
                