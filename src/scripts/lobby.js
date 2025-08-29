const username_textfield = document.getElementById("username");
const message_textfield = document.getElementById("message");
const message_areafield = document.getElementById("message-area");

function Lobby_send() {
    const Data = {
        username: username_textfield.value,
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
    fetch('/lobby_new_get', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username: "test"})
    })
    .then(response => {
        if (!response.ok) {throw new Error('Network response was not ok');}
    })
    .then(result => {
        message_areafield.value = result;
    })
}

setInterval(Lobby_Update, 3000);