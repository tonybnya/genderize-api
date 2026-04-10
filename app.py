"""
Script Name: app.py
Description: Flask API endpoint for gender classification using Genderize.io API
Author: @tonybnya
"""

from flask import Flask

app = Flask(__name__)

DEBUG = True
HOST = "0.0.0.0"
PORT = 5000


if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)
