import requests
from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

REGISTER_API = "http://20.244.56.144/train/register"



registration_data = {
    "companyName":"train management",
    "ownerName":"Tetali syam kumar reddy",
    "rollNo":"BL.EN.U4CSE20177",
    "ownerEmail":"syamkumartetali@gmail.com",
    "accessCode":"hMkCJZ"
}

response = requests.post(REGISTER_API, json=registration_data)


if response.status_code == 200:
    response_data = response.json()
    access_code = response_data.get(["clientID",'clientSecret'])
    print("Registration successful! Access code:", access_code)
else:
    print("Registration failed. Status code:", response.status_code)