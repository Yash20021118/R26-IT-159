import os
import joblib
import pandas as pd
import numpy as np

# Find the base directory and the models folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_DIR = os.path.join(BASE_DIR, 'models') # pkl file

# Loading Model and 4 Encoders
try:
    model = joblib.load(os.path.join(MODEL_DIR, 'soil_model.pkl'))
    scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
    le_zone = joblib.load(os.path.join(MODEL_DIR, 'label_encoder_zone.pkl'))
    le_soil = joblib.load(os.path.join(MODEL_DIR, 'label_encoder_soil.pkl'))
    print("All AI Models loaded successfully!")
except Exception as e:
    print("Error loading models:", e)
    model = scaler = le_zone = le_soil = None


def predict_soil(params, weather_data=None):
    if model is None:
        return {"soil_type": "Model Error", "confidence": "--"}

    # Original data coming from the API goes directly to the Model.

    # Arrange columns in the order they were trained
    num_feats = [
        "soil_ph", "nitrogen_N", "phosphorus_P", "potassium_K",
        "soil_moisture", "soil_temp", "ambient_temp", "humidity",
        "rainfall", "altitude"
    ]
    
    # Complete list of columns required for the model
    all_feats = num_feats + ["agro_ecological_zone_encoded"]

    # Encoding Categorical Data (Zone)
    zone_val = str(params.get("agro_ecological_zone", "Unknown"))
    zone_val = zone_val.replace(" Zone", "").strip()
    
    try:
        zone_enc = le_zone.transform([zone_val])[0]
    except ValueError:
        zone_enc = 0 

    num_vals = []
    for f in num_feats:
        num_vals.append(float(params.get(f, 0.0)))
    
    num_df = pd.DataFrame([num_vals], columns=num_feats)
    num_scaled = scaler.transform(num_df)[0]

    # Putting everything together and getting the prediction
    full_vals = list(num_scaled) + [zone_enc]
    full_df = pd.DataFrame([full_vals], columns=all_feats)
    
    pred_encoded = model.predict(full_df)[0]
    pred_soil_name = le_soil.inverse_transform([pred_encoded])[0]
    
    confidence = model.predict_proba(full_df)[0].max() * 100

    return {
        "soil_type": pred_soil_name, 
        "confidence": round(confidence, 1)
    }
