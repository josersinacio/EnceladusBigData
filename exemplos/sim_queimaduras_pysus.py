from os import makedirs
from numpy import number, string_
from pysus.online_data.SIM import download
import pickle
import redis
import pandas as pd
import yaml

redisClient = redis.Redis('localhost')

def download_dataset(state, year):
    key = f'dataset-{state}-{year}'

    if redisClient.exists(key):
        print(f'Valor para {key} já armazenado.')

        return pickle.loads(redisClient.get(key))
    else:  
        value = download(state, year)

        print(f'Armazenando para {key}.')

        redisClient.set(key, pickle.dumps(value))
        return value

estados = [
    'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT',
    'MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC',
    'SP','SE','TO']

anos = [2014, 2015, 2016, 2017, 2018, 2019]


def get_queimaduras(estado: str, ano: number,  tipo: str, codigos: list):
    print(f'Obtendo registros de queimaduras para {estado} em {ano}')
    print(f'Obtendo registros de queimaduras do tipo "{tipo}"')
    print(f'Obtendo registros de queimaduras para os códigos {codigos}')

    dataframe = pd.DataFrame.from_dict(download_dataset(estado, ano))

    dataframe = dataframe[[
        'CIRCOBITO', 'DTOBITO', 'DTNASC', 'SEXO', 'RACACOR', 'ESTCIV', 'ESC', 'OCUP', 'CODMUNRES', 'LOCOCOR', 'ASSISTMED', 'CAUSABAS', 'CAUSABAS_O'
    ]]

    queimaduras_dataframe = dataframe[
        dataframe['CAUSABAS'].isin(codigos) | dataframe['CAUSABAS_O'].isin(codigos)
    ]

    if not queimaduras_dataframe.empty:
        print(queimaduras_dataframe.head())
        makedirs(f'./output/queimaduras/{estado}_{ano}', exist_ok=True)
        queimaduras_dataframe.to_csv(f'./output/queimaduras/{estado}_{ano}/{tipo.replace("/", "_")}.csv')
    else:
        print('Nenhum dado encontrado')
    print()


with open('./data/static/cid10_queimaduras.yml', 'r', encoding="utf-8") as stream:
    try:
        cid10Queimaduras: dict = yaml.safe_load(stream)

        for key, value in cid10Queimaduras.get('codigos').items():
            for estado in estados:
                for ano in anos:          
                    get_queimaduras(estado, ano, key, value)

    except yaml.YAMLError as exc:
        print(exc)