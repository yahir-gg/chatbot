from bs4 import BeautifulSoup # pip install beautifulsoup4
import pandas as pd
import requests
import json
import re

# Obtiene los datos de ueas, genera contexto de ueas y genera archivo
def get_data_ueas():
  headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
  }

  url = 'http://dccd.cua.uam.mx/Licenciatura_en_Tecnologias_y_Sistemas_de_Informacion'
  data_ueas = {}
  data_ueas['ueas']=[]
  respuesta = requests.get(url, headers=headers)

  soup = BeautifulSoup(respuesta.text)
  contenedor_de_preguntas = soup.find(id="div16") # ENCONTRAR UN ELEMENTO POR ID
  lista_de_preguntas = contenedor_de_preguntas.find('div', class_="col-md-12") # ENCONTRAR VARIOS ELEMENTOS POR TAG Y POR CLASE
  lista_de_preguntas_2 = lista_de_preguntas.find_all('p')
  lista_de_preguntas_2 = list(lista_de_preguntas_2)
  span_list = lista_de_preguntas_2[0].findAllNext('span')

  for elem in lista_de_preguntas_2:
    while elem.find_next('span') != None:
      elem.find_next('span').decompose()

  for elem in lista_de_preguntas_2:
    if elem.text == '':
      lista_de_preguntas_2.remove(elem)
  
  id_interno = 1
  for elem in lista_de_preguntas_2:
    
    if elem.text[0].isdigit():
      aux = elem.text.split()
      clave = aux[0]
      nombre = " ".join(aux[1:])
      #print(id_interno,clave,nombre)
      if id_interno < 10:
        id_interno = '0'+str(id_interno)
      if len(clave)<7:
        nueva_clave=''
        i=0
        for i in range(len(clave)):
          #print('e',e)
          if i != 4:
            nueva_clave = nueva_clave+clave[i]
            #print('Se aladio: ',elem['clave'][i])
            i+=1
          else:
            #print('c4')
            nueva_clave = nueva_clave+'0'
            nueva_clave = nueva_clave+clave[i]
            #print('Se añadio: ','0')
            #print('Se añadio: ',elem['clave'][i])
            i+=1
      else:
        nueva_clave=clave
      data_ueas['ueas'].append({
        'id': str(id_interno),
        'id_interno': 'datau'+str(id_interno),
        'clave': str(nueva_clave),
        'nombre': nombre,
        'grupo': []
      })
      id_interno=int(id_interno)
      id_interno+=1
  for elem in range(0,4):
    data_ueas['ueas'].append({
        'id': str(len(data_ueas['ueas'])+1),
        'id_interno': 'datau'+str(len(data_ueas['ueas'])+1),
        'clave': '-',
        'nombre': 'Optativa de orientacion',
        'grupo':[]
    })
    
  for elem in range(0,4):
    data_ueas['ueas'].append({
        'id': str(len(data_ueas['ueas'])+1),
        'id_interno': 'datau'+str(len(data_ueas['ueas'])+1),
        'clave': '-',
        'nombre': 'Optativa Divisional o Interdivisional',
        'grupo':[]
    })
  data_ueas['ueas'].append({
        'id_interno': 'link',
        'clave': 'link',
        'nombre': 'https://n9.cl/ueas-22i'
    })
  with open('data_ueas.json', 'w') as file:
    json.dump(data_ueas, file, indent=4)
  #return data_ueas
  return None

