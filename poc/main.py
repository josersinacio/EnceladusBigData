from flask import Flask, request, jsonify, make_response
import pandas as pd
from default_config import DefaultConfig
from datasus_utils import download_dataset
from send_email import send_email


app = Flask(__name__)
defaultConfig = DefaultConfig()

@app.route('/')
def home():
    return "Hello World"

@app.route('/config/anos')
def anos_disponiveis():
    return jsonify(defaultConfig.anos_disponiveis())

@app.route('/config/estados')
def estados_disponiveis():
    return jsonify(defaultConfig.estados_disponiveis())

@app.route('/config/codigoscid10')
def codigos_cid10():
    return jsonify(defaultConfig.codigos_cid10())


@app.route('/tabelas/queimaduras')
def get_queimaduras():

    estados_param = request.args.getlist('estado')
    anos_param = request.args.getlist('ano')
    email = request.args.get('email')    

    print(f'Obtendo registros de queimaduras para {estados_param} em {anos_param}')

    dataframe = pd.concat([
        pd.DataFrame.from_dict(download_dataset(estado, int(ano))) 
            for estado in estados_param
            for ano in anos_param
    ])

    dataframe = dataframe[[
        'CIRCOBITO', 'DTOBITO', 'DTNASC', 'SEXO', 'RACACOR', 'ESTCIV', 'ESC', 'OCUP', 'CODMUNRES', 'LOCOCOR', 'ASSISTMED', 'CAUSABAS', 'CAUSABAS_O'
    ]]

    codigos = []

    for key, value in defaultConfig.codigos_cid10().items():
        for item in value:
            codigos.append(item)

    queimaduras_dataframe = dataframe[
        dataframe['CAUSABAS'].isin(codigos) | dataframe['CAUSABAS_O'].isin(codigos)
    ]

    resultado_csv = queimaduras_dataframe.to_csv()

    # send_email('JosueP.Viana@gmail.com', f'Relatório para {estados_param} em {anos_param}', resultado_csv)
    send_email(email, f'Relatório para {estados_param} em {anos_param}', resultado_csv)
    response = make_response(resultado_csv, 200)
    response.mimetype = 'application/csv'

    return response

if __name__ == '__main__':
    app.run(debug=True)