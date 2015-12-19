#!/usr/bin/env python
'''
__author__ = "Fernando de Paz"
__copyright__ = "Copyright 2015, Mathobotix"

__version__ = "3.3.5"
__email__ = "f.depaz@hotmail.com"
__github__ = "yoshiscienceguy"




'''
import sys
sys.modules[__name__].__dict__.clear()

import Tkinter as tk
import tkFileDialog
import gdrive , Gifs , SSH
import time, platform, os, urllib2, webbrowser, threading


try:
    response = urllib2.urlopen("http://www.google.com",timeout=1)
except:
    print("You Don't Have an Active Internet Connection")
    print("Please ask a Mentor for HELP")
    quit()
StemLevels = [("Buildologie","Buildologie - (Tot-Bot)"),
              ("Buildologie I","Buildologie I - (Elementary)"),
              ("Buildologie II","Buildologie II - (Junior High)"),
              ("Buildologie III","Buildologie III - (High School)"),
              ("Intro Codologie","Codologie I (Intro)"),
              ("Intermediate Codologie","Codologie II (Intermediate)"),
              ("Advanced Codologie","Codologie III (Advanced)")]

CodologieLevel = [("Intro Codologie","Codologie I (Intro)"),
                  ("Intermediate Codologie","Codologie II (Intermediate)"),
                  ("Advanced Codologie","Codologie III (Advanced)")]

BuildologieLevel = [("Buildologie","Buildologie - (Tot-Bot)"),
                  ("Buildologie I","Buildologie I - (Elementary)"),
                  ("Buildologie II","Buildologie II - (Junior High)"),
                  ("Buildologie III","Buildologie III - (High School)")]
