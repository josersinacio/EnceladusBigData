from default_config import defaultConfig
from send_email import send_email
from subprocess import Popen, PIPE, STDOUT
import logging
from pathlib import Path
import os.path
import os

logger = logging.getLogger(__name__)


def _formatar_intervalo(ano_inicio: int, ano_fim: int):
    if ano_inicio == ano_fim:
        return f'em {ano_fim}'
    
    return f'entre {ano_inicio} e {ano_fim}'

def preparar_e_enviar_tabela_async(estados: list, ano_inicio: int, ano_fim: int, email: str):

    logger.info(f'Obtendo registros de queimaduras para %s %s.', estados, _formatar_intervalo(ano_inicio, ano_fim))

    queimaduras_folder = os.path.join(Path.home(), '.enceladus', 'queimaduras')

    os.makedirs(queimaduras_folder, exist_ok=True)

    file_path = os.path.join(queimaduras_folder, f'{".".join(estados)}.{ano_inicio}.{ano_fim}.csv')


    p = Popen(['Rscript', 'poc/tabela_queimaduras_sim.R', ','.join(estados), ano_inicio, ano_fim, file_path], stdout=PIPE, stdin=PIPE, stderr=STDOUT)   

    streamdata = p.communicate()[0]
    print(streamdata.decode())


    logger.info('Executou comando R com status %s.', p.returncode)


    if (p.returncode == 0):
        logger.info('Preparando para envio do relátorio de %s em %s com destinatário a %s.', estados, [ano_inicio, ano_fim], email)

        with open(file_path) as f:
            send_email(email, f'Relatório para {", ".join(estados)} {_formatar_intervalo(ano_inicio, ano_fim)}',  'relátorio.pdf', f.read())

def preparar_e_enviar_diagrama_async(estados: str, ano_inicio: int, ano_fim: int, email: str):

    logger.info(f'Obtendo registros de queimaduras para %s %s.', estados, _formatar_intervalo(ano_inicio, ano_fim))

    queimaduras_folder = os.path.join(Path.home(), '.enceladus', 'queimaduras')

    os.makedirs(queimaduras_folder, exist_ok=True)

    file_path = os.path.join(queimaduras_folder, f'{".".join(estados)}.{ano_inicio}.{ano_fim}.pdf')


    p = Popen(['Rscript', 'poc/diagrama_queimaduras_sim.R', ','.join(estados), ano_inicio, ano_fim, file_path], stdout=PIPE, stdin=PIPE, stderr=STDOUT)   

    streamdata = p.communicate()[0]
    print(streamdata.decode())


    logger.info('Executou comando R com status %s.', p.returncode)


    if (p.returncode == 0):
        logger.info('Preparando para envio do diagrama de %s em %s com destinatário a %s.', estados, [ano_inicio, ano_fim], email)

        with open(file_path, 'rb') as f:
            send_email(email, f'Diagrama de distribuição do local de falecimento para {", ".join(estados)}, {_formatar_intervalo(ano_inicio, ano_fim)}', 'diagrama.pdf', f.read())
    