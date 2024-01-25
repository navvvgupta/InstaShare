import socket
import os
import subprocess
import tqdm

s = socket.socket()
host = '192.168.29.212'
port = 9999
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024  # send 4096 bytes each time step
s.connect((host, port))

def send_single_file(file_transfer_conn, file_path):
    try:
        file_name = os.path.basename(file_path)
        filesize = os.path.getsize(file_path)
        file_transfer_conn.send(f"{file_name}{SEPARATOR}{filesize}".encode())
        filesize = int(filesize)
        total_packet = filesize / BUFFER_SIZE
        send_packet = 0

        progress = tqdm.tqdm(range(filesize), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(file_path, "rb") as f:
            while send_packet < total_packet:
                bytes_read = f.read(BUFFER_SIZE)
                file_transfer_conn.sendall(bytes_read)
                send_packet += 1
                progress.update(len(bytes_read))
            progress.close()

    except Exception as e:
        print(f"Error during file transfer: {e}")

ip='192.168.1.103'
print(f'Enter the file//folder path you want from {ip}: ')
file_path=input(r'')
send_single_file(s,file_path)

s.close()
