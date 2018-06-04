#!/usr/bin/env python
__author__ = "Domenico Majorana"

import requests, re
from bs4 import BeautifulSoup

login_url = "https://www.iliad.it/account/"
login_info = {'login-ident': 'VOSTRO_ID_UTENTE', 'login-pwd': 'VOSTRA_PASSWORD'}

labels = ["Chiamate:", "SMS inviati:", "MMS inviati:", "Dati utilizzati:"]
patterns = ['Chiamate: <span class="red">(.*)</span><br/>', '<div class="conso__text"><span class="red">(\d+) SMS</span>', '<span class="red">(\d+) MMS<br/></span>', '<span class="red">(.*)</span> / (.*)<br/>']
consumi_italia = []
consumi_estero = []

def info_linea():
    print "\nINFORMAZIONI SULLA LINEA"
    #Nome e cognome
    print "Intestatario:",re.compile(r'<div class=\"bold\">(.*)</div>').search(str(html)).group(1)
    #ID utente
    print "ID utente:",re.compile(r'ID utente: (\d+.\d+)').search(html.text).group(1)
    #Numero associato alla SIM Iliad
    print "Numero:",re.compile(r'Numero: (\d+.\d+)').search(html.text).group(1)
    #Credito residuo
    print "\nCREDITO RESIDUO\n",re.compile(r'- Credito : <b class="red">(\d.+.(.|,)?)</b>').search(str(html)).group(1)

def consumi():
    '''
    Indici:
    0 - Chiamate
    1 - SMS
    2 - MMS
    3 - Dati
    '''
    for x in range(0,len(labels)):
        if x == 3:
            consumi_italia.append(re.findall(re.compile(patterns[x]), str(html))[0][0])
            consumi_estero.append(re.findall(re.compile(patterns[x]), str(html))[1][0])
            break
        consumi_italia.append(re.findall(re.compile(patterns[x]), str(html))[0])
        consumi_estero.append(re.findall(re.compile(patterns[x]), str(html))[1])

    print "\nCONSUMI IN ITALIA:"
    for x in range(0,len(labels)):
        if x == len(labels)-1:
            print labels[x],consumi_italia[x],"/",re.findall(re.compile(patterns[3]), str(html))[0][1]
            break
        print labels[x],consumi_italia[x]

    print "\nCONSUMI ALL'ESTERO:"
    for x in range(0,len(labels)):
        if x == len(labels)-1:
            print labels[x],consumi_estero[x],"/",re.findall(re.compile(patterns[3]), str(html))[1][1],"\n"
            break
        print labels[x],consumi_estero[x]

with requests.session() as s:
    # fetch the login page
    s.get(login_url)

    # post to the login form
    response = s.post(login_url, data=login_info)
    html = BeautifulSoup(response.content, "html.parser")

if "ID utente o password non corretto." in html.text:
    print "Errore durante il login. ID utente o password non corretto."
else:
    info_linea()
    consumi()
