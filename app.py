from flask import Flask,jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from DevOps made easy..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
