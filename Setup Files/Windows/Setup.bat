git clone http://github.com/yoshiscienceguy/IrvineUploadProgram
move IrvineUploadProgram c:/Users/%USERNAME%
@echo off

set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\MxUpload.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "C:\Users\%USERNAME%\IrvineUploadProgram\src\MxPiDrive\GUI.pyw" >> %SCRIPT%
echo oLink.IconLocation = "C:\Users\%USERNAME%\IrvineUploadProgram\src\logo.ico" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%