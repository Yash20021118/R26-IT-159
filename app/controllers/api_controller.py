import re
import threading

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


# ---------------------------------------------------------------------------
# Helper: MongoDB indexes
# ---------------------------------------------------------------------------
# Nearly every route in this file filters sensor_readings by device_id and
# sorts by timestamp. Without an index that's a full collection scan on every
# request, which gets slow fast as the collection grows. This isn't called
# automatically (creating indexes belongs in app startup, not per-request) -
# call it once after mongo.init_app(app) in your app factory, e.g. in
# app/__init__.py:
#
#     from app.routes.api_controller import ensure_indexes
#     mongo.init_app(app)
#     with app.app_context():
#         ensure_indexes()
#
# create_index() is a no-op if the index already exists, so it's safe to
# leave this call in place permanently rather than running it as a one-off.
def ensure_indexes():
    mongo.db.sensor_readings.create_index([("device_id", 1), ("timestamp", -1)])
    mongo.db.soil_rules.create_index([("Soil Type", 1), ("Factor", 1)])
    mongo.db.SL_Agro_Ecological_Zones.create_index([("District", 1)])


# ---------------------------------------------------------------------------
# Helper: time-range filtering + bucketed aggregation for analytics_data
# ---------------------------------------------------------------------------
# Fixes two things at once: (1) the analytics endpoint used to always show
# just "the last 20 readings" with no way to see more history, and (2) if you
# simply widened that to "last 30 days" without aggregating, a device
# reporting every few minutes would pack thousands of points onto the X-axis.
# Longer ranges get bucketed into coarser time slices so the chart stays
# readable regardless of reporting frequency.
RANGE_CONFIG = {
    "24h": {"delta": timedelta(hours=24), "bucket": None},     # raw points, no aggregation
    "7d":  {"delta": timedelta(days=7), "bucket": "hour"},
    "30d": {"delta": timedelta(days=30), "bucket": "day"},
    "90d": {"delta": timedelta(days=90), "bucket": "day"},
}
DEFAULT_RANGE = "7d"

def bucket_readings(readings, bucket):
    """Group raw readings into hour/day buckets, averaging numeric fields.
    `bucket=None` returns the readings unchanged (used for the 24h view,
    where raw granularity is usually still readable)."""
    if not bucket or not readings:
        return readings

    buckets = {}
    for r in readings:
        ts = r.get('timestamp')
        if not isinstance(ts, datetime):
            continue
        key = ts.replace(minute=0, second=0, microsecond=0) if bucket == "hour" \
            else ts.replace(hour=0, minute=0, second=0, microsecond=0)
        buckets.setdefault(key, []).append(r)

    def avg_field(group, field):
        vals = [float(g.get(field, 0)) for g in group if g.get(field) not in (None, '--')]
        return round(np.mean(vals), 2) if vals else None

    bucketed = []
    for key in sorted(buckets.keys()):
        group = buckets[key]
        bucketed.append({
            "timestamp": key,
            "soil_moisture": avg_field(group, "soil_moisture"),
            "temperature": avg_field(group, "temperature"),
            "ph_level": avg_field(group, "ph_level"),
            "nitrogen": avg_field(group, "nitrogen"),
            "phosphorus": avg_field(group, "phosphorus"),
            "potassium": avg_field(group, "potassium"),
            "predicted_soil": group[-1].get('predicted_soil'),  # most recent label in the bucket
        })
    return bucketed


