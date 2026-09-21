from flask_cors import CORS
from flask import Flask, jsonify, request, render_template
from services.prediction_service import predict
import os

# --------------------------------------------------
# Create Flask application
# --------------------------------------------------

app = Flask(__name__)

# Allow requests from frontend
CORS(app)


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "success",
        "message": "Mental Health AI API is running",
        "model": "XGBoost",
        "model_version": "v1"
    })


# --------------------------------------------------
# Prediction endpoint
# --------------------------------------------------

@app.route("/predict", methods=["POST"])
def prediction():

    try:

        # Get JSON request body
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Request body is required"
            }), 400

        # Run model prediction
        result = predict(data)

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except ValueError as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 400

    except Exception as error:

        print("Prediction error:", error)

        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

@app.route("/test", methods=["GET"])
def test_page():
    return render_template("test.html")

# --------------------------------------------------
# Run Flask server
# --------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )