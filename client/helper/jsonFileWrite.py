json_file_path = r"client\receiveFileData.json"
import json
import os


def write_error_data_to_json(error_data):
    existing_data = []
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as error_file:
            try:
                existing_data = json.load(error_file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                # Handle case where file exists but is empty or not valid JSON
                pass

    basefolder_name = list(error_data.keys())[0]
    bytes_downloaded = error_data[basefolder_name]

    flag = True
    for item in existing_data:
        if basefolder_name in item:
            item[basefolder_name] = bytes_downloaded
            flag = False

    if flag:
        existing_data.append(error_data)

    with open(json_file_path, "w") as error_file:
        json.dump(existing_data, error_file)
