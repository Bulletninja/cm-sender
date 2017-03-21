from firebase import firebase
from sender import Sender
from pprint import pprint
firebaseio_url = ''
firebApp = firebase.FirebaseApplication(firebaseio_url, None)
res = firebApp.get('/', None)

appointment = res['companies']['-KBKWZHl1n8r05Oh15gV']['appointments']['-KCIIy9-S-vM5RfZP3_p']
company = res['companies']['-KBKWZHl1n8r05Oh15gV']
gera = company['patients']['-KCII2ucKgZpW8w5nA04']
data = {'name': gera['first_name'], 'replyto': gera['email'], 'where': company['name'], 'when': appointment['date']}
sndr = Sender()
#sndr.set_data(data)
sndr.send()
#{'birthday': 'Tue Nov 22 1988',
# 'email': 'gerardo@quody.co',
# 'first_name': 'Gerardo',
# 'gender': 'Male',
# 'last_name': 'Dominguez',
# 'phones': [{'number': '', 'type': 'Mobile'}],
# 'reminder_type': '3',
# 'timestamp': 1457391419157,
# 'title': 'Zombie Lord'}
#pprint(res)
#pprint(res['companies']['-KBKWZHl1n8r05Oh15gV']['patients']['-KCII2ucKgZpW8w5nA04'])
