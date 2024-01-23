import socket
import os
import tqdm
BUFFER_SIZE = 1024
SEPARATOR = '<SEPARATOR>'

def receive_file(client_conn):
    try:
        #receive the file infos(FileName+FileSize)
        file_info_data = client_conn.recv(BUFFER_SIZE).decode()
        filename, filesize = file_info_data.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)
        # start receiving the file from the socket
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = client_conn.recv(BUFFER_SIZE)
                if not bytes_read:
                    progress.close()
                    f.close()
                    client_conn.close()
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                progress.update(len(bytes_read))
    except socket.error as msg:
        print("Erorr aaya hai",str(msg))
    except Exception as e:
        print("Erorr aaya hai: ",str(e))
        msg = client_conn.recv(1024).decode('utf-8')
        if msg:
            print(msg)