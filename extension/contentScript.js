var saved_element = document;


function refresh(){
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "http://127.0.0.1:5000/load_buffer");
  xhr.send();
  xhr.onerror = function(e){
    clearInterval(refreh_deamonId);
    document.getElementById('ChromeControllerStatusBox').style.backgroundColor = 'red'
    document.getElementById('ChromeControllerStatusBox').innerText = 'No Connection'
  };
  xhr.responseType = "json";
  xhr.onload = () => {
    if (xhr.readyState == 4 && xhr.status == 200) {
      document.getElementById('ChromeControllerStatusBox').style.backgroundColor = 'green'
      document.getElementById('ChromeControllerStatusBox').innerText = 'Connected'

      data = xhr.response
      for (let i=0; i<data['command_buffer'].length; i++){
        // perform a action
        console.log(data['command_buffer'][i])
        command = data['command_buffer'][i]
        execute_command(command)
        console.log(saved_element)
      }
    } else {
      console.log(`Error: ${xhr.status}`);
    }
  };
}

function execute_command(command){
  let action = command['action']
  if (action == 'reset-search'){
    saved_element = document
  }
  if (action == 'search-element'){
    let method = command['method']
    if (method == 'id'){
      saved_element = saved_element.getElementById(command['value']);
    }
    if (method == 'class'){
      var results = saved_element.getElementsByClassName(command['value'])
      if (command['visible'] == 'true'){
        for (let x=0; x<results.length; x++){
          if (results[x].style.display !== 'none'){
            saved_element = results[x]
            return;
          }
        }
      }else{
        saved_element = results[command['list-index']]
      }
    }
    if (method == 'tag'){
      saved_element = saved_element.getElementsByTagName(command['value'])[command['list-index']]
    }
  }
  if (action == 'click'){
    // alert('click?')
    saved_element.click()
  }
  if (action == 'send-keys'){
    for (let letter_index=0; letter_index<command['text'].length; letter_index++){
      SimulateKeyPress(saved_element, command['text']);
    }
  }
  if (action == 'dispatch-event'){
    var event = new Event(command['event-name'])
    saved_element.dispatchEvent(event);
  }
  if (action == 'location'){
    window.location = command['href']
  }
}

function SimulateKeyPress(element, text){
  element.value = text;

  //refresh the search bar by simulating a keyUp event
  var keyboardEvent = document.createEvent('KeyboardEvent');
  var initMethod = typeof keyboardEvent.initKeyboardEvent !== 'undefined' ? 'initKeyboardEvent' : 'initKeyEvent';
      
  keyboardEvent[initMethod](
    'keyup', // event type: keydown, keyup, keypress
    true, // bubbles
    true, // cancelable
    window, // view: should be window
    false, // ctrlKey
    false, // altKey
    false, // shiftKey
    false, // metaKey
    40, // keyCode: unsigned long - the virtual key code, else 0
    0, // charCode: unsigned long - the Unicode character associated with the depressed key, else 0
  );
  element.dispatchEvent(keyboardEvent);
}


var refreh_deamonId = setInterval(refresh, 1000)


// set connection symbol
var loading_div = document.createElement('div')
loading_div.innerHTML = '<div id="ChromeControllerStatusBox" style="padding: 20px; position: absolute; top:50px; right:0; background-color: gray; border-radius:10px;">Loading...</div>'

document.body.appendChild(loading_div)