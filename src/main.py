from quart import Quart, request, jsonify, Response
from quart_cors import cors
from default_config import defaultConfig
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


@app.route('/config/relatorios')
def relatorios():
    return jsonify(defaultConfig.relatorios())

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