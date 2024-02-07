from models.publicdata import PublicData

def searchByFile(fileName):
    public_files_and_folders = PublicData.objects(name__contains=fileName)
    result_array = []
    for item in public_files_and_folders:
        owner=item.user.username
        data_dict = {
        'name': item.name,
        'isFile': item.is_file,
        'path': item.path,
        'size': item.size,
        'owner': owner
        }
        result_array.append(data_dict)
    return result_array