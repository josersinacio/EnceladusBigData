from send_email import send_email
from subprocess import Popen, PIPE, STDOUT
import logging
import glob
from pathlib import Path
import os.path
import os

logger = logging.getLogger(__name__)

queimaduras_folder = os.path.join(
    Path.home(), '.enceladus', 'queimaduras', 'densidade-municipal-por-periodo')


def _formatar_intervalo(data_inicio: str, data_fim: str):
    if data_inicio == data_fim:
        return f'em {data_inicio}'
    
    return f'entre {data_inicio} e {data_fim}'

def preparar_e_enviar_relatorio_async(estado: str, data_inicio: str, data_fim: str, email: str):

    logger.info(f'Obtendo registros de queimaduras para %s %s.',
                estado, _formatar_intervalo(data_inicio, data_fim))

    os.makedirs(queimaduras_folder, exist_ok=True)

    file_path = os.path.join(
        queimaduras_folder, f'{estado}.{data_inicio}.{data_fim}.pdf')

    print(file_path)

    if not os.path.exists(file_path):
        p = Popen(['Rscript', 'poc2/relatorio_queimaduras_sim.R', estado,
                  data_inicio, data_fim, file_path], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

        streamdata = p.communicate()[0]

        logger.debug('Retorno da execução: %s', streamdata.decode())
        logger.info('Executou comando R com status %s.', p.returncode)

        if (p.returncode != 0):
            return
    
    logger.info('Preparando para envio do diagrama de %s em %s com destinatário a %s.', estado, [
                data_inicio, data_fim], email)


    with open(file_path, 'rb') as f:
        send_email(email, f'Relatório de densidade municipal por período - {estado}, {_formatar_intervalo(data_inicio, data_fim)}', 'relatorio_densidade_municipal.pdf', f.read())


def listar_relatorios_processados():

    arquivos_pdf = []

    for file in glob.glob(os.path.join(queimaduras_folder, '*.pdf')):
        nome_base = os.path.basename(file).split('.')

        arquivos_pdf.append(dict(
            estado=nome_base[0],
            data_inicio=nome_base[1],
            data_fim=nome_base[2],
            uri=f'/relatorios/queimaduras/densidade-municipal-por-periodo/{".".join(nome_base)}',
        ))


    return arquivos_pdf


def ler_relatorio(relatorio: str):
    with open(os.path.join(queimaduras_folder, relatorio), 'rb') as f:
        return f.read()
