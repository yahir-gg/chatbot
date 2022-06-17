#requisitos
# To be able to convert text to Speech
#pip install SpeechRecognition  #(3.8.1)
#To convey the Speech to text and also speak it out
#pip install gTTS  #(2.2.3)
#pip install pipwin
#pipwin install pyaudio
#pip install pygame
#pip install mutagen
import hist_academico_file
#import getData

from transformers import AutoTokenizer
from transformers import pipeline
import speech_recognition as sr
from pygame import mixer
from gtts import gTTS
import pandas as pd
import pyaudio
import mutagen
import time
import json
import os
import re


# -------------------------------------------------------------------F U N C I O N E S 

def leer_data_ueas():
  with open('data_ueas.json') as file:
    data_ueas = json.load(file)
  return data_ueas

def leer_data_profesores():
  with open('data_profesores.json') as file:
    data_profesores = json.load(file)
  return data_profesores

def leer_data_clases():
  with open('data_clases.json') as file:
    data_clases = json.load(file)
  return data_clases

# Entrega informacion de uea (nombre, clave, grupos, horararios y profesor)
def get_info_uea(id_interno):
  data_ueas = leer_data_ueas()
  if id_interno != 'link':
    informacion = list(filter(lambda item: item['id_interno'] == id_interno, data_ueas['ueas']))
    respuesta = '''Nombre de la uea: '''+informacion[0]['nombre']+'''
Clave de la uea: '''+informacion[0]['clave']
    if len(informacion[0]['grupo']) > 0:
      for i in range(len(informacion[0]['grupo'])):
        respuesta += '''\n\nGrupo: '''+informacion[0]['grupo'][i]['grupo']+'''\nProfesor:'''+informacion[0]['grupo'][i]['profesor']+'''
\nHorario '''+informacion[0]['grupo'][i]['horario']+'''\nSalón: '''+informacion[0]['grupo'][i]['salon']
      return respuesta
    else:
      return respuesta + '\nEl curso no se imparte en el actual trimestre'
  else:
    return 'Las ueas que se imparten en el actual trimestre las puedes consultar en: https://n9.cl/ueas-22i'

# Entrega solo los nombres de las materias
def materias_por_trimestre(clave):
  if clave != 'datata':
    data_ueas = leer_data_ueas()
    x = trimestres.get(clave)
    nombres = ''
    try:
      for e in range(len(x)):
        informacion = list(filter(lambda item: item['clave'] == x[e], data_ueas['ueas']))
        nombres += informacion[0]['nombre']+'\n'
    except:
      for e in range(len(x)):
        informacion = list(filter(lambda item: item['id_interno'] == x[e], data_ueas['ueas']))
        nombres += informacion[0]['nombre']+'\n'
    return nombres
  else:
    return 'Las materias que se imparten en el actual trimestre las puedes consultar en el siguiente link: <a href="https://n9.cl/ueas-22i" target="_blank">https://n9.cl/ueas-22i</a> '

# Genera contexto con clases actuales
def get_contexto_clases():
  df = pd.read_csv('clases.csv')  
  clases={}
  clases['clases']=[]

  contexto_clases =''
  for i in range(len(df)):
    if i<9:
      id = '0'+str(i+1)
    else:
      id = i+1
    #contexto_clases += 'Informacion de la uea '+str(id)+': materia, profesor, clave, horario y salon estan en '+'pclase'+str(id)+'\n'
    contexto_clases += 'Informacion de la uea '+str(id)+': '+'pclase'+str(id)+'\n'
  return contexto_clases

# Entrega datos del profesor a buscar (nombre, cargo e informacion)
def get_datos_profe(id_profe):
  print('Buscando clave:', id_profe)
  data_profesores = leer_data_profesores()
  x = list(filter(lambda item: item['id'] == id_profe, data_profesores['profesores']))
  print(x)
  if len(x) > 0:
    str_datos_prof = f"Nombre: {x[0]['nombre']}\nCargo: {x[0]['cargo']}\nDatos: {x[0]['información']}"
    return str_datos_prof
  else:
    return 'No se encontraron datos del profesor '

def do_context_ueas():
  data_ueas = leer_data_ueas()  
  contexto_ueas = ''
  for e in data_ueas['ueas']:
    contexto_ueas += 'Los datos de '+e['nombre']+': '+e['id_interno']+'.\n'
  return contexto_ueas

