import glob
import logging
import os
from pathlib import Path
from default_config import defaultConfig


logger = logging.getLogger(__name__)

home_folder = os.path.join(Path.home(), '.enceladus')


def listar_relatorios_processados():

    relatorios = []

    for diretorio in defaultConfig.relatorios():
        path = os.path.join(home_folder, diretorio.get('path')[1:], '*.pdf')

        for file in glob.glob(path):
            nome_base = os.path.basename(file).split('.')

            relatorios.append(dict(
                tipo=diretorio.get('nome'),
                estado=nome_base[0],
                data_inicio=nome_base[1],
                data_fim=nome_base[2],
                uri=f"{diretorio.get('path')}/{'.'.join(nome_base)}",
            ))

    return relatorios
