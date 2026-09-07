#!/usr/bin/env python3

import os

import pymysql
from dotenv import load_dotenv
from argon2 import PasswordHasher

from crypto import encrypt

load_dotenv()

ph = PasswordHasher()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"missing required env var: {name}")
    return value

HOST = require_env("MYSQL_HOST")
PORT = int(require_env("MYSQL_PORT"))
DB = "appdb"

APP_USER = "appuser"
APP_PASSWORD = os.getenv("APP_PASSWORD")

ROOT_USER = "root"
ROOT_PASSWORD = os.getenv("ROOT_PASSWORD")

def initialize_account(username, password):
    user = encrypt(password, username, "USERNAME")
    password = ph.hash(password)
    conn = pymysql.connect(host=HOST, port=PORT, user=ROOT_USER, password=ROOT_USER, database=DB)
    try:
        with conn.cursor() as cur:
            # launguage=sql
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users
                (
                    internal_id INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    username    VARCHAR(255) NOT NULL UNIQUE,
                    password    VARCHAR(255) NOT NULL
                )
                """
                )
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user, password))
            conn.commit()

            cur.execute("SELECT internal_id FROM users WHERE username = %s", (user,))
            result = cur.fetchone()[0]

            return result

    finally:
        conn.close()

try:
    print(initialize_account("tester", "hello-test"))
except Exception as e:
    print(e)