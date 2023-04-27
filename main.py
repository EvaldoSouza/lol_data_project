import player_data_collection as pdc


primeiro_de_marco_2023 = 1677639600
primeiro_de_fevereiro_2023 = 1675209600
#alguns nomes de invocador foram alterados, ou estão incorretors, dando um erro NoneType, e a mensagem Summoner with that ridiculous name not found
#para não ter que rodar tudo de novo, criei dois conjuntos de vetores, e fui comentando
#o_conselho = ["BruselsPuroMalte", "F1dget Spinner", "ILLEOI", "Kandriel", "Uchisori"]
o_conselho = []
#alcoolatras = ["CachaçaCorote", "CachaçaYpióca", "samarula", "Lokal Enjoyer", "GoróSeuRoberto", "CachaçaSeleta"]
alcoolatras = []
#cyber_seniors = ["sNowayBr", "Kuhaku", "KÄT CHUP", "h J", "DaviPirado"]
cyber_seniors = []
#tropa = ["Lar1nhacs", "OMTemisu", "Brockadorr", "aninhaclarasc", "AThreshTalker ", "Nidhogg30"]
tropa = []
#grito = ["Quaglietta", "James The 7th", "C0UL0BRE", "Anicio", "Jose Ze"]
grito = []
#byte_b = ["TuniKrime", "Allora", "BorschDrill", "ASWFrajola", "xXVitoReisXx"]
byte_b = []
#estrelas = ["Bolianinouli", "Linus501512", "Yo Megumy S2", "Egirl Rolezeira", "GatinhaArisca", "Anonineteen"]
estrelas = ["Linus501512", "Yo Megumy S2", "Egirl Rolezeira", "GatinhaArisca", "Anonineteen"]
soca_fofo = []

times = {
    "O Conselho": o_conselho,
    "Alcoolatras Anonimos": alcoolatras,
    "Cyber Seniors": cyber_seniors,
    "Tropa do Guarda Chuva": tropa,
    "Grito": grito,
    "Byte Brawler": byte_b,
    "Estrela Negras": estrelas
}
#get_match_data_from_list_of_players(cyber_seniors, 50)
# for player in alcoolatras:
#    search_for_champs_played_in_folder_of_matches(player)
#search_for_champs_played_in_folder_of_matches("h J")

#procurando a lista de partidas que cada jogador listado jogou
# for time in times.values():
#     for player in time:
#         print("Pegando partidas de {}", player)
#         pdc.get_list_of_matchs_based_on_time(player, primeiro_de_fevereiro_2023)

#lendo o id dos matches da pasta