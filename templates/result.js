window.onload = function () {
    var rooms = JSON.parse(localStorage.getItem("rooms")),
    ele = document.getElementById('js_result_list'),
    fragment = document.createDocumentFragment();

    console.log(rooms)
  
    if (rooms) {
      for (var i = 0; i < rooms.length; i++) {

        var li = document.createElement('li'),
            h2 = document.createElement('h2'),
            name = document.createElement('div');
            // dorm = documen.createElement('div');

        name.classList.add('name');
        // dorm.classList.add('dorm');
        
      
        h2.appendChild(document.createTextNode(rooms[i].name));
        // h2.appendChild(document.createTextNode(rooms[i].dorm));
        li.appendChild(h2);
        fragment.appendChild(li);
      }
    }
  
    ele.appendChild(fragment);  
  };