def do_context_profesores():
  data = leer_data_profesores()
  str_data_profes=''
  for elem in data['profesores']:
    str_data_profes += 'Los datos del profesor '+elem['nombre'] +': '+ elem['id'] +'.\n'
  return str_data_profes

def get_recomendacion(hist_academico):
  data_ueas = leer_data_ueas()
  claves_uea=[]
  
  for elem in data_ueas['ueas']:
    claves_uea.append(elem['clave'])
  
  ueas_no_registradas = []
  for elem in hist_academico:
    if elem not in claves_uea:
      ueas_no_registradas.append(elem)
  #ueas_no_registradas

  all_ueas_a_recomendar=[]
  for elem in data_ueas['ueas']:
    if elem['clave'] not in hist_academico:
      all_ueas_a_recomendar.append(elem)
  ueas_a_recomendar=all_ueas_a_recomendar[:5]
  str_recomendacion = ''
  for elem in ueas_a_recomendar:
    str_recomendacion +=  elem['nombre']+'\n'
  
  return str_recomendacion
# -------------------------------------------------------------------T R A N S F O R M E R S  

contexto_trimestres = '''
Las materias que deben inscribir en el trimestre número 1 son datat1.
Las materias que deben inscribir en el trimestre número 2 son datat2. 
Las materias que deben inscribir en el trimestre número 3 son datat3.
Las materias que deben inscribir en el trimestre número 4 son datat4. 
Las materias que deben inscribir en el trimestre número 5 son datat5. 
Las materias que deben inscribir en el trimestre número 6 son datat6.
Las materias que deben inscribir en el trimestre número 7 (siete) son datat7. 
Las materias que deben inscribir en el trimestre número 8 son datat8.
Las materias que deben inscribir en el trimestre número 9 son datat9.
Las materias que deben inscribir en el trimestre número 10 son datat10.
Las materias que deben inscribir en el trimestre número 11 son datat11. 
Las materias que deben inscribir en el trimestre número 12 son datat12.
Las materias que se imparten en el actual trimestre son: datata
'''
# Clave -> Número de trimestre / Valor-> ueas que se cursan en dicho trimestre
trimestres={
      'datat1':['4000005','4000007','4000008','4600000'],
      'datat2':['4502002','4502004','4600001','4600005'],
      'datat3':['4502001','4600002','4600009','4600012'],
      'datat4':['4210011','4502003','4600006','4600017'],
      'datat5':['4210025','4502007','4600011','4600013','4600020'],
      'datat6':['4210013','4502006','4502015','4600018','4600021'],
      'datat7':['4210018','4502008','4502009','4502010','4502016'],
      'datat8':['4502011','4502012','4502013','4502014','4502017'],
      'datat9':['4502051','4502052','4502053','4502054'],
      'datat10':['datau41','datau44','datau45','datau46'],
      'datat11':['datau42','datau47','datau48','datau49'],
      'datat12':['datau43','datau50','datau51'],
      'datata': 'https://n9.cl/ueas-22i'
}

# diccionario de optativas de orientacion
optativas_orientacion =[
  {
      'id':'4502021',
      'nombre': 'Bases de datos avanzadas'
  },
 {
     'id': '4502026',
      'nombre': 'Seminario de sistemas de información I'
 },
 {
     'id': '4502027',
      'nombre': 'Seminario de sistemas de información II'
 },
 {
     'id': '4502028',
      'nombre': 'Inteligencia Artificial II'
 },
 {
     'id': '4502032',
      'nombre': 'Seminario de sistemas inteligentes I'
 },
  {
     'id': '4502033',
      'nombre': 'Seminario de sistemas inteligentes II'
 },
 {
     'id': '4502034',
      'nombre': 'Computación inalambrica y móvil'
 },
 {
     'id': '4502036',
      'nombre': 'Seminario de Tecnologías de la información I'
 },
 {
     'id': '4502037',
      'nombre': 'Seminario de Tecnologías de la información II'
 }
]

contexto_ueas = do_context_ueas()
contexto_profesores = do_context_profesores()

contexto = ''
contexto = contexto_ueas+contexto_profesores+contexto_trimestres

tokenizer = AutoTokenizer.from_pretrained('mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es')

