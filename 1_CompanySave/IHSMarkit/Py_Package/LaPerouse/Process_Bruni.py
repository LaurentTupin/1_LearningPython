import pandas as pd
import datetime as dt
from pandas.tseries.offsets import BDay
import sys
sys.path.append('../')
import fct_Ftp as ftp
import fct_Files as fl

#-----------------------------------------------------------------
# Messages for the user to have information
#-----------------------------------------------------------------
def Initt(str_date = ''):
    str_return = '\n' + '------------------------------------------------'
    str_return += '\n' + 'Today is : ' + str_date
    str_return += '\n' + '------------------------------------------------'
    return str_return


#------------------------------------------------------------------------------------------------------------------------------------   
def Act_UpFiles_FTP(df_Param, row, str_folder, str_FileName, dte_date, bl_download = False):
    # Param
    str_FileUploadMode = str(df_Param.loc[row, 'FileUploadMode'])
    str_Perimeter = str(df_Param.loc[row, 'Perimeter'])
    str_FTP_server = str(df_Param.loc[row, 'FTP_server'])
    str_FTP_uid = str(df_Param.loc[row, 'FTP_uid'])
    str_FTP_pwd = str(df_Param.loc[row, 'FTP_pwd'])
    str_FTP_directory = str(df_Param.loc[row, 'FTP_directory'])
    
    # Get folder
    l_ftpFolder = str_FTP_directory.split('/')
    if l_ftpFolder[0] == '': l_ftpFolder = l_ftpFolder[1:]
    elif l_ftpFolder[0] == 'nan': l_ftpFolder = []	
    try:
        if bl_download:
            print('Downloading... ' + str_FileName)
            if fl.fBl_createDir(str_folder):
                print(' (*) Creation of the folder: {}'.format(str_folder))
            if str_FileUploadMode == 'FTP':
                ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folder)
            elif str_FileUploadMode == 'FTP_SSL':
                ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folder, -1, True)
            elif str_FileUploadMode == 'SFTP_Paramiko':
                ftp.ssh_downFile(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folder)
        else:
            print('Uploading... ' + str_FileName)
            if str_FileUploadMode == 'FTP':
                ftp.fBl_ftpUpFile_Bi(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folder)
            elif str_FileUploadMode == 'FTP_SSL':
                ftp.fBl_ftpUpFile_Bi(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folder, -1, True)
            elif str_FileUploadMode == 'SFTP_Paramiko':
                ftp.ssh_upFile(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folder)
    except:
        print('  ERROR in Act_UpFiles_FTP. Perimeter: {0}'.format(str_Perimeter))
        return False
    return True


#------------------------------------------------------------------------------------------------------------------------------------
def fStr_generateFileName(df_Param, row, dte_date):
    str_fileName = str(df_Param.loc[row, 'fileName'])
    str_DateOffset = str(df_Param.loc[row, 'DateOffset'])
    str_fileDate = str(df_Param.loc[row, 'fileDate'])
    str_fileName = str_fileName.replace('{fileDate}', (dte_date-BDay(-int(str_DateOffset))).strftime(str_fileDate))
    return str_fileName
def fStr_generateFolder(df_Param, row, str_folderRoot, dte_date):
    str_Dir_Dest = str(df_Param.loc[row, 'Dir_Source'])
    str_folderDate = str(df_Param.loc[row, 'folderDate'])
    if str_Dir_Dest[:2] == '\\\\':
        str_folderRaw = str_Dir_Dest.replace('{folderDate}', dte_date.strftime(str_folderDate)) + '\\'
    else: 
        str_folderRaw = str_folderRoot + str_Dir_Dest.replace('{folderDate}', dte_date.strftime(str_folderDate)) + '\\'
    return str_folderRaw


#-----------------------------------------------------------------
# Download Files Functions
#-----------------------------------------------------------------
def fStr_UploadFromParam(str_perimeter, str_folderRoot, dte_date, bl_download = False):
    # Upload Files
    try:
        print('============= ' +  str_perimeter + ' =============')
        # Init
        str_return = Initt(str(dte_date))
        # From CSV Parameters
        try: df_Param = pd.read_csv('LaPerouse_Param.csv')
        except: print(' ERROR: Cannot read LaPerouse_Param')
        df_Param.fillna(value = '', inplace = True)
        df_Param = df_Param.loc[df_Param['Perimeter'] == str_perimeter]
        
        # Make the Upload
        for i, row in enumerate(df_Param.index):
            # Path
            str_ID = str(df_Param.loc[row, 'ID'])
            str_FileName = fStr_generateFileName(df_Param, row, dte_date)
            str_folder = fStr_generateFolder(df_Param, row, str_folderRoot, dte_date)            
            bl_success = Act_UpFiles_FTP(df_Param, row, str_folder, str_FileName, dte_date, bl_download)
            #bl_success = Act_UpFiles(df_Param, row, str_folder, str_FileName, dte_date, str_folderRoot)
            if not bl_success:      
                str_return += 'ERROR: Upload did not work for : {}'.format(str_ID)        
    except: 
        print(' ERROR: Upload files: fStr_UploadFromParam')
        print('str_folderRoot: ', str_folderRoot)
        print(str_perimeter, dte_date)
        raise
    return str_return
    

