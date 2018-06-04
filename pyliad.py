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

with requests.session() as s:
    # fetch the login page
    s.get(login_url)

    # post to the login form
    response = s.post(login_url, data=login_info)
    html = BeautifulSoup(response.content, "html.parser")

print "\nINFORMAZIONI SULLA LINEA"
#Nome e cognome
print "Intestatario:",re.compile(r'<div class=\"bold\">(.*)</div>').search(str(html)).group(1)
#ID utente
print "ID utente:",re.compile(r'ID utente: (\d+.\d+)').search(html.text).group(1)
#Numero associato alla SIM Iliad
print "Numero:",re.compile(r'Numero: (\d+.\d+)').search(html.text).group(1)
#Credito residuo
print "\nCREDITO RESIDUO\n",re.compile(r'- Credito : <b class="red">(\d.+.(.|,)?)</b>').search(str(html)).group(1)

consumi_italia.append(re.findall(re.compile(patterns[0]), str(html))[0]) #chiamate
consumi_italia.append(re.findall(re.compile(patterns[1]), str(html))[0]) #SMS
consumi_italia.append(re.findall(re.compile(patterns[2]), str(html))[0]) #MMS
consumi_italia.append(re.findall(re.compile(patterns[3]), str(html))[0][0]) #dati utilizzati
labels.append(re.findall(re.compile(patterns[3]), str(html))[0][1]) #dati inclusi nella tariffa, indice nell'array = 4

print "\nCONSUMI IN ITALIA:"
for x in range(0,len(labels)-1):
    if x == 3:
        print labels[x],consumi_italia[x],"/",labels[x+1]
        break
    print labels[x],consumi_italia[x]

consumi_estero.append(re.findall(re.compile(patterns[0]), str(html))[1]) #chiamate
consumi_estero.append(re.findall(re.compile(patterns[1]), str(html))[1]) #SMS
consumi_estero.append(re.findall(re.compile(patterns[2]), str(html))[0]) #MMS
consumi_estero.append(re.findall(re.compile(patterns[3]), str(html))[1][0]) #dati utilizzati
labels.append(re.findall(re.compile(patterns[3]), str(html))[1][1]) #dati inclusi nella tariffa, indice nell'array = 5

print "\nCONSUMI ALL'ESTERO:"
for x in range(0,len(labels)-2):
    if x == 3:
        print labels[x],consumi_estero[x],"/",labels[x+2],"\n"
        break
    print labels[x],consumi_estero[x]
