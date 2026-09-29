import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime
from config import MEDICINE_LIMITS

load_dotenv()

username = quote_plus(os.getenv("MONGO_USERNAME"))
password = quote_plus(os.getenv("MONGO_PASSWORD"))
cluster = os.getenv("MONGO_CLUSTER")

mongo_uri = f"mongodb+srv://{username}:{password}@{cluster}/"

client = MongoClient(mongo_uri)

db = client["medicine_monitor"]
collection = db["temperature_readings"]

temperature = 5.0

MIN_TEMP, MAX_TEMP = MEDICINE_LIMITS["Medicine A"]

if MIN_TEMP <= temperature <= MAX_TEMP:
    status = "SAFE"
else:
    status = "UNSAFE"

reading = {
    "temperature": temperature,
    "timestamp": datetime.now(),
    "medicine": "Medicine B",
    "status": status
}

collection.insert_one(reading)

print("Test temperature reading inserted successfully!")