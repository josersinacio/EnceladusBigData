from pysus.online_data.SIM import download
import pandas as pd

banco = download(state= 'DF', year= 2019)
 
dataframe = pd.DataFrame.from_dict(banco)

dataframe = dataframe[[
    'CIRCOBITO', 'DTOBITO', 'DTNASC', 'SEXO', 'RACACOR', 'ESTCIV', 'ESC', 'OCUP', 'CODMUNRES', 'LOCOCOR', 'ASSISTMED', 'CAUSABAS', 'CAUSABAS_O'
]]

filter_list = ["X{}".format(x) for x in range(600, 850)]

dataframe = dataframe[
    dataframe['CAUSABAS'].isin(filter_list) | dataframe['CAUSABAS_O'].isin(filter_list)
]

print(dataframe.head())