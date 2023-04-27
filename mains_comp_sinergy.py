from utility_funcs import read_csv
import pandas as pd
import ast
#Pegar os mains da pessoa e ver quais comps funcionam memlhor

def match_champs_to_table(main_champions):
    #vai ler o csv "champ_class_comp.csv" e retornar o ACPSS de cada campeão
    champ_class_comp = pd.read_csv("champ_class_comp.csv")

    mask = champ_class_comp['Campeão'].str.contains('|'.join(main_champions), na=False) #melhorar isso daqui, pq tá dando uns erros toscos, tipo pegando Vi e Viego
    weights = champ_class_comp.loc[mask, 'Comps']
    w = weights.tolist()
    lista_de_pesos = []
    #A forma como fez essa leitura ta tosca. Está retornando uma string com a lista
    # Preciso desse for para converter a string em literal. Talvez tenha um jeito melhor, pesquisar depois
    for lista in w:
        literal = ast.literal_eval(lista)
        lista_de_pesos.append(literal) 
    # for main, comp in zip(main_champions, weights):
    #     print(main + ': ', comp )

    return lista_de_pesos

def calc_comp_preference(lista_de_champs):
    lista_de_pesos_por_champ = match_champs_to_table(lista_de_champs)
   
    # for lista in lista_de_strings_de_peso_por_champ:
    #     literal = ast.literal_eval(lista)
    #     lista_de_pesos_por_champ.append(literal)
    preferencia = [sum(value) for value in lista_de_pesos_por_champ]
    
    return preferencia

def calc_comp_median_weight_ACPSS(champs_no_time):
    scores = calc_comp_preference(champs_no_time)
    
    media_de_preferencia_de_comp = [value/5 for value in scores]
    return media_de_preferencia_de_comp

Illaoi = [ "Illao", "Warwick", "Tristana", "Veigar", "Pantheon"]
Ivern =	["Renekton","Ivern" ,"Yone", "Kalista", "Alistar"]
Lulu	=["Sylas", "Volibear", "Akali", "Tristana", "Lulu"]
Vi	=["Warwick", "Vi", "Cho'gath", "Nilah", "Annie"] #está dando problema com a Vi, provavelmente por causa do Viego e do Viktor
Kassadin=	["Pantheon", "Sejuani", "Kassadin", "Nilah", "Rell"]
Poppy=	["Poppy", "Talon", "Pantheon", "Karthus", "Shaco"]

testes = {
    "Illaoi": Illaoi,
    "Ivern": Ivern,
    "Lulu": Lulu,
    "Kassadin": Kassadin,
    "Poppy": Poppy
}
#values = match_champs_to_table(mains)
#print(calc_comp_weight_by_ACPSS(time))
for time in testes.keys():
    print(time)
    print(time, calc_comp_median_weight_ACPSS(testes[time]), match_champs_to_table([time]),calc_comp_preference(testes[time]))
