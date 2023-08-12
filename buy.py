from browser_controll import ChromeBrowser
from pricing import search_av_price
import time
import json

LINK = '/trading?filterItem=966&filterCertification=0&filterPaint=0&filterSeries=A&filterTradeType=0&filterMinCredits=0&filterMaxCredits=100000&filterPlatform%5B%5D=1&filterSearchType=1&filterItemType=0'

class Buyer(ChromeBrowser):
  def __init__(self):
    super().__init__()
    # ...

  def get_items(self):
    self.execute('set_location', {'location':LINK})
    self.execute('get_market_items')
    data = self.response_data
    # with open('output.json', 'w+') as f:
    #   json.dump(data, f)
    self.analyse_trades(data)

  def analyse_trades(self, data):
    trade_advantages = []
    for trade in data:
      if len(trade['has']) == len(trade['wants']):
        # an item in 'has' matches an item in 'wants'
        for index in range(len(trade['has'])):
          item_has = trade['has'][index]
          item_wants = trade['wants'][index]
          advantage = self.calculate_trade_advantage(item_has, item_wants)
          print(advantage)
          if advantage:
            trade_advantages.append({'advantage':advantage, 'tradeID':trade['id'], 'has':item_has, 'wants':item_wants})
    print(sorted(trade_advantages, key=lambda x:x['advantage'], reverse=True))
  
  def calculate_trade_advantage(self, item_has:dict, item_wants):
    if item_has['name'] != 'Credits' and item_wants['name'] == 'Credits' and not('Blueprint' in item_has['name']):
      price = int(item_wants['quantity'])
      av_price = search_av_price(item_has['name'], item_has['paint'])
      if av_price:
        if price < av_price[0]:
          if av_price[0]-price > 100:
            # scam/error/bug
            pass
          else:
            # print(item_has['name'], price, av_price)
            return av_price[0]-price



if __name__ == '__main__':
  buyer = Buyer()
  buyer.get_items()
  # with open('output.json', 'r') as f:
  #   buyer.analyse_trades(json.load(f))