class Menu():
    def __init__(self):
        self.root = tk.Tk()
        self.root.iconbitmap(os.path.expanduser("~")+"\\IrvineUploadProgram\\src\\logo.ico")
        self.root.minsize(400,200)
        self.root.maxsize(400,700)
        self.root.title("Google Drive Upload")
        self.firstoption = tk.Frame(self.root,width = 300)
        self.secondoption = tk.Frame(self.root,width = 300,relief = tk.RIDGE,borderwidth = 3)
        self.firstScreen = tk.Frame(self.root,width= 300)
        self.master = tk.Frame(self.root,width= 300)
        self.gifsection = tk.Frame(self.root,width = 300)
        self.menu = tk.Frame(self.root,width= 300,height = 2,relief = tk.SUNKEN,borderwidth = 1)
        self.buttons = tk.Frame (self.root,width= 300)
        self.master.pack()
        self.gifsection.pack()
        #tk.mainloop()
        
    def drawDropDown(self,frame,functionName,listDisplay,Default = False):
        AssociatedVariable = tk.StringVar(frame)
        AssociatedVariable.trace("w",eval(functionName))
        DropDown = apply(tk.OptionMenu,(frame,AssociatedVariable)+tuple(listDisplay))
        if(Default):
            AssociatedVariable.set("Choose Student Type")

        DropDown.pack(pady=(10,0))

        return DropDown , AssociatedVariable
        
        
    def drawButton(self,frame,toSay,functionName,picName = None):
        submit = tk.Button(frame, text = toSay,command = eval(functionName),borderwidth = 4,relief =tk.GROOVE)
        if(picName):
            photo = tk.PhotoImage (file="ICONS//"+picName+".gif")
            submit.config(image = photo)
            return submit,photo

        else: 
        

            return submit
    
    def drawRadioButtons(self,frame,options,excluded = None):
        
        self.v = tk.StringVar()

        Buttons = []
        if(excluded == None):
            for texts, option in options:
                rb = tk.Radiobutton(frame, text = texts, variable = self.v, value = option)
                rb.pack(anchor = tk.W)
                rb.deselect()
                Buttons.append(rb)
            self.v.set(options[1][1])
        else:

            for texts, option in options:
                if(option in excluded):
                    rb = tk.Radiobutton(frame, text = texts, variable = self.v, value = option,state = "disabled")
                else:
                    rb = tk.Radiobutton(frame, text = texts, variable = self.v, value = option)
                
                rb.pack(anchor = tk.W)
                rb.deselect()
                Buttons.append(rb)
            self.v.set(options[0][1])
        
        
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
    def drawMessage(self,frame,toSay,options = None):
        self.vartoSay = tk.StringVar()
        textbox = tk.Label(frame,textvariable = self.vartoSay, fg = "red",font = ("Helvetica",10))
        self.vartoSay.set(toSay)
        if(options):
            textbox.pack(pady = 10,side = options)
        else:
            textbox.pack(pady = 10,)
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
    def ComputerType(self):
        global RPiAddress, ComputerType
        ComputerType = "Raspberry Pi"
        DisplayText2.set("Searching for the Raspberry Pi")
        m.root.update()
        RPiAddress = SSH.Search()
        if(RPiAddress == 0):
            for i in range(5):
                DisplayText2.set("Raspberry not Found... \n Exiting in "+str(5-i)+" seconds")
                time.sleep(1)
                m.root.update()
            quit()
        RaspberryPiDevice.pack_forget()
        m.firstScreen.pack_forget()
        
        self.message0 = m.drawMessage(m.firstoption,"Student Type:  ",tk.LEFT)
        self.message1 = m.drawMessage(m.secondoption,"Level:  ",tk.LEFT)
        TypeObj.pack(side = tk.LEFT)
        m.firstoption.pack()
        m.menu.pack_forget()
        self.message2 = m.drawMessage(m.menu,"Choose Student:  ",tk.LEFT)
        DisplayText.set("Raspberry Pi found at: " + RPiAddress +"\nConnected!"+"\n\nSelect Student's type")
    def ComputerType2(self):
        ComputerType = "Windows"
        RaspberryPiDevice.pack_forget()
        m.firstScreen.pack_forget()
        self.message0 = m.drawMessage(m.firstoption,"Student Type:  ",tk.LEFT)
       
        TypeObj.pack(side = tk.LEFT)
        DisplayText.set("Select Student's type")
        m.firstoption.pack()
        m.menu.pack_forget()
        self.message2 = m.drawMessage(m.menu,"Choose Student:  ",tk.LEFT)
        self.message1 = m.drawMessage(m.secondoption,"Level:  ",tk.LEFT)
    def StudentLevel(self,p,a,c):


        
        if(StudentLevelVar.get() == "Choose One"):
            return
        DisplayText.set("Current Selected: "+ self.studentName+"\n\nSelect Student's Project\n\n")

        m.firstoption.pack_forget()
        m.secondoption.pack_forget()
        m.firstoption.pack(pady = 00)
        m.secondoption.pack(pady = 0)
        m.secondoption.config(borderwidth = 0,relief = tk.FLAT)
        m.buttons.pack_forget()
        m.menu.pack_forget()
        m.menu.pack(pady = (0,10))
        m.buttons.pack()
        m.root.update()
        self.message2.set("Select Project: ")
        m.packMenu(StudentNames,gns)
        m.buttons.pack()
        UploadFolderID = self.LevelIDs[StudentLevelVar.get()]

        self.Projects = gdrive.GetFolders(drive,UploadFolderID)
        CodeFolder = gdrive.GetFiles(drive,self.Projects["Code"])
        self.CodeFolderId = self.Projects["Code"]


        Codes = GetList(CodeFolder)
        m.UpdateMenu(StudentNames,Codes,False)
        os = platform.platform().split('-')[0]
        if(os == "Windows"):
           TechnicalReport.pack(pady = 10) 

        ChooseUploadFolder.pack(pady = 10)
        ChooseDownloadCode.pack(pady = 10,anchor = tk.W)

        newLevelButton.pack_forget()


    def StudentType(self,p,a,c):
        #used
        
        try:
            StudentNames.unbind("<Double-Button-1>")
            StudentNames.bind("<Double-Button-1>",self.ChooseStudent)
            
            DisplayText.set("Select Student's Name")
            self.message2.set("Select Student: ")
            os = platform.platform().split('-')[0]
            if(os == "Windows"):
               TechnicalReport.pack_forget() 
            
            ChooseUploadFolder.pack_forget()
            ChooseDownloadCode.pack_forget()
            chooseGroupButton.pack_forget()
            m.buttons.pack_forget()
            m.menu.pack_forget()
            m.secondoption.pack_forget()
            self.school = TypeVar.get()

            self.StudentsIds = gdrive.GetFolders(drive,folders[TypeVar.get()])
            m.menu.pack_forget()
            m.menu.pack()
            
            
            m.packMenu(StudentNames,gns)
                    
            StudentNames.pack(side = tk.LEFT)
            gns.pack(side = tk.LEFT)
            Students = GetList(self.StudentsIds)
            Students.sort()
            m.UpdateMenu(StudentNames,Students,True)
            chooseGroupButton.pack(pady = 10)
            m.buttons.pack()
            newLevelButton.pack_forget()
        except:
            print("Starting")
            pass
    def CreateNewFolder(self):
        self.slaveMain = tk.Toplevel(m.master)
        self.slaveMain.geometry("300x250")
        newFrame = tk.Frame(self.slaveMain,width = 500)
        self.slaveMain.title("Enter New Folder Name")
        self.NewTextMessage = m.drawMessage(newFrame,"Select New Student's Level")
        if(TypeVar.get() == "Buildologie"):
            self.slaveMain.geometry("300x280")
            self.NewLevelObject, self.NewLevelVariable = m.drawRadioButtons(newFrame,BuildologieLevel)
        elif(TypeVar.get() == "Codologie"):
            self.slaveMain.geometry("300x250")
            self.NewLevelObject, self.NewLevelVariable = m.drawRadioButtons(newFrame,CodologieLevel)
        else:
            self.slaveMain.geometry("300x340")
            self.NewLevelObject, self.NewLevelVariable = m.drawRadioButtons(newFrame,StemLevels)
        self.NewTextMessage = m.drawMessage(newFrame,"Enter the New Student's Name")
        self.NewNameObject, self.NewNameVariable = m.drawTextBox(newFrame)
        
        self.Createbutton = m.drawButton(newFrame,"Create","h.FolderCreation")
        self.Createbutton.pack(pady = (0,10))
        newFrame.pack()
        newFrame.update()

    def FolderCreation(self):
        name = self.NewNameObject.get()
        if(name.strip() != "" and name != "Enter Name Here"):
            
            dummy = name.split()
            name = ""
            for part in dummy:
                name += part[0].upper() + part[1:].lower() + " "
            if(not name in self.StudentsIds):
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
        self.slave = tk.Toplevel(m.master)
        self.slave.geometry("200x75")
        newFrame = tk.Frame(self.slave,width = 200)
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

        
        
    def NewLevel(self):
        self.slaveLevel = tk.Toplevel(m.master)
        self.slaveLevel.geometry("300x250")
        newFrame = tk.Frame(self.slaveLevel,width = 500)
        self.slaveLevel.title("Enter New Folder Name")
        self.NewTextMessageLevel = m.drawMessage(newFrame,"Select Student's New Level")
        CurrentLevels = gdrive.GetFolders(drive,self.studentID)
        CLevels = GetList(CurrentLevels)
        CLevels.sort()
        if(TypeVar.get() == "Buildologie"):
            self.slaveLevel.geometry("300x280")
            self.NewLevel2Object, self.NewLevel2Variable = m.drawRadioButtons(newFrame,BuildologieLevel,CLevels)
        elif(TypeVar.get() == "Codologie"):
            self.slaveLevel.geometry("300x250")
            self.NewLevel2Object, self.NewLevel2Variable = m.drawRadioButtons(newFrame,CodologieLevel,CLevels)
        else:
            self.slaveLevel.geometry("300x340")
            self.NewLevel2Object, self.NewLevel2Variable = m.drawRadioButtons(newFrame,StemLevels,CLevels)

        
        self.CreatebuttonLevel = m.drawButton(newFrame,"Create New Level","h.LevelCreation")
        self.CreatebuttonLevel.pack(pady = (0,10))
        newFrame.pack()
        newFrame.update()
    def LevelCreation(self):

        newid = self.StudentsIds[self.studentName]
        try:
            self.slave.destroy()
        except:
            self.slaveLevel.destroy()

        
        LevelId = gdrive.CreateFolder(drive,self.NewLevel2Variable.get(),newid)
        DocId = gdrive.CreateFolder(drive,"Documents",LevelId)
        CodeId = gdrive.CreateFolder(drive,"Code",LevelId)
        MediaId = gdrive.CreateFolder(drive,"Media",LevelId)
                         
        self.LevelIDs = gdrive.GetFolders(drive,self.studentID)
        self.Levels = GetList(self.LevelIDs)
        self.Levels.sort()
        
        m.UpdateList (StudentLevelObj,StudentLevelVar,self.Levels)
        self.CreateAlert("New Level Created")
    def ChooseStudent(self,event = None):
