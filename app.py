"""
Script Name: app.py
Description: Flask API endpoint for gender classification using Genderize.io API
Author: @tonybnya
"""

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from utils import make_response, validate_name

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Config constants
GENDERIZE_API_URL = "https://api.genderize.io"
REQUEST_TIMEOUT = 5  # seconds
DEBUG = True
HOST = "0.0.0.0"
PORT = 5000


@app.route("/")
def root():
    """Root endpoint.
    """
    return {
        "message": "Welcome to Genderize API",
        "version": "v1.0.0",
        "author": "@tonybnya"
    }


@app.route("/api/classify", methods=["GET"])
def classify_name():
    """Classify a name using Genderize.io API.
    """
    name = request.args.get("name")

    # validate name query parameter
    is_valid, error_message = validate_name(name)
    if not is_valid:
        if "Missing" in error_message:
            return jsonify({"status": "error", "message": error_message}), 400
        elif "string" in error_message:
            return jsonify({"status": "error", "message": error_message}), 422
        else:
            return jsonify({"status": "error", "message": error_message}), 400

    name = name.strip()

    try:
        # Call Genderize.io API
        response = requests.get(
            GENDERIZE_API_URL,
            params={"name": name},
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()

        # process the response
        processed_data, error = make_response(data)
        if error:
            return jsonify({"status": "error", "message": error}), 404

        return jsonify({"status": "success", "data": processed_data}), 200

    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "Upstream API request timed out"}), 502
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"Upstream API error: {e!s}"}), 502
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {e!s}"}), 500


if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)
