@echo off

::CodePackage\
set currentpath=%~dp0
::@echo %currentpath%

cd %currentpath%
cd "CodePackage\"
cd "Scan_FTP\"

"C:\ProgramData\Anaconda3\python.exe" "Jiro_FTP.py"


::pause

