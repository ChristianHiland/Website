const username_textfield = document.getElementById("username");
const login_btn = document.getElementById("sumbit-btn");

function login() {
    const Data = {
        username: username_textfield.value
    }

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
        console.log(result);
    })
}