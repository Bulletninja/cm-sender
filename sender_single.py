import yaml
import sendgrid
from smtpapi import SMTPAPIHeader

with open('cfg.yml', 'r') as ymlfile:
	config = yaml.load(ymlfile)

client = sendgrid.SendGridClient(config['mail']['key'])
message = sendgrid.Mail()

message.set_from(config['mail']['from_transaction'])
message.set_from_name(config['mail']['from_transaction_name'])

message.add_category('Reminder')
message.add_filter('templates', 'enable', '1')
message.add_filter('templates', 'template_id', '28f15464-d6e7-4b5e-aa57-6a1d0829a1d6')

message.add_to('pablo@castelo.mx')

message.set_replyto('-replyto-')
message.set_subject('Hola -name-, este es un recordatorio de Clinicamia')
message.set_html('<h2>Hola -name-,</h2></br>Este es un recordatorio para que vayas a que te arreglen los dientes en -where- -when-.')
message.add_substitution('-name-', 'Hugo')
message.add_substitution('-where-', 'el consultorio')
message.add_substitution('-when-', 'el martes 3 de febrero')
message.add_substitution('-replyto-', 'pablo+prueba@castelo.mx')

status, msg = client.send(message)
print(status, msg)
