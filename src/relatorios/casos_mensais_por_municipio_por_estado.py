from send_email import send_email
from subprocess import Popen, PIPE, STDOUT
import storage
import logging
from pathlib import Path
import os.path
import os

logger = logging.getLogger(__name__)

relatorios_folder = os.path.join(
    Path.home(), '.enceladus', 'relatorios', 'queimaduras', 'casos-mensais-por-municipio-por-estado')

id_relatorio = 'CASOS_MENSAIS_POR_MUNICIPIO_POR_ESTADO'

os.makedirs(relatorios_folder, exist_ok=True)


def _formatar_intervalo(ano_inicio: int, ano_fim: int):
    if ano_inicio == ano_fim:
        return f'em {ano_fim}'

    return f'entre {ano_inicio} e {ano_fim}'


def ler_relatorio(relatorio: str):
    with open(os.path.join(relatorios_folder, relatorio), 'rb') as f:
        return f.read()

def preparar_e_enviar_diagrama_async(estados: str, ano_inicio: int, ano_fim: int, email: str):

    logger.info(f'Obtendo registros de queimaduras para %s %s.',
                estados, _formatar_intervalo(ano_inicio, ano_fim))

    file_path = os.path.join(relatorios_folder, f'{"-".join(estados)}.{ano_inicio}.{ano_fim}.pdf')

    if not os.path.exists(file_path):
        p = Popen(['Rscript', 'rscripts/casos_mensais_por_municipio_por_estado.R', ','.join(estados),
                ano_inicio, ano_fim, file_path], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

        streamdata = p.communicate()[0]

        logger.debug('Retorno da execução: %s', streamdata.decode())
        logger.info('Executou comando R com status %s.', p.returncode)

        if (p.returncode != 0):
            return

        storage.salvar_data_processamento(id_relatorio, os.path.basename(file_path))

    logger.info('Executou comando R com status %s.', p.returncode)

    if (p.returncode == 0):
        logger.info('Preparando para envio do diagrama de %s em %s com destinatário a %s.', estados, [
                    ano_inicio, ano_fim], email)

        with open(file_path, 'rb') as f:
            send_email(
                email, f'Diagrama de distribuição do local de falecimento para {", ".join(estados)}, {_formatar_intervalo(ano_inicio, ano_fim)}', 'relatorio.pdf', f.read())
