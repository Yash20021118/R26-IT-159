from flask import Blueprint, jsonify, request, session
from app.models.farm import Farm
from app import mongo
import os
import requests
from datetime import datetime
from app.utils.model_predictor import predict_soil 

api_bp = Blueprint('api', __name__, url_prefix='/api')



@api_bp.route('/farm_data/<farm_id>', methods=['GET'])
def get_farm_data(farm_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        farm = Farm.get_farm_by_id(farm_id)
        if not farm or str(farm['user_id']) != session['user_id']:
            return jsonify({"error": "Farm not found"}), 404
        
        farm['_id'] = str(farm['_id'])
        farm['user_id'] = str(farm['user_id'])

        device_id = farm['sensors']['device_id']
        location = farm['location']
        lat, lng = location['lat'], location['lng']

        # Retrieving data from the OpenWeather API
        weather_api_key = os.getenv('WEATHER_API_KEY')
        current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={weather_api_key}&units=metric"
        
        try:
            curr_resp = requests.get(current_weather_url, timeout=5).json()
            curr_temp = curr_resp['main']['temp']
            w_desc = curr_resp['weather'][0]['description']
        except:
            curr_temp, w_desc = 30.0, 75.0, "Clear Sky"

        # Retrieving the latest sensor data from the database
        latest_reading = mongo.db.sensor_readings.find_one(
            {"device_id": device_id},
            sort=[("timestamp", -1)]
        )

        db_moisture = "--"
        db_ph = "--"
        db_temp = "--"
        db_N = "--"
        db_P = "--"
        db_K = "--"
        soil_prediction = {"soil_type": "No Sensor Data", "confidence": "--"}
        
        # Obtaining the Agro Zone directly from the Farm Data in the Database
        db_agro_zone = farm.get('location', {}).get('agro_zone', 'Unknown')

        if latest_reading:
            db_moisture = latest_reading.get('soil_moisture', 0)
            db_ph = latest_reading.get('ph_level', 0)
            db_temp = latest_reading.get('temperature', curr_temp) 
            db_N = latest_reading.get('nitrogen', 0)
            db_P = latest_reading.get('phosphorus', 0)
            db_K = latest_reading.get('potassium', 0)

            saved_soil_type = latest_reading.get('predicted_soil', 'No Prediction')
            saved_confidence = latest_reading.get('confidence', '--')
            
            soil_prediction = {
                "soil_type": saved_soil_type, 
                "confidence": saved_confidence
            }

        else:
            soil_prediction = {"soil_type": "No Sensor Data", "confidence": "--"}

        return jsonify({
            "status": "success",
            "farm_details": farm,
            "agro_zone": db_agro_zone, 
            "sensor_data": {
                "soil_moisture": db_moisture,
                "ph_level": db_ph,
                "temperature": db_temp,
                "nitrogen": db_N,
                "phosphorus": db_P,
                "potassium": db_K,
                "weather_desc": w_desc,
                "weather_temperature": round(curr_temp, 2)
            },
            "soil_prediction": soil_prediction
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
        


@api_bp.route('/sensor_update', methods=['POST'])
def update_sensor_data():
    data = request.json
    device_id = data.get('device_id')
    
    # Retrieving farm details and location from the database
    farm = Farm.get_farm_by_device(device_id) 
    if not farm:
        return jsonify({"error": "Device not registered to any farm"}), 404
        
    lat = float(farm['location']['lat'])
    lng = float(farm['location']['lng'])
    zone = farm['location']['zone']

    # Getting the current weather from the Weather API
    weather_api_key = os.getenv('WEATHER_API_KEY')
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={weather_api_key}&units=metric"
    
    rainfall = 0.0
    ambient_temp = 28.0
    humidity = 60.0
    
    try:
        res = requests.get(weather_url).json()
        rainfall = res.get('rain', {}).get('1h', 0.0)
        ambient_temp = res['main']['temp']
        humidity = res['main']['humidity']
    except Exception as e:
        print("Weather API Error:", e)

    weather_data = {
        'rainfall': rainfall,
        'ambient_temp': ambient_temp,
        'humidity': humidity
    }

    # Preparing data for sending to the model (according to new names)
    params = {
        'soil_ph': data.get('ph_level', 7.0),
        'nitrogen_N': data.get('nitrogen', 0),
        'phosphorus_P': data.get('phosphorus', 0),
        'potassium_K': data.get('potassium', 0),
        'soil_moisture': data.get('soil_moisture', 0),
        'soil_temp': data.get('temperature', 0),
        'ambient_temp': ambient_temp,
        'humidity': humidity,
        'rainfall': rainfall,
        'altitude': farm.get('altitude', 50.0), # If not in the database, it is assumed to be 50m.
        'agro_ecological_zone': zone
    }

    # Predicting (with Weather Data)
    prediction = predict_soil(params, weather_data=weather_data)

    # Saving in the database
    reading_data = {
        "device_id": device_id,
        "farm_id": farm['_id'],
        "timestamp": datetime.utcnow(),
        "soil_moisture": data.get('soil_moisture'),
        "ph_level": data.get('ph_level'),
        "temperature": data.get('temperature'),
        "nitrogen": data.get('nitrogen'),
        "phosphorus": data.get('phosphorus'),
        "potassium": data.get('potassium'),
        "predicted_soil": prediction['soil_type'],
        "confidence": prediction['confidence']
    }
    mongo.db.sensor_readings.insert_one(reading_data)

    return jsonify({"message": "Data saved and predicted successfully", "prediction": prediction}), 201
