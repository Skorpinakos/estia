from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Initialize the app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Setup logging to file
logging.basicConfig(filename='visit_logs.log', level=logging.INFO,
                    format='%(asctime)s %(message)s')

@app.route('/log_visit', methods=['POST'])
def log_visit():
    # Get the data from the POST request
    visit_data = request.json
    if not visit_data:
        return jsonify({"error": "No data received"}), 400

    # Log the visit data
    app.logger.info(f"Visit data received: {visit_data}")

    # Return a success response
    return jsonify({"message": "Visit logged successfully"}), 200

if __name__ == '__main__':
    # Run the app on 0.0.0.0 (accessible over the network)
    app.run(host='0.0.0.0', port=1801, debug=False)  # Secure, debug mode off
