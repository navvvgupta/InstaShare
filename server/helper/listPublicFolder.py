from models.publicdata import PublicData
from models.user import User


def list_public_folder(username):
    user = User.objects(username=username).first()
    if user:
        public_files_and_folder = PublicData.objects(user=user)
        result_array = []
        for item in public_files_and_folder:
            data_dict = {"name": item.name, "isFile": item.is_file, "path": item.path}
            result_array.append(data_dict)
        return result_array
    else:
        return "User not found based on the provided IP address."
