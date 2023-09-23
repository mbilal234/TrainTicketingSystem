"""
    The purpose of this script is to fill data in the collections.
    This data includes trains, seats and fair prices.
"""

import pymongo
from dotenv import load_dotenv
import os

load_dotenv

my_client = pymongo.MongoClient(os.getenv("MONGO_URI"))

print("Database Successfully Connected")


