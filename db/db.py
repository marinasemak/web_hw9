import os

from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()


MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB", "test_db092024")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "authors")

print(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD, MONGO_DB)

def connect_db():
    """Establishes a connection to the MongoDB database using MongoEngine."""
    try:
        connect(
            db=MONGO_DB,
            host=MONGO_HOST,
            port=MONGO_PORT,
            username=MONGO_USER,
            password=MONGO_PASSWORD,
            authentication_source="admin",
        )
        print("MongoDB connection: SUCCESS")
    except ConnectionError as e:
        print(f"MongoDB connection: FAILED\nError: {e}")
        exit(1)
