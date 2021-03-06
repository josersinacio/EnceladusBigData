import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging

logger = logging.getLogger(__name__)


def send_email(to: str, subject: str, file_name: str,  attachment: str):
    SENDER = 'Enceladus Big Data <enceladus.bigdata@hotmail.com>'
    RECIPIENT = to
    CONFIGURATION_SET = 'Default'
    SUBJECT = subject

    AWS_REGION = 'us-east-2'

    BODY_TEXT = (f'{subject}\r\n'
                 'This email was sent with Amazon SES using the '
                 'AWS SDK for Python (Boto).'
                 )

    # The HTML body of the email.
    BODY_HTML = f"""<html>
    <head></head>
    <body>
    <h1>{subject}</h1>
    <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
                """

    CHARSET = 'UTF-8'

    ATTACHMENT = file_name

    client = boto3.client('ses', region_name=AWS_REGION)

    msg = MIMEMultipart('mixed')

    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = RECIPIENT

    msg_body = MIMEMultipart('alternative')

    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    att = MIMEApplication(attachment)

    att.add_header('Content-Disposition', 'attachment', filename=ATTACHMENT)

    msg.attach(msg_body)

    msg.attach(att)

    try:
        logger.info(
            'Enviando relatório por e-mail com destinatário para %s.', to)

        response = client.send_raw_email(
            Destinations=[
                RECIPIENT
            ],
            RawMessage={
                'Data': msg.as_string(),
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        logger.error('Erro ao enviar e-mail',
                     e.response['Error']['Message'], exc_info=True)
    else:
        logger.info("E-mail enviado! ID da mensagem: %s",
                    response['MessageId'])
