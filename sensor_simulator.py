import requests
import time
import random
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()
port = os.getenv('PORT', '5050')
API_URL = os.getenv('SENSOR_API_URL', f"http://localhost:{port}/api/sensor_update")


DEVICES = ["S_001", "S_002","S_003" ]

def generate_random_sensor_data(device_id):

    data = {
        "device_id": device_id,
        "soil_moisture": round(random.uniform(30.0, 85.0), 1),  # Humidity between 30% - 85%
        "ph_level": round(random.uniform(5.5, 7.8), 1),         # pH value between 5.5 - 7.8
        "temperature": round(random.uniform(22.0, 35.0), 1),    # Temperature between 22C - 35C
        "nitrogen": round(random.uniform(20.0, 80.0), 1),       # N value
        "phosphorus": round(random.uniform(15.0, 60.0), 1),     # P value
        "potassium": round(random.uniform(25.0, 70.0), 1)       # K value
    }
    return data

def run_simulator():
    print("=" * 50)
    print("SmartSeed Sensor Simulator Started!")
    print("Sending random data every 10 seconds. Press Ctrl+C to stop.")
    print("=" * 50)

    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n[{current_time}] Sending new data batch...")


            for device in DEVICES:
                payload = generate_random_sensor_data(device)
                
                try:
                    response = requests.post(API_URL, json=payload)
                    
                    if response.status_code == 201:
                        print(f"Success -> {device}: Temp {payload['temperature']}°C | Moist {payload['soil_moisture']}%")
                    else:
                        print(f"Failed  -> {device}: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    print(f"Error: Could not connect to {API_URL}. Is the Flask server running?")
                    break # The loop stops if the server is not available.


            print("Waiting 10 seconds...")
            time.sleep(10)

    except KeyboardInterrupt:
        print("\nSimulator Stopped by User.")

if __name__ == "__main__":
    run_simulator()