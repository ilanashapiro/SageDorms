window.onload = function () {
    var rooms = JSON.parse(localStorage.getItem("rooms")),
    ele = document.getElementById('js_result_list'),
    fragment = document.createDocumentFragment(),
  
    if (rooms) {
      for (var i = 0; i < items.length; i++) {


        var li = document.createElement('li'),
        h2 = document.createElement('h2'),
        name = document.createElement('div');

        name.classList.add('name');
      
        h2.appendChild(document.createTextNode(rooms[i].name));
        li.appendChild(h2);
        fragment.appendChild(li);
      }
    }
  
    ele.appendChild(fragment);  
  };