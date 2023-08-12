var commands = {
  "debug":debug,
  "set_location":set_location,
  "select_slot":select_slot,
  "select_inventory_item":select_inventory_item,
  "set_credit_amount":set_credit_amount,
  "set_note":set_note,
  "get_market_items":get_market_items
}

function execute(command_name, data){
  commands[command_name](data)
  var xhr = new XMLHttpRequest();
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

function set_note(data){
  document.getElementById('note').value = data['text'];
}

function get_market_items(){
  function read_trade_item(dom){
    var name = dom.getElementsByClassName('rlg-item__text')[0].getElementsByTagName('h2')[0].innerText
    var quantity_element = dom.getElementsByClassName('rlg-item__quantity')[0]
    if (quantity_element == undefined){
      var quantity = 1
    }else{
      var quantity = quantity_element.innerText
    }
    var paint = dom.getElementsByClassName('rlg-item__paint')[0]
    if (paint !== undefined){
      var paint = paint.getAttribute('data-name')
    }else{
      var paint = null
    }
    return {'name':name, 'quantity':quantity, "paint":paint}
  }
  var trades = document.getElementsByClassName('rlg-trade')
  const all_trades_data = []
  for (let trade_index=0; trade_index<trades.length; trade_index++){
    var trade = trades[trade_index]
      
    var trade_data = {
      "id":trade.getAttribute('data-trade'),
      "has":[],
      'wants':[]
    }

    var items = trade.getElementsByClassName('rlg-trade__content')[0].getElementsByClassName('rlg-trade__items')[0].getElementsByClassName('rlg-trade__itemshas')[0].getElementsByClassName('rlg-item')
    for (let i=0; i<items.length; i++){
      resp = read_trade_item(items[i])
      trade_data['has'].push(resp)
    }
    var items = trade.getElementsByClassName('rlg-trade__content')[0].getElementsByClassName('rlg-trade__items')[0].getElementsByClassName('rlg-trade__itemswants')[0].getElementsByClassName('rlg-item')
    for (let i=0; i<items.length; i++){
      resp = read_trade_item(items[i])
      trade_data['wants'].push(resp)
    }
    console.log(trade_data)
    all_trades_data.push(trade_data)
  }
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:5000/post_response_data");
  xhr.send(JSON.stringify(all_trades_data));
}