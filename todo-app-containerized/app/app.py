import os

from flask import Flask, render_template

app = Flask(__name__)

# The API URL will be '/api' because Nginx will route requests from '/api/*' to the API container.
# If you were making direct requests from Flask, you'd use 'http://api:5001'
API_BASE_URL = os.environ.get(
    "API_URL", "/api"
)  # Use env var or default to /api for HTMX


@app.route("/")
def index():
    """Serves the main To-Do application page."""
    return render_template("index.html", API_BASE_URL=API_BASE_URL)


if __name__ == "__main__":
    # Run the Flask app on all available interfaces on port 5000
    app.run(host="0.0.0.0")
