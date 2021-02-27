from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/home')
def home():
    print("Request Received for Home Page")
    return "Welcome to the home page"

if __name__ == "__main__":
    app.run(debug=True)