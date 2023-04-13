from utility_funcs import *
from bs4 import BeautifulSoup
import pandas as pd
import requests

def champions_names_and_classe():
    with open("champions_and_classes.json") as file:
        data = json.load(file)
    
    champ_e_classe = dict(zip(data["Champion"].values(), data["Classes"].values()))
    return champ_e_classe


#cria um json pra não ficar importando toda hora. Só usar para atualizar ou regerar a lista
def import_champ_classes_from_wiki():

    # fazendo a solicitação HTTP para a página web
    url = "https://leagueoflegends.fandom.com/wiki/List_of_champions"
    response = requests.get(url)

    # enviar uma requisição para a página

    # analisar o conteúdo da página com BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # encontrar a tabela desejada pelo ID HTML
    table = soup.find_all('table', class_= 'article-table')

    # extrair os dados da tabela e armazená-los em um dataframe do Pandas
    df = pd.read_html(str(table))[0]
    champions_classes = df.loc[:, ["Champion","Classes"]]

    #champions_and_classes = pd.concat([champions_names, classes], ignore_index=True, axis=1)
    jls_extract_var = "champions_and_classes.json"
    champions_classes.to_json(jls_extract_var)

#não tá funcionando
def dict_to_csv(dados):
    df = pd.DataFrame.from_dict(dados, orient='index', columns=['Classes'])
    df.index.name = 'Champs'

    df.to_csv('dados.csv', index=True, columns=['Classes'])


def dict_to_json(dados):
    with open("champs_e_classes.json", "w") as outfile:
        json.dump(dados, outfile)

#fazer o comp weigther

def search_class_weight(class_name: str, table: pd.DataFrame) -> list:
    """
    Retorna os valores associados a uma classe de campeão específica em uma tabela.

    Args:
        class_name (str): Nome da classe a ser procurada.
        table (pd.DataFrame): Tabela contendo as informações dos campeões.

    Returns:
        list: Lista com os valores associados à classe de campeão.
    """
    try:
        row_index = table.index[table['Classes'] == class_name].tolist()[0]
        row_values = table.iloc[row_index, 1:].tolist()
        return row_values
    except IndexError:
        print(f'Classe {class_name} não encontrada na tabela.')


def get_champion_class_from_dict(table):
    with open("champs_e_classes.json") as file:
        data = json.load(file)
    """Para os campeões com duas classes, estou somando o peso de cada classe e dividindo por dois. Não sei se é a medida mais exata,
    E talvez seja interessante criar uma função mais sofisticada para representar o real peso desses campeões para cada comp"""
    champ_class_comps = {}
    for champ in data.keys():
        champ_classes = data.get(champ).split()
        if len(champ_classes) == 1:
            class_comp = search_class_weight(champ_classes[0], table)
        else:
            class_comp1 = search_class_weight(champ_classes[0], table)
            class_comp2 = search_class_weight(champ_classes[1], table)
            class_comp_sum = [sum(x) for x in zip(class_comp1, class_comp2)]
            class_comp = []
            for x in class_comp_sum:
                x = x/2
                class_comp.append(x)
        champ_class_comps[champ] = [data.get(champ), class_comp]
    
    return champ_class_comps

df = pd.read_csv(r"C:\Users\Evaldo\Documents\LoL API\pesos_classe_fav_comp - Página1.csv")
champ_class_comp = get_champion_class_from_dict(df)
ccc = pd.DataFrame.from_dict(champ_class_comp, orient='index')
ccc.to_csv("champ_class_comp.csv")