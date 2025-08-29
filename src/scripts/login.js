const username_textfield = document.getElementById("username");
const login_btn = document.getElementById("sumbit-btn");
const status_text = document.getElementById("status_text");

function login() {
    const Data = {
        username: username_textfield.value
    }
    // Saving Username in local storage
    localStorage.setItem("username", Data.username)
    fetch('/login_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(Data)
    })
    .then(response => {
        if (!response.ok) {throw new Error('Network response was not ok');}
    })
    .then(result => {
        console.log("Login on as " + Data.username);
        status_text.textContent = "Welcome " + Data.username + "!";
    })
}

if (localStorage.getItem("username") != "") {
    status_text.textContent = "Your already logged-in!"
}