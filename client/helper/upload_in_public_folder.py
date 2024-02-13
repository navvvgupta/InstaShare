import os

SEPARATOR = "SEPARATOR"

global total_size
total_size = 0


def list_files_and_folders(directory, indent=""):
    global total_size
    result = ""
    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                result += rf"{indent}File: {os.path.basename(entry)}: {entry.path}\n"
                total_size += os.path.getsize(entry.path)
            elif entry.is_dir():
                result += rf"{indent}Folder: {os.path.basename(entry)}: {entry.path}\n"
                result += list_files_and_folders(
                    entry.path, indent + "  "
                )  # Recursive call with increased indentation
    except (Exception, OSError) as e:
        result += f"Error accessing directory {directory}: {str(e)}\n"
    return result


def upload_in_public_folder(file_name):
    try:
        if os.path.isfile(file_name):
            file_details_dict = {
                "isFile": True,
                "file_baseName": os.path.basename(file_name),
                "file_path": file_name,
                "file_content": None,
                "file_size": os.path.getsize(file_name),
            }
            return file_details_dict
        elif os.path.isdir(file_name):
            folder_details_dict = {
                "isFile": False,
                "file_baseName": os.path.basename(file_name),
                "file_path": file_name,
                "file_content": list_files_and_folders(file_name),
                "file_size": total_size,
            }
            return folder_details_dict
        else:
            raise FileNotFoundError(f"The specified path '{file_name}' does not exist.")
    except Exception as e:
        return {"error": str(e)}
