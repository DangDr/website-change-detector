import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    # Read the log file
    with open("website_change_detector.log", "r") as file:
        logs = file.readlines()
    return render_template("index.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
