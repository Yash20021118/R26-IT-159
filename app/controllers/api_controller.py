
from flask import Blueprint, jsonify, request, session
from app.models.farm import Farm
from app import mongo
import os
import requests
from datetime import datetime
from app.utils.model_predictor import predict_soil 
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

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
            curr_temp, w_desc = 30.0, "Clear Sky"

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
        
        # Obtaining the Agro Zone
        district = farm.get('location', {}).get('district', '')
        zone_doc = mongo.db.SL_Agro_Ecological_Zones.find_one({"District": district})

        if zone_doc:
            db_agro_zone = zone_doc.get('Zone_Code', 'Unknown') 
        else:
            db_agro_zone = farm.get('location', {}).get('zone', 'Unknown')

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

        soil_alerts = []
        if soil_prediction["soil_type"] not in ["No Sensor Data", "No Prediction", "Model Error"]:
            rules = list(mongo.db.soil_rules.find({"Soil Type": soil_prediction["soil_type"]}))
            
            factor_mapping = {
                "Moisture (%)": db_moisture,
                "pH Level": db_ph,
                "Nitrogen (N)": db_N,
                "Phosphorus (P)": db_P,
                "Potassium (K)": db_K,
                "Temperature (°C)": db_temp
            }
            
            historical_docs = list(mongo.db.sensor_readings.find(
                {"device_id": device_id}
            ).sort([("timestamp", -1)]).limit(7))
            historical_docs.reverse() 


            db_field_map = {
                "Moisture (%)": "soil_moisture",
                "pH Level": "ph_level",
                "Nitrogen (N)": "nitrogen",
                "Phosphorus (P)": "phosphorus",
                "Potassium (K)": "potassium",
                "Temperature (°C)": "temperature"
            }

            for rule in rules:
                factor_name = rule.get("Factor")
                min_val = float(rule.get("min_value", 0))
                max_val = float(rule.get("max_value", 99999))
                current_val = factor_mapping.get(factor_name)
                
                if current_val != "--":
                    try:
                        val = float(current_val)
                        if min_val <= val <= max_val:
                            

                            timestamp_val = latest_reading.get('timestamp')
                            if isinstance(timestamp_val, datetime):

                                local_time = timestamp_val + timedelta(hours=5, minutes=30)
                                time_str = local_time.strftime("%Y-%m-%d %I:%M %p")
                            else:
                                local_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
                                time_str = local_time.strftime("%Y-%m-%d %I:%M %p")


                            db_field = db_field_map.get(factor_name)
                            hist_labels = []
                            hist_data = []
                            
                            for h_doc in historical_docs:
                                h_time = h_doc.get('timestamp')
                                if isinstance(h_time, datetime):
                                    local_h_time = h_time + timedelta(hours=5, minutes=30)
                                    hist_labels.append(local_h_time.strftime("%b %d, %I:%M %p")) 
                                else:
                                    hist_labels.append("N/A")
                                
                                h_val = h_doc.get(db_field, 0)
                                hist_data.append(float(h_val) if h_val != "--" else 0)


                            soil_alerts.append({
                                "factor": factor_name,
                                "level": rule.get("Condition Level"),
                                "message": rule.get("Message"),
                                "advice": rule.get("Advice"),
                                "timestamp": time_str,
                                "current_value": str(val),
                                "history_labels": hist_labels,
                                "history_data": hist_data
                            })
                    except ValueError:
                        pass

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
            "soil_prediction": soil_prediction,
            "soil_alerts": soil_alerts  
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500      


@api_bp.route('/sensor_update', methods=['POST'])
def update_sensor_data():
    data = request.json
    device_id = data.get('device_id')
    

    farm = Farm.get_farm_by_device(device_id) 
    if not farm:
        return jsonify({"error": "Device not registered to any farm"}), 404
        
    lat = float(farm['location']['lat'])
    lng = float(farm['location']['lng'])
    zone = farm['location']['zone']


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
        'altitude': farm.get('altitude', 50.0), 
        'agro_ecological_zone': zone
    }

    # Predicting (with Weather Data)
    prediction = predict_soil(params, weather_data=weather_data)


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




