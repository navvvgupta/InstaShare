import socket
import os
import tqdm
import shutil
from .packetOffet import get_packet_for_filename
from .jsonFileWrite import write_error_data_to_json
from .remove_filename import remove_filename
import sys
import subprocess

json_file_path = r"client\receiveFileData.json"
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"


def get_downloads_folder():
    # Get the home directory of the current user
    home_directory = os.path.expanduser("~")

    # Append 'Downloads' to the home directory to get the Downloads folder path
    downloads_folder = os.path.join(home_directory, "Downloads")

    return downloads_folder


def receive_file(client_conn):
    try:
        file_info_data = client_conn.recv(BUFFER_SIZE).decode("utf-8")
        file_name_here, file_size = file_info_data.split(SEPARATOR)
        print(file_name_here)
        if file_name_here.endswith(".zip"):
            receive_folder(client_conn, file_name_here)
        else:
            receive_single_file(client_conn, file_info_data)

    except Exception as e:
        print(f"Error during file/folder reception: {e}")
    finally:
        # Close the connection after completing the file/folder reception
        client_conn.close()


def receive_single_file(client_conn, file_info_data):
    try:
        filename, filesize = file_info_data.split(SEPARATOR)
        filename = os.path.basename(filename)
        basefile_name = filename
        packet_offset = int(get_packet_for_filename(filename))
        filesize = int(filesize)

        downloads_path = get_downloads_folder()
        filename = os.path.join(downloads_path, filename)
        bytes_downlaoded = packet_offset

        # Start a new terminal for tqdm progress bar
        progress_proc = subprocess.Popen(
            [sys.executable, "progress_bar.py", basefile_name, str(filesize)],
            stdin=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )

        # progress = tqdm.tqdm(
        #     range(filesize),
        #     f"Receiving {filename}",
        #     unit="B",
        #     unit_scale=True,
        #     unit_divisor=1024,
        # )

        if os.path.exists(filename):
            with open(filename, "ab") as f:
                while True:
                    bytes_read = client_conn.recv(BUFFER_SIZE)
                    bytes_downlaoded += len(bytes_read)
                    if not bytes_read:
                        f.close()
                        break
                    f.write(bytes_read)
                    progress_proc.stdin.write(f"{bytes_downlaoded}\n")
                    progress_proc.stdin.flush()

        else:
            with open(filename, "wb") as f:
                while True:
                    bytes_read = client_conn.recv(BUFFER_SIZE)
                    bytes_downlaoded += len(bytes_read)
                    if not bytes_read:
                        f.close()
                        break
                    f.write(bytes_read)
                    progress_proc.stdin.write(f"{bytes_downlaoded}\n")
                    progress_proc.stdin.flush()

        # remove file_name from json file when downloading is completed
        remove_filename(basefile_name)

        # with open(filename, "wb") as f:
        #     while True:
        #         bytes_read = client_conn.recv(BUFFER_SIZE)
        #         if not bytes_read:
        #             progress.close()
        #             f.close()
        #             break
        #         f.write(bytes_read)
        #         progress.update(len(bytes_read))

    except Exception as e:
        print(f"Error during file reception: {e}")
        error_data = {basefile_name: bytes_downlaoded}
        write_error_data_to_json(error_data)

    finally:
        # Close the connection after completing the file/folder reception
        client_conn.close()
        progress_proc.stdin.close()
        progress_proc.wait()


def receive_folder(client_conn, zip_file_path):
    try:
        folder_name = os.path.basename(zip_file_path).replace(".zip", "")
        basefolder_name = folder_name
        print("basefolder_name", basefolder_name)
        downloads_path = get_downloads_folder()
        zip_file_path = os.path.join(downloads_path, zip_file_path)
        packet_offset = int(get_packet_for_filename(basefolder_name))
        bytes_downlaoded = packet_offset

        print("folder_name", basefolder_name)

        if os.path.exists(zip_file_path):
            with open(zip_file_path, "ab") as f:
                while True:
                    bytes_read = client_conn.recv(BUFFER_SIZE)
                    bytes_downlaoded += len(bytes_read)
                    if not bytes_read:
                        break
                    f.write(bytes_read)

        else:
            with open(zip_file_path, "wb") as f:
                while True:
                    bytes_read = client_conn.recv(BUFFER_SIZE)
                    bytes_downlaoded += len(bytes_read)
                    if not bytes_read:
                        # progress.close()
                        f.close()
                        break
                    f.write(bytes_read)

        # remove folder_name from json file when downloading is completed
        remove_filename(basefolder_name)

        # receive_zip_file(client_conn, zip_file_path)
        folder_name = os.path.join(downloads_path, folder_name)
        shutil.unpack_archive(zip_file_path, folder_name, "zip")
        os.remove(zip_file_path)

    except Exception as e:
        print(f"Error during folder reception: {e}")
        error_data = {basefolder_name: bytes_downlaoded}
        write_error_data_to_json(error_data)


# new helper function for receiving zip files
# def receive_zip_file(client_conn, zip_file_path):
#     try:
#         with open(zip_file_path, "wb") as f:
#             while True:
#                 bytes_read = client_conn.recv(BUFFER_SIZE)
#                 if not bytes_read:
#                     break
#                 f.write(bytes_read)
#         print(f"File received successfully: {zip_file_path}")
#         return True
#     except Exception as e:
#         print(f"Error receiving file: {str(e)}")
#         return False