#-----------------------------------------------------------------
# List Files in FTP
#-----------------------------------------------------------------
def fL_FileInFtp(str_FileUploadMode, str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder):
    if str_FileUploadMode == 'FTP':
        l_nameFiles = ftp.ftp_listFolder(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder) 
    elif str_FileUploadMode == 'FTP_SSL':
        l_nameFiles = ftp.ftp_listFolder(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, -1, True)
    elif str_FileUploadMode == 'SFTP_Paramiko':
        l_nameFiles = ftp.ssh_listFilesInFolder(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder)
    return l_nameFiles


#-----------------------------------------------------------------
# Entrance Function for UPLOADING
#-----------------------------------------------------------------
def fStr_Upload_LaPerouse(str_perimeter, str_folderRoot, dte_date, bl_download = False):
    # Param
    if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
    
    str_return = fStr_UploadFromParam(str_perimeter, str_folderRoot, dte_date, bl_download)
    if not str_return:
        str_return = ' ERROR: ' + str_perimeter + ' did not run correctly'
        print(str_return)
    return str_return
    



#-----------------------------------------------------------------
# Entrance Function for List Files
#-----------------------------------------------------------------
def fL_ListFilesFTP(str_perimeter, str_folderRoot, dte_date):
    # Param
    if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
    l_ListFilesFolder = []
    l_ListFilesFTP = []
    str_errorReport = ''
    d_FileInFTP = {}
    #    print('d_FileInFTP shoud be empty: ', d_FileInFTP)
    
    # From CSV Parameters
    try: df_Param = pd.read_csv('LaPerouse_Param.csv')
    except: str_errorReport = ' ERROR: Cannot read LaPerouse_Param'
    df_Param.fillna(value = '', inplace = True)
    df_Param = df_Param.loc[df_Param['Perimeter'] == str_perimeter]
    if df_Param.index.empty: str_errorReport = ' ERROR: LaPerouse_Param is empty for the perimeter: ' + str_perimeter
    
    # Loop on them
    for i, row in enumerate(df_Param.index):     
        # Param
        str_FileName = fStr_generateFileName(df_Param, row, dte_date)
        str_folder = fStr_generateFolder(df_Param, row, str_folderRoot, dte_date)
        str_FileUploadMode = str(df_Param.loc[row, 'FileUploadMode'])
        str_FTP_server = str(df_Param.loc[row, 'FTP_server'])
        str_FTP_uid = str(df_Param.loc[row, 'FTP_uid'])
        str_FTP_pwd = str(df_Param.loc[row, 'FTP_pwd'])
        str_FTP_directory = str(df_Param.loc[row, 'FTP_directory'])
        
        #Test if they are in the folder
        try:
            if str_FileName in fl.fList_FileInDir(str_folder):
                l_ListFilesFolder.append('OK : ' + str_FileName)
            else:
                l_ListFilesFolder.append('KO : ' + str_FileName)
        except:
            str_errorReport += '\n  ERROR: Cannot Connect to the Folder: ' + str_folder
            l_ListFilesFolder.append('NA : ' + str_FileName)
        
        # Get folder FTP
        l_ftpFolder = str_FTP_directory.split('/')
        if l_ftpFolder[0] == '': l_ftpFolder = l_ftpFolder[1:]
        elif l_ftpFolder[0] == 'nan': l_ftpFolder = []	            
        
        # Detect if the Files in FTP
        try:
            # Put in dictionary to avoid multiple request
            if (str_FileUploadMode, str_FTP_server, str_FTP_uid, str_FTP_pwd, '/'.join(l_ftpFolder)) in d_FileInFTP:
                l_fileInFtp = d_FileInFTP[(str_FileUploadMode, str_FTP_server, str_FTP_uid, str_FTP_pwd, '/'.join(l_ftpFolder))]
            else:
                l_fileInFtp = fL_FileInFtp(str_FileUploadMode, str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder)
                d_FileInFTP[(str_FileUploadMode, str_FTP_server, str_FTP_uid, str_FTP_pwd, '/'.join(l_ftpFolder))] = l_fileInFtp
            # File in the List on files in FTP
            if l_fileInFtp == ['ERROR: Cannot Connect to the FTP']:
                l_ListFilesFTP.append('NA : ' + str_FileName)
            elif str_FileName in l_fileInFtp:
                l_ListFilesFTP.append('OK : ' + str_FileName)
            else:
                l_ListFilesFTP.append('KO : ' + str_FileName)
                try:    print(l_fileInFtp[5])
                except: pass
        except:
            str_errorReport += '\n  ERROR: Cannot Connect to the FTP'
            l_ListFilesFTP.append('NA : ' + str_FileName)
            d_FileInFTP[(str_FileUploadMode, str_FTP_server, str_FTP_uid, str_FTP_pwd, '/'.join(l_ftpFolder))] = ['ERROR: Cannot Connect to the FTP']
    
    # Delete the Dico
    d_FileInFTP.clear()
    
    return str_errorReport, l_ListFilesFolder, l_ListFilesFTP
    

#str_perimeter = "BS_ASX"
#str_folderRoot = "\\\\uk-pdeqtfs01\\E\\Data\\Lucerne\\Data\\SOLA PCF\\Auto_Py\\"
#dte_date = dt.datetime.now().date()
#
#print(fL_ListFilesFTP(str_perimeter, str_folderRoot, dte_date))


#d = {}
#if (1,1,'/'.join(['0','1'])) in d:
#    print(1)
#else:
#    print(0)
#d[(1,1,'/'.join(['0','1']))] = 0
#if (1,1,'/'.join(['0','1'])) in d:
#    print(1)
#else:
#    print(0)




