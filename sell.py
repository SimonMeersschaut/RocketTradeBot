from browser_controll import ChromeBrowser
import time

class Seller(ChromeBrowser):
  def sell(self, itemname:str, price:int):

    self.wait_for_response() # wait for client to connect with server
    print('client connected')

    self.add_command({'action':'location', 'href':"https://rocket-league.com/trading/new"})
    self.wait_for_response()
    time.sleep(2)
    self.wait_for_response()

    # enter item name
    self.select_slot('has', 0)
    self.select_inventory_item(itemname)
    self.wait_for_response()

    # add credits
    self.select_slot('wants', 0)
    self.select_inventory_item('credits')
    self.wait_for_response()
    
    # select price
    self.select_slot('wants', 0)
    print('waiting')
    # time.sleep(3)
    print('waitin')
    self.find_element('#amount_credits')
    self.add_command({"action":"send-keys", "text":str(price)})
    self.add_command({'action':'dispatch-event', 'event-name':'change'})
    self.find_element('.fa fa-times rlg-popup-options-close')
    self.wait_for_response()
    self.add_command({'action':'click'})
    self.wait_for_response()

    # submit
    self.find_element('.rlg-btn-process-trade rlg-btn-trade-form g-recaptcha rlg-btn-primary prevent')
    self.add_command({'action':'click'})

    input('done??')
  
  def select_inventory_item(self, itemname:str):
    # enter name
    self.find_element('#trade-selector-all-items', '.rlg-trade-selector-header --with-padding', 'input')
    self.add_command({"action":"send-keys", "text":itemname})
    # wait
    self.wait_for_response()
    # click item
    time.sleep(.5)
    print('sending clicker')
    self.find_element('#trade-items-all', '.row')
    self.add_command({'action':'search-element', 'method':'class', 'value':'rlg-trade-selector-section', 'visible':'true'})
    self.add_command({'action':'search-element', 'method':'class', 'value':'rlg-item rlg-creator-item ', 'visible':'true'})
    print('end of clicker')
    self.wait_for_response()
    input("OKOOKKOOKOOOKOKOKOK")
    self.add_command({'action':'click'})
    self.wait_for_response()
  
  def select_slot(self, container:str, slot_index:int):
    '''
      container:
          - 'wants'
          - 'has'
    '''
    self.find_element('.rlg-trade__items'+container) # wants/has
    self.add_command({'action': 'search-element', 'method':'class', 'value':'rlg-item', 'list-index':slot_index}) # take the first slot in items want
    self.add_command({'action':'click'})



if __name__ == '__main__':
  seller = Seller()
  seller.sell('fennec', 550)