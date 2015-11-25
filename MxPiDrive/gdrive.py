from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import platform
#SFID  Source Folder Id
SFID = "0B5wtxWXBa7L8S2dYaEtJMXMxeUk"
#Technical Report Id
TechID = "16grOWcXkxrjt1JundUKUQoGlPZigPBsOzExyKozcpD8"

def Connect():
    print("Authenticating")
    gauth = GoogleAuth()

    os = platform.platform().split('-')[0]
    print(os)
    if(os != "Windows"):
        gauth.LoadCredentialsFile("./Mx/MxPiDrive/mycreds.txt")
    else:
        gauth.LoadCredentialsFile("./mycreds.txt")
        
    if( gauth.credentials is None):
        gauth.LocalWebserverAuth()
    elif( gauth.access_token_expired):
        gauth.Refresh()
    else:
        gauth.Authorize()
           

    if(os != "Windows"):
        gauth.SaveCredentialsFile("./Mx/MxPiDrive/mycreds.txt")
    else:
        gauth.SaveCredentialsFile("./mycreds.txt")
        
    print("Done Authenticating")

    drive = GoogleDrive(gauth)
    return drive
def CopyTechnicalReport(drive,parent,name = "Technical Report"):
    file_list = drive.ListFile({"q":"'"+parent+"' in parents and trashed = false"}).GetList()
    found = False
    for file1 in file_list:
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            if(file1['title'] == name):
                found = True
                    
    if(not found):
        drive.auth.service.files().copy(fileId = TechID, body={"parents":[{"kind": "drive#fileLink",
                                                                   "id": parent}], 'title': name}).execute()
   
