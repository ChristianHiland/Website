from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json

app = Flask(__name__, template_folder='templates', static_folder='src', static_url_path='/src')


# Server Config
ServerConfig = None
with open("config.json", "r") as config:
    ServerConfig = json.load(config)


# Runtime Vars
people_login = []
lobby_messages = {}             # Format: "index": {"content": "hello world!", "sender": "LeeLunbin", "DateTime": "2025-08-28 19:37:36"}
lobby_message_count = 1

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

def WriteMessage(content, sender, data):
    with open("src/data/lobby.json", "w") as file:
        data["messages"][f"{sender}{len(data["messages"]) + 1}"] = {"content": content, "sender": sender, "datetime": "idkyet"}
        json.dump(data, file, indent=4)

@app.route('/lobby_send', methods=['POST'])
def lobby_send():
    data = request.get_json()
    message = data.get("message")
    sender = data.get("sender")
    # Add Content to lobby list
    data2 = None
    with open("src/data/lobby.json", "r") as file:
        data2 = json.load(file)

    WriteMessage(message, sender, data2)
    return jsonify({"Return": "Ok"})

@app.route('/lobby_chatlog')
def lobby_chatlog():
    with open("src/data/lobby.json", "r") as file:
        data = json.load(file)
        return jsonify(data)

#
# Profiles Events
#

@app.route('/profile_create/<username>/<tags>', methods=['POST'])
def profile_create(username, tags):
    if request.method == 'POST':
        data = request.get_json()
        # Get Name, Tags
        name = data.get("Username")
        tags = data.get("Tags")
        with open(ServerConfig["Paths"]["Data"]["Users"], "r") as file:
            data = json.load(file)
            if name not in data["Users"]:
                data["Users"][name] = {"Profile": {"Display": name, "Tags": tags}}
                WriteToJson(ServerConfig["Paths"]["Data"]["Users"], data)
                return jsonify({"Request": "Ok"})
            else:
                return jsonify({"Request": "Taken", "Data": data["Users"][name]})
    else:
        with open(ServerConfig["Paths"]["Data"]["Users"], "r") as file:
            data = json.load(file)
            if name not in data["Users"]:
                data["Users"][name] = {"Profile": {"Display": name, "Tags": tags}}
                WriteToJson(ServerConfig["Paths"]["Data"]["Users"], data)
                return jsonify({"Request": "Ok"})
            else:
                return jsonify({"Request": "Taken", "Data": data["Users"][name]})

@app.route('/profile_request/<username>', methods=['POST', 'GET'])
def profile_request(username):
    if request.method == 'POST':
        data = request.get_json()
        username = data.get("Username")
        with open(ServerConfig["Paths"]["Data"]["Users"], "r") as file:
            userData = json.load(file)

            for profile in userData["Users"]:
                if username in profile:
                    return jsonify(userData["Users"][username])
                else:
                    return jsonify({"Request": "Error"})
    else:
        with open(ServerConfig["Paths"]["Data"]["Users"], "r") as file:
            userData = json.load(file)

            for profile in userData["Users"]:
                if username in profile:
                    return jsonify(userData["Users"][username])
                else:
                    return jsonify({"Request": "Error"})

# Helpers
def WriteToJson(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)

def ReadFromJson(path):
    with open(path, "r") as file:
        return json.load(file)

if __name__ == "__main__":
    app.run(debug=True)