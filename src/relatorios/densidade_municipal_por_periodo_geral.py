import os
import logging
import shutil
import storage
from default_config import defaultConfig
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT
from send_email import send_email

logger = logging.getLogger(__name__)

relatorios_folder = os.path.join(
    Path.home(), '.enceladus', 'relatorios', 'queimaduras', 'densidade-municipal-por-periodo')

id_relatorio = 'DENSIDADE_MUNICIPAL_POR_PERIODO'

os.makedirs(relatorios_folder, exist_ok=True)


def _formatar_intervalo(data_inicio: str, data_fim: str):
    if data_inicio == data_fim:
        return f'em {data_inicio}'

    return f'entre {data_inicio} e {data_fim}'

def ler_relatorio(relatorio: str):
    with open(os.path.join(relatorios_folder, relatorio), 'rb') as f:
        return f.read()


def preparar_e_enviar_relatorio_async(estados: list, data_inicio: str, data_fim: str, email: str, id_requisicao: str):

    if 'TODOS' in estados:
        estados = [k for e in defaultConfig.estados_disponiveis()
                   for k in e.keys()]

    logger.info(f'Obtendo registros de queimaduras para %s %s.',
                estados, _formatar_intervalo(data_inicio, data_fim))

    file_path = os.path.join(relatorios_folder, f"{'-'.join(estados)}.{data_inicio}.{data_fim}.pdf")
    working_path = os.path.join(relatorios_folder, id_requisicao, '')

    os.makedirs(working_path, exist_ok=True)

    if not os.path.exists(file_path):
        p = Popen(['Rscript', 'rscripts/densidade_municipal_por_periodo_geral.R', ','.join(estados),
                  data_inicio, data_fim, file_path, working_path], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

        streamdata = p.communicate()[0]

        logger.debug('Retorno da execução: %s', streamdata.decode())
        logger.info('Executou comando R com status %s.', p.returncode)

        if (p.returncode != 0):
            return
        
        storage.salvar_data_processamento(id_relatorio, os.path.basename(file_path))

    
    shutil.rmtree(working_path, ignore_errors=True)

    logger.info('Preparando para envio do diagrama de %s em %s com destinatário a %s.', estados, [
                data_inicio, data_fim], email)

    with open(file_path, 'rb') as f:
        send_email(
            email, f'Relatório de densidade municipal por período - {", ".join(estados)}, {_formatar_intervalo(data_inicio, data_fim)}', 'relatorio_densidade_municipal.pdf', f.read())
