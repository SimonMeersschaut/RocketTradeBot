var saved_element = document;


function refresh(){
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "http://127.0.0.1:5000/load_buffer");
  xhr.send();
  xhr.onerror = function(e){
    // clearInterval(refreh_deamonId);
    document.getElementById('ChromeControllerStatusBox').style.backgroundColor = 'red'
    document.getElementById('ChromeControllerStatusBox').innerText = 'Connection closed'
    setTimeout(refresh, 5000)
  };
  xhr.responseType = "json";
  xhr.onload = () => {
    if (xhr.readyState == 4 && xhr.status == 200) {
      document.getElementById('ChromeControllerStatusBox').style.backgroundColor = 'green'
      document.getElementById('ChromeControllerStatusBox').innerText = 'Connected'

      data = xhr.response
    if (data['command_name'] !== null){
        console.log(data)
        execute(data['command_name'], data['data'])
    }
    } else {
      console.log(`Error: ${xhr.status}`);
    }
    console.log('done')
    setTimeout(refresh, 1000)
  };

  
}

// var refreh_deamonId = setInterval(refresh, 1000)

refresh()

// set connection symbol
var loading_div = document.createElement('div')
loading_div.innerHTML = '<div id="ChromeControllerStatusBox" style="padding: 20px; position: absolute; top:50px; right:0; background-color: gray; border-radius:10px;">Loading...</div>'

document.body.appendChild(loading_div)