##        try:
        if(int(StudentNames.curselection()[0]) == 0):
            
            self.CreateNewFolder()
            
        else:
            StudentNames.unbind("<Double-Button-1>")
            StudentNames.bind("<Double-Button-1>",h.DownloadButton)
            Students = GetList(self.StudentsIds)
            Students.sort()
            m.menu.pack_forget()
            self.studentName = Students[int(StudentNames.curselection()[0])-1]
            self.studentID = self.StudentsIds[self.studentName]
            self.LevelIDs = gdrive.GetFolders(drive,self.studentID)

            DisplayText.set("\n\nCurrent Student : " + self.studentName+ "\n\nChoose Student's Level")
            

            self.Levels = GetList(self.LevelIDs)
            self.Levels.sort()
            
            self.message1.set("Level: ")
            StudentLevelObj.pack(side = tk.LEFT)
            m.firstoption.pack_forget()
            m.buttons.pack_forget()
            m.firstoption.pack(pady = 20)
            m.secondoption.pack(pady = (100,40))
            
            m.buttons.pack(pady = 20)
            
            m.UpdateList (StudentLevelObj,StudentLevelVar,self.Levels)
            
            self.UploadFolderId = self.LevelIDs[self.Levels[0]]
        

            
            self.UploadDirectoryIds= gdrive.GetFiles(drive,self.UploadFolderId)
            self.UploadDirectory = GetList(self.UploadDirectoryIds)
            
            

            m.UpdateMenu(StudentNames,self.UploadDirectory,False)
            StudentNames.pack_forget()
            gns.pack_forget()
            
            newLevelButton.pack(pady = (0,10))
            
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
    def SelectProjectUpload(self):
        projectName = self.RaspProjects[self.RPiProjectsMenu.curselection()[0]]
        location = self.RaspProjectsLocation[projectName]
        self.slaveLevel2.destroy()
        path = ""
        if(location == ""):
            path = "/home/pi"
        else:
            path = "home/pi/Desktop"
        print(path)
        print(projectName)
        SSH.DownloadFile(RPiAddress,path,projectName)
        print(os.getcwd()+"\\"+projectName + "<----------")
        gdrive.UploadFile (drive,self.CodeFolderId,os.getcwd()+"\\"+projectName,projectName)
        print('Upload \"'+ projectName+'\" Successful')
        self.CreateAlert('Upload \"'+ projectName+'\" Successful')

        CodeFolder = gdrive.GetFiles(drive,self.Projects["Code"])

        Codes = GetList(CodeFolder)
        m.UpdateMenu(StudentNames,Codes,False)
        DisplayText.set("Upload Sucessful")
    def UploadButton(self):


    #Folder2Upload = self.TeamFolder[Folders[int(GroupFolders.curselection()[0])]]
    #Folder2Upload = self.TeamFolder['Code']
    
        if(ComputerType == "Raspberry Pi"):
            #UploadFile(RPiAddress,FileName)
            self.slaveLevel2 = tk.Toplevel(m.master)
            self.slaveLevel2.geometry("300x250")
            newFrame = tk.Frame(self.slaveLevel2,width = 500)
            self.buttonFrame = tk.Frame(self.slaveLevel2,width =500)
            self.slaveLevel2.title("Enter New Folder Name")
            self.RaspProjectsLocation,self.RaspProjects = SSH.SearchRPi(RPiAddress)
            self.RaspProjects.sort()
            self.RPiProjectsMenu,scrollbar = m.drawMenu(newFrame,self.RaspProjects,False)
            m.packMenu(self.RPiProjectsMenu,scrollbar)
            self.selectProjectButton = m.drawButton(self.buttonFrame,"Select Project","h.SelectProjectUpload")
            self.selectProjectButton.pack()
            newFrame.pack()
            self.buttonFrame.pack()
            
            
        else:
            try:
                options = {}
                options['defaultextension'] = '.py'
                options['filetypes'] = [('Programming Files', '.py .io .txt .sb2'),('All Files', '.*')]
                osType = platform.platform().split("-")[0]
                if(osType!= "Windows"):
                    options['initialdir'] = '/home/pi/Desktop'
                else:
                    options['initialdir'] = os.path.expanduser("~")+"\\Desktop\\"
                
                

                options['parent'] = m.buttons
                options['title'] = 'Select file to Upload'
                
                path = tkFileDialog.askopenfilename(**options)

                
                parts = path.split("/")
                FileName = parts[-1]


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
                
                



    def DownloadButton(self,event = None):
