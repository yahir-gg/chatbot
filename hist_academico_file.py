#!pip install selenium
#!apt-get update 
#!apt install chromium-chromedriver

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver = webdriver.Chrome('./chromedriver')
from selenium.webdriver.common.by import By
from selenium.webdriver.common import by
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def get_ha():
  driver.get('https://juno.uam.mx:8443/sae/cua/aewbf001.omuestraframes?mod=1')

  user = "2183033830"
  password = 'Pumadrid78'
  # Navegacion por frames hasta encontrar los input user y password
  driver.switch_to.frame("bodyFrame")
  WebDriverWait(driver, 3).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"controlFrame")))
  WebDriverWait(driver, 3).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"menuFrame")))
  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'menu')))
  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, 'form')))
  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#menu > form > table > tbody')))
  input_user = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr:nth-child(2) > td > input[type=text]')))
  input_pass = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr:nth-child(4) > td:nth-child(1) > input:nth-child(1)')))
  login_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr:nth-child(5) > td:nth-child(1) >input.ir:nth-child(1)'))) 

  # envio de datos
  input_user.send_keys(user)
  input_pass.send_keys(password)
  login_button.click()

  # Acceso a la seccion kardex
  datapage = driver.find_element(by=By.LINK_TEXT,value="Kardex").get_attribute('href')
  driver.execute_script("window.open('');")
  driver.switch_to.window(driver.window_handles[1])
  driver.get(datapage)
  # escribo HTML del kardex completo
  with open("grades.html", "w") as f:
      f.write(driver.page_source)

  # Lectura del HTML
  with open("grades.html") as fp:
      soup = BeautifulSoup(fp, 'html.parser')

  # Obtener tabla de calificaciones
  x = soup.find('table',id="t1")

  #Nuevo archivo HTML solo con tabla
  with open("gradesTable.html", "w") as f2:
      f2.write(str(x))
  info = pd.read_html('gradesTable.html')
  info[0].columns = ['Registro','UEA','Nombre','Trimestre','Tipo Eval','Calificacion','No Acta','Creditos']
  data = info[0][['UEA','Nombre','Calificacion']]
  data = data.query("Calificacion == 'S' or Calificacion == 'B' or Calificacion == 'MB'").reset_index(drop=True)
  ha = list(data['UEA'])
  for i in range(len(ha)):
    ha[i] = str(ha[i])
  os.remove('grades.html')
  os.remove('gradesTable.html')
  return ha