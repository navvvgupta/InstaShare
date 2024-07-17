import socket
import threading
from helper.receiveFile import receive_file
from helper.request_class import Request
from helper.upload_in_public_folder import upload_in_public_folder
from helper.get_lan_ip import get_lan_ip
from utils.constants import STOP_THREAD
from helper.request_client import ClientRequest
from helper.packetOffet import get_packet_for_filename
from termcolor import colored

import json
import os


def client_conn(ip, file_name):
    try:
        client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_conn.connect((ip, 10500))

        file_search_name = file_name.split("\\")[-1]
        print("file_search_name", file_search_name)
        packet_offset = int(get_packet_for_filename(file_search_name))
        client_request = ClientRequest(filename=file_name, packet_offset=packet_offset)
        serialized_client_request = json.dumps(client_request.to_dict())
        client_conn.send(serialized_client_request.encode())
        # client_conn.send(file_name.encode("utf-8"))
        receive_file(client_conn)
        client_conn.close()  # Close the connection after file transfer
        print("File transfer completed successfully.")
    except Exception as e:
        print(f"Error in client conn: {str(e)}")


def format_size(size_in_bytes):
    """Convert a size in bytes to a readable format (MB or GB)."""
    if size_in_bytes >= 1e9:  # Convert to GB if size is 1 GB or more
        size = size_in_bytes / 1e9
        unit = "GB"
    elif size_in_bytes >= 1e6:  # Convert to MB if size is 1 MB or more
        size = size_in_bytes / 1e6
        unit = "MB"
    else:
        size = size_in_bytes
        unit = "bytes"
    return f"{size:.2f} {unit}"


def listen_messages(main_server_conn):
    try:
        while not STOP_THREAD:
            res_data = main_server_conn.recv(1024).decode()
            res_object = json.loads(res_data)

            # different header
            res_online_user = res_object["header"]["listOnlineUser"]
            res_message = res_object["header"]["isMessage"]
            res_public_file_data = res_object["header"]["listPublicFile"]
            res_search_by_file = res_object["header"]["searchByFile"]
            res_upload_file = res_object["header"]["uploadFile"]

            if res_online_user:
                online_users_info = res_object["body"]["data"]
                print("")
                for user_info in online_users_info:
                    username = user_info["username"]
                    ip_address = user_info["ip_address"]
                    print(
                        f"{colored(username, 'blue')} -> {colored(ip_address, 'yellow')}"
                    )
                print("")

            elif res_search_by_file:
                result_array = res_object["body"]["data"]
                print("")

                if "not present." in result_array:
                    print(colored(result_array, "red"))

                else:
                    for item in result_array:
                        if item["isFile"]:
                            message = (
                                f"{colored('File:', 'blue')} {colored(item['name'], 'yellow')}: "
                                f"{colored(format_size(item['size']), 'green')} "
                                f"{colored('Owner: ' + item['owner'], 'blue')} "
                                f"{colored('Online' if item['online'] else 'Offline', 'green' if item['online'] else 'red')}"
                            )
                            print(message)

                        else:
                            message = (
                                f"{colored('Folder:', 'blue')} {colored(item['name'], 'yellow')}: "
                                f"{colored(format_size(item['size']), 'green')} "
                                f"{colored('Owner: ' + item['owner'], 'blue')} "
                                f"{colored('Online' if item['online'] else 'Offline', 'green' if item['online'] else 'red')}"
                            )
                            print(message)

                print("")

            elif res_public_file_data:
                result_array = res_object["body"]["data"]
                print(" ")

                if "User not found." in result_array:
                    print(colored("User not found.", "red"))

                else:
                    for item in result_array:
                        if item["isFile"]:
                            file_text = colored("File:", "blue")
                            name_text = colored(item["name"], "yellow")
                            size_text = colored(format_size(item["size"]), "green")
                            print(f"{file_text} {name_text}: {size_text}")
                        else:
                            foler_text = colored("Folder:", "blue")
                            name_text = colored(item["name"], "yellow")
                            size_text = colored(format_size(item["size"]), "green")
                            print(f"{foler_text} {name_text}: {size_text}")
                print(" ")

            elif res_upload_file:
                data = res_object["body"]["data"]
                if "Content Uploaded :)." in data:
                    print("")
                    print(colored(data, "green"))
                    print("")
                else:
                    print("")
                    print(colored(data, "red"))
                    print("")

            elif res_message:
                # Broadcasting Messages
                message = res_object["body"]["data"]
                print(message)

    except Exception as e:
        # Close Connection When Error
        print("An error occurred in listen message!")
        print(e)


# Broadcasting messages through the main server
def send_message(main_server_conn, username):
    try:
        while not STOP_THREAD:
            user_input = input("")
            message = "{}: {}".format(username, user_input)

            # connect to other client for data sharing
            if "connect(" in user_input:
                start_index = user_input.find("(")
                end_index = user_input.find(")")
                ip = user_input[start_index + 1 : end_index]
                print(f"Enter the file/folder name you want from {ip}: ")
                file_name = input(r"")
                receive_thread = threading.Thread(
                    target=client_conn, args=(ip, file_name)
                )
                receive_thread.start()

            elif "upload(" in user_input:
                print(f"Enter the file/folder you want to upload:")
                file_name = input(r"")
                file_data = upload_in_public_folder(file_name)
                data = {"file_data": file_data, "username": username}
                req = Request(upload_to_public_folder=True, data=data)
                serialized_request = json.dumps(req.to_dict())
                main_server_conn.send(serialized_request.encode())

            elif "list_public_folder(" in user_input:
                start_index = user_input.find("(")
                end_index = user_input.find(")")
                username = user_input[start_index + 1 : end_index]
                data = {"username": username}
                req = Request(list_public_data=True, data=data)
                serialized_request = json.dumps(req.to_dict())
                main_server_conn.send(serialized_request.encode())

            elif "search_by_file(" in user_input:
                start_index = user_input.find("(")
                end_index = user_input.find(")")
                file_name = user_input[start_index + 1 : end_index]
                data = {"file_name": file_name}
                req = Request(search_by_file=True, data=data)
                serialized_request = json.dumps(req.to_dict())
                main_server_conn.send(serialized_request.encode())
            #  request to common server
            elif user_input:
                if "list_all_user" in user_input:
                    req = Request(list_online_user=True)
                    serialized_request = json.dumps(req.to_dict())
                    main_server_conn.send(serialized_request.encode())

                else:
                    req = Request(is_message=True, data=message)
                    serialized_request = json.dumps(req.to_dict())
                    main_server_conn.send(serialized_request.encode())
    except EOFError as e:
        print("Stop send_message", str(e))
    except Exception as e:
        print("Send message error", str(e))