# ---------------------------------------------------------------------------
# Helper: historical weather lookup
# ---------------------------------------------------------------------------
# OpenWeatherMap's free /forecast endpoint only returns FUTURE data, which is
# why the analytics/prediction charts were mixing past sensor readings with
# future rain forecasts. True historical weather needs either:
#   (a) OpenWeather's One Call 3.0 "timemachine" endpoint - requires a paid
#       subscription tier, but stays on the same provider/key you already use.
#   (b) Open-Meteo's free Archive API - no key required, ~5 day reporting lag
#       on the most recent data, coverage/precision can be lower in some regions.
# This uses (b) since it needs no billing/account changes. If you already have
# a paid OpenWeather plan, swap the implementation for the timemachine call
# (same signature) and nothing else in this file needs to change.
def get_historical_weather(lat, lng, timestamps):
    """
    Fetch historical temperature + rainfall for a list of datetime timestamps.
    Returns (temps, rains) lists aligned index-for-index with `timestamps`.
    """
    if not timestamps:
        return [], []

    dates = sorted(set(ts.strftime("%Y-%m-%d") for ts in timestamps if isinstance(ts, datetime)))
    if not dates:
        return [28.0] * len(timestamps), [0.0] * len(timestamps)

    start_date, end_date = dates[0], dates[-1]
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lng}"
        f"&start_date={start_date}&end_date={end_date}"
        "&hourly=temperature_2m,rain&timezone=UTC"
    )

    try:
        resp = requests.get(url, timeout=8).json()
        hourly_times = resp['hourly']['time']
        hourly_temp = resp['hourly']['temperature_2m']
        hourly_rain = resp['hourly']['rain']
        time_index = {t: i for i, t in enumerate(hourly_times)}
    except Exception as e:
        print("Historical Weather API Error:", e)
        return [28.0] * len(timestamps), [0.0] * len(timestamps)

    temps, rains = [], []
    for ts in timestamps:
        if not isinstance(ts, datetime):
            temps.append(28.0)
            rains.append(0.0)
            continue

        hour_key = ts.strftime("%Y-%m-%dT%H:00")
        idx = time_index.get(hour_key)
        if idx is None:
            day_prefix = ts.strftime("%Y-%m-%d")
            idx = next((i for t, i in time_index.items() if t.startswith(day_prefix)), None)

        if idx is not None and hourly_temp[idx] is not None:
            temps.append(hourly_temp[idx])
            rains.append(hourly_rain[idx] or 0.0)
        else:
            # No archive data yet for this hour (common for the last few days -
            # Open-Meteo's archive has a reporting lag). Use nearest neighbours.
            temps.append(28.0)
            rains.append(0.0)

    return temps, rains


# ---------------------------------------------------------------------------
# Helper: crop-specific NPK targets
# ---------------------------------------------------------------------------
# ASSUMPTION: expects an optional `crop_npk_requirements` collection keyed by
# crop name, e.g. {"crop": "Tea", "N": 120, "P": 45, "K": 180}. If that
# collection/field doesn't exist yet in your DB, this silently falls back to
# the same generic values that were hardcoded before - so nothing breaks, but
# you'll want to add real per-crop rows for this to stop being a placeholder.
DEFAULT_NPK_TARGET = {"N": 140, "P": 50, "K": 200}

def get_npk_target(farm):
    crop = farm.get('crop_type') or farm.get('crop')
    if crop:
        doc = mongo.db.crop_npk_requirements.find_one({"crop": crop})
        if doc:
            return [
                doc.get('N', DEFAULT_NPK_TARGET['N']),
                doc.get('P', DEFAULT_NPK_TARGET['P']),
                doc.get('K', DEFAULT_NPK_TARGET['K']),
            ]
    return [DEFAULT_NPK_TARGET['N'], DEFAULT_NPK_TARGET['P'], DEFAULT_NPK_TARGET['K']]


# ---------------------------------------------------------------------------
# Helper: soil health scores grounded in the same soil_rules collection
# already used for alerts, instead of ad hoc /60, /6.5 style magic numbers.
# ASSUMPTION: soil_rules has rows with Condition Level == "Optimal" per
# Factor/Soil Type. If your rule data uses a different label for the "good"
# band (e.g. "Ideal"), update OPTIMAL_LABEL below.
# ---------------------------------------------------------------------------
OPTIMAL_LABEL = "Optimal"
_HEALTH_FACTOR_MAP = {
    "moisture": "Moisture (%)",
    "ph": "pH Level",
    "nitrogen": "Nitrogen (N)",
    "phosphorus": "Phosphorus (P)",
    "potassium": "Potassium (K)",
    "temp": "Temperature (°C)",
}
_GENERIC_RANGES = {
    "moisture": (40, 60), "ph": (6.0, 7.0), "nitrogen": (100, 140),
    "phosphorus": (30, 50), "potassium": (150, 200), "temp": (20, 32),
}

def compute_health_scores(avg_values, soil_type):
    rules = {}
    if soil_type and soil_type not in ["No Sensor Data", "No Prediction", "Model Error"]:
        for rule in mongo.db.soil_rules.find({"Soil Type": soil_type, "Condition Level": OPTIMAL_LABEL}):
            for key, label in _HEALTH_FACTOR_MAP.items():
                if rule.get("Factor") == label:
                    rules[key] = (float(rule.get("min_value", 0)), float(rule.get("max_value", 99999)))

    scores = []
    for key in ["moisture", "ph", "nitrogen", "phosphorus", "potassium", "temp"]:
        low, high = rules.get(key, _GENERIC_RANGES[key])
        val = avg_values.get(key, 0)
        if low <= val <= high:
            scores.append(100)
        else:
            span = (high - low) or 1
            distance = min(abs(val - low), abs(val - high))
            scores.append(max(0, round(100 - (distance / span) * 100)))
    return scores


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




