from browser_controll import ChromeBrowser
import time

class Seller(ChromeBrowser):
  def sell(self, itemname:str, price:int):
    self.execute('set_location', {'location':'/trading/new'})
    self.execute('select_slot', {'side':'has', 'index':0})
    self.execute('select_inventory_item', {'name':itemname})
    self.execute('select_slot', {'side':'wants', 'index':0})
    self.execute('select_inventory_item', {'name':'credits'})
    self.execute('select_slot', {'side':'wants', 'index':0})
    self.execute('set_credit_amount', {'value':price})
    self.execute('set_note', {'text':'Just emptying my inventory.'})



if __name__ == '__main__':
  seller = Seller()
  seller.sell('Venom', 150)