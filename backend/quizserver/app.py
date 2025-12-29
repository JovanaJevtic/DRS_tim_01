from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "User Server radi!"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
