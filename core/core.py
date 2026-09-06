import hvac
import secrets
from dotenv import load_dotenv, set_key
import os
import base64

load_dotenv()

client = hvac.Client(
    url="https://vault.arc-lab.studio",
    token="hvs.ohZDruf1mwi0Z1CkhHlitJJD"
)

# Key Initialization

def initialize_keys():
    master_key = base64.b64encode(secrets.token_bytes(32)).decode()
    db_key = base64.b64encode(secrets.token_bytes(32)).decode()
    client.secrets.kv.v2.create_or_update_secret(
        path="/projects/pwd-manager",
        secret=dict(master_key=master_key, db_key=db_key)
    )
    set_key(dotenv_path=".env", key_to_set="INITIALIZED_MASTER_KEY", value_to_set="True")
    set_key(dotenv_path=".env", key_to_set="INITIALIZED_DB_KEY", value_to_set="True")
    return True

if os.getenv("INITIALIZED_MASTER_KEY") and os.getenv("INITIALIZED_DB_KEY"):
    pass
else:
    print("db key initializing")
    initialize_keys()

####################

def get_master_key():
    secret = client.secrets.kv.v2.read_secret_version(
        path="projects/pwd-manager",
        raise_on_deleted_version=True
    )

    master_key = base64.b64decode(secret["data"]["data"]["master_key"])
    return master_key

def get_db_key():
    secret = client.secrets.kv.v2.read_secret_version(
        path="projects/pwd-manager",
        raise_on_deleted_version=True
    )

    master_key = base64.b64decode(secret["data"]["data"]["db_key"])
    return master_key