@api_bp.route('/map_data', methods=['GET'])
def map_data():

    weather_api_key = os.getenv('WEATHER_API_KEY')
    
    districts_info = [
        {"name": "Ampara", "zone": "Dry Zone", "lat": 7.2945, "lng": 81.6744},
        {"name": "Anuradhapura", "zone": "Dry Zone", "lat": 8.3114, "lng": 80.4037},
        {"name": "Badulla", "zone": "Intermediate Zone", "lat": 6.9819, "lng": 81.0558},
        {"name": "Batticaloa", "zone": "Dry Zone", "lat": 7.7170, "lng": 81.6985},
        {"name": "Colombo", "zone": "Wet Zone", "lat": 6.9271, "lng": 79.8612},
        {"name": "Galle", "zone": "Wet Zone", "lat": 6.0328, "lng": 80.2150},
        {"name": "Gampaha", "zone": "Wet Zone", "lat": 7.0873, "lng": 79.9996},
        {"name": "Hambantota", "zone": "Dry Zone", "lat": 6.1246, "lng": 81.1213},
        {"name": "Jaffna", "zone": "Dry Zone", "lat": 9.6615, "lng": 80.0255},
        {"name": "Kalutara", "zone": "Wet Zone", "lat": 6.5854, "lng": 79.9607},
        {"name": "Kandy", "zone": "Wet Zone", "lat": 7.2906, "lng": 80.6337},
        {"name": "Kegalle", "zone": "Wet Zone", "lat": 7.2513, "lng": 80.3464},
        {"name": "Kilinochchi", "zone": "Dry Zone", "lat": 9.3803, "lng": 80.3770},
        {"name": "Kurunegala", "zone": "Intermediate Zone", "lat": 7.4818, "lng": 80.3609},
        {"name": "Mannar", "zone": "Dry Zone", "lat": 8.9810, "lng": 79.9044},
        {"name": "Matale", "zone": "Intermediate Zone", "lat": 7.4675, "lng": 80.6234},
        {"name": "Matara", "zone": "Wet Zone", "lat": 5.9549, "lng": 80.5469},
        {"name": "Monaragala", "zone": "Intermediate Zone", "lat": 6.8728, "lng": 81.3507},
        {"name": "Mullaitivu", "zone": "Dry Zone", "lat": 9.2671, "lng": 80.8142},
        {"name": "Nuwara Eliya", "zone": "Wet Zone", "lat": 6.9497, "lng": 80.7828},
        {"name": "Polonnaruwa", "zone": "Dry Zone", "lat": 7.9403, "lng": 81.0188},
        {"name": "Puttalam", "zone": "Dry Zone", "lat": 8.0362, "lng": 79.8283},
        {"name": "Ratnapura", "zone": "Wet Zone", "lat": 6.7056, "lng": 80.3847},
        {"name": "Trincomalee", "zone": "Dry Zone", "lat": 8.5711, "lng": 81.2333},
        {"name": "Vavuniya", "zone": "Dry Zone", "lat": 8.7542, "lng": 80.4982}
    ]
    
    map_result = []  

    for d in districts_info: 
        lat = d['lat']
        lng = d['lng']
        temp = 28.0
        rainfall = 0.0

        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&units=metric&appid={weather_api_key}"
            response = requests.get(url, timeout=5).json()
            
            temp = response['main']['temp']
            rainfall = response.get('rain', {}).get('1h', 0.0)

            if rainfall > 0.5:
                color = "#3b82f6"
                condition = "Rainy"
            elif temp > 32.0:
                color = "#eab308"
                condition = "High Temp"
            else:
                color = "#22c55e"
                condition = "Normal Weather"

        except Exception as e:
            print(f"Weather API Error for {d['name']}: {e}")
            color = "#22c55e"
            condition = "Normal Weather"

        map_result.append({  
            "district": d['name'],
            "zone": d['zone'],
            "temp": round(temp, 1),
            "rainfall": round(rainfall, 1),
            "condition": condition,
            "color": color
        })

    return jsonify(map_result)  




