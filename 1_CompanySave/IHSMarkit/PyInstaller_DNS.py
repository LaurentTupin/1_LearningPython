import os
import time
try:
    from Py_Package import fct_Files as fl
except:
    print('ERORR: from Py_Package import fct_Files as fl')
    
    

def Act_movePyFiles_Installer(str_folder_dest, str_folder_origin = '', l_fichierToMv = []):
    #print(str_folder_dest)
    # Folder Origin
    l_subDir = fl.fL_GetListSubFolder_except(str_folder_origin, '.')
    # Get Tuples in Liste (Path, File Python)
    l_PathFic = fl.fL_GetListDirFileInFolders(l_subDir)
    l_PathFic = [t_pathFic for t_pathFic in l_PathFic if t_pathFic[1] in l_fichierToMv]
    #print(l_PathFic)
    
    # Folder Destination
    l_subDir_Dest = fl.fL_GetListSubFolder_except(str_folder_dest, '')
     # Get Tuples in Liste (Path, File Python)    
    l_PathFic_Dest = fl.fL_GetListDirFileInFolders(l_subDir_Dest)
    #print(l_PathFic_Dest)
    
    # Copy / Update files from a list of tuple to another
    fl.Act_CopyUpdateFiles(l_PathFic, l_PathFic_Dest, str_folder_dest, str_folder_origin.replace('.', ''))
    
    
#==============================================================================
# 1. Create the Folder
try:
    str_pathDest = r'C:\temp'
    fl.act_createDir(str_pathDest)
    str_pathDest2 = r'C:\temp\temp'
    fl.act_createDir(str_pathDest2)
except:
    print('Could not create Folder1: ', str_pathDest2)


# 2. Copy / Update the Py_package in the folder
try:
    str_folderSource = '.' #r'\\uk-pdeqtfs01\E\SolaBI\Python_Installer'
    l_fichierToMove = ['fct_dataframe.py', 'fct_Date.py', 'fct_DB.py', 'fct_Files.py', 'fct_Ftp.py', 'fct_html.py', 'fct_outlook.py', 
                       'DNS.py','DNS_1MainFct.py','DNS_3genericProcess.py','DNS_design.ui','DNS_Param.csv','DNS_Param_Mail.csv','DNS_Param_PcfAdr.csv',
                       'Test_Installed_Libraries.py'
                       ]
    Act_movePyFiles_Installer(str_pathDest, str_folderSource, l_fichierToMove)
except:
    print('Could not move Py file')

# 3. Create a Folder For BAT + Guide + Updater
try:
    str_pathDesktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    str_pathDest = os.path.join(str_pathDesktop,'Python_App')
    fl.act_createDir(str_pathDest)
except:
    print('Could not create Folder2: ', str_pathDest)
    
# 4. Fill the folder to use
try:
    l_fichierToMove = ['DNS.bat']
    Act_movePyFiles_Installer(str_pathDest, str_folderSource + '\\Py_Package\\BAT', l_fichierToMove)
except:
    print('Could not move Py file2')

try:
    l_fichierToMove = ['PyUpdate_Solution.py']
    Act_movePyFiles_Installer(str_pathDest, str_folderSource + '\\Py_Package', l_fichierToMove)
except:
    print('Could not move Py file3')

# END
time.sleep(3)
print('\n')
print('-------------------------------------')
print('The App has been installed. You can access it in the folder: ' + str_pathDest + '\n')
input("Press Enter to close the window: ")

