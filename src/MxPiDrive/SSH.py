import paramiko, base64
import subprocess, re, threading, socket,sys,os

goodAddresses = []
def GetFiles(place,client):
    
    stdin, stdout, stderr = client.exec_command('ls .//' +place )
    files = []
    files2 = []
    for line in stdout:
        files.append({line.strip("\n"):place})
        files2.append(line.strip("\n"))
    return files,files2



def GetEthernetAddress():
    proc = subprocess.check_output("ipconfig" ).split("\n")
    count = 0
    index = 0
    final = 0
    findexit = False
    try:
        for thing in  proc:
            if(len(thing) > 1):
                if("Ethernet" in thing):
                    index = count
                    findexit = True
                if(findexit):
                    if("IPv4" in thing):
                        final = count
                        break
                    
            count +=1 
        
        return(proc[final].strip().split()[-1])
    except:
        print("Please Check Your Ethernet Connection, restart this program")
        sys.exit()
def Ping(ip,count = 0):
    global goodAddresses
    if(count > 5):

        return 0
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW 
        info = subprocess.Popen("ping "+ip+" -n 1 -w 5",startupinfo = si,stdout=subprocess.PIPE)
        (output,err) = info.communicate()
        messages = output.split("\n")
        if("unreachable" in messages[2]):
            return 0
        sucess = int(messages[5].strip().split("=")[-1].split()[0])
        if(sucess == 0):
            
            goodAddresses.append(ip)
            return 1
    except:
        Ping(ip,count+1)


#
def Search():
    address = GetEthernetAddress()
    
    threads = []
    print("Scanning Ip's... Please be patient, this might take a while!")
    for i in range(254):
        newAddress = address[:address.rfind(".")+1]+str(i+2)
##        print(newAddress)
##        print(Ping(newAddress))
##        if(Ping(newAddress) == 1):
##            break
        threads.append(threading.Thread(target = Ping,args =(newAddress,)))
    for thread1 in threads:
        thread1.start()
    for thread1 in threads:
        thread1.join()
    print(goodAddresses)
    RPiAddress = 0
    for address in goodAddresses:
        try:
            if("raspberry" in socket.gethostbyaddr (address)[0]):
                return address
        except:
            pass
             
    print("No raspberries found")
    return 0

def SearchRPi(Address):
    if(Address != 0):
                                  
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(Address, username='pi', password='raspberry')

        dir1,list1 = GetFiles("",client)
        dir2,list2 = GetFiles("Desktop",client)
        
        dirs = dir1+dir2
        directories = {}
        for dir1 in dirs:
            directories.update(dir1)
        files = list1 + list2
        pyfiles = []
        for file1 in files:
            if(file1.endswith(".py")):
                pyfiles.append(file1)
            
        client.close()
        return directories,pyfiles

def DownloadFile(Address,Path,Filename):
    if(Address != 0):
                                  
        paramiko.util.log_to_file(os.getcwd()+"\\LOG.txt")
        # Open a transport
        host = Address
        port = 22
        transport = paramiko.Transport((host, port))
        # Auth
        transport.connect(username = "pi", password = "raspberry")
        sftp = paramiko.SFTPClient.from_transport(transport)
        # Download
        filepath = "/"+Path+"/"+Filename
        print(filepath)
        localpath = os.getcwd()+"\\"+Filename
        print(localpath)
        sftp.get(filepath, localpath)

        # Close
        sftp.close()
        transport.close()
def UploadFile(Address,Path,Filename):
    if(Address != 0):                 
        paramiko.util.log_to_file(os.getcwd()+"\\LOG.txt")
        # Open a transport
        host = Address
        port = 22
        transport = paramiko.Transport((host, port))
        # Auth
        transport.connect(username = "pi", password = "raspberry")
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Upload
        
        filepath = '/home/pi/Desktop/'+Filename
        print(filepath)
        localpath = Path
        print(Path)
        sftp.put(localpath, filepath)
        # Close
        sftp.close()
        transport.close()
        print("sucess!")