def GetFileURL(drive,ProjectName,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()


    for file1 in file_list:
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            if(file1['title'] == ProjectName):
                return file1['alternateLink']
def GetFileID(drive,FileName,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()


    for file1 in file_list:
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            if(file1['title'] == FileName):
                return file1['id']
    return None
def GetFiles(drive,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()
    Files = {}
    for file1 in file_list:
        #print(file1['alternateLink'])
        if(not file1['mimeType'] == "application/vnd.google-apps.folder"):
            Files[file1["title"]] = file1["id"]
    return Files   
def GetFolders(drive,ParentId = None):
    if(not ParentId):
        ParentId = SFID
    file_list = drive.ListFile({"q":"'"+ParentId+"' in parents and trashed = false"}).GetList()
    Folders = {}
    for file1 in file_list:
        #print(file1['alternateLink'])
        if(file1['mimeType'] == "application/vnd.google-apps.folder"):
            Folders[file1["title"]] = file1["id"]
    return Folders
def DownloadFile(drive,FileId,FileName):
    file1 = drive.CreateFile({'id':FileId})
    file1.GetContentFile(FileName)
def UploadFile(drive,ParentId,FilePath,FileName):
    Id = GetFileID(drive,FileName,ParentId)
    if(Id ==None):
        file2Upload = drive.CreateFile({"parents":[{"id" : ParentId}]})
    else:
        file2Upload = drive.CreateFile({'id':Id})
    file2Upload.SetContentFile(FilePath)
    file2Upload["title"] = FileName
    file2Upload.Upload()
def GetTeacherID(drive,dayId,Name):
    file_list = drive.ListFile({"q":"'"+dayId+"' in parents and trashed = false"}).GetList()
    for file1 in file_list:
        if(Name == file1['title']):
            return {file1['title'] : file1['id']}
            
def GetClassFolderID(drive,SchoolId,Day):
    file_list = drive.ListFile({"q":"'"+SchoolId+"' in parents and trashed = false"}).GetList()
    for file1 in file_list:
        if(Day in file1['title']):
            return {file1['title'] : file1['id']}
            
def GetSchoolFolderIDs(drive):
    file_list = drive.ListFile({"q":"'"+SFID+"' in parents and trashed = false"}).GetList()
    SchoolIds = {}
    for file1 in file_list:
        if(not "Technical" in file1['title']):
            SchoolIds[file1['title'].strip()] = file1['id']
    return SchoolIds
def CreateFolder(drive,FolderName,ParentId):
    newFolder = drive.CreateFile({"title":FolderName,
                                  "mimeType": "application/vnd.google-apps.folder",
                                  "parents" : [{"id" : ParentId}]})
    newFolder.Upload()
    return newFolder['id']

##drive = Connect()
##file_list = drive.ListFile({"q":"'"+SFID+"' in parents and trashed = false"}).GetList()
##
##for file1 in file_list:
##    #print(file1['alternateLink'])
##    if(file1['mimeType'] == "application/vnd.google-apps.folder" and file1["title"] != "Buildologie"):
##        sublist = drive.ListFile({"q":"'"+file1["id"]+"' in parents and trashed = false"}).GetList()
##        for file2 in sublist:
##
##            
##            if(file2["title"] != ""):
##                print(file2["title"])
##                sublist = drive.ListFile({"q":"'"+file2["id"]+"' in parents and trashed = false"}).GetList()
##                found = False
##                exists = False
##                for file3 in sublist:
##                    if(file3["title"] == "Codologie II (Intermediate)"):
##                        exists = True
##                        break
##                    if( file3["title"] in ["Code","Document","Media", "Documents"]):
##                        found = True
##                        
##                        file4 = drive.CreateFile({'title': "Codologie II (Intermediate)", "parents":  [{"id": file2['id']}], "mimeType": "application/vnd.google-apps.folder"})
##                        file4.Upload()
##                        break
##                if (not exists):
##
##                    if(not found):
##                        filec = drive.CreateFile({'title': "Code", "parents":  [{"id": file2['id']}], "mimeType": "application/vnd.google-apps.folder"})
##                        filec.Upload()
##                        fileb = drive.CreateFile({'title': "Document", "parents":  [{"id": file2['id']}], "mimeType": "application/vnd.google-apps.folder"})
##                        fileb.Upload()
##                        filea = drive.CreateFile({'title': "Media", "parents":  [{"id": file2['id']}], "mimeType": "application/vnd.google-apps.folder"})
##                        filea.Upload()
##                        file4 = drive.CreateFile({'title': "Codologie II (Intermediate)", "parents":  [{"id": file2['id']}], "mimeType": "application/vnd.google-apps.folder"})
##                        file4.Upload()
##                        
##                    id1 = 0
##                    sublist = drive.ListFile({"q":"'"+file2["id"]+"' in parents and trashed = false"}).GetList()
##                    
##                    for file3 in sublist:
##                        if(file3["title"] =="Codologie II (Intermediate)"):
##                            id1 = file3["id"]
##                            break
##                    for file3 in sublist:
##                        if(file3["title"] == "Code"):
##                            CodeId = file3["id"]
##                            break
##                    for file3 in sublist:
##                        if(file3["title"] in ["Document","Documents"]):
##                            DocId = file3["id"]
##                            break
##                    for file3 in sublist:
##                        if(file3["title"] == "Media"):
##                            MediaId = file3["id"]
##                            break
##                    for file3 in sublist:
##                        
##                        if((not file3["title"] in ["Code","Document","Media", "Documents","Codologie II (Intermediate)"])):
##                            print(file3["title"])
##                            ext = file3["title"].split(".")[-1].lower() 
##                            print(ext + " " +" <-------This")
##                            if(ext in ["jpg","png","bmp"]):
##                                file3["parents"] = [{"id":MediaId}]
##                                file3.Upload()
##                            elif(ext in ["doc","txt"] or len(ext) > 3 and not (file3['mimeType'] == "application/vnd.google-apps.folder")):
##                                file3["parents"]= [{"id": DocId}]
##                                file3.Upload()
##                            elif(ext in ["py","sb2"] or (file3['mimeType'] == "application/vnd.google-apps.folder") and not file3["title"] in ["Code","Document","Media", "Documents","Codologie II (Intermediate)"] ):
##                                file3["parents"]= [{"id": CodeId}]
##                                file3.Upload()
##
##                    sublist = drive.ListFile({"q":"'"+file2["id"]+"' in parents and trashed = false"}).GetList()
##            
##                    for file3 in sublist:
##                        if( file3["title"] in ["Code","Document","Media", "Documents"]):
##                            file3["parents"]= [{"id": id1}]
##                            file3.Upload()
    
##DRIVE = Connect()
##Ids = GetSchoolFolderIDs(DRIVE)
##cD = time.strftime("%A")
##DayId = GetClassFolderID(DRIVE,Ids['Ponderosa'],cD)
##p = "C:\\Users\\Fernando\\Desktop\\Anaheim GoogleDrive\\test.txt"
##ClassId = GetTeacherID(DRIVE,DayId[cD],"Vasquez")
##Upload(DRIVE,ClassId["Vasquez"],"Code",p,"test")
