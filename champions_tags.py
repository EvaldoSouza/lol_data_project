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

dict_to_json(champions_names_and_classe())