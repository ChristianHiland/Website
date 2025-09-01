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

if (localStorage.getItem("username") == null) {
    localStorage.setItem("username", "GUEST")
} else {
    request_profile(localStorage.getItem("username"));
}