import os

BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"
import tqdm
import shutil


def send_file(file_transfer_conn):
    try:
        file_path = file_transfer_conn.recv(1024).decode("utf-8")

        if os.path.isfile(file_path):
            send_single_file(file_transfer_conn, file_path)
        elif os.path.isdir(file_path):
            send_folder(file_transfer_conn, file_path)
        else:
            print(f"Invalid path: {file_path}")

    except Exception as e:
        print(f"Error during file/folder transfer: {e}")
    finally:
        # Close the connection after completing the file/folder transfer
        file_transfer_conn.close()


def send_single_file(file_transfer_conn, file_path):
    try:
        file_name = os.path.basename(file_path)
        print(file_name)
        filesize = os.path.getsize(file_path)
        file_transfer_conn.send(f"{file_name}{SEPARATOR}{filesize}".encode())
        filesize = int(filesize)
        total_packet = filesize / BUFFER_SIZE
        send_packet = 0

        progress = tqdm.tqdm(
            range(filesize),
            f"Sending {file_name}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )
        with open(file_path, "rb") as f:
            while send_packet < total_packet:
                bytes_read = f.read(BUFFER_SIZE)
                file_transfer_conn.sendall(bytes_read)
                send_packet += 1
                progress.update(len(bytes_read))
            progress.close()

    except Exception as e:
        print(f"Error during file transfer: {e}")
    finally:
        # Close the connection after completing the file/folder transfer
        file_transfer_conn.close()


def send_folder(file_transfer_conn, folder_path):
    try:
        folder_name = os.path.basename(folder_path.rstrip(os.path.sep))
        shutil.make_archive(folder_name, "zip", folder_path)

        file_transfer_conn.send(
            f"{folder_name}.zip{SEPARATOR}{os.path.getsize(folder_name + '.zip')}".encode()
        )

        with open(folder_name + ".zip", "rb") as f:
            file_transfer_conn.sendfile(f)

        os.remove(folder_name + ".zip")

    except Exception as e:
        print(f"Error during folder transfer: {e}")
