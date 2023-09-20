import json
import os
import socket
import time

from dotenv import load_dotenv
from flask import Flask, render_template
from markupsafe import escape
import ngrok
import pyautogui
import pyqrcode


load_dotenv()

app = Flask(__name__)

# Constants
APP_HOST = "0.0.0.0"
APP_PORT = 6969

NGROK_DOMAIN = os.environ.get("NGROK_DOMAIN")

# Load Data
f = open("data/data.json")
cheat_data = json.load(f)
f.close()


@app.route("/")
def home():
    return render_template("index.html", cheat_data=cheat_data)


@app.route("/activate/<string:cheat_code>/")
def apply_cheat(cheat_code):
    pyautogui.write(cheat_code)
    return {
        "status": "success",
        "cheat_code": cheat_code,
    }


if __name__ == "__main__":
    # Use Ngrok URL
    # tunnel = ngrok.connect(
    #     addr=f"localhost:{APP_PORT}",
    #     domain=NGROK_DOMAIN,
    #     authtoken_from_env=True,
    # )
    # URL = tunnel.url()

    # Use Local Network URL
    URL = f"http://{socket.gethostbyname(socket.gethostname())}:{APP_PORT}"

    # Generate and Show QR Code
    qr = pyqrcode.create(URL)
    print(qr.terminal("black", "white"))

    # Run Flask
    app.run(
        host=APP_HOST,
        port=APP_PORT,
        # Need to turn off when using ngrok
        debug=True,
    )
