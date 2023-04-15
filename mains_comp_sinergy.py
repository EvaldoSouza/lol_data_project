from utility_funcs import read_csv
import pandas as pd
import ast
#Pegar os mains da pessoa e ver quais comps funcionam memlhor

def match_champs_to_table(main_champions):
    #vai ler o csv "champ_class_comp.csv"
    #talvez seja preciso ordenar a lista de mains
    #main_champions.sort()
    champ_class_comp = pd.read_csv("champ_class_comp.csv")

    mask = champ_class_comp['Campeão'].str.contains('|'.join(main_champions), na=False)
    weights = champ_class_comp.loc[mask, 'Comps']
    for main, comp in zip(main_champions, weights):
        print(main + ': ', comp )

    return weights.tolist()

def calc_comp_preference(lista_de_strings_de_peso_por_champ):
    lista_de_pesos_por_champ = []
    #preciso desse for para converter a string em literal. Talvez tenha um jeito melhor, pesquisar depois
    #está dando erro com os especialistas sem valores. Mudei todos os especialistas para 0 na planilha local  
    for lista in lista_de_strings_de_peso_por_champ:
        literal = ast.literal_eval(lista)
        lista_de_pesos_por_champ.append(literal)
    
    preferencia = [0,0,0,0,0] #os cinco tipos de comp
    for i in range(len(preferencia)):
        for champion in lista_de_pesos_por_champ:
            preferencia[i] = preferencia[i] + champion[i]
    
    print(preferencia)



mains = [ "Malzahar","Syndra","Lissandra","LeBlanc", "Vex", "Sylas","Viktor"]
values = match_champs_to_table(mains)
calc_comp_preference(values)