window.onload = function () {

    var rooms = JSON.parse(localStorage.getItem("rooms")),
        ele = document.getElementById('js_result_list'),
        fragment = document.createDocumentFragment(),
        button;

    window.onpageshow = function (event) {
        if (event.persisted) {
            window.location.reload()
        }
    };

    console.log(rooms);

    if (rooms) {
        for (var i = 0; i < rooms.length; i++) {

            var li = document.createElement('li'),
                h2 = document.createElement('h2'),
                name = document.createElement('div'),
                button = document.createElement("button");
            button.innerHTML = "Delete";
            button.style.fontSize = '15px';

            name.classList.add('name');
            h2.appendChild(document.createTextNode(rooms[i].name));
            h2.appendChild(document.body.appendChild(button));

            li.appendChild(h2);
            fragment.appendChild(li);

            h2.setAttribute("id", i);
        }
    }

    ele.appendChild(fragment);

    var all_buttons = document.querySelectorAll('button');

    all_buttons.forEach(function (all_buttons, index) {
        all_buttons.addEventListener('click', function () {

            document.getElementById(index).remove();

            rooms.splice(index, 1);
            localStorage.setItem("rooms", JSON.stringify(rooms));

            console.log(rooms);

            //problem: when you delete a room, it appears to be deleted on page but sometimes doesn't actually
            //remove from array
        });
    });
};