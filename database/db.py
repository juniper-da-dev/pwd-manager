#!/usr/bin/env python3

import os
from typing import TypedDict

from pymongo import MongoClient

uri = os.environ.get("MONGO_URI")
client = MongoClient(uri)
db = client["Vault"]
secret_db = db["Secrets"]

class Secret:
    def __init__(self, key, value, project_id):
        self.key = key
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

create_secret("test", "test", "123")

