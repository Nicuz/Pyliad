#!/usr/bin/env python
__author__ = "Domenico Majorana"

import re
import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://www.iliad.it/account/"
LOGIN_INFO = {'login-ident': 'VOSTRO_ID_UTENTE', 'login-pwd': 'VOSTRA_PASSWORD'}

LABELS = ["Chiamate", "SMS inviati", "MMS inviati", "Dati utilizzati"]
PATTERNS = ['Chiamate: <span class="red">(.*)</span><br/>', \
    r'<div class="conso__text"><span class="red">(\d+) SMS</span>', \
    r'<span class="red">(\d+) MMS<br/></span>', '<span class="red">(.*)</span> / (.*)<br/>']
CONSUMI_ITALIA = []
CONSUMI_ESTERO = []

def info_linea():
    '''
    Ritorna info sulla linea attiva
    '''
    print("\nINFORMAZIONI SULLA LINEA")
    #Nome e cognome
    print("Intestatario: {nome}".format(
        nome=re.compile(r'<div class=\"bold\">(.*)</div>').search(str(HTML)).group(1)))
    #ID utente
    print("ID utente: {id}".format(
        id=re.compile(r'ID utente: (\d+.\d+)').search(HTML.text).group(1)))
    #Numero associato alla SIM Iliad
    print("Numero: {numero}".format(
        numero=re.compile(r'Numero: (\d+.\d+)').search(HTML.text).group(1)))
    #Credito residuo
    print("\nCREDITO RESIDUO\n{credito}".format(
        credito=re.compile(r'- Credito : <b class="red">(\d.+.(.|,)?)</b>').search(
            str(HTML)).group(1)))

def consumi():
    '''
    Indici:
    0 - Chiamate
    1 - SMS
    2 - MMS
    3 - Dati
    '''
    for x_0 in range(len(LABELS)):
        if x_0 == 3:
            CONSUMI_ITALIA.append(re.findall(re.compile(PATTERNS[x_0]), str(HTML))[0][0])
            CONSUMI_ESTERO.append(re.findall(re.compile(PATTERNS[x_0]), str(HTML))[1][0])
            break
        CONSUMI_ITALIA.append(re.findall(re.compile(PATTERNS[x_0]), str(HTML))[0])
        CONSUMI_ESTERO.append(re.findall(re.compile(PATTERNS[x_0]), str(HTML))[1])

    print("\nCONSUMI IN ITALIA:")
    for x_1, _ in enumerate(LABELS):
        if x_1 == 3:
            print("{label}: {consumo} / {totale}".format(
                label=LABELS[x_1],
                consumo=CONSUMI_ITALIA[x_1],
                totale=re.findall(re.compile(PATTERNS[3]), str(HTML))[0][1]))
            break
        print("{label}: {consumo}".format(
            label=LABELS[x_1],
            consumo=CONSUMI_ITALIA[x_1]))

    print("\nCONSUMI ALL'ESTERO:")
    for x_2, _ in enumerate(LABELS):
        if x_2 == 3:
            print("{label}: {consumo} / {totale}\n".format(
                label=LABELS[x_2],
                consumo=CONSUMI_ESTERO[x_2],
                totale=re.findall(re.compile(PATTERNS[3]), str(HTML))[1][1]))
            break
        print("{label}: {consumo}".format(
            label=LABELS[x_2],
            consumo=CONSUMI_ESTERO[x_2]))

with requests.session() as s:
    # fetch the login page
    s.get(LOGIN_URL)

    # post to the login form
    RESPONSE = s.post(LOGIN_URL, data=LOGIN_INFO)
    HTML = BeautifulSoup(RESPONSE.content, "html.parser")

if "ID utente o password non corretto." in HTML.text:
    print("Errore durante il login. ID utente o password non corretto.")
else:
    info_linea()
    consumi()
