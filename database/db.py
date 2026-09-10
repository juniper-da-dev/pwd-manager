#!/usr/bin/env python3

import os

import pymysql
from argon2.exceptions import InvalidHash, VerifyMismatchError, InvalidHashError
from dotenv import load_dotenv
from argon2 import PasswordHasher

from crypto import encrypt
from crypto.exceptions import InvalidKey, InvalidData
from exceptions import NoAccount

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

def verify_password(account_id, password):
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user="root",
        password="a89Kj6If80wExCj9E8iTSfKSpfJKoZ",
        database=DB
    )

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE internal_id = %s", (account_id,))
        result = cur.fetchone()

        if result is None: raise NoAccount
        stored_password = result[2]

        try:
            ph.verify(stored_password, password)
            return True
        except InvalidHashError:
            raise InvalidData("Hash")
        except VerifyMismatchError:
            raise InvalidKey

def initialize_account(username, password):
    user = encrypt(password, username, "USERNAME")
    password = ph.hash(password)
    conn = pymysql.connect(host=HOST, port=PORT, user=ROOT_USER, password="a89Kj6If80wExCj9E8iTSfKSpfJKoZ", database=DB)
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

            cur.execute("SELECT internal_id FROM users WHERE username = %s", (user,))
            result = cur.fetchone()[0]

            return result

    finally:
        conn.commit()
        conn.close()


verify_password(initialize_account("Aaj", "051114"), "051114")

def initialize_pwdatabase(account_id, password):
    try:
        verify_password(account_id, password)
    except InvalidKey:
        raise InvalidKey
    except InvalidData:
        return "Please provide valid data."

    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=ROOT_USER,
        password="a89Kj6If80wExCj9E8iTSfKSpfJKoZ",
        database=DB
    )

    if not isinstance(account_id, int):
        raise InvalidData("Account ID")

    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS passwords_{account_id}
                (
                    pwd_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    service VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
                """
            )
    finally:
        conn.commit()
        conn.close()

