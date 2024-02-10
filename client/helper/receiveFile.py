import socket
import os
import tqdm
import shutil

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
            print("AACHA bache")
            receive_folder(client_conn, file_name_here)
        else:
            print("Hello")
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
        filesize = int(filesize)

        progress = tqdm.tqdm(
            range(filesize),
            f"Receiving {filename}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )
        downloads_path = get_downloads_folder()
        filename = os.path.join(downloads_path, filename)
        with open(filename, "wb") as f:
            while True:
                bytes_read = client_conn.recv(BUFFER_SIZE)
                if not bytes_read:
                    progress.close()
                    f.close()
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

    except Exception as e:
        print(f"Error during file reception: {e}")
    finally:
        # Close the connection after completing the file/folder reception
        client_conn.close()


def receive_folder(client_conn, zip_file_path):
    try:
        folder_name = os.path.basename(zip_file_path).replace(".zip", "")
        downloads_path = get_downloads_folder()
        zip_file_path = os.path.join(downloads_path, zip_file_path)
        receive_zip_file(client_conn, zip_file_path)
        folder_name = os.path.join(downloads_path, folder_name)
        shutil.unpack_archive(zip_file_path, folder_name, "zip")
        os.remove(zip_file_path)

    except Exception as e:
        print(f"Error during folder reception: {e}")


# new helper function for receiving zip files
def receive_zip_file(client_conn, zip_file_path):
    try:
        with open(zip_file_path, "wb") as f:
            while True:
                bytes_read = client_conn.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
        print(f"File received successfully: {zip_file_path}")
        return True
    except Exception as e:
        print(f"Error receiving file: {str(e)}")
        return False
