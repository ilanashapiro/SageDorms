window.onload = function () {
    var wishlist_button = document.querySelectorAll('js_wishlist_button'),
    clicked = [],
    save_rooms = [],
    rooms = JSON.parse(localStorage.getItem("rooms"));
  
    if (rooms) {
        var id;
        for (var i = 0; i < rooms.length; i++) {
          id = rooms[i].id;
          save_rooms.push(rooms[i]);
          clicked.push(id);
        }
      }
  
    wishlist_button.forEach(function (wishlist_button,index) {
        wishlist_button.addEventListener('click',function () {
  
        if (clicked.indexOf(index) >= 0) {
  
          for (var i = 0; i < clicked.length; i++) {
            if(clicked[i] == index){
              clicked.splice(i, 1);
              save_rooms.splice(i, 1);
            }
          }
    
        }else if(clicked.indexOf(index) == -1){
  
          var name = wishlist_button.dataset.name;
  
          clicked.push(index);
          save_rooms.push({
            id: index,
            name: name,
          });
          }
  
        localStorage.setItem("rooms",JSON.stringify(save_rooms));

      });
    });
};  