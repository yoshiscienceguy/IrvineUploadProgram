import Tkinter as tk
import tkFileDialog
import gdrive
import time, platform, os, urllib2, webbrowser

try:
    response = urllib2.urlopen("http://www.google.com",timeout=1)
except:
    print("You Don't Have an Active Internet Connection")
    print("Please ask a Mentor for HELP")
    quit()
Level = [("Intro","Codologie I (Intro)"),
         ("Intermediate","Codologie II (Intermediate)"),
         ("Advanced","Codologie III (Advanced)")]
class Menu():
    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(400,200)
        self.root.maxsize(400,500)
        self.root.title("Google Drive Upload")
        self.master = tk.Frame(self.root,width= 300)
        self.menu = tk.Frame(self.root,width= 300)
        self.buttons = tk.Frame (self.root,width= 300)
        self.master.pack()
        #tk.mainloop()
        
    def drawDropDown(self,frame,functionName,listDisplay,Default = False):
        AssociatedVariable = tk.StringVar(frame)
        AssociatedVariable.trace("w",eval(functionName))
        DropDown = apply(tk.OptionMenu,(frame,AssociatedVariable)+tuple(listDisplay))
        if(Default):
            AssociatedVariable.set("Choose Student Type")

        DropDown.pack(pady=(10,0))

        return DropDown , AssociatedVariable
        
        
    def drawButton(self,frame,toSay,functionName):
        submit = tk.Button(frame, text = toSay,command = eval(functionName))

        return submit
    
    def drawRadioButtons(self,frame,options):
        self.v = tk.StringVar()

        Buttons = []
        
        for texts, option in options:
            rb = tk.Radiobutton(frame, text = texts, variable = self.v, value = option)
            rb.pack(anchor = tk.W)
            rb.deselect()
            Buttons.append(rb)

        
        self.v.set(options[1][1])
        return Buttons , self.v
    def drawMenu(self,frame,listDisplay,NewOption = False):

        scrollbar = tk.Scrollbar(frame,orient = tk.VERTICAL)
        listbox = tk.Listbox(frame,yscrollcommand = scrollbar.set,width = 30)
        scrollbar.config(command = listbox.yview)
        

        if(NewOption):
            listbox.insert(tk.END,"(create New)")
        for item in listDisplay:
            listbox.insert(tk.END,item)

        return listbox,scrollbar
    def drawMessage(self,frame,toSay):
        self.vartoSay = tk.StringVar()
        textbox = tk.Label(frame,textvariable = self.vartoSay, fg = "red",font = ("Helvetica",10))
        self.vartoSay.set(toSay)
        textbox.pack(pady = 10)
        return self.vartoSay
    
    def drawTextBox (self,frame):
        self.userinput = tk.StringVar()
        self.entry = tk.Entry(frame,textvariable = self.userinput,width = 30,justify =tk.CENTER)
        self.entry.bind("<Button-1>", lambda clicked : self.userinput.set(""))
        self.userinput.set("Enter Name Here")
        self.entry.pack(pady = 10)
        return self.entry , self.userinput

    def UpdateList(self,obj,var,lis):
        obj["menu"].delete(0,"end")
        var.set ("Choose One")
        for things in lis:
            obj["menu"].add_command(label = things,command = tk._setit(var,things))
    def UpdateMenu(self,obj,newlist,makeNew = False):
    
        obj.delete(0,tk.END)
        if(makeNew):
            obj.insert(tk.END,"(Create New Student Folder)")
        for thing in newlist:
            obj.insert(tk.END,thing)
    def packMenu(self,listbox,scrollbar):
        
        listbox.pack(side = tk.LEFT, fill = tk.BOTH, expand = 0)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

