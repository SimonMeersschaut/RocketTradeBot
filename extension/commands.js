commands = {
  "debug":debug,
  "set_location":set_location,
  "select_slot":select_slot,
  "select_inventory_item":select_inventory_item,
  "set_credit_amount":set_credit_amount
}

function execute(command_name, data){
  commands[command_name](data)
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:5000/register_execution");
  xhr.send();
}

function debug(data){
  alert(data['text'])
}

function set_location(data){
  setTimeout(() => {
    window.location.href = data['location']
  }, 500)
}

function select_slot(data){
  var side = document.getElementsByClassName('rlg-trade__items'+data['side'])[0]
  side.getElementsByTagName('div')[data['index']].click()
}

function select_inventory_item(data){
  // enter name
  var input = document.getElementById('trade-selector-all-items').getElementsByClassName('rlg-trade-selector-header --with-padding')[0].getElementsByTagName('input')[0]
  input.value = data['name']
  
  var keyboardEvent = document.createEvent('KeyboardEvent');
  var initMethod = typeof keyboardEvent.initKeyboardEvent !== 'undefined' ? 'initKeyboardEvent' : 'initKeyEvent';
  keyboardEvent[initMethod]('keyup', true, true,window, false, false, false, false, 40, 0,);
  input.dispatchEvent(keyboardEvent);

  setTimeout(
    () => {
      
        var item_rows = document.getElementById('trade-items-all').getElementsByClassName('row')[0].getElementsByClassName('rlg-trade-selector-section')
        for (var i=0; i<item_rows.length; i++){ if (item_rows[i].style.display !== 'none'){ console.log(item_rows[i]); break }}
        item_rows = item_rows[i].getElementsByClassName('rlg-item rlg-creator-item')
        for (var i=0; i<item_rows.length; i++){ if (item_rows[i].style.display !== 'none'){ console.log(item_rows[i]); break }}
        item_rows[i].click()

    }, 500
  )
}

function set_credit_amount(data){
  var cred_input = document.getElementById('amount_credits');
  cred_input.value = data['value'];
  cred_input.dispatchEvent(new Event('change'));

}