from flask import Flask, render_template

app = Flask(__name__)

# Default 'Home' Page
@app.route('/')
def home_page():
    return render_template('index.html')

# Project Page
@app.route('/project/<projectID>')
def project_page(projectID):
    return f"<h1>{projectID}</h1>"

