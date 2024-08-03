from ..models.publicdata import PublicData


def searchByFile(fileName):
    public_files_and_folders = PublicData.objects(name__contains=fileName)

    if not public_files_and_folders:
        msg = f"'{fileName}' is not present."
        return msg

    result_array = []
    for item in public_files_and_folders:
        owner = item.user.username
        online = item.user.is_online
        data_dict = {
            "name": item.name,
            "isFile": item.is_file,
            "size": item.size,
            "owner": owner,
            "online": online,
        }
        result_array.append(data_dict)
    return result_array
