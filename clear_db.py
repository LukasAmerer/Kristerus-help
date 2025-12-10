# Delete old data one by one (Cosmos DB compatible)
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
client = MongoClient(connection_string)
db = client["kmu_meet_ki"]
collection = db["validated_results"]

# Find and delete each document
count = 0
for doc in collection.find({}):
    collection.delete_one({"_id": doc["_id"]})
    count += 1

print(f"Deleted {count} documents")

# Delete timestamp file
timestamp_file = os.path.join(os.path.dirname(__file__), '.last_auto_search')
if os.path.exists(timestamp_file):
    os.remove(timestamp_file)
    print("Deleted timestamp file")

print("Database cleared!")
