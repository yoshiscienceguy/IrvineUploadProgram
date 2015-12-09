git clone http://github.com/yoshiscienceguy/IrvineUploadProgram
move IrvineUploadProgram c:/Users/%USERNAME%/Documents

@echo off

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\MxUpload.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "C:\Users\%USERNAME%\Documents\IrvineUploadProgram\src\MxPiDrive\GUI.py" >> %SCRIPT%
echo oLink.IconLocation = "C:\Users\%USERNAME%\Documents\IrvineUploadProgram\src\logo.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%