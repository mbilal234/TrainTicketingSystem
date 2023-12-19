"""
    The purpose of this script is to connect with the database
"""

import pymongo
from dotenv import load_dotenv
import os

def connect():
    """Connects to the MongoDB database specified in the MONGO_URI environment variable and returns a reference to the
    'train_reservation_system' database.

    Returns:
        pymongo.database.Database: A reference to the 'train_reservation_system' database.
    """
    
    load_dotenv()
    my_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = my_client["test_trs"]

    return db

if __name__=="__main__":
    print("Database Successfully Connected")


