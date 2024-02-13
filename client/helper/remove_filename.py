import json

json_file_path = r"client\receiveFileData.json"


def remove_filename(filename):
    # Load data from the JSON file
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Iterate over each dictionary in the list
    for item in data:
        # Check if the filename is present in the dictionary
        if filename in item:
            # Remove the filename from the dictionary
            del item[filename]

    # Write the updated data back to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