class Handlers:

    def StudentLevel(self,p,a,c):

        try:

            if(StudentLevelVar.get() == "Choose One"):
                return
            DisplayText.set("Current Selected: "+ self.studentName+"\n\nSelect Student's Project\n\n")
            m.packMenu(StudentNames,gns)

            UploadFolderID = self.LevelIDs[StudentLevelVar.get()]

            self.Projects = gdrive.GetFolders(drive,UploadFolderID)
            CodeFolder = gdrive.GetFiles(drive,self.Projects["Code"])
            self.CodeFolderId = self.Projects["Code"]
            Codes = GetList(CodeFolder)
            m.UpdateMenu(StudentNames,Codes,False)
            os = platform.platform().split('-')[0]
            if(os == "Windows"):
               TechnicalReport.pack() 

            ChooseUploadFolder.pack()
            ChooseDownloadCode.pack(anchor = tk.W)


        except:
            print("something")
            pass

    def StudentType(self,p,a,c):
        #used
        
        try:
            StudentNames.unbind("<Double-Button-1>")
            StudentNames.bind("<Double-Button-1>",self.ChooseStudent)
            
            DisplayText.set("Select Student's Name")
            os = platform.platform().split('-')[0]
            if(os == "Windows"):
               TechnicalReport.pack_forget() 

            ChooseUploadFolder.pack_forget()
            ChooseDownloadCode.pack_forget()
            StudentLevelObj.pack_forget()
            self.school = TypeVar.get()

            self.StudentsIds = gdrive.GetFolders(drive,folders[TypeVar.get()])
        
            m.packMenu(StudentNames,gns)
            
            Students = GetList(self.StudentsIds)
            Students.sort()
            m.UpdateMenu(StudentNames,Students,True)
            chooseGroupButton.pack(pady = 10)
            m.buttons.pack()
        except:
            print("Starting")
            pass
    def CreateNewFolder(self):
        self.slaveMain = tk.Toplevel(m.master)
        self.slaveMain.geometry("300x250")
        newFrame = tk.Frame(self.slaveMain,width = 500)
        self.slaveMain.title("Enter New Folder Name")
        self.NewTextMessage = m.drawMessage(newFrame,"Select New Student's Level")
        self.NewLevelObject, self.NewLevelVariable = m.drawRadioButtons(newFrame,Level)
        self.NewTextMessage = m.drawMessage(newFrame,"Enter the New Student's Name")
        self.NewNameObject, self.NewNameVariable = m.drawTextBox(newFrame)
        
        self.Createbutton = m.drawButton(newFrame,"Create","h.FolderCreation")
        self.Createbutton.pack(pady = (0,10))
        newFrame.pack()
        newFrame.update()
    def Exists(self,name):
        if(name in self.StudentsIds):
            return True
        return False
    def FolderCreation(self):
        name = self.NewNameObject.get()
        if(name.strip() != "" and name != "Enter Name Here"):
            
            dummy = name.split()
            name = ""
            for part in dummy:
                name += part[0].upper() + part[1:].lower() + " "
            if(not self.Exists(name)):
                newid = gdrive.CreateFolder(drive,name,folders[TypeVar.get()])
                try:
                    self.slave.destroy()
                except:
                    self.slaveMain.destroy()
                
                LevelId = gdrive.CreateFolder(drive,self.NewLevelVariable.get(),newid)
                DocId = gdrive.CreateFolder(drive,"Documents",LevelId)
                CodeId = gdrive.CreateFolder(drive,"Code",LevelId)
                MediaId = gdrive.CreateFolder(drive,"Media",LevelId)

                self.StudentsIds = gdrive.GetFolders(drive,folders[TypeVar.get()])
                
                Students = GetList(self.StudentsIds)
                Students.sort()
                m.UpdateMenu(StudentNames,Students,True)
            else:
                self.CreateAlert("The Folder Already Exists")
        else:
            self.CreateAlert("Please Enter a Name")
        #gdrive.CopyTechnicalReport(drive,DocId)
        #self.TeamFolder = gdrive.GetFolders (drive,self.TeacherIds[self.teacher])
        #Teams = GetList(self.TeamFolder)

        #m.UpdateMenu(GroupNames,Teams,True)
    def CreateAlert(self,message):
        self.slave = slave = tk.Tk()
        newFrame = tk.Frame(self.slave, width = 200)
        self.slave.title("Alert")
        T = tk.Label(self.slave,text = message)
        T.pack(padx = (10,10),pady = (10,10))


        self.Createbutton = m.drawButton(newFrame,"Ok",'h.destroy')
        self.Createbutton.pack(pady = (0,10))
        newFrame.pack()
    def destroy(self):
        try:
            self.slave.destroy()
        except:
            self.slaveMain.destroy()
    def ChooseStudent(self,event = None):
##        try:
        if(int(StudentNames.curselection()[0]) == 0):
            
            self.CreateNewFolder()
            
        else:
            StudentNames.unbind("<Double-Button-1>")
            StudentNames.bind("<Double-Button-1>",h.DownloadButton)
            Students = GetList(self.StudentsIds)
            Students.sort()
            self.studentName = Students[int(StudentNames.curselection()[0])-1]
            self.studentID = self.StudentsIds[self.studentName]
            self.LevelIDs = gdrive.GetFolders(drive,self.studentID)
            print(self.studentName)
            DisplayText.set("Choose Student's Level")
            

            self.Levels = GetList(self.LevelIDs)
            self.Levels.sort()

            StudentLevelObj.pack()
            m.UpdateList (StudentLevelObj,StudentLevelVar,self.Levels)
            
            self.UploadFolderId = self.LevelIDs[self.Levels[0]]
        

            
            self.UploadDirectoryIds= gdrive.GetFiles(drive,self.UploadFolderId)
            self.UploadDirectory = GetList(self.UploadDirectoryIds)
            
            

            m.UpdateMenu(StudentNames,self.UploadDirectory,False)
            StudentNames.pack_forget()
            gns.pack_forget()
            
            chooseGroupButton.pack_forget()
                

                #m.packMenu(GroupFolders,gfs)
                #GroupFolders.pack()
                #m.menu.pack_forget ()
    ##

                    
     
                #self.CreateAlert("Please Choose a Team")