##        try:
            #Folder2Download = self.TeamFolder['Code']
            
            

        path = '/home/pi'
        Files = gdrive.GetFiles(drive,self.CodeFolderId)
        FileNames = GetList(Files)
        
        FileName = FileNames[StudentNames.curselection()[0]]
        FileID = Files[FileName]

        if(FileID and FileName):
            gdrive.DownloadFile(drive,FileID,FileName)
            if(ComputerType == "Raspberry Pi"):
                #UploadFile(RPiAddress,FileName)
                filepath = os.getcwd()+"\\"+FileName
                SSH.UploadFile(RPiAddress,filepath,FileName)
                print('Download \"'+ FileName+'\" Successful')
                self.CreateAlert("File Downloaded! Look for it on the Raspberry Pi Desktop")
                DisplayText.set("Download Sucessful to the Raspberry Pi")

            
            else:
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
##        except:
##            self.CreateAlert("Please Select a Folder")

            
def GetList(tup,ex = []):
    newlist = tup.keys()
    toreturn = []
    for thing in newlist:
        if(not thing in ex):
            toreturn.append(thing)
    return toreturn




drive = gdrive.Connect()
m = Menu()
h = Handlers()


##
##
##

folders = gdrive.GetFolders(drive)
osType = platform.platform().split("-")[0]

