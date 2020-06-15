import sys, os
import datetime as dt
import shutil
sys.path.append('../')
import fct_Files as fl


def fStr_Message(str_in):
    print(str_in)
    return '\n' + str_in


def Act_CopyUpdateFiles_specialBackUp(l_FolderFic_from, str_DestFolder, int_onlyFileMoreRecentThan = 7, str_removeInDestFolder = ''):
    str_message = ''
    # Loop on File to copy / update them
    for t_file in l_FolderFic_from:
        str_folder = t_file[0]
        str_file = t_file[1]
        str_pathOrigin = os.path.join(str_folder, str_file)
        
        str_folder_Dest = str_folder.replace('.', str_DestFolder)
        str_folder_Dest = str_folder_Dest.replace(str_removeInDestFolder, '')
        str_pathDest = os.path.join(str_folder_Dest, str_file)
        
        # Process Only if more recent for 7 days (7 for example)
        dte_lastmod = fl.fDte_GetModificationDate(str_pathOrigin)
        dte_limit = dt.datetime.now() - dt.timedelta(int_onlyFileMoreRecentThan)
        
        if dte_lastmod > dte_limit:
            # If File DOES NOT Exists
            if not fl.fBl_FileExist(str_pathDest):
                str_message += fStr_Message('COPY...  Origin:  ' + str_folder + ' ||| Dest:  ' 
                                            + str_folder_Dest + ' ||| File:  ' + str_file)
                fl.fBl_createDir(str_folder_Dest)
                shutil.copy(str_pathOrigin, str_pathDest)
            else:
                # Compare Date (Update only if CLoud is more recent)
                dte_lastmod_dest = fl.fDte_GetModificationDate(str_pathDest)
                if dte_lastmod > dte_lastmod_dest:
                    str_message += fStr_Message('UPDATE...  Origin:  ' + str_folder + ' ||| Dest:  ' 
                                                + str_folder_Dest + ' ||| File:  ' + str_file)
                    shutil.copy(str_pathOrigin, str_pathDest)
    print('End BackUp !!!')
    return str_message


def fstr_BackUp(dte_date, str_folderOrigin, str_folderTarget, int_onlyFileMoreRecentThan):
    dir_current = os.getcwd()
    # Get all the sub Dir in the folder -- Except the folder (if empty, no exception)
    os.chdir(str_folderOrigin)
    l_SubDir_Cloud = fl.fL_GetListSubFolder_except('.', '')
    # Get Tuples in List (Path, File Python)
    l_PathFic_Cloud = fl.fL_GetListDirFileInFolders(l_SubDir_Cloud, ['.csv', '.txt', '.xls', 'xlsx', '.hdx', 'docx', '.etf'])
    # Copy / Update files from a list of tuple to another
    str_message = Act_CopyUpdateFiles_specialBackUp(l_PathFic_Cloud, str_folderTarget, int_onlyFileMoreRecentThan)
    # Fin !!
    os.chdir(dir_current)
    return str_message
