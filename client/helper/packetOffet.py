import json

json_file_path = r"C:\Users\rdrl\OneDrive\Desktop\apna-hub\client\receiveFileData.json"


def get_packet_for_filename(filename):
    # Load data from the JSON file
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Iterate over each dictionary in the list
    for item in data:
        if filename in item:
            return item[filename]

    else:
        return 0
