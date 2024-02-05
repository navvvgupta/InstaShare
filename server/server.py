import socket
import threading
import pickle
import json
from db.connect import connect_to_mongodb
from helper.auth import isAuth
from helper.userRegistation import userRegistration
from helper.userUploadInPublicFolder import upload_in_public_folder
from helper.listOnlineUser import listOnlineUser
from helper.broadcast import broadcast
from helper.setofflineStatus import setOfflineStatus
FORMAT = "utf-8"

# Lists For Clients and Their Nicknames
clients = []
usernames = []
ip_address_map = {}

#create socket
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            req_data = client.recv(1024).decode()
            req_object = json.loads(req_data)
            
            # different header 
            req_online_user = req_object['header']['isOnlineUser']
            req_message = req_object['header']['isMessage']
            req_server_close = req_object['header']['isSystem']
            req_file_sharing = req_object['header']['isFileSharing']
            req_public_file = req_object['header']['isPublicFile']

            if req_online_user:
                online_users_info = listOnlineUser()
                client.send(online_users_info.encode(FORMAT))
            
            if req_public_file:
                fileData=req_object['body']['fileInfo']
                user_ip=req_object['body']['fromC1']
                print('Mummy kasasm idhar aaya hai')
                upload_in_public_folder(fileData,user_ip)
                
            elif req_message:
                # Broadcasting Messages
                message=req_object['body']['content']
                print(message)
                broadcast(message.encode(FORMAT),clients)
            
            elif req_server_close:
                # closing the server
                index=clients.index(client)
                clients.remove(client)
                username=usernames[index]
                usernames.remove(username)
                client.close()
                setOfflineStatus(username)
                online_users_info = listOnlineUser()
                broadcast(online_users_info.encode(FORMAT),clients)
            
            elif req_file_sharing:
                # protocol to start client2 socket_server 
                fromC1 = req_object['body']['fromC1']
                toC2 = req_object['body']['toC2']



            # message = client.recv(1024).decode(FORMAT)
            # if "list_all_user" in message:
            #     online_users_info = listOnlineUser()
            #     client.send(online_users_info.encode(FORMAT))
            # elif message == "close":
            #      index=clients.index(client)
            #      clients.remove(client)
            #      username=usernames[index]
            #      usernames.remove(username)
            #      client.close()
            #      setOfflineStatus(username)
            #      online_users_info = listOnlineUser()
            #      broadcast(online_users_info.encode(FORMAT),clients)

            # elif message:
            # # Broadcasting Messages
            #     print(message)
            #     broadcast(message.encode(FORMAT),clients)
        except Exception as e:
            # Removing And Closing Clients
            print("An error occurred!")
            print(e)
            index=clients.index(client)
            clients.remove(client)
            username=usernames[index]
            usernames.remove(username)
            client.close()
            setOfflineStatus(username)
            online_users_info = listOnlineUser()
            broadcast(online_users_info.encode(FORMAT),clients)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = s.accept()
        userInfo_json = client.recv(1024).decode(FORMAT) # first recv
        userInfo = json.loads(userInfo_json)
        print(userInfo)
        flag = False
        if userInfo['isLoginAuth'] =="False":
            flag = userRegistration(userInfo,client,clients,usernames)
        elif userInfo['isLoginAuth'] =="True":
            flag = isAuth(userInfo,client,clients,usernames)
        
        if flag == True:
            print("Connected with {}".format(str(address[0])))
            online_users_info = listOnlineUser()
            broadcast(online_users_info.encode(FORMAT),clients)
            client.send('Connected to server!'.encode(FORMAT))
            # Start Handling Thread For Client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            client.close()

def main(): 
    create_socket()
    bind_socket()
    connect_to_mongodb()
    receive()

main()