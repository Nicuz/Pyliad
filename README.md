# Pyliad
<p align="center">
  <img src="https://github.com/Nicuz/Pyliad/blob/master/images/pyliad.png" width="70%">
</p>

Come suggerisce il nome, Pyliad è un semplice script realizzato in python che efettua il login sul sito di Iliad e restituisce tutte le informazioni sulla propria linea ed i relativi consumi sia in Italia che all'estero.

**ATTENZIONE:**
> Al momento non è presente una gestione degli errori, prestate attenzione alle credenziali di accesso!

## Requisiti
* requests
* BeautifulSoap

Entrambi i moduli si possono installare tramite ```pip```

## Utilizzo
Una volta scaricato lo script è necessario inserire le proprie credenziali nella riga 8 sostituendo "VOSTRO_ID_UTENTE" e "VOSTRA_PASSWORD" rispettivamente con l'ID utente generato da Iliad e la password di accesso al sito. In seguito salvare il file ed eseguirlo col comando:

```python pyliad.py```
