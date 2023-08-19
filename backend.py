from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

authorization_token = "YOUR_AUTH_TOKEN"

def get_train_data():
    url = "http://20.244.56.144/train/trains"
    headers = {
        "Authorization": f"Bearer {authorization_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def filter_and_sort_trains(train_data):
    current_time = datetime.now()
    next_12_hours = current_time + timedelta(hours=12)
    
    filtered_trains = []
    for train in train_data:
        departure_time = datetime(
            year=current_time.year,
            month=current_time.month,
            day=current_time.day,
            hour=train["departureTime"]["Hours"],
            minute=train["departureTime"]["Minutes"]
        )
        if current_time <= departure_time <= next_12_hours:
            filtered_trains.append(train)
    
    sorted_trains = sorted(filtered_trains, key=lambda x: (
        x["price"]["sleeper"],
        -x["seatsAvailable"]["sleeper"],
        departure_time
    ))
    
    return sorted_trains

@app.route("/api/register-upi", methods=["POST"])
def register_upi_id():
    data = request.json
    upi_id = data.get("upiId")
    
    return jsonify({"message": f"UPI ID {upi_id} registered successfully!"})

@app.route("/api/train-schedules", methods=["GET"])
def get_train_schedules():
    train_data = get_train_data()
    sorted_trains = filter_and_sort_trains(train_data)
    return jsonify(sorted_trains)

if __name__ == "__main__":
    app.run(debug=True)
