window.onload = function () {

    localStorage.clear();

    var wishlist_button = document.querySelectorAll('.js_wishlist_button'),
        clicked = [],
        save_rooms = [],
        rooms = JSON.parse(localStorage.getItem("rooms"));

    console.log(rooms)
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
                console.log("You can't add anymore!")
                console.log(clicked)

                // for (var i = 0; i < clicked.length; i++) {

                //     // get the room we clicked
                //     if(clicked[i] == index){
                //         clicked.splice(i, 1);
                //         save_rooms.splice(i, 1);
                //         break;
                //     }
                // }

                
            } else if(clicked.indexOf(index) == -1){ // nothing in clicked list

                var name = wishlist_button.dataset.name;

                clicked.push(index);
                save_rooms.push({
                    id: index,
                    name: name,
                });
                console.log(clicked)
                console.log(save_rooms)
            }

            localStorage.setItem("rooms",JSON.stringify(save_rooms));

        });
    });
};  
