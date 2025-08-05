# app.py (or map.py) - CORRECTED VERSION

from flask import Flask, request, jsonify
from flask_cors import CORS
# We no longer need generate_map from the service
from map_service import find_hospitals_osm 

app = Flask(__name__)
CORS(app) # Allows your frontend to call this backend

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        postal_code = data.get("postal_code", "")

        # Basic validation
        if not postal_code or not postal_code.isdigit() or len(postal_code) != 6:
            return jsonify({"error": "Invalid postal code provided"}), 400

        # This function returns either a list of hospitals or an error string
        hospitals = find_hospitals_osm(postal_code)

        # Check if the result is a list (success) or a string (error)
        if isinstance(hospitals, list):
            # SUCCESS! Send the raw hospital data back to the frontend.
            return jsonify({"hospitals": hospitals}), 200
        else:
            # An error message was returned from find_hospitals_osm
            return jsonify({"error": hospitals}), 404

    except Exception as e:
        # Log the error for debugging on the server
        print(f"An internal server error occurred: {e}")
        return jsonify({"error": "An internal server error occurred. Please try again later."}), 500

# This part is for local testing. Render will use the Procfile to start the app.
if __name__ == '__main__':
    app.run(debug=True)