# Obtiene los datos de profesores, genera contexto de profesores y genera archivo JSON
def get_data_prof():  
  data_profesores = {}
  data_profesores['profesores']=[]
  headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
  }

  url = 'http://dccd.cua.uam.mx/Directorio'
  respuesta = requests.get(url, headers=headers)

  soup = BeautifulSoup(respuesta.text)
  contenedor_de_preguntas = soup.find(id="panel4") # ENCONTRAR UN ELEMENTO POR ID
  lista_de_preguntas = contenedor_de_preguntas.find('div', class_="row") # ENCONTRAR VARIOS ELEMENTOS POR TAG Y POR CLASE
  #lista_de_preguntas2 = lista_de_preguntas.find('div', class_="col-lg-4 col-md-6 mb-r") # ENCONTRAR VARIOS ELEMENTOS POR TAG Y POR CLASE
  lista_de_preguntas_2 = lista_de_preguntas.find_all('div', class_="col-lg-4")
  #print(len(lista_de_preguntas_2))
  id_interno = 1
  str_data_profes=''
  for elem in lista_de_preguntas_2:
    nombre = elem.find('h6', class_="card-title")
    cargo = nombre.find_next('h6')
    info = cargo.find_next('p')
    clean_info = " ".join(re.split(r"\s+",info.text))
    #print("agregando",str(id_interno),nombre.text,cargo.text,clean_info)
    str_data_profes += 'Los datos del profesor '+nombre.text+': '+ 'datap'+ str(id_interno)+'.\n'
    numeros = re.findall('[0-9]+',clean_info)
    grado = ''
    for e in clean_info:
      if e.isdigit() == False:
        grado+=e
      else:
        break
    tel = numeros[0]
    telefono = ''
    for e in range(len(tel)):
      #print(e)
      if e % 2 == 0 and e!=0:
        telefono += ' '+tel[e]
      else:
        telefono += tel[e]
    telefono
    ext = numeros[1]
    if len(numeros) > 2:
      cubiculo = numeros[2]
    else:
      cubiculo = ''
    #identificar correo  
    y = clean_info.split()
    for e in y:
      h = re.findall("[@]", e)
      if h:
        correo = e
    info = grado+'\nTeléfono: '+telefono+' \nExtensión: '+ext+''+' \nEmail: '+correo
    data_profesores['profesores'].append({
        'id': 'datap'+str(id_interno),
        'clave': 'datap'+str(id_interno),
        'nombre': nombre.text,
        'cargo': cargo.text,
       'información': info
    })
    #print(clean_info.split())
    id_interno+=1
      #z.find('br').decompose()
      #print("Nombre: ",x.text)
      #print("Cargo: ",y.text)
      #print("Información: ",z.text)
  with open('data_profesores.json', 'w') as file:
    json.dump(data_profesores, file, indent=4)
  return None

# Lee archivo csv de clases del trimestre actual y lo pasa a JSON
def get_data_clases():
  df = pd.read_csv('clases.csv')  
  data_clases={}
  data_clases['clases']=[]

  for i in range(len(df)):
    if i < 10:
      id_interno = '0'+str(i+1)
    else:
      id_interno = i 
    data_clases['clases'].append({
      #'id': str(id_interno),
      'clave': str(df.loc[i,'clave']),
      'nombre': str(df.loc[i,'materia']),
      'grupo': str(df.loc[i,'grupo']),
      'profesor': str(df.loc[i,'profesor']),
      'horario': str(df.loc[i,'horario']),
      'salon': str(df.loc[i,'salon']),
      'id_interno': 'pclase'+str(id_interno)
    })
  with open('data_clases.json', 'w') as file:
    json.dump(data_clases, file, indent=4)
  data_clases_corregida = corregir_claves(data_clases)
  #return data_clases_corregida
  return None

# Corrige las claves a siete digitos
def corregir_claves(data_clases):
  #data_clases = leer_data_ueas()
  for elem in data_clases['clases']:
    if elem['clave']!='-':
      if len(elem['clave'])<7:
        nueva_clave=''
        i=0
        for i in range(len(elem['clave'])):
          #print('e',e)
          if i != 4:
            nueva_clave = nueva_clave+elem['clave'][i]
            #print('Se aladio: ',elem['clave'][i])
            i+=1
          else:
            #print('c4')
            nueva_clave = nueva_clave+'0'
            nueva_clave = nueva_clave+elem['clave'][i]
            #print('Se añadio: ','0')
            #print('Se añadio: ',elem['clave'][i])
            i+=1
          
        elem['clave']=nueva_clave
  return data_clases

def leer_data_ueas():
  with open('data_ueas.json') as file:
    data_ueas = json.load(file)
  return data_ueas

def leer_data_clases():
  with open('data_clases.json') as file:
    data_clases = json.load(file)
  return data_clases

# Agregar grupo y horario al archivo de las ueas
def add_grupo_horario():
  data_ueas = leer_data_ueas()
  #print(data_ueas)
  data_clases1 = leer_data_clases()
  data_clases = corregir_claves(data_clases1)
  #print(data_clases)
  for uea in data_ueas['ueas']:
    #print(uea['clave'])
    x = list(filter(lambda item: item['clave'] == uea['clave'], data_clases['clases'])) 
    #print(x)
    lista=[]
    for clase in x:
      #uea.update({'grupo':clase['grupo']})
      lista.append({
          'grupo':clase['grupo'],
          'horario':clase['horario'],
          'profesor': clase['profesor'],
          'salon': clase['salon']
      })
    uea.update({'grupo':lista})
  with open('data_ueas.json', 'w') as file:
    json.dump(data_ueas, file, indent=4)


if __name__ == "__main__":      
    # hacemos los archivos JSON
    get_data_ueas()
    get_data_clases()
    get_data_prof()
    add_grupo_horario()
    print('Archivos creados con exito')