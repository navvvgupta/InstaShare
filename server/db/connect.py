import os
from mongoengine import connect


def connect_to_mongodb():
    # Replace 'your_mongodb_uri' and 'your_database_name' with your actual MongoDB URI and database name
    connect("ApnaHub", host="localhost", port=27017)
    # print("Connected To DataBase")
