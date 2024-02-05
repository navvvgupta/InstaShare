from models.publicdata import PublicData
from models.user import User

def list_public_folder(ip):
    user = User.objects(ip_address=ip).first()
    if user:
        public_files_and_folders = PublicData.objects(user=user)
        return public_files_and_folders
    else:
        return "User not found based on the provided IP address."
    