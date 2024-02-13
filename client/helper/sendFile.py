import os

BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"
import tqdm
import shutil
import json


def send_file(file_transfer_conn):
    try:

        req_data = file_transfer_conn.recv(1024).decode()
        req_object = json.loads(req_data)
        file_path = req_object["filename"]
        packet_offset = req_object["packet_offset"]
        # file_path = file_transfer_conn.recv(1024).decode("utf-8")

        if os.path.isfile(file_path):
            send_single_file(file_transfer_conn, file_path, packet_offset)
        elif os.path.isdir(file_path):
            send_folder(file_transfer_conn, file_path, packet_offset)
        else:
            print(f"Invalid path: {file_path}")

    except Exception as e:
        print(f"Error during file/folder transfer: {e}")
    finally:
        # Close the connection after completing the file/folder transfer
        file_transfer_conn.close()


def send_single_file(file_transfer_conn, file_path, packet_offset):
    try:
        file_name = os.path.basename(file_path)
        print(file_name)
        filesize = os.path.getsize(file_path)
        file_transfer_conn.send(f"{file_name}{SEPARATOR}{filesize}".encode())
        filesize = int(filesize)
        # total_packet = filesize / BUFFER_SIZE
        # send_packet = 0

        progress = tqdm.tqdm(
            range(filesize),
            f"Sending {file_name}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

        binary_data = b""
        with open(file_path, "rb") as file:
            binary_data = file.read()
        total_sent = packet_offset
        print(len(binary_data))

        while total_sent < len(binary_data):
            bytes_to_send = binary_data[total_sent : total_sent + BUFFER_SIZE]
            file_transfer_conn.sendall(bytes_to_send)
            total_sent += len(bytes_to_send)
            progress.update(len(bytes_to_send))
        progress.close()

        # with open(file_path, "rb") as f:
        #     while send_packet < total_packet:
        #         bytes_read = f.read(BUFFER_SIZE)
        #         file_transfer_conn.sendall(bytes_read)
        #         send_packet += 1
        #         progress.update(len(bytes_read))
        #     progress.close()

    except Exception as e:
        print(f"Error during file transfer: {e}")
    finally:
        # Close the connection after completing the file/folder transfer
        file_transfer_conn.close()


def send_folder(file_transfer_conn, folder_path, packet_offset):
    try:
        folder_name = os.path.basename(folder_path.rstrip(os.path.sep))
        shutil.make_archive(folder_name, "zip", folder_path)

        file_transfer_conn.send(
            f"{folder_name}.zip{SEPARATOR}{os.path.getsize(folder_name + '.zip')}".encode()
        )

        progress = tqdm.tqdm(
            range(os.path.getsize(folder_name + ".zip")),
            f"Sending {folder_name}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

        binary_data = b""
        with open(folder_name + ".zip", "rb") as file:
            binary_data = file.read()

        total_sent = packet_offset
        print(len(binary_data))

        while total_sent < len(binary_data):
            bytes_to_send = binary_data[total_sent : total_sent + BUFFER_SIZE]
            file_transfer_conn.sendall(bytes_to_send)
            total_sent += len(bytes_to_send)
            progress.update(len(bytes_to_send))
        # with open(folder_name + ".zip", "rb") as f:
        #     file_transfer_conn.sendfile(f)
        progress.close()
        os.remove(folder_name + ".zip")

    except Exception as e:
        print(f"Error during folder transfer: {e}")
