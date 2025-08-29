const message_textfield = document.getElementById("message");
const dataOutputTextArea = document.getElementById("message-area");

function Lobby_send() {
    const Data = {
        sender: localStorage.getItem("username"),
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
    fetch('/lobby_chatlog')
    .then(response => response.json())
    .then(result => {
        displayDataInTextArea(result.messages);
    })
}

function displayDataInTextArea(messagesArray) {
    let formattedText = '';

    // Loop through the provided array
    for (var key in messagesArray) {
        if (messagesArray.hasOwnProperty(key)) {
            var val = messagesArray[key];
            formattedText += val["sender"] + ": " + val["content"] + "\n";
        }
    }

    // Set the textarea's value
    dataOutputTextArea.value = formattedText;
}

function request_profile(username) {
    const data = {
        Username: username
    }
    // Process Fetch
    fetch('/profile_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log("Profile: " + result)
        return result;
    })
}

request_profile(localStorage.getItem("username"));
setInterval(Lobby_Update, 1000);

if (localStorage.getItem("username") == null) {
    message_textfield.value = "Please Login."
    localStorage.setItem("username", "GUEST")
}