#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
import crypto

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from crypto import encrypt

load_dotenv()
uri = os.environ.get("MONGO_URI")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    # Verify connection
    client.server_info()
    print("Successfully connected to MongoDB!")
except ConnectionFailure as e:
    print(f"Failed to connect to the MongoDB server. {e}")
    sys.exit(1)

db = client["Vault"]
secret_db = db["Secrets"]



class Secret:
    def __init__(self, key, value, project_id):
        self.key = encrypt()
        self.value = value
        self.project_id = project_id

def create_secret(key, value, project_id):
    secret_class = Secret(key, value, project_id)
    secret = {
        "project_id": secret_class.project_id,
        "key": secret_class.key,
        "value": secret_class.value,
    }
    secret_db.insert_one(secret)
    return True

def get_secret(key, project_id):

# create_secret("test", "test", "123")


