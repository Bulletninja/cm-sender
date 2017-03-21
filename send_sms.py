#!/usr/bin/env python
import sys
import argparse as ap
from twilio.rest import TwilioRestClient
import yaml

s = open("./cfg.yaml", encoding="utf-8").read()
config = yaml.load(s)
def send_sms(de="+5216681610296", para="+525549998687", notes="holi :]",  account_sid = config["sms"]["sid"] ,auth_token = config["sms"]["key"]):
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body=notes,to=de,from_=para)
    print(message.sid)


if __name__=="__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("--to", "-t" , help="Destino")
    parser.add_argument("--source", "-s", help="Origen")
    parser.add_argument("--message", "-m", help="Mensaje")
    args = parser.parse_args()
    #initialize if void
    if args.to==None:
        args.to="+5216681610296"
    if args.source==None:
        args.source="+525549998687"
    if args.message==None:
        args.message="holi :]"
    #print args.to, args.source, args.message
    send_sms(args.to, args.source, args.message)
#    print args
