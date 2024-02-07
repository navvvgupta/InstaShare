from models.publicdata import PublicData

def searchByFile(fileName):
    public_files_and_folders = PublicData.objects(name__contains=fileName)
    return public_files_and_folders