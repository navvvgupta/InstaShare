from mongoengine import connect

def connect_to_mongodb():
    # Replace 'your_mongodb_uri' and 'your_database_name' with your actual MongoDB URI and database name
    connect('ApnaHub', host='mongodb://localhost:27017', port=27017)
    print("Connected To DataBase")
