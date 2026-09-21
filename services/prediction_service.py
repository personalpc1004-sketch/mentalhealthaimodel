import json
import os

import joblib
import xgboost as xgb

from utils.feature_engineering import create_features


# --------------------------------------------------
# Model paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "model"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "xgboost_model.json"
)

ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "label_encoder.pkl"
)

METADATA_PATH = os.path.join(
    MODEL_DIR,
    "metadata.json"
)


# --------------------------------------------------
# Load model
# --------------------------------------------------

model = xgb.XGBClassifier()

model.load_model(MODEL_PATH)


# --------------------------------------------------
# Load label encoder
# --------------------------------------------------

label_encoder = joblib.load(
    ENCODER_PATH
)


# --------------------------------------------------
# Load metadata
# --------------------------------------------------

with open(
    METADATA_PATH,
    "r",
    encoding="utf-8"
) as file:
    metadata = json.load(file)


# --------------------------------------------------
# Prediction function
# --------------------------------------------------

def predict(data):

    # Create the same 36 features
    # used during model training.
    features = create_features(data)

    # Get encoded prediction
    prediction_encoded = model.predict(
        features
    )

    # Convert encoded label to actual severity
    prediction = label_encoder.inverse_transform(
        prediction_encoded.astype(int)
    )[0]

    # Get class probabilities
    probabilities = model.predict_proba(
        features
    )[0]

    # Get class names in the same order
    class_names = label_encoder.classes_

    probability_dict = {
        class_name: float(probability)
        for class_name, probability in zip(
            class_names,
            probabilities
        )
    }

    # Highest probability
    confidence = float(
        max(probabilities)
    )

    return {
        "model_version": metadata.get(
            "model_version",
            "v1"
        ),
        "predicted_severity": str(
            prediction
        ),
        "confidence": confidence,
        "probabilities": probability_dict
    }