from models.publicdata import PublicData
from models.user import User

def upload_in_public_folder(fileData, user_ip):
    print('Idhar to aaya hi nhi')
    print(fileData['isFile'])
    print('_______')
    print(fileData['file_content'])
    # Find the user based on the provided IP address
    user = User.objects(ip_address=user_ip).first()
    if user:
        # User found, create a new PublicData instance
        new_upload = PublicData(
            name=fileData['file_baseName'],
            path=fileData['file_path'],  # Set your desired path value here
            content=fileData['file_content'],
            user=user,
            size=fileData['file_size'],
            is_file=fileData['isFile'],
        )
        new_upload.save()
        print("Upload successful!")
    else:
        print("User not found based on the provided IP address.")
    