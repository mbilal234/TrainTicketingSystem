"""
    The purpose of this script is to connect with the database
"""

import pymongo
from dotenv import load_dotenv
import os

def connect():
    load_dotenv()
    my_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = my_client["train_reservation_system"]

    return db

if __name__=="__main__":
    print("Database Successfully Connected")


