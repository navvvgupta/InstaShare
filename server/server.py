import socket
import threading
import pyfiglet
import json
import time
import os
import dotenv
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
from helper.searchSingleUser import searchSingleUser
from termcolor import colored

FORMAT = "utf-8"
dotenv.load_dotenv()
# Lists For Clients and Their Nicknames
clients = []
usernames = []
ip_address_map = {}
welcome_text = pyfiglet.figlet_format("ApnaHub Server")


# create socket
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
        # print("Binding the Port: " + str(port))

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
            req_online_user = req_object["header"]["listOnlineUser"]
            req_message = req_object["header"]["isMessage"]
            req_server_close = req_object["header"]["closeSystem"]
            req_upload_to_public_folder = req_object["header"]["UploadToPublicFolder"]
            req_list_public_data = req_object["header"]["listPublicData"]
            req_search_by_file = req_object["header"]["searchByFile"]
            req_search_file_user = req_object["header"]["search_file_user"]

            if req_online_user:
                online_users_info = listOnlineUser()
                res = Response(list_online_user=True, data=online_users_info)
                serialized_request = json.dumps(res.to_dict())
                client.send(serialized_request.encode())

            elif req_list_public_data:
                username = req_object["body"]["data"]["username"]
                result_array = list_public_folder(username)
                res = Response(list_public_file_data=True, data=result_array)
                serialized_request = json.dumps(res.to_dict())
                client.send(serialized_request.encode())

            elif req_search_by_file:
                fileName = req_object["body"]["data"]["file_name"]
                result_array = searchByFile(fileName)
                res = Response(search_by_file_result=True, data=result_array)
                serialized_request = json.dumps(res.to_dict())
                client.send(serialized_request.encode())

            elif req_upload_to_public_folder:
                file_data = req_object["body"]["data"]["file_data"]
                username = req_object["body"]["data"]["username"]
                upload_in_public_folder(file_data, username, client)

            elif req_message:
                # Broadcasting Messages
                message = req_object["body"]["data"]
                broadcast(message, clients)

            elif req_search_file_user:
                user_name = req_object["body"]["data"]["user_name"]
                file_name = req_object["body"]["data"]["file_name"]
                res_user = searchSingleUser(user_name, file_name)
                res = Response(search_file_user_result=True, data=res_user)
                serialized_request = json.dumps(res.to_dict())
                client.send(serialized_request.encode())

            elif req_server_close:
                # closing the server
                index = clients.index(client)
                clients.remove(client)
                username = usernames[index]
                usernames.remove(username)
                client.close()
                setOfflineStatus(username)
                # online_users_info = listOnlineUser()
                message = f"{username} is Disconnected."
                broadcast(message, clients)

        except (socket.error, json.JSONDecodeError, KeyError) as e:
            message = f"Error handling client: {str(e)}"
            colored_message = colored(message, "red")
            print(colored_message)

            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            username = usernames[index]
            usernames.remove(username)
            client.close()
            setOfflineStatus(username)
            # online_users_info = listOnlineUser()
            message = f"{username} is Disconnected."
            broadcast(message, clients)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = s.accept()
        userInfo_json = client.recv(1024).decode(FORMAT)
        userInfo = json.loads(userInfo_json)
        flag = False
        if userInfo["isLoginAuth"] == "False":
            flag = userRegistration(userInfo, client, clients, usernames)
        elif userInfo["isLoginAuth"] == "True":
            flag = isAuth(userInfo, client, clients, usernames)

        if flag == True:
            message = (
                f'{userInfo["username"]} : {userInfo["ip_address"]} has Connected.'
            )
            colored_message = colored(message, "green")
            print(colored_message)
            # online_users_info = listOnlineUser()
            message = f'{userInfo["username"]} : {userInfo["ip_address"]} has join.'
            broadcast(message, clients)
            # Start Handling Thread For Client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            client.close()


def welcomeNote():
    colored_text = colored(welcome_text, "cyan")
    print(colored_text)


def main():
    create_socket()
    bind_socket()
    connect_to_mongodb()
    welcomeNote()
    receive()


if __name__ == "__main__":
    main()
