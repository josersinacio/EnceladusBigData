from datasus_utils import download_dataset
from default_config import defaultConfig
from send_email import send_email
import pandas as pd
import logging


logger = logging.getLogger(__name__)

def preparar_e_enviar_async(estados: list, anos: list, email: str):

    logger.info(f'Obtendo registros de queimaduras para %s em %s.', estados, anos)

    dataframe = pd.concat([
        pd.DataFrame.from_dict(download_dataset(estado, int(ano))) 
            for estado in estados
            for ano in anos
    ])

    logger.info('Obtidos %s registros do SIM.', len(dataframe.index))

    dataframe = dataframe[[
        'CIRCOBITO', 'DTOBITO', 'DTNASC', 'SEXO', 'RACACOR', 'ESTCIV', 'ESC', 'OCUP', 'CODMUNRES', 'LOCOCOR', 'ASSISTMED', 'CAUSABAS', 'CAUSABAS_O'
    ]]

    codigos = []

    for _, value in defaultConfig.codigos_cid10().items():
        for item in value:
            codigos.append(item)

    queimaduras_dataframe = dataframe[
        dataframe['CAUSABAS'].isin(codigos) | dataframe['CAUSABAS_O'].isin(codigos)
    ]

    logger.info('%s registros após filtrar por queimaduras para %s em %s.', len(queimaduras_dataframe.index), estados, anos)

    resultado_csv = queimaduras_dataframe.to_csv()

    logger.info('Preparando para envio do relátorio de %s em %s com destinatário a %s.', estados, anos, len(queimaduras_dataframe.index))

    # send_email('JosueP.Viana@gmail.com', f'Relatório para {estados_param} em {anos_param}', resultado_csv)
    send_email(email, f'Relatório para {", ".join(estados)} em {", ".join(anos)}', resultado_csv)
    