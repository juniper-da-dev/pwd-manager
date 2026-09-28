from dotenv import load_dotenv

load_dotenv()

with open(".env", "r") as f:
    test = f.read()

if