nlp = pipeline(
    'question-answering', 
    model='mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es',
    tokenizer=tokenizer
)


# redireccion de preguntas comunes
def preguntar(enunciado):
  enunciado = '¿'+enunciado+'?'
  print('Preguntando: ',enunciado)
  long_answer = nlp({
    'question': enunciado,
    'context': contexto
  })
  short_answer = long_answer['answer']
  print('SHORTANSW:',short_answer)
  
  if enunciado.find('recom') != -1:
      hist_academico = hist_academico_file.get_ha()
      recomendacion = get_recomendacion(hist_academico)
      return recomendacion
  else: 
    if len(short_answer.split()) == 1:
      if short_answer[4] == 'p':
        datos = get_datos_profe(short_answer)
      elif short_answer[4] == 'u':
        datos = get_info_uea(short_answer)
      elif short_answer[4] == 't':
        datos = materias_por_trimestre(short_answer)
      return datos
    else:
      respuesta_larga = short_answer.split()
      short_answer = respuesta_larga[-1]
      if short_answer[4] == 'p':
        datos = get_datos_profe(short_answer)
      elif short_answer[4] == 'u':
        datos = get_info_uea(short_answer)
      elif short_answer[4] == 't':
        datos = materias_por_trimestre(short_answer)
      return datos
    
      
pa = pyaudio.PyAudio()
pa.get_default_input_device_info()
{'defaultLowOutputLatency': 0.008707482993197279, 
 'maxOutputChannels': 32, 
 'hostApi': 0, 
 'defaultSampleRate': 44100.0, 
 'defaultHighOutputLatency': 0.034829931972789115, 
 'name': 'default', 
 'index': 15, 
 'maxInputChannels': 32,
 'defaultHighInputLatency': 0.034829931972789115, 
 'defaultLowInputLatency': 0.008707482993197279, 
 'structVersion': 2}
#pyaudio.pa.__file_


# Beginning of the AI
class ChatBot():
     name=""
     def __init__(self, name):
          print("----- starting up", name, "-----")
          self.name = name
          self.despidos = 'gracias'
     def speech_to_text(self):
          recognizer = sr.Recognizer()
          with sr.Microphone() as mic:
               print("listening...")
               audio = recognizer.listen(mic)
          try:
               self.text = recognizer.recognize_google(audio, language="es-ES")
               print("yo ---> ", self.text)
               #respuesta = preguntar(self.text)
               #tranformar_respuesta = getUeaName(respuesta)
               #print(tranformar_respuesta)
          except:
               print("yo -->  ERROR")
               exit()
     def wake_up(self,text):
          return True if self.name in text.lower() else False
     def bye(self,text):
          return True if self.despidos in text.lower() else False     
     @staticmethod
     def know_mp3_duration(mp3_path):
          audio = mutagen.File(mp3_path)
          longitud = audio.info.length
          minutos, segundos = divmod(longitud, 60)
          minutos, segundos = int(minutos), int(segundos)
          return (minutos*60)+segundos
     @staticmethod
     def text_to_speech(text):
          print(ChatBot.name+" --> ", text)
          speaker=gTTS(text=text,lang="es", slow=False)
          speaker.save("res.mp3")
          mixer.init()
          mixer.music.load("res.mp3")
          length=ChatBot.know_mp3_duration("res.mp3")
          #print("duración: "+str(length))
          mixer.music.play()
          #os.system("start res.mp3")
          time.sleep(length+1)
          mixer.music.stop()
          mixer.music.unload()
          #os.remove("res.mp3")
     
# iniciar chatbot terminal
def trabaja_bot():
      chatbot_name="tutor"
      ai = ChatBot(name=chatbot_name)
      while True:
           ai.speech_to_text()
           if ai.wake_up(ai.text) is True:
                res="Hola Soy "+chatbot_name+", ¿Qué puedo hacer por ti?"
                ai.text_to_speech(res)
           elif ai.bye(ai.text) is True:
                res = 'Espero haberte ayudado. Adios'
                ai.text_to_speech(res)
           else:
                respuesta = preguntar(ai.text)
                print('Preguntando: ',ai.text)
                ai.text_to_speech(respuesta)
      return respuesta

# Execute the AI
if __name__ == "__main__":
     trabaja_bot()
     