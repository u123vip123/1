import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "OK - Web Service is running"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    print(f"Listening on port {port}")
    app.run(host="0.0.0.0", port=port)