DisplayText = m.drawMessage(m.master,"Welcome to MxUpload")

TypeObj,TypeVar = m.drawDropDown(m.firstoption,"h.StudentType",GetList(folders),True)
RPiAddress = 0
ComputerType = "Windows"
if(osType== "Windows"):
    DisplayText2 = m.drawMessage(m.firstScreen,"Welcome to MxUpload\n\nPlease Choose the device your files are on")
    TypeObj.pack_forget()
    RaspberryPiDevice,image = m.drawButton(m.firstScreen,"Raspberry Pi","h.ComputerType","rpiLogo")
    RaspberryPiDevice.pack(padx = 20,pady=20)
    WindowsDevice,image2 = m.drawButton(m.firstScreen, "Windows","h.ComputerType2","windowsLogo")
    WindowsDevice.pack(padx = 20,pady=(0,20))
    m.firstScreen.pack()
try:
    time.sleep(.5)
    Gifs.Start(m.root)
    time.sleep(.5)
except:
    pass

StudentLevelObj,StudentLevelVar = m.drawDropDown(m.secondoption,"h.StudentLevel",[""])
StudentLevelObj.pack_forget()
StudentNames,gns = m.drawMenu(m.menu,[],True)
StudentNames.pack_forget()
gns.pack_forget()
StudentNames.bind("<Double-Button-1>",h.ChooseStudent)
DisplayText.set("")
chooseGroupButton = m.drawButton(m.buttons,"Choose","h.ChooseStudent")
newLevelButton = m.drawButton(m.buttons,"Create New Level","h.NewLevel")
##
##
##
##
TechnicalReport = m.drawButton(m.buttons,"Technical Report", "h.TechnicalReport")
ChooseUploadFolder = m.drawButton(m.buttons,"Upload Code","h.UploadButton")
ChooseDownloadCode = m.drawButton(m.buttons,"Download Code", "h.DownloadButton")
##
m.menu.pack(pady=20)
##m.buttons.pack ()
tk.mainloop()

