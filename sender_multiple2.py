import yaml
import sendgrid
import requests
import json
import datetime
from smtpapi import SMTPAPIHeader
from sender import Sender

url = "/companies/.json"
querystring = {"auth":""}
response = requests.request("GET", url,params=querystring)
companies = json.loads(response.text)
companies_with_appointment = [companies[company_id] for company_id in companies if companies[company_id].get('appointments')]

#is it a tomorrow's appointment??
pop_idx = []
n = len(companies_with_appointment)
for company_idx in range(n):
    tmp_appointment = companies_with_appointment[company_idx]['appointments'].copy()
    for appointment_id in companies_with_appointment[company_idx]['appointments']:
        fbdate = datetime.datetime.strptime(tmp_appointment[appointment_id]['date'], "%a %b %d %Y").ctime()
        tomorrow = (datetime.date.today()+datetime.timedelta(days=1)).ctime()
        if not fbdate == tomorrow:
            tmp_appointment.pop(appointment_id, None)
    if tmp_appointment == {}:
        pop_idx.append(company_idx)
    else:
        companies_with_appointment[company_idx]['appointments'] = tmp_appointment

companies_with_appointment = [companies_with_appointment[i] for i in range(n) if i not in pop_idx]

with open('cfg.yml', 'r') as ymlfile:
    config = yaml.load(ymlfile)

for company in companies_with_appointment:
    for appointment_id in company['appointments']:
        appt = company['appointments'][appointment_id]
        appt['company'] = company['name']
        sndr = Sender(company, appt)
        sndr.send()
