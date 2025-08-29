from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__, template_folder='templates', static_folder='src', static_url_path='/src')


# Runtime Vars
people_login = []
lobby_messages = {}             # Format: "index": {"content": "hello world!", "sender": "LeeLunbin", "DateTime": "2025-08-28 19:37:36"}
lobby_message_count = 1
new_message = {}

# Default 'Home' Page
@app.route('/')
def index():
    return render_template('index.html')

# Login Page
@app.route('/login')
def login():
    return render_template('login.html')

# Lobby Page
@app.route('/lobby')
def lobby():
    return render_template('lobby.html')

#
# Login Events
#

@app.route('/login_request', methods=['POST'])
def login_request():
    data = request.get_json()
    username = data.get("username")

    if username != "":
        people_login.append(username)
        print(f"{username} has login on!")
        return "Shit"
    else:
        return "double shit"

#
# Lobby Events
#

def WriteMessage(content, sender, data):
    with open("src/data/lobby.json", "w") as file:
        data["messages"][f"{sender}{len(data["messages"]) + 1}"] = {"content": content, "sender": sender}
        json.dump(data, file, indent=4)
        

@app.route('/lobby_send', methods=['POST'])
def lobby_send():
    data = request.get_json()
    message = data.get("message")
    sender = data.get("sender")
    # Add Content to lobby list
    data = None
    with open("src/data/lobby.json", "r") as file:
        data = json.load(file)

    WriteMessage(message, sender, data)
    return "Ok"

@app.route('/lobby_new_get', methods=["POST"])
def lobby_new_get():
    data2 = request.get_json()
    data = None
    with open("src/data/lobby.json", "r") as file:
        data = json.load(file)
        print(f"Data: {data}{data2}")
    
    return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True)