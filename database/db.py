#!/usr/bin/env python3

import os

import pymysql
from argon2.exceptions import InvalidHash, VerifyMismatchError, InvalidHashError
from dotenv import load_dotenv
from argon2 import PasswordHasher
from dbutils.pooled_db import PooledDB

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

pool = PooledDB(
    creator=pymysql,
    host=HOST,
    port=PORT,
    user=require_env("MYSQL_USER_USERNAME"),
    password=require_env("MYSQL_USER_PASSWORD"),
    database=DB,
)

if not os.path.exists(".db_initialized"):
    conn = pool.connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS projects
                (
                    project_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    project_name VARCHAR(255) NOT NULL
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS kms
                (
                    pwd_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    project_id INT NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    value VARCHAR(255) NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects(project_id)
                )
                """
            )
    finally:
        with open(".db_initialized", "w") as f:
            f.write("true")
        print("Database initialized")
        conn.commit()
        conn.close()

def verify_password(account_id, password):
    conn = pool.connection()
    try:
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
    finally:
        conn.commit()
        conn.close()

def initialize_account(username, password):
    conn = pool.connection()
    user = encrypt(password, username, "USERNAME")
    password = ph.hash(password)
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user, password))
            cur.execute("SELECT internal_id FROM users WHERE username = %s", (user,))
            result = cur.fetchone()[0]

            return result
    except pymysql.err.IntegrityError as e:
        code = e.args[0]
        if code == 1062:
            raise InvalidData("Username was not unique")
    finally:
        conn.commit()
        conn.close()

def store_password(account_id, pwd, service, password):
    conn = pool.connection()
    try:
        verify_password(account_id, pwd)
    except InvalidKey:
        raise InvalidKey
    except NoAccount:
        raise NoAccount

    service = encrypt(pwd, service, f"SERVICE_{account_id}")
    password = encrypt(pwd, password, f"PASSWORD_{account_id}")

    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO passwords (account_id, service, password) VALUES (%s, %s, %s)", (account_id, service, password))

            return True
    finally:
        conn.commit()
        conn.close()    