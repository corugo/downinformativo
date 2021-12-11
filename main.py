import requests
import os
from os import path
from datetime import datetime, timedelta
import zipfile
import shutil

if os.path.exists("informativo.mp4"):
    os.remove("informativo.mp4")

offset = 0
print("Dia da semana: " + str(datetime.now().strftime('%w')))
if int(datetime.now().strftime('%w')) == 0:
    offset = 6
elif int(datetime.now().strftime('%w')) == 1:
    offset = 5
elif int(datetime.now().strftime('%w')) == 2:
    offset = 4
elif int(datetime.now().strftime('%w')) == 3:
    offset = 3
elif int(datetime.now().strftime('%w')) == 4:
    offset = 2
elif int(datetime.now().strftime('%w')) == 5:
    offset = 1

print("Offset: " + str(offset))
ano = datetime.strftime(datetime.now() + timedelta(days=offset),'%Y')[2:]
print("ano: " + str(ano))
mes = datetime.strftime(datetime.now() + timedelta(days=offset),'%m')
print("mes: " + str(mes))
dia = datetime.strftime(datetime.now() + timedelta(days=offset),'%d')
print("dia: " + str(dia))
print("informativo_{2}{1}{0}_alta.zip".format(ano, mes, dia))
diaSemana = datetime.strftime(datetime.now() + timedelta(days=offset),'%w')
trimestre = 0

def baixar_arquivo(url, endereco=None):
    if endereco is None:
        endereco = os.path.basename(url.split("?")[0])
    resposta = requests.get(url, stream=True)
    if resposta.status_code == requests.codes.OK:
        print("iniciando download")
        with open(endereco, 'wb') as novo_arquivo:
            for parte in resposta.iter_content(chunk_size=256):
                novo_arquivo.write(parte)
            print("Download finalizado. Arquivo salvo em: {}".format(endereco))
    else:
        resposta.raise_for_status()

def verifica_trimestre():
    if (int(mes)<=3):
        return 1
    elif (int(mes)<=6):
        return 2
    elif (int(mes)<=9):
        return 3
    else:
        return 4

trimestre = verifica_trimestre()
print("Trimestre: " + str(trimestre))
url_informativo = "https://files.adventistas.org/daniellocutor/informativo/{3}trimestre20{0}/informativo_{2}{1}{0}_alta.zip".format(ano, mes, dia, trimestre)
baixar_arquivo(url_informativo)
with zipfile.ZipFile("informativo_{2}{1}{0}_alta.zip".format(ano, mes, dia, trimestre),"r") as zip_ref:
    zip_ref.extractall("targetdir")
if path.exists("informativo.mp4"):
    os.remove("{0}\\informativo.mp4".format(os.getcwd()))
os.rename(r'{4}\targetdir\informativo_{2}{1}{0}_alta.mp4'.format(ano, mes, dia, trimestre, os.getcwd()),r'{0}\informativo.mp4'.format(os.getcwd()))
#os.rmdir("targetdir")
shutil.rmtree('targetdir')
#os.system('rmdir /S /Q "{}"'.format(os.getcwd()+"targetdir"))
os.remove("informativo_{2}{1}{0}_alta.zip".format(ano, mes, dia))

