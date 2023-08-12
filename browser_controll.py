from flask import Flask
import os
import json
import threading
import time
import sys

# logging options
import logging
log = logging.getLogger('werkzeug')
log.disabled = True

class ChromeBrowser:
  def __init__(self, **configs):
    self.app = Flask(__name__)
    self.app.logger.disabled = True
    self.add_endpoint('/load_buffer', 'load_buffer', self.load_buffer)
    self.command_buffer = [{'action': 'wait_for_connection'}]
    self.run(port=5000)
  
  def wait_for_response(self):
    self.add_command({'action':'wait_for_connection'})
    while len(self.command_buffer) > 0:
      time.sleep(.7)
      print('waiting for buffer')
  
  def find_element(self, *args):
    self.add_command({'action':'reset-search'})
    for arg in args:
      if arg[0] == '#':
        method = 'id'
        self.add_command({'action':'search-element', 'method':method, 'value':arg[1:]})
      elif arg[0] == '.':
        method = 'class'
        index = 0
        self.add_command({'action':'search-element', 'method':method, 'value':arg[1:], 'list-index':index})
      else:
        method = 'tag'
        index = 0
        self.add_command({'action':'search-element', 'method':method, 'value':arg, 'list-index':index})
      

  def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET', 'OPTIONS'], *args, **kwargs):
    self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

  def run(self, **kwargs):
    # os.system('"C:/Program Files (x86)\Google\Chrome\Application\chrome.exe" --new-window https://rocket-league.com/')
    try:
      print('starting Chrome Controller')
      thread = threading.Thread(target=self.app.run, kwargs=kwargs)
      thread.daemon = True
      thread.start()
      print('Chrome Controller started')
    except KeyboardInterrupt:
      pass
      # print('exiting')
      # sys.exit()
    # self.app.run(**kwargs)
  
  def load_buffer(self):
    bckp_buffer = self.command_buffer
    self.command_buffer = [] # empty buffer
    response = json.dumps({"success":True, "command_buffer":bckp_buffer})
    return response
  
  def add_command(self, command):
    self.command_buffer.append(command)

if __name__ == '__main__':
  browser = ChromeBrowser()