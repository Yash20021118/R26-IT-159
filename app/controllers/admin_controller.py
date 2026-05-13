from flask import Blueprint, render_template, request, jsonify, session, redirect
from app.models.admin import Admin
from app.models.user import User
from app.models.farm import Farm
import bcrypt
from app import mongo
import requests
import os
import math

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')



# Obtain the latitude and longitude of the farm and find the district and climate zone (Dry, Wet, Intermediate) to which it belongs.
def get_location_details(lat, lng):

    weather_api_key = os.getenv('WEATHER_API_KEY')
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lng}&limit=5&appid={weather_api_key}"
    
    detected_district = "Unknown"
    detected_zone = "Unknown Zone"
    
    zones = {
        "Ampara": "Dry Zone", "Anuradhapura": "Dry Zone", "Badulla": "Intermediate Zone",
        "Batticaloa": "Dry Zone", "Colombo": "Wet Zone", "Galle": "Wet Zone",
        "Gampaha": "Wet Zone", "Hambantota": "Dry Zone", "Jaffna": "Dry Zone",
        "Kalutara": "Wet Zone", "Kandy": "Wet Zone", "Kegalle": "Wet Zone",
        "Kilinochchi": "Dry Zone", "Kurunegala": "Intermediate Zone", "Mannar": "Dry Zone",
        "Matale": "Intermediate Zone", "Matara": "Wet Zone", "Monaragala": "Intermediate Zone",
        "Mullaitivu": "Dry Zone", "Nuwara Eliya": "Wet Zone", "Polonnaruwa": "Dry Zone",
        "Puttalam": "Dry Zone", "Ratnapura": "Wet Zone", "Trincomalee": "Dry Zone",
        "Vavuniya": "Dry Zone"
    }
    
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            
            search_text = ""
            for item in data:
                search_text += f" {item.get('name', '')} {item.get('state', '')}"
                if 'local_names' in item:
                    search_text += " ".join(str(v) for v in item['local_names'].values())
            
            search_text = search_text.lower()

            sorted_zones = sorted(zones.items(), key=lambda x: len(x[0]), reverse=True)
            
            for d_name, d_zone in sorted_zones:
                if d_name.lower() in search_text:
                    detected_district = d_name
                    detected_zone = d_zone
                    break
                    
    except Exception as e:
        print(f"Geocoding Error: {e}")

    # If the exact district is not captured by the OpenWeather API (Fallback Method)
    if detected_district == "Unknown":
        districts_coords = [
            {"name": "Ampara", "lat": 7.2945, "lng": 81.6744}, {"name": "Anuradhapura", "lat": 8.3114, "lng": 80.4037},
            {"name": "Badulla", "lat": 6.9819, "lng": 81.0558}, {"name": "Batticaloa", "lat": 7.7170, "lng": 81.6985},
            {"name": "Colombo", "lat": 6.9271, "lng": 79.8612}, {"name": "Galle", "lat": 6.0328, "lng": 80.2150},
            {"name": "Gampaha", "lat": 7.0873, "lng": 79.9996}, {"name": "Hambantota", "lat": 6.1246, "lng": 81.1213},
            {"name": "Jaffna", "lat": 9.6615, "lng": 80.0255}, {"name": "Kalutara", "lat": 6.5854, "lng": 79.9607},
            {"name": "Kandy", "lat": 7.2906, "lng": 80.6337}, {"name": "Kegalle", "lat": 7.2513, "lng": 80.3464},
            {"name": "Kilinochchi", "lat": 9.3803, "lng": 80.3770}, {"name": "Kurunegala", "lat": 7.4818, "lng": 80.3609},
            {"name": "Mannar", "lat": 8.9810, "lng": 79.9044}, {"name": "Matale", "lat": 7.4675, "lng": 80.6234},
            {"name": "Matara", "lat": 5.9549, "lng": 80.5469}, {"name": "Monaragala", "lat": 6.8728, "lng": 81.3507},
            {"name": "Mullaitivu", "lat": 9.2671, "lng": 80.8142}, {"name": "Nuwara Eliya", "lat": 6.9497, "lng": 80.7828},
            {"name": "Polonnaruwa", "lat": 7.9403, "lng": 81.0188}, {"name": "Puttalam", "lat": 8.0362, "lng": 79.8283},
            {"name": "Ratnapura", "lat": 6.7056, "lng": 80.3847}, {"name": "Trincomalee", "lat": 8.5711, "lng": 81.2333},
            {"name": "Vavuniya", "lat": 8.7542, "lng": 80.4982}
        ]
        min_distance = float('inf')
        for d in districts_coords:
            dist = math.sqrt((lat - d['lat'])**2 + (lng - d['lng'])**2)
            if dist < min_distance:
                min_distance = dist
                detected_district = d['name']
                detected_zone = zones[d['name']]

    return detected_district, detected_zone




