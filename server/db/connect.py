import os
from mongoengine import connect


def connect_to_mongodb():
    # Replace 'your_mongodb_uri' and 'your_database_name' with your actual MongoDB URI and database name
    connect("ApnaHub", host=os.getenv("MONGO_URI"), port=27017)
    print("Connected To DataBase")
