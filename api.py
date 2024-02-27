from flask import Flask, jsonify, abort, request
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "MySecureApiKey1234"

def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        # Check if 'Authorization' header is present and correct
        if request.headers.get('Authorization') == f'Bearer {API_KEY}':
            return view_function(*args, **kwargs)
        else:
            # If the API key is missing or incorrect, return 403 Forbidden
            abort(403)
    return decorated_function


@app.route('/api/helloworld', methods=['POST'])
# @require_api_key
def hello_world():
    data = request.json  # Parse JSON data from the request body
    # You can now process the data as needed, for example:
    message = data.get("message", "No message provided")
    return jsonify({"response": f"Received your message: {message}"})

if __name__ == '__main__':
    app.run(debug=True)