@api_bp.route('/forecast_chart/<farm_id>', methods=['GET'])
def forecast_chart(farm_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        farm = Farm.get_farm_by_id(farm_id)
        if not farm:
            return jsonify({"error": "Farm not found"}), 404

        device_id = farm.get('sensors', {}).get('device_id')
        location = farm.get('location', {})
        lat = location.get('lat')
        lng = location.get('lng')


        historical_readings = list(mongo.db.sensor_readings.find(
            {"device_id": device_id}
        ).sort([("timestamp", 1)]).limit(100))


        X_train = [] 
        y_train = []
        
        has_enough_data = len(historical_readings) > 10 
        
        if has_enough_data:
            base_time = historical_readings[0]['timestamp']
            
            for reading in historical_readings:
                try:

                    hours_diff = (reading['timestamp'] - base_time).total_seconds() / 3600
                    temp = float(reading.get('temperature', 30.0))
                    moisture = float(reading.get('soil_moisture', 50.0))
                    
                    X_train.append([hours_diff, temp])
                    y_train.append(moisture)
                except (ValueError, TypeError):
                    continue
       
            model = LinearRegression()
            if len(X_train) > 0:
                model.fit(X_train, y_train)


        weather_api_key = os.getenv('WEATHER_API_KEY')
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&appid={weather_api_key}&units=metric"
        
        forecast_res = requests.get(forecast_url, timeout=5).json()
        
        if 'list' not in forecast_res:
            return jsonify({"error": "Failed to fetch forecast list"}), 400

        dates, temps, moistures = [], [], []


        current_sim_moisture = float(historical_readings[-1].get('soil_moisture', 50.0)) if historical_readings else 50.0
        

        for i in [7, 15, 23]:
            if i < len(forecast_res['list']):
                day_data = forecast_res['list'][i]
                date_str = day_data['dt_txt'].split(' ')[0]
                forecast_temp = day_data['main']['temp']
                rain = day_data.get('rain', {}).get('3h', 0.0)

                if has_enough_data and len(X_train) > 0:


                    future_hours = (historical_readings[-1]['timestamp'] - base_time).total_seconds() / 3600 + (i * 3) 
                    
                    predicted_moisture = model.predict([[future_hours, forecast_temp]])[0]

                    rain_boost = rain * 5.0
                    predicted_moisture += rain_boost
                    

                    final_moisture = max(0, min(100, predicted_moisture))
                    current_sim_moisture = final_moisture 
                    
                else:

                    temp_factor = (forecast_temp - 25) * 0.5 if forecast_temp > 25 else 0
                    rain_factor = rain * 5.0
                    current_sim_moisture = current_sim_moisture - temp_factor + rain_factor - 2.0
                    final_moisture = max(0, min(100, current_sim_moisture))

                dates.append(date_str)
                temps.append(round(forecast_temp, 1))
                moistures.append(round(final_moisture, 1))

        return jsonify({
            "status": "success",
            "dates": dates,
            "temps": temps,
            "moistures": moistures
        })

    except Exception as e:
        print(f"ML Forecast Error: {e}")
        return jsonify({"error": str(e)}), 500


@api_bp.route('/analytics_data/<farm_id>', methods=['GET'])
def get_analytics_data(farm_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        farm = Farm.get_farm_by_id(farm_id)
        if not farm:
            return jsonify({"error": "Farm not found"}), 404

        device_id = farm.get('sensors', {}).get('device_id')
        location = farm.get('location', {})
        lat, lng = location.get('lat'), location.get('lng')


        readings = list(mongo.db.sensor_readings.find(
            {"device_id": device_id}
        ).sort([("timestamp", -1)]).limit(20))
        readings.reverse()  

        if not readings:
            return jsonify({"status": "no_data", "message": "No sensor readings found"})


        avg_moisture = round(np.mean([r.get('soil_moisture', 0) for r in readings if r.get('soil_moisture') != '--']), 1)
        avg_temp = round(np.mean([r.get('temperature', 0) for r in readings if r.get('temperature') != '--']), 1)
        avg_ph = round(np.mean([r.get('ph_level', 0) for r in readings if r.get('ph_level') != '--']), 1)
        avg_n = round(np.mean([r.get('nitrogen', 0) for r in readings if r.get('nitrogen') != '--']), 1)
        avg_p = round(np.mean([r.get('phosphorus', 0) for r in readings if r.get('phosphorus') != '--']), 1)
        avg_k = round(np.mean([r.get('potassium', 0) for r in readings if r.get('potassium') != '--']), 1)


        weather_api_key = os.getenv('WEATHER_API_KEY')
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&appid={weather_api_key}&units=metric"
        
        rain_data = []
        ambient_temps = []
        try:
            f_resp = requests.get(forecast_url, timeout=5).json()
            if 'list' in f_resp:
                for item in f_resp['list'][:len(readings)]:
                    rain_data.append(item.get('rain', {}).get('3h', 0.0))
                    ambient_temps.append(item.get('main', {}).get('temp', 28.0))
        except Exception:
            rain_data = [0.0] * len(readings)
            ambient_temps = [28.0] * len(readings)


        timestamps = []
        moistures = []
        soil_temps = []
        phs = []
        n_vals, p_vals, k_vals = [], [], []

        for r in readings:
            ts = r.get('timestamp')
            if isinstance(ts, datetime):
                local_ts = ts + timedelta(hours=5, minutes=30)
                timestamps.append(local_ts.strftime("%b %d %I:%M %p"))
            else:
                timestamps.append("N/A")

            moistures.append(r.get('soil_moisture', 0))
            soil_temps.append(r.get('temperature', 0))
            phs.append(r.get('ph_level', 0))
            n_vals.append(r.get('nitrogen', 0))
            p_vals.append(r.get('phosphorus', 0))
            k_vals.append(r.get('potassium', 0))

        # Soil Health Index (%) Calculation
        soil_health_scores = [
            min(100, int((avg_moisture / 60) * 100)),
            min(100, int((avg_ph / 6.5) * 100)),
            min(100, int((avg_n / 140) * 100)),
            min(100, int((avg_p / 50) * 100)),
            min(100, int((avg_k / 200) * 100)),
            100 if 20 <= avg_temp <= 32 else 70
        ]

        return jsonify({
            "status": "success",
            "averages": {
                "moisture": avg_moisture,
                "temp": avg_temp,
                "ph": avg_ph,
                "nitrogen": avg_n,
                "phosphorus": avg_p,
                "potassium": avg_k
            },
            "charts": {
                "timestamps": timestamps,
                "moisture": moistures,
                "rain": rain_data,
                "soil_temp": soil_temps,
                "ambient_temp": ambient_temps,
                "ph": phs,
                "npk_actual": [avg_n, avg_p, avg_k],
                "npk_target": [140, 50, 200],  # Standard target NPK values
                "npk_history": {"N": n_vals, "P": p_vals, "K": k_vals},
                "health_scores": soil_health_scores
            }
        })

    except Exception as e:
        print(f"Analytics API Error: {e}")
        return jsonify({"error": str(e)}), 500



@api_bp.route('/soil_predictions/<farm_id>', methods=['GET'])
def get_soil_predictions(farm_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        farm = Farm.get_farm_by_id(farm_id)
        if not farm:
            return jsonify({"error": "Farm not found"}), 404

        device_id = farm.get('sensors', {}).get('device_id')
        location = farm.get('location', {})
        lat, lng = location.get('lat'), location.get('lng')


        readings = list(mongo.db.sensor_readings.find(
            {"device_id": device_id}
        ).sort([("timestamp", 1)]).limit(100)) 

        # 2. OpenWeather Forecast Data 
        weather_api_key = os.getenv('WEATHER_API_KEY')
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&appid={weather_api_key}&units=metric"
        
        forecast_res = requests.get(forecast_url, timeout=5).json()
        
        daily_weather = {}
        for item in forecast_res.get('list', []):
            date_str = item['dt_txt'].split(' ')[0]
            if date_str not in daily_weather:
                daily_weather[date_str] = {'temp': [], 'rain': []}
            daily_weather[date_str]['temp'].append(item['main']['temp'])
            daily_weather[date_str]['rain'].append(item.get('rain', {}).get('3h', 0.0))

   
        future_dates = list(daily_weather.keys())[:5]
        forecast_temps = [round(np.mean(daily_weather[d]['temp']), 2) for d in future_dates]
        forecast_rains = [round(sum(daily_weather[d]['rain']), 2) for d in future_dates]

        # 3. Data Preparation for ML Models
        has_enough_data = len(readings) > 10
        base_time = readings[0]['timestamp'] if has_enough_data else datetime.utcnow()


        last_reading_time = readings[-1]['timestamp'] if has_enough_data else datetime.utcnow()
        future_days = [(last_reading_time - base_time).days + i + 1 for i in range(5)]

        # --- PREDICTION 1: Moisture Depletion ---
        moisture_preds = []
        m_insights = []
        if has_enough_data:
            X_m = [[(r['timestamp'] - base_time).days, float(r.get('temperature', 30)), float(r.get('humidity', 60))] for r in readings if r.get('temperature') != '--']
            y_m = [float(r.get('soil_moisture', 50)) for r in readings if r.get('soil_moisture') != '--']
            
            if len(X_m) > 0 and len(y_m) > 0:
                model_m = LinearRegression().fit(X_m, y_m)
                for i in range(5):

                    pred = model_m.predict([[future_days[i], forecast_temps[i], 60]])[0]

                    pred += (forecast_rains[i] * 2.5) 
                    moisture_preds.append(round(max(0, min(100, pred)), 1))
        
        if not moisture_preds: 
            moisture_preds = [50.0] * 5 # Fallback
        
        min_moisture = min(moisture_preds)
        if min_moisture < 30:
            m_insights.append(f"🔴 Critical: Soil moisture will drop to {min_moisture}% due to high temps. Immediate irrigation required.")
        elif sum(forecast_rains) > 20:
            m_insights.append(f"🟢 Optimal: Upcoming rainfall ({sum(forecast_rains)}mm) will naturally maintain soil moisture above 40%.")
        else:
            m_insights.append(f"🟡 Warning: Moisture levels are steadily decreasing. Plan irrigation by {future_dates[moisture_preds.index(min_moisture)]}.")
        m_insights.append(f"Average expected temperature for the next 5 days is {round(np.mean(forecast_temps),1)}°C.")


        n_preds = []
        n_insights = []
        current_n = float(readings[-1].get('nitrogen', 100)) if has_enough_data and readings[-1].get('nitrogen') != '--' else 100.0
        
        for i in range(5):

            depletion_rate = 1.5 + (forecast_rains[i] * 0.8) 
            current_n = max(0, current_n - depletion_rate)
            n_preds.append(round(current_n, 1))

        n_drop = n_preds[0] - n_preds[-1]
        n_insights.append(f"📉 Trend: Nitrogen levels are predicted to drop by {round(n_drop, 1)} mg/kg over the next 5 days.")
        if sum(forecast_rains) > 30:
             n_insights.append("🔴 High Risk: Heavy rainfall will cause severe Nitrogen leaching. Do NOT apply fertilizers right now.")
        elif n_preds[-1] < 50:
             n_insights.append("🟡 Warning: Nitrogen levels will reach a critical low. Prepare for top-dressing fertilizer application.")
        else:
             n_insights.append("🟢 Stable: Nitrogen depletion is at a normal biological rate.")

        # --- PREDICTION 3: pH Shift / Soil Acidity Trend ---
        ph_preds = []
        ph_insights = []
        if has_enough_data:
            X_ph = [[(r['timestamp'] - base_time).days] for r in readings if r.get('ph_level') != '--']
            y_ph = [float(r.get('ph_level', 7.0)) for r in readings if r.get('ph_level') != '--']
            
            if len(X_ph) > 0 and len(y_ph) > 0:
                model_ph = LinearRegression().fit(X_ph, y_ph)
                for i in range(5):
                    pred_ph = model_ph.predict([[future_days[i]]])[0]

                    pred_ph -= (forecast_rains[i] * 0.01)
                    ph_preds.append(round(max(0, min(14, pred_ph)), 2))
        
        if not ph_preds:
            ph_preds = [7.0] * 5

        ph_trend = ph_preds[-1] - ph_preds[0]
        if abs(ph_trend) < 0.1:
            ph_insights.append("🟢 Stable: Soil pH remains highly stable within the current range.")
        elif ph_trend < 0:
            ph_insights.append(f"🟡 Acidification: Soil is slowly becoming more acidic (Expected drop to {ph_preds[-1]}).")
            if ph_preds[-1] < 5.5:
                ph_insights.append("🔴 Action Required: pH is dropping below optimal levels. Consider applying agricultural lime.")
        else:
            ph_insights.append(f"🟡 Alkalization: Soil is becoming more alkaline (Expected rise to {ph_preds[-1]}).")



        # --- PREDICTION 4: Moisture vs Temp (Dashboard style for 5 days) ---
        mt_insights = []
        highest_temp = max(forecast_temps)
        if highest_temp > 32:
            mt_insights.append(f"🔴 Warning: Expected peak temperature is {highest_temp}°C. Rapid moisture evaporation expected.")
        else:
            mt_insights.append("🟢 Thermal balance is optimal. Soil moisture retention will be stable.")

        # --- PREDICTION 5: Rainfall Prediction ---
        rain_insights = []
        total_rain = sum(forecast_rains)
        if total_rain == 0:
            rain_insights.append("🟡 Drought Risk: Zero rainfall predicted. Heavy reliance on manual irrigation required.")
        elif total_rain > 50:
            rain_insights.append(f"🔴 Flood/Waterlogging Risk: Heavy total rainfall ({total_rain}mm) expected. Ensure proper farm drainage.")
        else:
            rain_insights.append(f"🟢 Good Condition: Moderate rainfall ({total_rain}mm) expected. Ideal for crop growth.")

        # --- PREDICTION 6: Fungal & Disease Risk ---
        disease_preds = []
        disease_insights = []
        for i in range(5):

            risk_index = min(100, max(0, (forecast_rains[i] * 3) + (forecast_temps[i] - 25) * 4))
            disease_preds.append(round(risk_index, 1))

        peak_disease = max(disease_preds)
        if peak_disease > 70:
            disease_insights.append("🔴 High Risk: Hot & humid conditions favor fungal diseases (e.g., Blight, Mildew). Apply preventative fungicides.")
        elif peak_disease > 40:
            disease_insights.append("🟡 Moderate Risk: Keep an eye on leaf moisture and fungal spots.")
        else:
            disease_insights.append("🟢 Low Risk: Weather conditions are not favorable for major crop diseases.")


        formatted_dates = [datetime.strptime(d, "%Y-%m-%d").strftime("%b %d") for d in future_dates]

        return jsonify({
            "status": "success",
            "dates": formatted_dates,
            "predictions": {
                "moisture": {"data": moisture_preds, "insights": m_insights},
                "nitrogen": {"data": n_preds, "insights": n_insights},
                "ph": {"data": ph_preds, "insights": ph_insights},
                

                "moisture_temp": {"temps": forecast_temps, "moistures": moisture_preds, "insights": mt_insights},
                "rainfall": {"data": forecast_rains, "insights": rain_insights},
                "disease": {"data": disease_preds, "insights": disease_insights}
            }
        })

    except Exception as e:
        print(f"Prediction API Error: {e}")
        return jsonify({"error": str(e)}), 500



@api_bp.route('/sensor_history/<farm_id>', methods=['GET'])
def get_sensor_history(farm_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        farm = Farm.get_farm_by_id(farm_id)
        if not farm:
            return jsonify({"error": "Farm not found"}), 404

        device_id = farm.get('sensors', {}).get('device_id')
        

        readings = list(mongo.db.sensor_readings.find(
            {"device_id": device_id}
        ).sort([("timestamp", -1)]).limit(50))
        
        history_list = []
        for r in readings:
            ts = r.get('timestamp')
            if isinstance(ts, datetime):

                local_ts = ts + timedelta(hours=5, minutes=30)
                time_str = local_ts.strftime("%Y-%m-%d %I:%M %p")
            else:
                time_str = "N/A"
                
            history_list.append({
                "timestamp": time_str,
                "moisture": r.get('soil_moisture', '--'),
                "temp": r.get('temperature', '--'),
                "ph": r.get('ph_level', '--'),
                "nitrogen": r.get('nitrogen', '--'),
                "phosphorus": r.get('phosphorus', '--'),
                "potassium": r.get('potassium', '--')
            })
            
        return jsonify({"status": "success", "history": history_list})
    
    except Exception as e:
        print(f"Sensor History Error: {e}")
        return jsonify({"error": str(e)}), 500
