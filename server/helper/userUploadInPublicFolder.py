from models.publicdata import PublicData
from models.user import User
from termcolor import colored
from helper.response_class import Response
import json


def upload_in_public_folder(fileData, username, client):
    # Find the user based on the provided username
    user = User.objects(username=username).first()
    if user:
        # User found, create a new PublicData instance
        new_upload = PublicData(
            name=fileData["file_baseName"],
            path=fileData["file_path"],  # Set your desired path value here
            content=fileData["file_content"],
            user=user,
            size=fileData["file_size"],
            is_file=fileData["isFile"],
        )
        new_upload.save()
        print(colored("Upload successful!", "green"))
        res = Response(uploadFile=True, data="Content Uploaded 📁.")
        serialized_request = json.dumps(res.to_dict())
        client.send(serialized_request.encode())

    else:
        print(colored("User not found based.", "red"))
        res = Response(uploadFile=True, data="Failed in Uploading the Contennt")
        serialized_request = json.dumps(res.to_dict())
        client.send(serialized_request.encode())
