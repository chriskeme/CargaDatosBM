from tkinter import *
from tkinter import filedialog
import json
import requests
import pandas as pd
import datetime
import time
import os
import tkinter.scrolledtext as tkscrolled

#path = "carga domicilios.csv"
path = "Base direccionesCSV - copia.csv"
#path = "prueba.csv"
logTxt = open("log.txt", "w")
logTxt.write("")
logTxt.close()
logTxt = open("log.txt", "a")
TokenNoti = 'eyJhbGciOiJIUzUxMiJ9.eyJidXNpbmVzc0lkIjoiTWVMaU5vdGlmaWNhY2lvbmVzIiwibmFtZSI6IkNocmlzdGlhbiBIZXJuYW4gU2NoZXR0aW5vIiwiYXBpIjp0cnVlLCJpZCI6InpuR1pwbVBCbDhSS1RlZ2NuQ2JrcVNJb2xHOTIiLCJleHAiOjE3NjE0Mjg3NDEsImp0aSI6InpuR1pwbVBCbDhSS1RlZ2NuQ2JrcVNJb2xHOTIifQ.gdZ4XoOuNngG09MmKwA963oN6xzQPwshiwaHBVlg12-tMWn1GYQaR37izdU9yZL9rSlrL5vgp_Jm8YT1XPsYlQ'


def GetContactId(p_email):

    byEmailUrl = "https://go.botmaker.com/api/v1.0/customer/byEmail"
    payload = {}
    headers = {
        'access-token': TokenNoti,
        'Accept': 'application/json',
        'customerEmail': p_email.lower()
    }
    response = requests.request("GET", byEmailUrl, headers=headers, data=payload)
    try:
        ContactId = json.loads(response.text.encode('utf8'))
        return ContactId['PLATFORM_CONTACT_ID']
    except:
        return ''


def actUser(email, direccion):

    contactId = GetContactId(email)

    url = "https://go.botmaker.com/api/v1.0/customer"
    variables = "{'direccion':'"+direccion+"'}"
    payload = "chatPlatform=MESSENGER&platformContactId="+contactId+"&variables="+variables
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'charset': 'utf-8',
        'access-token': TokenNoti
    }

    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
    try:
        resultado = response.reason
        return contactId+' '+resultado
    except:
        return contactId+' Error'

def recorroEmails():
    try:
      df = pd.read_csv(path, sep=';')
      datos = df.to_dict('records')
    except Exception as e:
      logTxt.write( "Error en la obtención del archivo \n")
      return

    logTxt.write( "-Cantidad de usuarios a actualizar: "+str(len(datos))+".\n")
    segTot = len(datos) * 0.7
    min = segTot // 60
    logTxt.write( "-Tiempo aproximado de la ejecución completa: "+ str(min) +" min.\n\n")
    print( "-Tiempo aproximado de la ejecución completa: "+ str(min) +" min.\n\n")
    indx_n = 0
    try:
        for email in datos:
           #result="Error"#Comentar
           encoded_string = email['direccion'].encode("iso-8859-1", "ignore")
           email['direccion'] = encoded_string.decode("iso-8859-1", "ignore")

           result = actUser(email['email'], email['direccion'])#Descomentar
           logTxt.write(email['email']+"\t"+result+"\n")
           print(email['email']+"\t"+result)
           indx_n += 1
    except Exception as e:
        logTxt.write("se produjo un error en la lectura del archivo, por favor chequear el formato en la linea "+str(indx_n)+' :'+e)
        return
    return

def iniciar():
    today = datetime.date.today()
    fecha = today.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")
    logTxt.write("####Inicio del proceso "+fecha+"\n\n")
    recorroEmails()
    today = datetime.date.today()
    fecha = today.strftime("%d/%m/%Y") + ' ' + time.strftime("%H:%M:%S")
    logTxt.write("\n\n####Proceso finalizado "+fecha)

iniciar()