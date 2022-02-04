import os
import glob
import logging
import storage
from datetime import datetime
from pathlib import Path
from default_config import defaultConfig


logger = logging.getLogger(__name__)

home_folder = os.path.join(Path.home(), '.enceladus')


def listar_relatorios_processados():

    relatorios = []
    datas_processamento = storage.datas_processamento()

    for diretorio in defaultConfig.relatorios():
        path = os.path.join(home_folder, diretorio.get('path')[1:], '*.pdf')
        
        for file in glob.glob(path):
            nome_base = os.path.basename(file)
            partes_nome = nome_base.split('.')
            chave_redis = f"dataProcessamento.{diretorio.get('id')}.{nome_base}"

            relatorios.append(dict(
                tipo=diretorio.get('nome'),
                estado=partes_nome[0],
                data_inicio=partes_nome[1],
                data_fim=partes_nome[2],
                uri=f"{diretorio.get('path')}/{nome_base}",
                data_processamento=datas_processamento.get(chave_redis)
            ))

    relatorios.sort(key=lambda relatorio: datetime.strptime(relatorio.get('data_processamento'), "%Y-%m-%dT%H:%M:%S%z"), reverse=True)

    return relatorios
