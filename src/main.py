from quart import Quart, request, jsonify, Response
from quart_cors import cors
from default_config import defaultConfig
from relatorios import relatorios, densidade_municipal_por_periodo_geral, densidade_municipal_por_periodo, casos_mensais_por_municipio_por_estado
from pathlib import Path
import logging.config
import os.path
import asyncio
import uuid
import os

app = Quart(__name__, static_url_path='', static_folder='public')

app = cors(app, allow_origin="*")

@app.route('/')
async def root():
    return await app.send_static_file('index.html')

@app.route('/config/anos')
def anos_disponiveis():
    return jsonify(defaultConfig.anos_disponiveis())

@app.route('/config/estados')
def estados_disponiveis():
    return jsonify(defaultConfig.estados_disponiveis())

@app.route('/config/codigoscid10')
def codigos_cid10():
    return jsonify(defaultConfig.codigos_cid10())

@app.route('/config/relatorios')
def relatorios_disponiveis():
    return jsonify(defaultConfig.relatorios())


# Relatórios

@app.route('/relatorios/processados')
def get_relatorios_processados():
    return jsonify(relatorios.listar_relatorios_processados())

## Densidade municipal por período geral


@app.route('/relatorios/queimaduras/densidade-municipal-por-periodo-geral/<path:path>')
async def get_relatorio_geral(path):
    arquivo = densidade_municipal_por_periodo_geral.ler_relatorio(path)

    response = Response(arquivo)
    response.headers.set('Content-Disposition',
                         'attachment', filename=path)
    response.headers.set('Content-Type', 'application/pdf')

    return response


@app.route('/relatorios/queimaduras/densidade-municipal-por-periodo-geral', methods=['POST'])
async def post_relatorio_queimaduras_geral():

    estados_param = request.args.getlist('estado')
    data_inicio_param = request.args.get('data_inicio')
    data_fim_param = request.args.get('data_fim')
    email_param = request.args.get('email')

    id_req = str(uuid.uuid1())

    asyncio.get_event_loop().run_in_executor(None, densidade_municipal_por_periodo_geral.preparar_e_enviar_relatorio_async,
                                             estados_param, data_inicio_param, data_fim_param, email_param, id_req)

    return dict(destino=email_param, id_requisicao=id_req), 202


## Densidade municipal por período

@app.route('/relatorios/queimaduras/densidade-municipal-por-periodo/<path:path>')
async def get_relatorio(path):
    arquivo = densidade_municipal_por_periodo.ler_relatorio(path)

    response = Response(arquivo)
    response.headers.set('Content-Disposition',
                         'attachment', filename=path)
    response.headers.set('Content-Type', 'application/pdf')

    return response


@app.route('/relatorios/queimaduras/densidade-municipal-por-periodo', methods=['POST'])
async def post_relatorio_queimaduras():

    estados_param = request.args.get('estado')
    data_inicio_param = request.args.get('data_inicio')
    data_fim_param = request.args.get('data_fim')
    email_param = request.args.get('email')

    id_req = str(uuid.uuid1())

    asyncio.get_event_loop().run_in_executor(None, densidade_municipal_por_periodo.preparar_e_enviar_relatorio_async,
                                             estados_param, data_inicio_param, data_fim_param, email_param, id_req)

    return dict(destino=email_param, id_requisicao=id_req), 202


## Casos Mensais por Município por Estado

@app.route('/relatorios/queimaduras/casos-mensais-por-municipio-por-estado/<path:path>')
async def get_relatorio_2(path):
    arquivo = casos_mensais_por_municipio_por_estado.ler_relatorio(path)

    response = Response(arquivo)
    response.headers.set('Content-Disposition',
                         'attachment', filename=path)
    response.headers.set('Content-Type', 'application/pdf')

    return response


@app.route('/relatorios/queimaduras/casos-mensais-por-municipio-por-estado', methods=['POST'])
async def post_relatorio_queimaduras_2():

    estados_param = request.args.getlist('estado')
    ano_inicio_param = request.args.get('ano_inicio')
    ano_fim_param = request.args.get('ano_fim')
    email_param = request.args.get('email')

    asyncio.get_event_loop().run_in_executor(None, casos_mensais_por_municipio_por_estado.preparar_e_enviar_diagrama_async,
                                             estados_param, ano_inicio_param, ano_fim_param, email_param)

    return dict(destino=email_param, id_requisicao=str(uuid.uuid1())), 202

app_home = os.path.join(Path.home(), '.enceladus', 'logs')
os.makedirs(app_home, exist_ok=True)

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': os.path.join(app_home, 'application.log'),
            'encoding': 'utf8'
        },
        'console_handler': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file_handler', 'console_handler'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
logging.config.dictConfig(logging_config)

if __name__ == '__main__':
    app.run(debug=True)
