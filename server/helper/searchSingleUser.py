from models.user import User
from models.publicdata import PublicData
from bson import json_util


def searchSingleUser(user_name, file_name):
    try:
        # Query to find the user with the given username and is_online status
        user = User.objects(username=user_name, is_online=True).first()
        if not user:
            msg = "User does not exit"
            return msg

        file = PublicData.objects(name=file_name, user=user).first()
        if not file:
            msg = "File or folder does not exist"
            return msg

        result = {"user": user.to_dict(), "file": file.to_dict()}
        print(result)
        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