# ---------------------------------------------------------------------------
# Helper: /map_data cache
# ---------------------------------------------------------------------------
# 25 districts x 1 OpenWeather call each, hit every 30s by every open
# dashboard tab, was the single biggest way to burn through the free-tier
# rate limit. Weather doesn't meaningfully change minute to minute, so an
# in-process TTL cache removes almost all of that traffic: the first request
# after the TTL expires pays for the 25 calls, every request within the TTL
# window is served from memory.
#
# NOTE: this is a per-process cache (a plain dict), which is fine for a
# single Flask process (e.g. `flask run`, one gunicorn worker). If this is
# ever deployed behind multiple gunicorn/uwsgi workers, each worker has its
# own copy and you'd still get up to (workers x 25) calls per TTL window -
# at that point swap MAP_DATA_CACHE for a real Redis GET/SETEX and the
# route logic below doesn't need to change.
MAP_DATA_TTL = timedelta(minutes=10)
_map_data_cache = {"data": None, "fetched_at": None}
_map_data_lock = threading.Lock()

DISTRICTS_INFO = [
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


def _fetch_all_districts_weather():
    """The actual 25-call OpenWeather fan-out. Only called on a cache miss."""
    weather_api_key = os.getenv('WEATHER_API_KEY')
    map_result = []

    for d in DISTRICTS_INFO:
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

    return map_result


@api_bp.route('/map_data', methods=['GET'])
def map_data():
    now = datetime.utcnow()

    # Fast path: serve from cache without taking the lock if it's still
    # fresh - this is the common case (every request within the TTL window).
    cached = _map_data_cache["data"]
    fetched_at = _map_data_cache["fetched_at"]
    if cached is not None and fetched_at is not None and (now - fetched_at) < MAP_DATA_TTL:
        return jsonify(cached)

    # Cache miss (or expired): only one request should actually pay for the
    # 25 OpenWeather calls. Others that arrive while it's in flight wait for
    # the lock and then get the result it just computed, instead of each
    # kicking off their own 25-call fan-out.
    with _map_data_lock:
        # Re-check inside the lock in case another request refreshed the
        # cache while we were waiting for it.
        cached = _map_data_cache["data"]
        fetched_at = _map_data_cache["fetched_at"]
        if cached is not None and fetched_at is not None and (datetime.utcnow() - fetched_at) < MAP_DATA_TTL:
            return jsonify(cached)

        map_result = _fetch_all_districts_weather()
        _map_data_cache["data"] = map_result
        _map_data_cache["fetched_at"] = datetime.utcnow()

    return jsonify(map_result)




# ---------------------------------------------------------------------------
# Helper: /forecast_chart model cache
# ---------------------------------------------------------------------------
# The IoT device pushes a new sensor reading every few minutes (via
# /sensor_update); the dashboard polls this endpoint every 30s. Retraining a
# fresh LinearRegression on every poll was pure wasted CPU - the training
# data (and therefore the fitted model) is identical between two polls
# unless a new reading has actually landed in Mongo. So: cache the fitted
# model per device_id, and only retrain when the timestamp of the latest
# reading has moved on from what the cached model was trained on.
#
# Per-process cache, same caveat as MAP_DATA_CACHE above - fine for a single
# worker, needs a shared store (Redis, or pickle the model into Mongo) if
# this ever runs behind multiple gunicorn workers.
_forecast_model_cache = {}
_forecast_model_lock = threading.Lock()


def _get_or_train_forecast_model(device_id):
    """Returns (model_or_None, base_time_or_None, has_enough_data).

    Retrains only when the latest reading for this device is newer than
    what's cached. The cheap `find_one` sorted-desc query below is answered
    straight from the (device_id, timestamp) index already created in
    ensure_indexes(), so checking "is there new data yet?" doesn't require
    pulling/scanning the full 100-reading window on every request.
    """
    latest = mongo.db.sensor_readings.find_one(
        {"device_id": device_id}, sort=[("timestamp", -1)]
    )
    latest_ts = latest.get('timestamp') if latest else None

    cached = _forecast_model_cache.get(device_id)
    if cached and cached["latest_ts"] == latest_ts:
        return cached["model"], cached["base_time"], cached["has_enough_data"]

    with _forecast_model_lock:
        # Re-check inside the lock - another request may have just retrained.
        cached = _forecast_model_cache.get(device_id)
        if cached and cached["latest_ts"] == latest_ts:
            return cached["model"], cached["base_time"], cached["has_enough_data"]

        historical_readings = list(mongo.db.sensor_readings.find(
            {"device_id": device_id}
        ).sort([("timestamp", 1)]).limit(100))

        model = None
        base_time = None
        has_enough_data = len(historical_readings) > 10

        if has_enough_data:
            base_time = historical_readings[0]['timestamp']
            X_train, y_train = [], []

            for reading in historical_readings:
                try:
                    hours_diff = (reading['timestamp'] - base_time).total_seconds() / 3600
                    temp = float(reading.get('temperature', 30.0))
                    moisture = float(reading.get('soil_moisture', 50.0))

                    X_train.append([hours_diff, temp])
                    y_train.append(moisture)
                except (ValueError, TypeError):
                    continue

            if len(X_train) > 0:
                model = LinearRegression()
                model.fit(X_train, y_train)

        _forecast_model_cache[device_id] = {
            "model": model,
            "base_time": base_time,
            "has_enough_data": has_enough_data,
            "latest_ts": latest_ts,
        }

    return model, base_time, has_enough_data


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

        # historical_readings[-1] (most recent reading in this 100-window)
        # is still needed below for current_sim_moisture, so this query
        # stays - only the model itself is cached, not the reading fetch.
        historical_readings = list(mongo.db.sensor_readings.find(
            {"device_id": device_id}
        ).sort([("timestamp", 1)]).limit(100))

        model, base_time, has_enough_data = _get_or_train_forecast_model(device_id)

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

                if model is not None:


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


        range_key = request.args.get('range', DEFAULT_RANGE)
        range_cfg = RANGE_CONFIG.get(range_key, RANGE_CONFIG[DEFAULT_RANGE])
        cutoff = datetime.utcnow() - range_cfg['delta']

        raw_readings = list(mongo.db.sensor_readings.find(
            {"device_id": device_id, "timestamp": {"$gte": cutoff}}
        ).sort([("timestamp", 1)]))

        if not raw_readings:
            return jsonify({"status": "no_data", "message": f"No sensor readings found in the selected range ({range_key})"})

        readings = bucket_readings(raw_readings, range_cfg['bucket'])


        avg_moisture = round(np.mean([r.get('soil_moisture', 0) for r in readings if r.get('soil_moisture') not in (None, '--')]), 1)
        avg_temp = round(np.mean([r.get('temperature', 0) for r in readings if r.get('temperature') not in (None, '--')]), 1)
        avg_ph = round(np.mean([r.get('ph_level', 0) for r in readings if r.get('ph_level') not in (None, '--')]), 1)
        avg_n = round(np.mean([r.get('nitrogen', 0) for r in readings if r.get('nitrogen') not in (None, '--')]), 1)
        avg_p = round(np.mean([r.get('phosphorus', 0) for r in readings if r.get('phosphorus') not in (None, '--')]), 1)
        avg_k = round(np.mean([r.get('potassium', 0) for r in readings if r.get('potassium') not in (None, '--')]), 1)


        # FIX: previously this pulled FUTURE forecast data and zipped it
        # against PAST sensor readings by index, so e.g. today's actual soil
        # moisture got compared against next week's predicted rain. Now we
        # fetch weather for the actual date/hour of each reading.
        reading_timestamps = [r.get('timestamp') for r in readings]
        ambient_temps, rain_data = get_historical_weather(lat, lng, reading_timestamps)


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

        # FIX: was a fixed /60, /6.5, ... formula with no relation to the
        # farm's actual predicted soil type. Now grounded in the same
        # soil_rules collection used for the alerts on this endpoint's sibling
        # route, falling back to generic FAO-style ranges if no rule exists.
        latest_soil_type = readings[-1].get('predicted_soil') if readings else None
        soil_health_scores = compute_health_scores(
            {"moisture": avg_moisture, "ph": avg_ph, "nitrogen": avg_n,
             "phosphorus": avg_p, "potassium": avg_k, "temp": avg_temp},
            latest_soil_type
        )

        # FIX: was hardcoded [140, 50, 200] regardless of crop. Now looks up
        # a per-crop target if crop_npk_requirements has a row for this farm's
        # crop, otherwise keeps the same generic defaults as before.
        npk_target = get_npk_target(farm)

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
                "npk_target": npk_target,
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
                daily_weather[date_str] = {'temp': [], 'rain': [], 'humidity': []}
            daily_weather[date_str]['temp'].append(item['main']['temp'])
            daily_weather[date_str]['rain'].append(item.get('rain', {}).get('3h', 0.0))
            daily_weather[date_str]['humidity'].append(item['main'].get('humidity', 70))

   
        future_dates = list(daily_weather.keys())[:5]
        forecast_temps = [round(np.mean(daily_weather[d]['temp']), 2) for d in future_dates]
        forecast_rains = [round(sum(daily_weather[d]['rain']), 2) for d in future_dates]
        forecast_humidity = [round(np.mean(daily_weather[d]['humidity']), 1) for d in future_dates]

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
            # FIX: was always exactly 50% regardless of the farm's actual
            # readings. If we have ANY readings (just not >10, the threshold
            # for a trend model), use their real average as a flat baseline
            # instead of a made-up constant. Only fall back to 50% if there
            # is truly zero sensor data for this device.
            known = [float(r.get('soil_moisture', 0)) for r in readings if r.get('soil_moisture') not in (None, '--')]
            baseline = round(np.mean(known), 1) if known else 50.0
            moisture_preds = [baseline] * 5
        
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

        # FIX: was a made-up formula (1.5 + rain*0.8) presented as if it came
        # from a model. Now fits a real regression on this farm's own
        # historical nitrogen readings against the actual historical rainfall
        # on those dates (same historical-weather helper used in analytics).
        if has_enough_data:
            hist_temps, hist_rains = get_historical_weather(lat, lng, [r['timestamp'] for r in readings])
            X_n = [[(r['timestamp'] - base_time).days, hist_rains[i]]
                   for i, r in enumerate(readings) if r.get('nitrogen') != '--']
            y_n = [float(r.get('nitrogen')) for i, r in enumerate(readings) if r.get('nitrogen') != '--']

            if len(X_n) >= 3:
                model_n = LinearRegression().fit(X_n, y_n)
                for i in range(5):
                    pred_n = model_n.predict([[future_days[i], forecast_rains[i]]])[0]
                    current_n = max(0, round(pred_n, 1))
                    n_preds.append(current_n)

        if not n_preds:
            # Not enough historical N+rainfall pairs to fit a model yet.
            # Documented agronomy rule-of-thumb fallback, NOT a model output -
            # the chart/insight copy should make this distinction to the user.
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
            # FIX: was always exactly 7.0 regardless of actual readings.
            known = [float(r.get('ph_level', 0)) for r in readings if r.get('ph_level') not in (None, '--')]
            baseline = round(np.mean(known), 2) if known else 7.0
            ph_preds = [baseline] * 5

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
        # NOTE: this was never a real candidate for supervised ML - the DB has
        # no historical field recording actual disease/outbreak incidents, so
        # there's no label to train against. (1.5+rain*0.8-style regression
        # elsewhere at least fits real sensor history; this can't, yet.)
        # Rather than keep an arbitrary formula dressed up as a prediction,
        # this is now an explicit, documented favorability index based on
        # standard plant-pathology heuristics: most fungal pathogens are most
        # active with high relative humidity and temperatures roughly in the
        # 20-30°C band, with prolonged leaf wetness (correlated with rain)
        # compounding risk. If you start logging confirmed disease incidents
        # per farm, that table + these same weather features is what a real
        # classifier should be trained on later.
        disease_preds = []
        disease_insights = []
        for i in range(5):
            humidity_score = max(0, forecast_humidity[i] - 60) * 1.5          # ramps up above 60% RH
            temp_score = max(0, 15 - abs(forecast_temps[i] - 25)) * 3          # peaks at 25°C, tapers off outside it
            rain_score = min(30, forecast_rains[i] * 2)                       # sustained leaf wetness proxy, capped
            risk_index = min(100, max(0, humidity_score + temp_score + rain_score))
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




@api_bp.route('/soil_info/<soil_type>', methods=['GET'])
def get_soil_info(soil_type):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # පස් වර්ගයේ නම lowercase සහ formatted කර සෙවීම
        formatted_type = re.sub(r'[^a-z0-9]+', '_', soil_type.lower().strip())
        soil = mongo.db.soil_details.find_one({"soil_type_id": formatted_type})

        if not soil:
            # නම කෙලින්ම match නොවන්නේ නම් regex මගින් සෙවීම
            soil = mongo.db.soil_details.find_one({"soil_type_id": {"$regex": soil_type, "$options": "i"}})

        if not soil:
            return jsonify({"status": "error", "message": "Soil details not found"}), 404

        soil['_id'] = str(soil['_id'])
        return jsonify({"status": "success", "data": soil})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route('/zone_info/<zone_code>', methods=['GET'])
def get_zone_info(zone_code):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        zone_info = mongo.db.SL_Agro_Ecological_Zones.find_one({"Zone_Code": zone_code})

        if not zone_info:
            return jsonify({"status": "error", "message": "Zone details not found"}), 404

        zone_info['_id'] = str(zone_info['_id'])
        return jsonify({"status": "success", "data": zone_info})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# Seed Recommendation & Guidance Endpoints
# ---------------------------------------------------------------------------
@api_bp.route('/recommend_seeds', methods=['POST', 'GET'])
def recommend_seeds():
    try:
        if request.method == 'POST':
            data = request.json or {}
        else:
            data = request.args.to_dict()

        farm_id = data.get('farm_id')
        if farm_id:
            farm = Farm.get_farm_by_id(farm_id)
            if farm and 'sensors' in farm:
                device_id = farm['sensors'].get('device_id')
                latest_reading = mongo.db.sensor_readings.find_one(
                    {"device_id": device_id},
                    sort=[("timestamp", -1)]
                )
                if latest_reading:
                    data.setdefault('N', latest_reading.get('nitrogen', 90))
                    data.setdefault('P', latest_reading.get('phosphorus', 42))
                    data.setdefault('K', latest_reading.get('potassium', 43))
                    data.setdefault('ph', latest_reading.get('ph_level', 6.5))
                    data.setdefault('temperature', latest_reading.get('temperature', 25.0))
                    data.setdefault('humidity', latest_reading.get('humidity', 80.0))
                    data.setdefault('rainfall', latest_reading.get('rainfall', 200.0))

        # Default fallback values if any missing
        N = float(data.get('N', 90))
        P = float(data.get('P', 42))
        K = float(data.get('K', 43))
        temperature = float(data.get('temperature', 25.0))
        humidity = float(data.get('humidity', 80.0))
        ph = float(data.get('ph', 6.5))
        rainfall = float(data.get('rainfall', 200.0))

        # Load trained crop model
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'SeedRecommendationEngine', 'backend', 'trained_models', 'crop_model.pkl'
        )

        if not os.path.exists(model_path):
            # Fallback if trained_models path is different
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                'models', 'crop_model.pkl'
            )

        if not os.path.exists(model_path):
            return jsonify({
                "status": "error",
                "message": "Crop recommendation model not trained yet. Please run train_model.py."
            }), 404

        import joblib
        import numpy as np

        model = joblib.load(model_path)
        feature_order = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

        probabilities = model.predict_proba(features)[0]
        classes = model.classes_

        ranked = sorted(zip(classes, probabilities), key=lambda x: x[1], reverse=True)
        recommendations = []
        for crop, prob in ranked[:5]:
            percentage = round(float(prob) * 100, 1)
            recommendations.append({
                "crop": str(crop),
                "confidence": percentage,
                "suitability_percentage": percentage
            })

        best_crop = recommendations[0]["crop"] if recommendations else "rice"

        return jsonify({
            "status": "success",
            "input_params": {
                "N": N, "P": P, "K": K,
                "temperature": temperature, "humidity": humidity,
                "ph": ph, "rainfall": rainfall
            },
            "best_crop": best_crop,
            "best_confidence": recommendations[0]["confidence"] if recommendations else 0.0,
            "recommendations": recommendations
        })

    except Exception as e:
        print(f"Seed Recommendation API Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@api_bp.route('/crop_guidance/<crop_name>', methods=['GET'])
def get_crop_guidance_api(crop_name):
    try:
        from app.utils.crop_guidance import get_crop_guidance
        guidance = get_crop_guidance(crop_name)
        return jsonify({
            "status": "success",
            "guidance": guidance
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500