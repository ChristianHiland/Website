const message_textfield = document.getElementById("message");
const message_areafield = document.getElementById("message-area");

function Lobby_send() {
    const Data = {
        username: localStorage.getItem("username"),
        message: message_textfield.value
    }

    fetch('/lobby_send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(Data)
    })
    .then(response => {
        if (!response.ok) {throw new Error('Network response was not ok');}
    })
}

function Lobby_Update() {
    fetch('/lobby_new_get')
    .then(response => {
        if (!response.ok) {throw new Error('Network response was not ok');}
    })
    .then(result => {
        message_areafield.value = result;
        console.log(result);
    })
}

setInterval(Lobby_Update, 3000);
console.log(localStorage.getItem("username") + " Username")