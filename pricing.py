import requests
import json

PAINT_DICT = {
  'Titanium White': 'white',
  'Grey':'grey',
  'Crimson':'crimson',
  'Pink':'pink',
  'Cobalt':'cobalt',
  'Skye Blue':'sblue',
  'Burnt Sienna':'sienna',
  'Saffron':'saffron',
  'Lime':'lime',
  'Forest Green':'fgreen',
  'Orange':'orange',
  'Purple':'purple'
}

def search_av_price(itemname:str, paint=None):
  response = requests.post(
    'https://rl.insider.gg/api/itemSearchEngine',
    data=json.dumps({"languageID":0,"query":itemname}))
  try:
    data = response.json()
  except requests.exceptions.JSONDecodeError:
    # no search results
    return False
  if 'options' in data:
    data = data['options'][0]
  try:
    uri = data['uri']
  except KeyError:
    return False

  if paint:
    try:
      uri += '/'+PAINT_DICT[paint]
    except KeyError:
      # unexpected paint like 'Painted set'
      return False

  # get price of item
  response = requests.get('https://rl.insider.gg/en/pc/'+uri)
  try:
    price = response.text.split('id="matrixRow0"')[1].split('</tr>')[0].split('</div>')[-1].split('<td>')[1].split('</td>')[0]
  except IndexError:
    # no price found
    # print('')
    return False
  if price == '&emsp;': #error
    return False
  lower, higher = price.split(' - ')
  if ' k' in higher:
    lower = int(lower)*1000
    higher = int(higher.split(' k')[0])*1000
  else:
    lower, higher = int(lower), int(higher)
  return lower, higher