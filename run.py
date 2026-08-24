from flask import jsonify
from app import create_app, mongo
from bson.objectid import ObjectId

app = create_app()

@app.route('/api/get_all_farm_hierarchy', methods=['GET'])
def get_all_farm_hierarchy():
    try:
        # 1. 'users' collection එකෙන් සියලුම පරිශීලකයින් (Farmers) ලබාගැනීම
        users = list(mongo.db.users.find({}))
        
        result_data = []

        for user in users:
            user_id = user.get('_id')
            
            # 2. අදාළ User ට අයත් Farms ලබාගැනීම 
            # (සටහන: ඔබේ farms collection එකේ user ට සම්බන්ධ field එක 'user_id' හෝ 'farmer_id' විය හැක. 
            # පහත දැක්වෙන්නේ 'user_id' මගින් සෙවීමයි. අවශ්‍ය නම් එය වෙනස් කරන්න.)
            farms = list(mongo.db.farms.find({"user_id": user_id}))
            
            farms_list = []
            for farm in farms:
                farm_id = farm.get('_id')
                
                # 3. අදාළ Farm එකට සම්බන්ධ සෙන්සර් වල නවතම දත්ත ලබාගැනීම (sensor_readings හරහා)
                pipeline = [
                    {"$match": {"farm_id": farm_id}},
                    {"$sort": {"timestamp": -1}},
                    {"$group": {
                        "_id": "$device_id",
                        "latest_reading": {"$first": "$$ROOT"}
                    }}
                ]
                sensor_readings = list(mongo.db.sensor_readings.aggregate(pipeline))
                
                sensors_list = []
                for sr in sensor_readings:
                    data = sr['latest_reading']
                    if '_id' in data: del data['_id']
                    if 'farm_id' in data: data['farm_id'] = str(data['farm_id'])
                    if 'timestamp' in data: data['timestamp'] = str(data['timestamp'])
                    sensors_list.append(data)

                # Farm දත්ත සැකසීම
                farms_list.append({
                    "farm_id": str(farm_id),
                    "farm_name": farm.get("farm_name", farm.get("name", "Unknown Farm")),
                    "sensors_count": len(sensors_list),
                    "sensors": sensors_list
                })

            # User / Farmer දත්ත සැකසීම
            result_data.append({
                "user_id": str(user_id),
                "username": user.get("username", user.get("name", "Unknown User")),
                "farms_count": len(farms_list),
                "farms": farms_list
            })

        return jsonify({
            "total_users": len(result_data),
            "data": result_data,
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("SmartSeed AI Core System Started (Full Hierarchy API)")
    print("http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000, host='0.0.0.0')