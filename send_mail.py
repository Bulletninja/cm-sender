import sendgrid
import yaml

s = open("./cfg.yaml", encoding="utf-8").read()
config = yaml.load(s)

client = sendgrid.SendGridClient(config["mail"]["key"])
message = sendgrid.Mail()

message.add_to("luis.valenzuela@mustache.mx")
message.set_from("")#from email
message.set_subject("Probando la api de sendgrid")
message.set_html("Funciona si marco <b>ESTO</b> como negritas???")

client.send(message)
