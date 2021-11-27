from quart import Quart, request, jsonify, Response
from quart_cors import cors
from default_config import defaultConfig
import queimaduras
from pathlib import Path
import logging.config
import os.path
import asyncio
import uuid
import os

app = Quart(__name__)
app = cors(app, allow_origin="*")

def fire_and_forget(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)

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

@app.route('/relatorios/queimaduras/densidade-municipal-por-periodo/processados', methods=['GET'])
def get_relatorio_queimaduras_processados():
    return jsonify(queimaduras.listar_relatorios_processados())


@app.route('/relatorios/queimaduras/densidade-municipal-por-periodo/<path:path>')
async def get_relatorio(path):
    arquivo = queimaduras.ler_relatorio(path)

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

    asyncio.get_event_loop().run_in_executor(None, queimaduras.preparar_e_enviar_relatorio_async,
                                             estados_param, data_inicio_param, data_fim_param, email_param)

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