##        except:
##            self.CreateAlert("Choose a Name")
            
    def TechnicalReport(self,silent = False):
        try:
            Files = gdrive.GetFiles(drive,self.CodeFolderId)
            FileNames = GetList(Files)
            FileName = FileNames[StudentNames.curselection()[0]]
            FileName = FileName.split(".")[0]
            ProjectName = FileName + " Technical Report"
            
            try:
                gdrive.CopyTechnicalReport (drive,self.Projects["Documents"],ProjectName)
                url = gdrive.GetFileURL(drive,ProjectName,self.Projects["Documents"])
            except:
                gdrive.CopyTechnicalReport (drive,self.Projects["Document"],ProjectName)
                url = gdrive.GetFileURL(drive,ProjectName,self.Projects["Document"])
            

            DisplayText.set("Launching WebBrowser")
            if(not silent):
                webbrowser.open(url,new = 2)
        except:
            self.CreateAlert("Please Select a Project")

    def UploadButton(self):
        try:

            #Folder2Upload = self.TeamFolder[Folders[int(GroupFolders.curselection()[0])]]
            #Folder2Upload = self.TeamFolder['Code']
            try:
                options = {}
                options['defaultextension'] = '.py'
                options['filetypes'] = [('Python Files', '.py'),('All Files', '.*')]
                osType = platform.platform().split("-")[0]
                if(osType!= "Windows"):
                    options['initialdir'] = '/home/pi/Desktop'
                else:
                    options['initialdir'] = os.path.expanduser("~")+"\\Desktop\\"
                
                

                options['parent'] = m.buttons
                options['title'] = 'Select file to Upload'
                
                path = tkFileDialog.askopenfilename(**options)

                
                parts = path.split("/")
                FileName = parts[-1].split(".")[0]


                FileName += ".py"


                #path = "C:\Users\Fernando\Desktop\Anaheim GoogleDrive\test.txt"
                gdrive.UploadFile (drive,self.CodeFolderId,path,FileName)
                print('Upload \"'+ FileName+'\" Successful')
                self.CreateAlert('Upload \"'+ FileName+'\" Successful')

                CodeFolder = gdrive.GetFiles(drive,self.Projects["Code"])

                Codes = GetList(CodeFolder)
                m.UpdateMenu(StudentNames,Codes,False)
                DisplayText.set("Upload Sucessful")
                #os.remove(path)
                #self.TechnicalReport(True)
            except:
                self.CreateAlert("No File Selected")
                
                
        except:
            self.CreateAlert("Please Select a Folder")


    def DownloadButton(self,event = None):
        try:
            #Folder2Download = self.TeamFolder['Code']
            path = '/home/pi'
            Files = gdrive.GetFiles(drive,self.CodeFolderId)
            FileNames = GetList(Files)
            
            FileName = FileNames[StudentNames.curselection()[0]]
            FileID = Files[FileName ]

            if(FileID and FileName):
                gdrive.DownloadFile(drive,FileID,FileName)
                osType = platform.platform().split("-")[0]
                if(osType!= "Windows"):
                    DesktopPath= "/home/pi/Desktop/"
                else:
                    DesktopPath = os.path.expanduser("~")+"\Desktop\\"

                try:
                    os.rename(FileName,DesktopPath+FileName)
                except:
                    os.remove(DesktopPath+FileName)
                    os.rename(FileName,DesktopPath+FileName)
                print('Download \"'+ FileName+'\" Successful')
                self.CreateAlert("File Downloaded! Look for it on Desktop")
                DisplayText.set("Download Sucessful")
                    
            else:
                self.CreateAlert("File Does not Exist")
        except:
            self.CreateAlert("Please Select a Folder")

            
def GetList(tup,ex = []):
    newlist = tup.keys()
    toreturn = []
    for thing in newlist:
        if(not thing in ex):
            toreturn.append(thing)
    return toreturn
m = Menu()
h = Handlers()
drive = gdrive.Connect()

##
##
##
folders = gdrive.GetFolders(drive)
TypeObj,TypeVar = m.drawDropDown(m.master,"h.StudentType",GetList(folders),True)
StudentLevelObj,StudentLevelVar = m.drawDropDown(m.master,"h.StudentLevel",[""])
StudentLevelObj.pack_forget()
DisplayText = m.drawMessage(m.master,"Please Choose a School")
StudentNames,gns = m.drawMenu(m.menu,[],True)

StudentNames.bind("<Double-Button-1>",h.ChooseStudent)
DisplayText.set("Welcome to MxUpload")
chooseGroupButton = m.drawButton(m.buttons,"Choose","h.ChooseStudent")
##
##
##
##
TechnicalReport = m.drawButton(m.buttons,"Technical Report", "h.TechnicalReport")
ChooseUploadFolder = m.drawButton(m.buttons,"Upload Code","h.UploadButton")
ChooseDownloadCode = m.drawButton(m.buttons,"Download Code", "h.DownloadButton")
##
m.menu.pack()
##m.buttons.pack ()
tk.mainloop()
