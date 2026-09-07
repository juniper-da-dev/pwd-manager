from infisical_sdk import InfisicalSDKClient
import secrets
from dotenv import load_dotenv, set_key
import os
import base64
import ast

load_dotenv()

client = InfisicalSDKClient(
  host="https://infisical.arc-lab.studio/", # Defaults to https://app.infisical.com
  cache_ttl = 300 # `None` to disable caching
)

auth = client.auth.token_auth.login(
    token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eUlkIjoiNzdjMTkyNWEtNDRhYi00NjRhLWJiMDgtM2M0NzYxNDZjNjA2IiwiaWRlbnRpdHlOYW1lIjoiUFdEIE1hbmFnZXIiLCJhdXRoTWV0aG9kIjoidG9rZW4tYXV0aCIsIm9yZ0lkIjoiNGM4YzQwNjYtOWRiZC00YjY0LWI2YTAtNjAyNzI2MjMwZWI0Iiwicm9vdE9yZ0lkIjoiNGM4YzQwNjYtOWRiZC00YjY0LWI2YTAtNjAyNzI2MjMwZWI0IiwicGFyZW50T3JnSWQiOiI0YzhjNDA2Ni05ZGJkLTRiNjQtYjZhMC02MDI3MjYyMzBlYjQiLCJjbGllbnRTZWNyZXRJZCI6IiIsImlkZW50aXR5QWNjZXNzVG9rZW5JZCI6IjJiMzQxOGYwLTFkMjUtNDA5Zi05YzRjLWI4MjkzZTdkMDc1OCIsImlwUmVzdHJpY3Rpb25FbmFibGVkIjp0cnVlLCJhY2Nlc3NUb2tlblRUTCI6MjU5MjAwMCwiYWNjZXNzVG9rZW5NYXhUVEwiOjI1OTIwMDAsImFjY2Vzc1Rva2VuUGVyaW9kIjowLCJjcmVhdGlvbkVwb2NoIjoxNzg4NzcwMTMyLCJhdXRoVG9rZW5UeXBlIjoiaWRlbnRpdHlBY2Nlc3NUb2tlbiIsImlkZW50aXR5QXV0aCI6e30sImlhdCI6MTc4ODc3MDEzMiwiZXhwIjoxNzkxMzYyMTMyLCJqdGkiOiIyYjM0MThmMC0xZDI1LTQwOWYtOWM0Yy1iODI5M2U3ZDA3NTgifQ.EALfwX2svIWNj49NMg--DVohbLv5X0_F7ljBTMd8AN0"
)

# Key Initialization

def initialize_keys():
    master_key = base64.b64encode(secrets.token_bytes(32)).decode()
    db_key = base64.b64encode(secrets.token_bytes(32)).decode()
    client.secrets.create_secret_by_name(
        project_id="6dbc2a1b-0c42-498c-a562-7591061baf3c",
        secret_name="db_key",
        secret_value=db_key,
        secret_path="/",
        environment_slug="dev"
    )
    client.secrets.create_secret_by_name(
        project_id="6dbc2a1b-0c42-498c-a562-7591061baf3c",
        secret_name="master_key",
        secret_value=master_key,
        secret_path="/",
        environment_slug="dev"
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
    secret = client.secrets.get_secret_by_name(
        project_slug="pwd-manager",
        secret_name="master_key",
        secret_path="/",
        environment_slug="dev"
    )

    master_key = base64.b64decode(secret.secretValue)
    return master_key

def get_db_key():
    secret = client.secrets.get_secret_by_name(
        project_slug="pwd-manager",
        secret_name="db_key",
        secret_path="/",
        environment_slug="dev"
    )

    db_key = base64.b64decode(secret.secretValue)
    return db_key
