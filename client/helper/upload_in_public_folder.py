import os
SEPARATOR="SEPARATOR"

global total_size
total_size = 0

def list_files_and_folders(directory, indent=""):
    global total_size
    result = ""
    for entry in os.scandir(directory):
        if entry.is_file():
            result += rf"{indent}File: {os.path.basename(entry)}: {entry.path}\n"
            total_size+=os.path.getsize(entry.path)
        elif entry.is_dir():
            result += rf"{indent}Folder: {os.path.basename(entry)}: {entry.path}\n"
            result += list_files_and_folders(entry.path, indent + "  ")  # Recursive call with increased indentation
    return result

def upload_in_public_folder(file_name):
    if(os.path.isfile(file_name)):
        file_details_dict={}
        file_details_dict['isFile']=True
        file_details_dict['file_baseName']=os.path.basename(file_name)
        file_details_dict['file_path']=file_name
        file_details_dict['file_content']=None
        file_details_dict['file_size']=os.path.getsize(file_name)
        return file_details_dict
    else:
        folder_details_dict={}
        folder_details_dict['isFile']=False
        folder_details_dict['file_baseName']=os.path.basename(file_name)
        folder_details_dict['file_path']=file_name
        folder_details_dict['file_content']=list_files_and_folders(file_name)
        folder_details_dict['file_size']=total_size
        return folder_details_dict
