from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
import json
from lxml import etree

@dataclass
class Item:
  product_id:int
  name:str
  slot:any
  paint:str
  certification:str
  certification_value:int
  certification_label:str
  quality:str
  create:str
  tradeable:int
  amount:int
  instance_id:int


def read_inventory(filename:str):
  with open(filename, 'r') as f:
    content = f.read()
  
  items = []
  for product_line in content.split('\n'):
    try:
      items.append(Item(*product_line.split(',')))
    except TypeError:
      pass # a comma in name
  return items


inventory = read_inventory('inventory.csv')
# inventory = [item for item in inventory if item.slot != 'Blueprint']
# inventory = [item for item in inventory if item.tradeable == 'true']
# for tradeable in inventory:
#   try:
#     response = search_av_price(tradeable)
#   except Exception as e:
#     print('unexpected error' + e.__repr__())
#   if response:
#     lower_bound, higher_bound = response
#     print(lower_bound, higher_bound)
#     with open('output.txt', 'a+') as f:
#       f.write(f'{tradeable.name},{lower_bound},{higher_bound}\n')