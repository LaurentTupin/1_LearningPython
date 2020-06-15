import os
import shutil
import datetime as dt


#==============================================================================
# Function
#==============================================================================
def fList_FileInDir(str_path):
    try:
        l_fic = os.listdir(str_path)
    except:
        print(' ERROR in fList_FileInDir')
        print('  ', str_path)
        raise
    return l_fic

def fDte_GetModificationDate(str_pathFile):
    try:
        dte_modif = os.path.getmtime(str_pathFile)
        dte_modif = dt.datetime.fromtimestamp(dte_modif)
    except:
        print(' ERROR in fDte_GetModificationDate')
        print('  ', str_pathFile)
        raise
    return dte_modif

def act_createDir(str_folder, str_folderShortName = ''):
    try:
        if str_folderShortName == '': str_folderShortName = str_folder
        if not os.path.exists(str_folder):
            try: os.makedirs(str_folder)
            except:
                print(' ERROR: act_createDir - Program could NOT create the Dir')
                print('  ', str_folder, str_folderShortName)
                raise
    except:
        print(' ERROR: act_createDir')
        print('  ', str_folder, str_folderShortName)
        raise 
    return True

def fL_GetListSubFolder_except(str_folder, str_folderExcept = ''):
   if str_folderExcept != '':
       return [x[0] for x in os.walk(str_folder) if x[0][:9] != str_folderExcept]
   else: return [x[0] for x in os.walk(str_folder)]

def fL_GetListDirFileInFolders(l_subDir, l_typeFile = []):
    listTuple_PathFic = []
    for Dir in l_subDir:
        if l_typeFile:
            list_fic = [(Dir, fic) for fic in fList_FileInDir(Dir) if fic[-3:] in l_typeFile or fic[-4:] in l_typeFile]
        else: 
            list_fic = [(Dir, fic) for fic in fList_FileInDir(Dir)]
        if list_fic: listTuple_PathFic += list_fic
    return listTuple_PathFic
#==============================================================================
    


def Act_importPyFiles(str_networkFolder, str_myLocalPath):
    
    # DESTINATION = LOCAL
    # Get all the sub Dir in the folder
    l_subDir_Local = fL_GetListSubFolder_except(str_myLocalPath)
    # Get Tuples in Liste (Path, File Python) of files in the Dest Folder
    l_PathFic_Local = fL_GetListDirFileInFolders(l_subDir_Local, ['.py', '.ui', '.txt', '.csv', 'bat', '.xml', 'docx'])
    # List Files to only import them
    l_files_Local = [t_pathFic[1] for t_pathFic in l_PathFic_Local if not t_pathFic[1] == 'PyUpdate_Solution.py']
    
    # ORIGIN = NETWORK
    # Get the same files in the Origin folder to import it
    l_subDir_network = fL_GetListSubFolder_except(str_networkFolder)
    # Get Tuples in Liste (Path, File Python)
    l_PathFic_network = fL_GetListDirFileInFolders(l_subDir_network)
    # Keep only the one already here
    l_PathFic_network = [t_pathFic for t_pathFic in l_PathFic_network if t_pathFic[1] in l_files_Local]
    
    # Loop on File to copy them
    for t_file in l_PathFic_network:
        path_network = t_file[0]
        file = t_file[1]
        path_local = path_network.replace(str_networkFolder,str_myLocalPath)
        
        # If file is new --> Create Folder + files
        if (path_local, file) not in l_PathFic_Local:
            #print('COPY NEW...  ', 'Folder: ' + path_network, ' |  Destination: ' + path_local, ' |  File:  ' + file)
            #act_createDir(path_local)
            #shutil.copy(path_network + '\\' + file, path_local + '\\' + file)
            pass
        else:
            dte_lastmod = fDte_GetModificationDate(path_network + '\\' + file)
            dte_lastmod_Arch = fDte_GetModificationDate(path_local + '\\' + file)
            # Compare Date
            if dte_lastmod > dte_lastmod_Arch:
                print('COPY UPDATE...  ', 'Folder: ' + path_network, ' |  Destination: ' + path_local, ' |  File:  ' + file)
                shutil.copy(path_network + '\\' + file, path_local + '\\' + file)



# UPDATE : List present files and Update then from : \\uk-pdeqtfs01\E\SolaBI\Python_Installer
str_myLocalPath = '.'
str_networkPath = r'\\uk-pdeqtfs01\E\SolaBI\Python_Installer\Py_Package'
Act_importPyFiles(str_networkPath, str_myLocalPath)


# UPDATE : List files in folder 'C:\temp\Py_Package' and Update then from : \\uk-pdeqtfs01\E\SolaBI\Python_Installer
str_pathDest = r'C:\temp\Py_Package'
Act_importPyFiles(str_networkPath, str_pathDest)


## END
#time.sleep(3)
#print('\n')
#print('-------------------------------------')
#print('The Solution has been update \n')
#input("Press Enter to close the window: ")

