import time
from Py_Package import fct_Files as fl


#------------------------------------------------------------------------------
#--------- Fonctions --------------
#------------------------------------------------------------------------------
def Act_archPyFiles():
    # Get all the sub Dir in the folder -- Split btw Archive and the rest
    l_subDir = fl.fL_GetListSubFolder_except('.', '.\\Archive')
    l_subDirArch = fl.fL_GetListSubFolder_except('.\\Archive', '')
    # Get Tuples in Liste (Path, File Python)
    l_PathFic = fl.fL_GetListDirFileInFolders(l_subDir, ['.py', '.ui', '.txt', '.csv', '.bat', '.xml', 'docx', '.exe'])
    l_PathFic_Arch = fl.fL_GetListDirFileInFolders(l_subDirArch)
    # Copy / Update files from a list of tuple to another
    fl.Act_CopyUpdateFiles(l_PathFic, l_PathFic_Arch, '.\\Archive')
    
    
#------------------------------------------------------------------------------
#--------- To Archives  --------------
#------------------------------------------------------------------------------   
# Archives the Python files
Act_archPyFiles()


print('Fini !!!')
time.sleep(10)
#input("Press Enter to close the window: ")