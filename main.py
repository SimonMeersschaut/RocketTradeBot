from selenium import webdriver
from selenium import common
import selenium
from selenium.webdriver.common.keys import Keys
import time
import threading
import pymsgbox
import json
import os

def message():
  pymsgbox.alert('Trade found!', 'Title')

USERNAME_ERROR = '!Fill in the username form under .gitignore and restart the program!'
try:
  with open('.gitignore/user.json', 'r') as f:
    content = json.load(f)
    email = content['email']
    password = content['password']
    if email == 'put your email here' or password == 'put your password here':
      input(USERNAME_ERROR)
      exit()
except FileNotFoundError:
  try:
    os.mkdir('.gitignore')
  except FileExistsError:
    pass
  _ = open('.gitignore/user.json', "w")
  with open('.gitignore/user.json', 'w') as f:
    f.write('{"email":"put your email here", "password":"put your password here"}')
  input(USERNAME_ERROR)
  exit()

chat_message = "I'm interested"
max_credits = 400
link = f"https://rocket-league.com/trading?filterItem=1892&filterCertification=0&filterPaint=0&filterSeries=A&filterMinCredits=0&filterMaxCredits={max_credits}&filterPlatform%5B%5D=1&filterSearchType=1&filterItemType=1"
max_minutes = 15
reload = 10#seconds

def searchBy(value, by='id'):
  found = False
  element = None
  while not found:
    try:
      element = driver.find_element(by=by, value=value)
      if element != None:
        return element
    except common.exceptions.NoSuchElementException:
        pass
      
def start_checking():
  driver.refresh()
  while True:
    cards = driver.find_elements_by_class_name('rlg-trade')
    for card in cards:
      try:
        wants = card.find_element_by_class_name('rlg-trade__itemswants ').find_elements_by_css_selector("*")
        has = card.find_element_by_class_name('rlg-trade__itemshas ').find_elements_by_css_selector("*")
      except Exception as e:
        print('!ERROR: '+str(e))
        continue
      print(len(wants))
      if len(wants) == len(has):
        return card
      text = card.find_element_by_class_name('rlg-trade__time').find_elements_by_css_selector("*")[0].get_attribute('innerHTML')
      print(card.find_element_by_class_name('rlg-trade__time').get_attribute('innerHTML'))
      print(text)
      if not('minute' in text) or int(text.split(' ')[0]) > max_minutes:
        return None

def send_message():
  time.sleep(1)
  element = searchBy('messagetext', 'id')
  element.send_keys(Keys.TAB)
  element.clear()
  element.send_keys(chat_message)
  input('.')
  searchBy('messagetext', 'id').send_keys(chat_message)

def login():
  
  driver.find_element_by_xpath('/html/body/header/section[1]/div/div[2]/div/a[1]').click()
  driver.find_element_by_xpath('/html/body/main/main/section/div/div/div[1]/form/input[2]').send_keys(email)
  driver.find_element_by_xpath('/html/body/main/main/section/div/div/div[1]/form/input[3]').send_keys(password)
  time.sleep(.5)
  driver.find_element_by_xpath('/html/body/main/main/section/div/div/div[1]/form/input[4]').click()


def setup():
  driver.get(link)
  searchBy('acceptPrivacyPolicy', 'id').click() #COOCKIES
  succes = False
  while not succes:
    try:
      searchBy('/html/body/div[1]/div/div/div/div[2]/div/button[2]', by='xpath').click() #PRIVACY
      succes = True
    except:
      time.sleep(1)
  login()
  searching = True
  while searching:
    card = start_checking()
    if card != None:
      searching = False
    else:
      time.sleep(reload)
  
  t1 = threading.Thread(target=message)
  t1.start()
  card.find_element_by_class_name('rlg-trade__meta').click()
  send_message()
  
  #card.click()
  

if __name__ == '__main__':
  driver = webdriver.Chrome()
  setup()