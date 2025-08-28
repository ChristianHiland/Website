from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='src', static_url_path='/src')

# Default 'Home' Page
@app.route('/')
def index():
    return render_template('index.html')

# Project Page
@app.route('/project/<projectID>')
def projects(projectID):
    return f"<h1>{projectID}</h1>"

if __name__ == "__main__":
    app.run()