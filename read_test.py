import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus

load_dotenv()

username = quote_plus(os.getenv("MONGO_USERNAME"))
password = quote_plus(os.getenv("MONGO_PASSWORD"))
cluster = os.getenv("MONGO_CLUSTER")

mongo_uri = f"mongodb+srv://{username}:{password}@{cluster}/"

client = MongoClient(mongo_uri)

db = client["medicine_monitor"]
collection = db["temperature_readings"]

reading = collection.find_one()

print(reading)