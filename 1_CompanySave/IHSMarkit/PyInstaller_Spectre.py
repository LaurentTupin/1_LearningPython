import os
import time
from Py_Package import fct_Files as fl


def Act_movePyFiles_Installer(str_folder_dest, str_folder_origin = '', l_fichierToMv = []):
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
str_pathDest = r'C:\temp'
fl.act_createDir(str_pathDest)

# 2. Copy / Update the Py_package in the folder
l_fichierToMove = ['fct_dataframe.py', 'fct_Date.py', 'fct_DB.py', 'fct_Files.py', 'fct_Ftp.py', 'fct_html.py', 'fct_outlook.py', 
                   'Spectre.py', 'NPA_BackUp.py', 'NPA_Republished.py', 'NPA_Log.py', 'NPA_design.ui', 'Re-Published ETF_Update Table.txt',
                   'Test_Installed_Libraries.py'
                   ]
Act_movePyFiles_Installer(str_pathDest, '.', l_fichierToMove)

# 3. Create a Folder For BAT + Guide + Updater
str_pathDesktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
str_pathDest = os.path.join(str_pathDesktop,'Python_App')
fl.act_createDir(str_pathDest)

# 4. Fill the folder to use
l_fichierToMove = ['Spectre.bat']
Act_movePyFiles_Installer(str_pathDest, '.\\Py_Package\\BAT', l_fichierToMove)

l_fichierToMove = ['PyUpdate_Solution.py']
Act_movePyFiles_Installer(str_pathDest, '.\\Py_Package', l_fichierToMove)


# END
time.sleep(3)
print('\n')
print('-------------------------------------')
print('The App has been installed. You can access it in the folder: ' + str_pathDest + '\n')
input("Press Enter to close the window: ")

