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
        
    })
    .then(result => {
        console.log("Login on as " + Data.username);
        status_text.textContent = "Welcome " + Data.username + "!";
        create_profile(Data.username);
    })
}

function create_profile(username) {
    const data = {
        Username: username,
        Tags: ["None"]
    }
    // Process Fetch
    fetch('/profile_create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.Request == "Taken") { status_text.textContent = "Username taken! Logging in..."; }
        else if (result.Request == "Created") { status_text.textContent = "Profile Created! Logging in..."; }
        else if (result.Request == "Error") { status_text.textContent = "Error creating profile! Logging in..."; }
    })
    window.location.href = "http://lunprojects.net/lobby";
}

if (localStorage.getItem("username") != null) {
    status_text.textContent = "Your already logged-in! as " + localStorage.getItem("username");
} else {
    status_text.textContent = "";
}

