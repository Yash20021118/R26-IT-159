from flask import jsonify
from app import create_app, mongo
from bson.objectid import ObjectId

app = create_app()

@app.route('/api/get_all_farm_hierarchy', methods=['GET'])
def get_all_farm_hierarchy():
    try:

        users = list(mongo.db.users.find({}))
        
        result_data = []

        for user in users:
            user_id = user.get('_id')
            

            farms = list(mongo.db.farms.find({"user_id": user_id}))
            
            farms_list = []
            for farm in farms:
                farm_id = farm.get('_id')
                

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


                farms_list.append({
                    "farm_id": str(farm_id),
                    "farm_name": farm.get("farm_name", farm.get("name", "Unknown Farm")),
                    "sensors_count": len(sensors_list),
                    "sensors": sensors_list
                })


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

import os

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5050))
    print("=" * 50)
    print("SmartSeed AI Core System Started (Full Hierarchy API)")
    print(f"http://localhost:{port}")
    print("=" * 50)
    app.run(debug=True, use_reloader=False, port=port, host='0.0.0.0')
