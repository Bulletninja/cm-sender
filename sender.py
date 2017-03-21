# -​*- coding: utf-8 -*​-
import yaml
import sendgrid
from smtpapi import SMTPAPIHeader
#from twilio.rest import TwilioRestClient
import plivo
from time import gmtime, strftime, strptime
weekday = {0: "Domingo", 1: "Lunes", 2:"Martes", 3:u"Miércoles",
4: "Jueves", 5: "Viernes", 6:u"Sábado"}

class Sender():
	with open('cfg.yml', 'r') as ymlfile:
		config = yaml.load(ymlfile)
	#instantiate sendgrid client
	sendgrid_client = sendgrid.SendGridClient(config['mail']['key'])
	# #configure twilio parameters
	# account_sid = config["sms"]["sid"]
	# auth_token = config["sms"]["key"]
	# #instantiate twilio client
	# twilio_client = TwilioRestClient(account_sid, auth_token)
	# twilio_text = ''
	# twilio_phone = config["sms"]["from"]
	# patient_phone = '+5216681610296'

	#plivo config
	auth_id = config["sms"]["auth_id"]
	auth_token = config["sms"]["auth_token"]
	plivo_client = plivo.RestAPI(auth_id, auth_token)
	params = {
		'src': config["sms"]["from"],# Sender's phone number with country code
		'dst': '5216681610296',# Receiver's phone Number with country code
		'text': u'',# Your SMS Text Message - English
		'url': 'http://example.com/report/',# The URL to which with the status of the message is sent
		'method': 'POST'# The method used to call the url
	}


	sendgrid_message = sendgrid.Mail()
	def __init__(self, company, appt):
		self.sendgrid_message.set_from(self.config['mail']['from_transaction'])
		self.sendgrid_message.set_from_name(self.config['mail']['from_transaction_name'])

		self.sendgrid_message.add_category('Reminder')
		self.sendgrid_message.add_filter('templates', 'enable', '1')
		self.sendgrid_message.add_filter('templates', 'template_id', '28f15464-d6e7-4b5e-aa57-6a1d0829a1d6')

		#self.sendgrid_message.add_to([company['patients'][appt['patient_id']]['email']])
		#self.sendgrid_message.add_to('pablo@castelo.mx')
		self.sendgrid_message.add_to('luis.valenzuela@mustache.mx')
		self.sendgrid_message.set_replyto('hola@clinicamia.com')
		self.sendgrid_message.set_subject(u'Hola {}, este es un recordatorio de Clinicamia'.format(appt['patient']))


		#self.sendgrid_message.set_html(u'Hola {}, tienes una cita en {}, mañana a las {}'.format(appt['patient'], appt['location'], appt['start_time']))
		self.sendgrid_message.set_html(u'<br>')
		self.sendgrid_message.add_substitution('-name-', appt['patient'])
		self.sendgrid_message.add_substitution('-practitioner-', appt['practitioner_name'])
		self.sendgrid_message.add_substitution('-company-', appt['company'])
		self.sendgrid_message.add_substitution('-appointment_date-', weekday[int(strftime("%w",strptime(appt['date'], "%a %b %d %Y")))])
		self.sendgrid_message.add_substitution('-appointment_time-', strftime('%I:%M %p', strptime(appt['start_time'].replace(' (MDT)', ''), '%H:%M:%S %Z%z')))

		#self.twilio_text = 'Hola {}, tienes una cita en {}, mañana a las {}'.format(appt['patient'], appt['location'], appt['start_time'])
		self.params['text'] = u'Hola {}, tienes una cita en {}, mañana a las {}'.format(appt['patient'], appt['location'], strftime('%I:%M %p', strptime(appt['start_time'].replace(' (MDT)', ''), '%H:%M:%S %Z%z')))
		print(appt)
		#self.patient_phone = company['patients'][appt['patient_id']]['phones'][0]['number']
		#self.params['dst'] = company['patients'][appt['patient_id']]['phones'][0]['number']

	def send(self, send_email = True, send_sms = True):
		status, msg = self.sendgrid_client.send(self.sendgrid_message) #if send_email
		#twilio_message = self.twilio_client.messages.create(body=self.twilio_text,to= self.patient_phone,from_= self.twilio_phone) #if send_sms
		response = self.plivo_client.send_message(self.params)

		#print("Twilio message id: ", twilio_message.sid)
		print("Plivo response: ", response)
		print("Sendgrid status: ", status, "Sendgrid message: ", msg)
