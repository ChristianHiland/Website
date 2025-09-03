from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime
from flask_cors import CORS
import json

# Safely Importing modules
try:
    from helpers import UpdateJSON, ReadJSON, GetStatus
except ImportError as e:
    print(f"Failed to import modules\n Error: {e}")

app = Flask(__name__, template_folder='templates', static_folder='src', static_url_path='/src')
# Enable CORS to allow your HTML file to fetch data from this server
CORS(app)

# Server Config
ServerConfig = None
with open("config.json", "r") as config:
    ServerConfig = json.load(config)

# Quick Vars
MESSAGES_FILE = ServerConfig["Paths"]["Data"]["Lobby"]
USERS_FILE = ServerConfig["Paths"]["Data"]["Users"]

# Runtime Vars
people_login = []
lobby_messages = {}             # Format: "index": {"content": "hello world!", "sender": "LeeLunbin", "DateTime": "2025-08-28 19:37:36"}
user_data = {
    "Users": {
        "LeeLunbin": {
            "Profile": {
                "Display": "Lee Lunbin",
                "Tags": [
                    "Dev",
                    "Web Dev",
                    "Solo Dev"
                ]
            }
        }
    }
}

with open(USERS_FILE, "r") as file:
    user_data = json.load(file)

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

# Profiles Page
@app.route('/profiles')
def profiles():
    return render_template('profiles.html')

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Projects Page
@app.route('/projects')
def projects():
    return render_template('projects.html')

# Links Page
@app.route('/links')
def links():
    return render_template('links.html')

# Howling Haven Page
@app.route('/howlinghaven')
def howlinghaven():
    return render_template('howlinghaven.html')

# Messages Debug Page
@app.route('/messages_loader')
def messages_loader():
    return render_template('messageLoader.html')


#
# Login Events
#

# This is ran when a user logins in. 
@app.route('/login_request', methods=['POST',"GET"])
def login_request():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")

        if username != "":
            people_login.append(username)
            print(f"{username} has login on!")
        else:
            return "double shit"
        return redirect(url_for("lobby"))

#
# Lobby Events
#

# This is ran when a user sends a message to the Lobby Chat.
# Format JSON: {"Content": "Blah Blah", "Sender": "LeeLunbin", "Color": "#1d4ed8"}
@app.route('/lobby_send', methods=['POST'])
def lobby_send():
    """API endpoint to add a new message."""
    # 1. Get the new message data sent from the JavaScript client
    new_message = request.get_json()

    # 2. Basic validation
    #if not new_message or 'content' not in new_message or 'sender' not in new_message:
    #    return jsonify({'status': 'error', 'message': 'Invalid message format'}), 400

    # Get Data from request.
    content = new_message.get("content")
    sender = new_message.get("sender")
    newData = {"content": content, "sender": sender, "color": "#1d4ed8", "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    # Using a helper function: Update the Lobby.json file
    UpdateJSON(ServerConfig["Paths"]["Data"]["Lobby"], newData)
    
    # 7. Send a success response back to the client
    return jsonify({'response': 'ok', 'message': 'Message saved!'})

# This is ran when a user fetches the current messages in a lobby.
@app.route('/lobby_chatlog')
def lobby_chatlog():
    data = ReadJSON(ServerConfig["Paths"]["Data"]["Lobby"])
    return jsonify(data)

#
# Profiles Events
#

@app.route('/profile_create', methods=['POST'])
def profile_create():
    data = request.get_json()
    # Get Name, Tags
    name = data.get("Username")
    tags = data.get("Tags")
    print(f"Creating Profile for: {name}")

    # Update Data
    if name not in user_data["Users"]:
        user_data["Users"][name] = {"Display": name, "Tags": tags}
    
    # Writing to JSON.
    with open(USERS_FILE, "w") as file:
        json.dump(user_data, file, indent=4)

    return jsonify({"Request": "Ok"})
@app.route('/profile_request', methods=['POST'])
def profile_request():
    data = request.get_json()
    username = data.get("Username")
    with open("src/data/users.json", "r") as file:
        data = json.load(file)
        if username in data["Users"]:
            return jsonify(data["Users"][username])
        else:
            return jsonify({"Request": "Failed"})


#
# API Requests
#

@app.route('/checkStatus', methods=['POST'])
def checkStatus():
    Status = {
        "VPN": {
            "Status": GetStatus("wg-quick@wg0.service")
        },
        "Website": {
            "Status": GetStatus("lunprojects")
        }
    }
    return jsonify(Status)

# Helpers
def WriteToJson(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    app.run(debug=True, port=9003)