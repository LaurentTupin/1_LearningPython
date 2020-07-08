import time
from Py_Package import fct_Files as fl

#------------------------------------------------------------------------------
#--------- Fonctions --------------
#------------------------------------------------------------------------------
def Act_movePyFiles(str_folder_dest, l_fichierToMv = []):
    # Get all the sub Dir in the folder -- Split btw Archive and the rest
    l_subDir = fl.fL_GetListSubFolder_except('.', '.\\Archive')
    l_subDir_Dest = fl.fL_GetListSubFolder_except(str_folder_dest, '')
    # Get Tuples in Liste (Path, File Python)
    l_PathFic = fl.fL_GetListDirFileInFolders(l_subDir)
    l_PathFic_Dest = fl.fL_GetListDirFileInFolders(l_subDir_Dest)
    l_PathFic = [t_pathFic for t_pathFic in l_PathFic if t_pathFic[1] in l_fichierToMv]
    # Copy / Update files from a list of tuple to another
    fl.Act_CopyUpdateFiles(l_PathFic, l_PathFic_Dest, str_folder_dest)
    
    
#------------------------------------------------------------------------------
#--------- To Prod --------------
#------------------------------------------------------------------------------
l_fichierToMove = ['PyInstaller_Seita.exe', 'PyInstaller_LaPerouse.exe', 'PyInstaller_DNS.exe', 'PyInstaller_Spectre.exe',                    
                   'IT_guide_PyInstall.docx', 'Test_Installed_Libraries.py','PyUpdate_Solution.py',
                   'fct_dataframe.py', 'fct_Date.py', 'fct_DB.py', 'fct_Files.py', 'fct_Ftp.py', 'fct_html.py', 'fct_outlook.py',
                   'Seita.py', 'pcfAutomate_design.ui', 'PCF_creater.py', 'PCF_download.py', 'PCF_genericProcess.py',
                   'Seita_Param.csv', 'Seita_Param_Mail.csv', 'Seita_UserGuide.docx', 'Add New PCF to Seita.docx',
                   'LaPerouse.py','LaPerouse.ui','LaPerouse_Param.csv','Process_Bruni.py',
                   'DNS.py','DNS_1MainFct.py','DNS_3genericProcess.py','DNS_design.ui','DNS_Param.csv','DNS_Param_Mail.csv','DNS_Param_PcfAdr.csv',
                   'Spectre.py','NPA_BackUp.py','NPA_Republished.py','NPA_Log.py','NPA_design.ui','Re-Published ETF_Update Table.txt',
                   'Jiro.bat','LaPerouse.bat','Seita.bat','DNS.bat','Spectre.bat'
                   ]

# Deliver for Singapore - SolaBI
str_path = r'\\uk-pdeqtfs01\E\SolaBI\Python_Installer'
Act_movePyFiles(str_path , l_fichierToMove)

print('Fini !!!')
time.sleep(6)
#input("Press Enter to close the window: ")