# Obtaining the correct Agro-Ecological Zone and Altitude above sea level where the farm is located.
def get_exact_agro_zone_and_altitude(target_lat, target_lng, auto_district):
    
    district_zones = list(mongo.db.SL_Agro_Ecological_Zones.find({"District": auto_district}))
    
    if not district_zones:
        district_zones = list(mongo.db.SL_Agro_Ecological_Zones.find({}))
    
    min_distance = float('inf')
    best_agro_zone = "Unknown"
    best_altitude = 50.0 # Default altitude
    
    # 2. Search for the nearest zone only among the zones within the relevant district
    for zone_data in district_zones:
        try:
            z_lat = float(zone_data.get('Latitude', 0))
            z_lng = float(zone_data.get('Longitude', 0))
        except ValueError:
            continue
            
        dist = math.sqrt((target_lat - z_lat)**2 + (target_lng - z_lng)**2)
        
        if dist < min_distance:
            min_distance = dist
            best_agro_zone = zone_data.get('Zone_Code', 'Unknown') 
            best_altitude = float(zone_data.get('Elevation_m', 50.0))
            
    return best_agro_zone, best_altitude


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password') 

        admin = Admin.get_admin_by_email(email)
        
        if admin and bcrypt.checkpw(password.encode('utf-8'), admin['password_hash']):
            session['admin_id'] = str(admin['_id'])
            return redirect('/admin/dashboard')
        else:
            return render_template('admin/login.html', error="Invalid email or password")
            
    return render_template('admin/login.html')

@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if 'admin_id' not in session:
        return redirect('/admin/login')
    
    farmers = list(mongo.db.users.find({}, {"_id": 1, "name": 1, "email": 1}))
    for farmer in farmers:
        farmer['_id'] = str(farmer['_id'])
        
    return render_template('admin/dashboard.html', farmers=farmers)

@admin_bp.route('/register_farmer', methods=['POST'])
def register_farmer():
    if 'admin_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.json
        hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        user_id = User.create_user(
            name=data['farmer_name'],
            email=data['email'],
            password_hash=hashed_pw,
            created_by_admin_id=session['admin_id']
        )

        lat = float(data['lat'])
        lng = float(data['lng'])
        
        auto_district, auto_zone = get_location_details(lat, lng)

        agro_zone, altitude = get_exact_agro_zone_and_altitude(lat, lng, auto_district)

        farm_id = Farm.create_farm(
            user_id=user_id,
            farm_name=data['farm_name'],
            lat=lat,
            lng=lng,
            district=auto_district,
            zone=auto_zone,
            agro_zone=agro_zone,  
            altitude=altitude,  
            device_id=data['device_id']
        )
        
        return jsonify({
            "message": f"Farmer & Farm registered! Auto-detected: {auto_district} ({agro_zone}), Altitude: {round(altitude, 2)}m", 
            "farm_id": str(farm_id)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@admin_bp.route('/add_farm', methods=['POST'])
def add_farm():
    if 'admin_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        data = request.json
        user_id = data['user_id']
        
        lat = float(data['lat'])
        lng = float(data['lng'])
        

        auto_district, auto_zone = get_location_details(lat, lng)

        agro_zone, altitude = get_exact_agro_zone_and_altitude(lat, lng, auto_district)

        farm_id = Farm.create_farm(
            user_id=user_id,
            farm_name=data['farm_name'],
            lat=lat,
            lng=lng,
            district=auto_district,
            zone=auto_zone,
            agro_zone=agro_zone,  
            altitude=altitude,    
            device_id=data['device_id']
        )
        
        return jsonify({
            "message": f"Farm added successfully! Auto-detected: {auto_district} ({agro_zone}), Altitude: {round(altitude, 2)}m", 
            "farm_id": str(farm_id)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    return redirect('/admin/login')