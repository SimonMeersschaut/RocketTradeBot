from flask import Flask, request
import os
import json
import threading
import time
import sys

# logging options
# import logging
# log = logging.getLogger('werkzeug')
# log.disabled = True

class ChromeBrowser:
  def __init__(self, **configs):
    self.app = Flask(__name__)
    # self.app.debug = True
    # self.app.logger.disabled = True
    
    self.add_endpoint('/load_buffer', 'load_buffer', self.load_buffer)
    self.add_endpoint('/register_execution', 'register_execution', self.register_execution, methods=['POST'])
    self.add_endpoint('/post_response_data', 'post_response_data', self.post_response_data, methods=['POST'])
    # self.add_endpoint('/connected', 'connected', self.connected, methods=['POST'])

    self.command = None
    self.executed = False
    self.waiting_for_response_data = False
    self.response_data = None
    self.run(port=5000)
    time.sleep(2)
    # self.wait_for_connection()
  
  # def connected(self):
  #   self.connected = True
  #   return {'success': True}
  
  def wait_for_connection(self):
    print('[SESSION] waiting for connection')
    while not self.connected:
      time.sleep(1)
    print('[SESSION] connected!')
  
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
  
  def load_buffer(self):
    ''' webserver request to load the load_buffer '''
    if not self.command:
      response = json.dumps({"success":True, "command_name":None})
    else:
      response = json.dumps({"success":True, "command_name":self.command['command_name'], "data":self.command['data']})
    
    return response
  
  def register_execution(self):
    self.executed = True
    print('SEEMS EXECUTED')
    return json.dumps({'success':True})
  
  def post_response_data(self):
    print('RESPONSE ACCEPTED')
    data = request.get_json(force=True)
    print(data)
    self.response_data = data
    self.waiting_for_response_data = False
    return json.dumps(data)
  
  def wait_for_response_data(self):
    ...
    # self.waiting_for_response_data = True
    
    # while self.waiting_for_response_data:
    #   time.sleep(.5)
    #   print(self.waiting_for_response_data)
    # print('DONE WAITING')
    # return self.response_data
    
  
  def execute(self, command, data={}):
    self.executed = False
    self.command = {"command_name":command, "data":data}

    print('[SESSION] wait for execution')
    while not self.executed:
      time.sleep(.5)
    self.command = None
    
    # success
    print('[SESSION] executed!')
    return

if __name__ == '__main__':
  browser = ChromeBrowser()
  input('>')
  
  input()