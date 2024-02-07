import socket
import threading
import pickle
import json
import time
from db.connect import connect_to_mongodb
from helper.auth import isAuth
from helper.userRegistation import userRegistration
from helper.userUploadInPublicFolder import upload_in_public_folder
from helper.listPublicFolder import list_public_folder
from helper.listOnlineUser import listOnlineUser
from helper.broadcast import broadcast
from helper.setofflineStatus import setOfflineStatus
from helper.searchByFile import searchByFile
from helper.response_class import Response
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
            req_online_user = req_object['header']['listOnlineUser']
            req_message = req_object['header']['isMessage']
            req_server_close = req_object['header']['closeSystem']
            req_upload_to_public_folder = req_object['header']['UploadToPublicFolder']
            req_list_public_data = req_object['header']['listPublicData']
            req_search_by_file = req_object['header']['searchByFile']

            if req_online_user:
                online_users_info = listOnlineUser()
                res = Response(is_message=True,data=online_users_info)
                serialized_request = json.dumps(res.to_dict())
                client.send(serialized_request.encode())
            
            elif req_list_public_data:
                username = req_object['body']['data']['username']
                result_array=list_public_folder(username)
                res = Response(is_public_file=True,data=result_array)
                serialized_request = json.dumps(res.to_dict())
                client.send(serialized_request.encode())
            
            elif req_search_by_file:
                fileName=req_object['body']['data']['file_name']
                result_array=searchByFile(fileName)
                res = Response(is_public_file=True,is_message=True,data=result_array)
                serialized_request = json.dumps(res.to_dict())
                client.send(serialized_request.encode())

            elif req_upload_to_public_folder:
                file_data = req_object['body']['data']['file_data']
                user_ip = req_object['body']['data']['ip']
                upload_in_public_folder(file_data,user_ip)
                
            elif req_message:
                # Broadcasting Messages
                message=req_object['body']['data']
                print(message)
                broadcast(message,clients)
            
            elif req_server_close:
                # closing the server
                index=clients.index(client)
                clients.remove(client)
                username=usernames[index]
                usernames.remove(username)
                client.close()
                setOfflineStatus(username)
                online_users_info = listOnlineUser()
                broadcast(online_users_info,clients)
            
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
            broadcast(online_users_info,clients)
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
            broadcast(online_users_info,clients)
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