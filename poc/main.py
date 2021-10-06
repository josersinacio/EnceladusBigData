from quart import Quart, request, jsonify
from default_config import defaultConfig
from queimaduras import preparar_e_enviar_async
from pathlib import Path
import logging.config
import os.path
import asyncio
import uuid
import os

app = Quart(__name__)

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


@app.route('/tabelas/queimaduras')
async def get_queimaduras():

    estados_param = request.args.getlist('estado')
    anos_param = request.args.getlist('ano')
    email_param = request.args.get('email') 

    asyncio.get_event_loop().run_in_executor(None, preparar_e_enviar_async, estados_param, anos_param, email_param)

    return dict(destino=email_param, id_requisicao=str(uuid.uuid1())), 202

if __name__ == '__main__':

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

    app.run(debug=True)