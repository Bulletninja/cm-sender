import yaml
import sendgrid
from smtpapi import SMTPAPIHeader
import requests
import json
from sender import Sender


url = "/companies/.json"
querystring = {"auth":""}
response = requests.request("GET", url,params=querystring)
companies = json.loads(response.text)
companies_with_appointment = [companies[company_id] for company_id in companies if companies[company_id].get('appointments')]

with open('cfg.yml', 'r') as ymlfile:
    config = yaml.load(ymlfile)

def send_sms(de="+5216681610296", para="+525549998687", notes="holi :]",  account_sid = config["sms"]["sid"] ,auth_token = config["sms"]["key"]):
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body=notes,to=de,from_=para)
    print(message.sid)

client = sendgrid.SendGridClient(config['mail']['key'])
for company in companies_with_appointment:
    for appointment_id in company['appointments']:
        appt = company['appointments'][appointment_id]
        sndr = Sender(company, appt)
        sndr.send()
        #New mail
        message = sendgrid.Mail()
        message.set_from(config['mail']['from_transaction'])
        message.set_from_name(config['mail']['from_transaction_name'])

        message.add_category('Reminder')
        message.add_filter('templates', 'enable', '1')
        message.add_filter('templates', 'template_id', '28f15464-d6e7-4b5e-aa57-6a1d0829a1d6')

        message.set_replyto('-replyto-')
        message.set_subject('Hola {}, este es un recordatorio de Clinicamia'.format(appt['patient']))
        message.set_html('Hola {}, tienes una cita en {}, mañana a las {}'.format(appt['patient'], appt['location'], appt['start_time'])

        message.add_to([company['patients'][appt['patient_id']]['email']])
        #message.set_substitutions({'-name-': ['Pablo', 'Alberto'],'-where-':['el consultorio', 'el hospital'],'-when-':['el martes', 'el lunes'], '-replyto-':['reply@to.mx', 'reply2@to.mx']})

        status, msg = client.send(message)
        print(status, msg)
