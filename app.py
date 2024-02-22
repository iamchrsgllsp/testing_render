from flask import Flask
app = Flask(__name__, static_folder="static")

@app.route('/')
def hello_world():
    return 'Hello, World!'
