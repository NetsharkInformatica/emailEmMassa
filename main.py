import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from variaveisambiente import chave

contaSendGrid= SendGridAPIClient(chave)
email=Mail(from_email="heliotome@netshark.com.br",to_emails=["netsharkinformatica@gmail.com"],
           subject="email enviado pelo sendgrid",plain_text_content="este email foi enviado via api do sendgrid")


resposta=contaSendGrid.send(email)
print(resposta.status_code)