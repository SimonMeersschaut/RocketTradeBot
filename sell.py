from browser_controll import ChromeBrowser
import time

class Seller(ChromeBrowser):
  def sell(self, itemname:str, price:int):
    self.execute('select_slot', {'side':'has', 'index':1})
    self.execute('select_inventory_item', {'name':'breakout'})
    self.execute('select_slot', {'side':'wants', 'index':1})
    self.execute('select_inventory_item', {'name':'credits'})
    self.execute('select_slot', {'side':'wants', 'index':1})
    self.execute('set_credit_amount', {'value':200})



if __name__ == '__main__':
  seller = Seller()
  seller.sell('fennec', 550)