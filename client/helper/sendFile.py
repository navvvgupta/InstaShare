import os
BUFFER_SIZE = 1024
SEPARATOR = '<SEPARATOR>'

def send_file(file_transfer_conn):
    try:
        file_name = file_transfer_conn.recv(1024).decode('utf-8')
        filesize = os.path.getsize(file_name)
        file_transfer_conn.send(f"{file_name}{SEPARATOR}{filesize}".encode())
        filesize=int(filesize)
        total_packet=filesize/1024
        send_packet=0
        # start sending the file
        # progress = tqdm.tqdm(range(filesize), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(file_name, "rb") as f:
            while send_packet < total_packet:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                # we use sendall to assure transmission in busy networks
                file_transfer_conn.sendall(bytes_read)
                send_packet+=1
                # update the progress bar
                # progress.update(len(bytes_read))
            # progress.close()
    
    except Exception as e:
        # print(f"Error during file transfer: {e}")
        file_transfer_conn.send(f"Error during file transfer from sender: {e}".encode('utf-8'))
    finally:
        # Close the connection after completing the file transfer
        file_transfer_conn.close()