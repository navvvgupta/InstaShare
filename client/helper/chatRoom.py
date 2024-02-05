import socket
import threading
from helper.receiveFile import receive_file
from helper.request_class import Request
from helper.upload_in_public_folder import upload_in_public_folder
from helper.get_lan_ip import get_lan_ip
import pickle
import json

def client_conn(ip, file_name):
    client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_conn.connect((ip, 10500))
    client_conn.send(file_name.encode('utf-8'))
    receive_file(client_conn)

def listen_messages(main_server_conn):
    while True:
        try:
            res_data = main_server_conn.recv(1024).decode()
            res_object = json.loads(res_data)
            # different header 
            res_online_user = res_object['header']['isOnlineUser']
            res_message = res_object['header']['isMessage']
            res_server_close = res_object['header']['isSystem']
            res_file_sharing = res_object['header']['isFileSharing']
            res_public_file = res_object['header']['isPublicFile']

            if res_public_file:
                # print('Hiiiiiiiiiiiiiiiiiiiiii')
                result_array=res_object['body']['data']
                for item in result_array:
                    if item['isFile']:
                      print(f"File: {item['name']}: {item['path']}")
                    else:
                      print(f"Folder: {item['name']}: {item['path']}")
            elif res_message:
                # Broadcasting Messages
                message=res_object['body']['data']
                print(message)
        except Exception as e :
            # Close Connection When Error
            print("An error occurred here!")
            print(e)
            main_server_conn.close()
            break

# Broadcasting messages through the main server
def send_message(main_server_conn, username):
    while True:
        user_input = input('')
        message = '{}: {}'.format(username, user_input)
        
        # connect to other client for data sharing
        if "connect(" in user_input:
            start_index = user_input.find('(')
            end_index = user_input.find(')')
            ip = user_input[start_index + 1 : end_index]
            print(f'Enter the file/folder name you want from {ip}: ')
            file_name=input(r'')
            receive_thread = threading.Thread(target=client_conn, args=(ip, file_name))
            receive_thread.start()

        elif "upload(" in user_input:
            start_index = user_input.find('(')
            end_index = user_input.find(')')
            ip = user_input[start_index + 1 : end_index]
            print(f'Enter the file/folder you want to upload:')
            file_name=input(r'')
            file_data = upload_in_public_folder(file_name)
            req = Request(is_public_file=True,file_info=file_data,from_c1=get_lan_ip())
            serialized_request = json.dumps(req.to_dict())
            main_server_conn.send(serialized_request.encode())
        elif "list_public_folder(" in user_input:
            start_index = user_input.find('(')
            end_index = user_input.find(')')
            ip = user_input[start_index + 1 : end_index]
            req = Request(is_public_file=True,to_c2=ip)
            serialized_request = json.dumps(req.to_dict())
            main_server_conn.send(serialized_request.encode())
        #  request to common server
        elif message:
            # print("1")
            if "list_all_user" in user_input:
                # print("2")
                req = Request(is_online_user=True)
                serialized_request = json.dumps(req.to_dict())
                main_server_conn.send(serialized_request.encode())
            
            elif "close" in user_input:
                # print("3")
                req=Request(is_system=True)
                serialized_request = json.dumps(req.to_dict())
                main_server_conn.send(serialized_request.encode())
            
            else:
                # print("4")
                req=Request(is_message=True, content=message)
                # print(req.body['content'])
                serialized_request = json.dumps(req.to_dict())
                # print(serialized_request)
                main_server_conn.send(serialized_request.encode())