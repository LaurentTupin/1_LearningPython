import pandas as pd
import sys
import os
import shutil
from pandas.tseries.offsets import BDay
import xlsxwriter
sys.path.append('../')
import fct_DB as db
import fct_Files as fl
import fct_outlook as out
import fct_Ftp as ftp
import fct_Date as dat
import fct_html as html


#-----------------------------------------------------------------
# Variables
#-----------------------------------------------------------------
str_dbAmundi = 'StagingDataFile'
str_dbSolaQC = 'SolaQC'
str_outlookAcc = 'sola@ihsmarkit.com'
str_outlookMailbox = 'Inbox'
str_outlookFolderToLookFor = 'PCF-Received'
str_outlookFolderToArchive = 'PCF-Treated'
str_from = 'Markit ETF Management'
#str_from = 'Markit.ETFManagement@ihsmarkit.com'
str_message = "Hello all, \r\n \r\n" +  \
            "Please find the files for today.\r\n" +  \
            "Please send any questions or feedback to DeltaOneSupport@ihsmarkit.com \r\n" +  \
            "Regards, \r\n \r\n" +  \
            "Markit ETF Management"


#-----------------------------------------------------------------
# Messages for the user to have information
#-----------------------------------------------------------------
def Initt(str_date = ''):
    str_return = '------------------------------------------------'
    str_return += '\n' + 'Today is : ' + str_date
    str_return += '\n' + '------------------------------------------------'
    return str_return


#-----------------------------------------------------------------
# Functions
#-----------------------------------------------------------------
def fBl_createFolder(str_folder):
    str_folderShortName = '\\' + '\\'.join(str_folder.split('\\')[-5:])
    bl_success = fl.act_createDir(str_folder, str_folderShortName)
    return bl_success


def fL_CreateTxtFile_RetunPath(str_pathPcf, l_pcfFileName, df_data, bl_header = False, str_sep = ','):
    try:
        l_pathPcf = [str_pathPcf + file for file in l_pcfFileName]
        for str_Pcf in l_pathPcf:
            df_data.to_csv(str_Pcf, index = False, header = bl_header, sep = str_sep) 
#            #For Amundi 
#            if 'PCFMKTN' in str_Pcf:
#                df_data.to_csv(str_Pcf.replace('PCFMKTN', 'PCFMKTN_2'), index=False, header = None, sep='\t')
    except:
        print('  ERROR: Could not create the file: ')
        print('  str_pathPcf :',str_pathPcf, 'l_pcfFileName :', l_pcfFileName, 'bl_header :',  bl_header)
        return False
    return l_pathPcf


def fL_createExcel_RetunPath(str_pathPcf, l_pcfFileName, df_data, bl_header = False, str_SheetName = ''):
    try:
        l_pathPcf = [str_pathPcf + file for file in l_pcfFileName]
        for str_Pcf in l_pathPcf:
            # Create the file (xlsxwriter cannot modify files)
            xlWb = xlsxwriter.Workbook(str_Pcf)
            #Sheet Name
            if str_SheetName == '': xlWs = xlWb.add_worksheet()                
            else: xlWs = xlWb.add_worksheet(str_SheetName)
            # fill in
            for i, row in enumerate(df_data.index):
                for j, col in enumerate(df_data.columns):
                    xlWs.write(i, j, str(df_data.iat[i, j]))
                    #xlWs.Cells(i+1, j+1).Value = str(df_data.iat[i, j])
        xlWb.close()
    except:
        try: xlWb.close()
        except: print('Could not close the file')
        print('  ERROR: fL_createExcel_RetunPath did not work ')
        print(str_pathPcf, l_pcfFileName)
        print('str_SheetName: ', str_SheetName)
        return False
    return l_pathPcf



#-----------------------------------------------------------------
# Main Function to download
#-----------------------------------------------------------------
def Act_DownFiles_outlook(df_Param, row, str_folderRaw, str_FileName, bl_ArchiveMails):
    # Param
    str_outlook_Acct = str(df_Param.loc[row, 'outlook_Acct'])
    str_outlook_mailBox = str(df_Param.loc[row, 'outlook_mailBox'])
    str_outlook_folder = str(df_Param.loc[row, 'outlook_folder'])
    str_outlook_folderToArchive = str(df_Param.loc[row, 'outlook_folderToArchive'])
    str_outlook_subject = str(df_Param.loc[row, 'outlook_subject'])
    str_outlook_fileType = str(df_Param.loc[row, 'outlook_fileType'])
    str_outlook_fileNameCheck = str(df_Param.loc[row, 'outlook_fileNameCheck'])
    str_to = str(df_Param.loc[row, 'outlook_To'])
    str_cc = str(df_Param.loc[row, 'outlook_Cc'])
    l_files = []
	
    # Get Mails
    o_mails, o_folderToMove = out.fMail_getMails(str_outlook_Acct, str_outlook_mailBox, str_outlook_folder, str_outlook_folderToArchive)
    if o_mails == False: 
        print(' EMPTY: Cannot Get Mails')
        print(' ', str_outlook_Acct, str_outlook_mailBox, str_outlook_folder, str_outlook_folderToArchive)
        return False
    # Filter on Subject and take most Recent mail
    if str_outlook_fileNameCheck.lower() == 'true': 
        l_mail = out.fMail_getmail_mostRecent(o_mails, [str_outlook_subject], str_to, str_cc, str_FileName)
    else: l_mail = out.fMail_getmail_mostRecent(o_mails, [str_outlook_subject], str_to, str_cc)
    
    #==============================================================================================
    # If the Mail cannot be found, We search in Inbox and Archive in the right folder to move it
    if l_mail == False and str_outlook_folder!= '' :
        print(' EMPTY: Cannot Get Most Recent Mails')
        print(' EMPTY: We will search in MailBox: #', str_outlook_mailBox, '#')
        bl_ArchiveMails = True
        str_outlook_folderToArchive = str_outlook_folder
        str_outlook_folder = ''
        # Get Mails
        o_mails, o_folderToMove = out.fMail_getMails(str_outlook_Acct, str_outlook_mailBox, str_outlook_folder, str_outlook_folderToArchive)
        # Filter on Subject and take most Recent mail
        if str_outlook_fileNameCheck.lower() == 'true': 
            l_mail = out.fMail_getmail_mostRecent(o_mails, [str_outlook_subject], str_to, str_cc, str_FileName)
        else: l_mail = out.fMail_getmail_mostRecent(o_mails, [str_outlook_subject], str_to, str_cc)       
    #==============================================================================================
    
    if l_mail == False: 
        print(' EMPTY: Cannot Get Most Recent Mails')
        print(' ', o_mails)
        return False
    # Download PJ
    l_files = out.fBl_downMailAttch(str_folderRaw, l_mail, [str_outlook_fileType])
    while not l_files:
        print(' EMPTY: Cannot download Attach from mail')
        print(' Archiving Mail without Attachement')
        # Archive the wrong Mail
        out.fBl_archiveMail(l_mail, o_folderToMove)
        # Filter on Subject and take most Recent mail
        l_mail = out.fMail_getmail_mostRecent(o_mails, [str_outlook_subject], str_to, str_cc)
        if l_mail == False: 
            print(' EMPTY: Cannot download Attach from mail')
            print(' Mail Subject: ' + str_outlook_subject)
            print(' Folder: ' + str_outlook_folder)
            return False
        else:
            print(' We now consider a new Mail: ', l_mail[0].Subject)
            print(' Attachements: ' + ' | '.join([str(o_attach) for o_attach in l_mail[0].Attachments]))
        l_files = out.fBl_downMailAttch(str_folderRaw, l_mail, [str_outlook_fileType])
        if l_files: print(' SUCCESS: We found a Mail with the Attach including: ', str_outlook_subject, str_outlook_fileType)
    # Rename the file - RENAMING
    if not str_outlook_fileNameCheck.lower() == 'true':
        str_file = str(l_files[0])
        fl.Act_Rename(str_folderRaw, str_file, str_FileName)
    # Archive PJ
    if bl_ArchiveMails:
        bl_success = out.fBl_archiveMail(l_mail, o_folderToMove)
        if not bl_success: print('Cannot Archive mail')
    return True

#------------------------------------------------------------------------------------------------------------------------------------   
def Act_DownFiles_FTP(df_Param, row, str_folderRaw, str_FileName, str_FileDownloadMode, dte_date):
    # Param
    str_PCF = str(df_Param.loc[row, 'PCF'])
    str_DateOffset = str(df_Param.loc[row, 'DateOffset'])
    str_fileDate = str(df_Param.loc[row, 'fileDate'])
    str_FTP_server = str(df_Param.loc[row, 'FTP_server'])
    str_FTP_uid = str(df_Param.loc[row, 'FTP_uid'])
    str_FTP_pwd = str(df_Param.loc[row, 'FTP_pwd'])
    str_FTP_directory = str(df_Param.loc[row, 'FTP_directory'])
    str_FTP_exactName = str(df_Param.loc[row, 'FTP_exactName'])
    
    # Get folder
    l_ftpFolder = str_FTP_directory.split('/')
    if l_ftpFolder[0] == '': l_ftpFolder = l_ftpFolder[1:]
    elif l_ftpFolder[0] == 'nan': l_ftpFolder = []	
    # Download
    try: 
        if str_FileDownloadMode == 'FTP':
            ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folderRaw)
        elif str_FileDownloadMode == 'SFTP_Paramiko':
            ftp.ssh_downFile(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folderRaw)
    except:
        if not str_FTP_exactName.lower() == 'true':
            int_DateOffset = int(str_DateOffset) - 1
            print('  ' + str_FileDownloadMode + ' did not find the file: ')
            print('  ' + str_FileName)
            print('  PCF: ' + str_PCF)
            print('  Download mode: ' + str_FileDownloadMode)
            print('  Offset was: ' + str_DateOffset + ' | And is now: ' + str(int_DateOffset))
            str_FileName = df_Param.loc[row, 'fileName'].replace('{fileDate}', (dte_date-BDay(-int_DateOffset)).strftime(str_fileDate))
            df_Param.loc[(df_Param.PCF == str_PCF) & (df_Param.FileDownloadMode == str_FileDownloadMode),'DateOffset'] = df_Param['DateOffset'] - 1
            #df_Param.loc[(df_Param.PCF==str_PCF) & (df_Param.FileDownloadMode==str_FileDownloadMode),'DateOffset'].apply(lambda x: x-1)
            try:
                if str_FileDownloadMode == 'FTP':
                    ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folderRaw)
                    print('   File Successfully downloaded... ' + str_FileName)
                elif str_FileDownloadMode == 'SFTP_Paramiko':
                    ftp.ssh_downFile(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folderRaw)				
                    print('   File Successfully downloaded... ' + str_FileName)
            except: 
                print('     ERROR: We could not download from ' + str_FileDownloadMode)
                print(str_FTP_server, str_FTP_uid, str_FTP_pwd)			
                print(l_ftpFolder)
                print(str_FileName)
                print(str_folderRaw)
                return False
        else: 
            print('     ERROR: We could not download from ' + str_FileDownloadMode)
            print(str_FTP_server, str_FTP_uid, str_FTP_pwd)			
            print(l_ftpFolder)
            print(str_FileName)
            print(str_folderRaw)
            return False
    return True

#------------------------------------------------------------------------------------------------------------------------------------   
def Act_DownFiles_SQL(df_Param, row, str_folderRaw, str_FileName, str_FileDownloadMode, dte_date):
    # Param
    str_PCF = str(df_Param.loc[row, 'PCF'])
    str_req = fStr_generateSQLReq(df_Param, row, dte_date)
    # Execute Req
    try:
        df_sql = db.db_SelectReq(str_req)
    except:
        print('     ERROR in Act_DownFiles_SQL: We could not execute the SQL in PCF: ', str_PCF)
        print(str_req)
        return False
    # Save in  the folder
    try:
        str_Path = os.path.join(str_folderRaw, str_FileName)
        df_sql.to_csv(str_Path, index = False, header = True)
    except:
        print('     ERROR in Act_DownFiles_SQL: We could not save the DF in PCF: ', str_PCF)
        print('     ', str_Path)
        return False
    return True
	
	
#------------------------------------------------------------------------------------------------------------------------------------			
def Act_DownFiles(df_Param, row, str_folderRaw, str_FileName, dte_date, str_folderRoot, bl_ArchiveMails):
    try:
        # Param
        str_File_PrefixName = str(df_Param.loc[row, 'File_PrefixName'])
        str_FileDownloadMode = str(df_Param.loc[row, 'FileDownloadMode'])
        str_DateOffset = str(df_Param.loc[row, 'DateOffset'])
        str_fileDate = str(df_Param.loc[row, 'fileDate'])
        str_url = str(df_Param.loc[row, 'URL'])
        str_url = str_url.replace('{fileDate}', (dte_date-BDay(-int(str_DateOffset))).strftime(str_fileDate))
        str_url_keyword = str(df_Param.loc[row, 'url_keyword'])
        str_SheetName = str(df_Param.loc[row, 'SheetName'])
        # Outlook
        if str_FileDownloadMode == 'OUTLOOK':
            bl_success = Act_DownFiles_outlook(df_Param, row, str_folderRaw, str_FileName, bl_ArchiveMails)
            if not bl_success: 
                return False
        # Folder
        elif str_FileDownloadMode == 'FOLDER':
            try:
                str_pathSource = df_Param.loc[row, 'Dir_Source'].replace('{folderDate}', 
                                             (dte_date-BDay(-int(df_Param.loc[row, 'DateOffset']))).strftime(df_Param.loc[row, 'folderDate']))
                if not str_pathSource[:2] == '\\\\': str_pathSource = str_folderRoot + str_pathSource 
                # Copy
                shutil.copy(os.path.join(str_pathSource, str_FileName), os.path.join(str_folderRaw, str_FileName))
                os.path.join(str_folderRaw, str_FileName)
            except:
                print('   ERROR in Act_DownFiles: shutil.copy did not work')
                print('   str_pathSource: ', str_pathSource)
                print('   str_FileName: ', str_FileName)
                return False
        # FTP
        elif str_FileDownloadMode == 'FTP':
            bl_success = Act_DownFiles_FTP(df_Param, row, str_folderRaw, str_FileName, str_FileDownloadMode, dte_date)
            if not bl_success: return False
        # FTP paramiko
        elif str_FileDownloadMode == 'SFTP_Paramiko':
            bl_success = Act_DownFiles_FTP(df_Param, row, str_folderRaw, str_FileName, str_FileDownloadMode, dte_date)
            if not bl_success: return False
        # SQL
        elif str_FileDownloadMode == 'SQL':
            bl_success = Act_DownFiles_SQL(df_Param, row, str_folderRaw, str_FileName, str_FileDownloadMode, dte_date)
            if not bl_success: return False        
        # HTML
        elif str_FileDownloadMode == 'HTML_JSON':
            df_fut = html.fDf_htmlGetArray_json(str_url, str_url_keyword)
            fL_CreateTxtFile_RetunPath(str_folderRaw, [str_FileName], df_fut, True)
        elif str_FileDownloadMode == 'HTML_SOUP':
            df_result = html.fDf_htmlGetArray_Soup(str_url)
            df_result.fillna(value = '', inplace = True)
            df_result.loc[0, 2] = ''            
            fL_createExcel_RetunPath(str_folderRaw, [str_FileName], df_result, False, str_SheetName)    
        # Renaming the INPUT Files
        if not str_File_PrefixName == '':
            try: fl.Act_Rename(str_folderRaw, str_FileName, str_File_PrefixName + str_FileName)
            except: print(' ERROR: Act_Rename')
    except: 
        print(' ERROR: Act_DownFiles')
        return False
    return True
	
#------------------------------------------------------------------------------------------------------------------------------------
def fDf_getDfFromDownloaded(df_Param, row, str_folderRaw, str_FileName, bl_header = 0):
    try:
        # Renaming the INPUT Files
        str_File_PrefixName = str(df_Param.loc[row, 'File_PrefixName'])
        if not str_File_PrefixName == '': str_FileName = str_File_PrefixName + str_FileName
    except: print('  Renaming did not work OR it is comparing Prod files')
    try:        
        # ------- XLSX -------
        if '.XLSX' in str_FileName.upper() or '.XLS' in str_FileName.upper():
            if 'LAST-VALUATION-MARKIT' in str_FileName.upper():
                df_data = pd.read_excel(str_folderRaw + str_FileName, header = 3)
            else:
                df_data = pd.read_excel(str_folderRaw + str_FileName, header = bl_header)
        # ------- HDX -------
        elif '.HDX' in str_FileName.upper():
            if '_SPGSCI_FIN_STD' in str_FileName.upper() :
                df_data = pd.read_csv(str_folderRaw + str_FileName, header = 1, sep='\t')
            else:
                print(' HDX: Case not taken into account')
                return None
        # ------- CSV -------
        elif '.CSV' in str_FileName.upper():
            if 'GMO' in str_FileName.upper() or 'fcnacl2v' in str_FileName.lower() or 'fdccc' in str_FileName.lower() \
            or 'fdcco' in str_FileName.lower() or 'navau' in str_FileName.lower():
                df_data = pd.read_csv(str_folderRaw + str_FileName, header = 2)
                # If it has been opened manually, it should take the 4th row
                l_colUnamed = ['Unnamed' for colName in df_data.columns if 'Unnamed' in colName]
                if l_colUnamed:
                    print(df_data.iloc[0:4, 0:3])
                    df_data = pd.read_csv(str_folderRaw + str_FileName, header = 3)
                    print('-------- After, header on 4th row ---------')
                    print(df_data.iloc[0:4, 0:3])
                # GMO treat
                if 'GMO' in str_FileName.upper():
                    df_data.dropna(axis = 'index', subset = ['ISIN'], inplace = True)
            else:
                df_data = pd.read_csv(str_folderRaw + str_FileName, header = bl_header)
        # ------- TXT -------
        elif '.TXT' in str_FileName.upper():
            if 'ELQC' in str_FileName.upper() or 'GOMA' in str_FileName.upper() \
            or 'PCFGSCE' in str_FileName.upper() or 'PCFGSCU' in str_FileName.upper() \
            or 'COGSDE_GSCE_' in str_FileName.upper() or 'COGSCU' in str_FileName.upper():
                df_data = pd.read_csv(str_folderRaw + str_FileName, header = bl_header, sep='\t')
            else:
                df_data = pd.read_csv(str_folderRaw + str_FileName, header = bl_header)
        else:
            print('** No files to look for...')
            print('---------------------------')
            df_data = 1
    except:
        print('   ERROR in fDf_getDfFromDownloaded : df_data could not be read: ' + str_FileName)
        return None
    return df_data


#------------------------------------------------------------------------------------------------------------------------------------
def fStr_generateFileName(df_Param, row, dte_date):
    str_fileName = str(df_Param.loc[row, 'fileName'])
    str_DateOffset = str(df_Param.loc[row, 'DateOffset'])
    str_fileDate = str(df_Param.loc[row, 'fileDate'])
    str_NewDate = (dte_date + BDay(int(str_DateOffset))).strftime(str_fileDate)
    str_fileName = str_fileName.replace('{fileDate}', str_NewDate)
    return str_fileName
def fStr_generateFolderRaw(df_Param, row, str_folderRoot, dte_date):
    str_Dir_Dest = str(df_Param.loc[row, 'Dir_Dest'])
    str_folderDateOffset = str(df_Param.loc[row, 'folderDateOffset'])
    str_folderDate = str(df_Param.loc[row, 'folderDate'])
    if str_Dir_Dest[:2] == '\\\\':
        #str_folderRaw = str_Dir_Dest.replace('{folderDate}', dte_date.strftime(str_folderDate)) + '\\'
        str_folderRaw = str_Dir_Dest.replace('{folderDate}', (dte_date + BDay(int(str_folderDateOffset))).strftime(str_folderDate)) + '\\'
    else:
        str_folderRaw = str_folderRoot + str_Dir_Dest.replace('{folderDate}', (dte_date + BDay(int(str_folderDateOffset))).strftime(str_folderDate)) + '\\'
    return str_folderRaw
def fStr_generateSQLReq(df_Param, row, dte_date):
    try:
        str_sqlReq = str(df_Param.loc[row, 'sqlReq'])
        str_sqlDateOffset = str(df_Param.loc[row, 'sqlDateOffset'])
        str_sqlDateFormat = str(df_Param.loc[row, 'sqlDateFormat'])
        str_sqlDateOffsetType = str(df_Param.loc[row, 'sqlDateOffsetType'])
        # Condition to offset the date and input into the QL req
        if str_sqlDateOffsetType == 'Month': 
            dte_NewDate = dat.fDte_AddMonth(dte_date, int(str_sqlDateOffset))
        else: 
            dte_NewDate = dte_date + BDay(int(str_sqlDateOffset))
        str_NewDate = dte_NewDate.strftime(str_sqlDateFormat).upper()
        str_sqlReq = str_sqlReq.replace('{sql_Date}', str_NewDate)
    except: print(' ERROR in fStr_generateSQLReq: str_sqlDateOffset might not be a number, try to fill the column in the CSV with 0 to make it a number column')
    return str_sqlReq


#------------------------------------------------------------------------------------------------------------------------------------	
def fDic_pcfAutomate_GetFiles2(df_Param, str_folderRoot, dte_date, bl_ArchiveMails, bl_dfRequired = True, bl_forceDwld = False):
    # Take parameters from CSV
    d_result = {}
    l_PathOutput = []
    bl_dwlFailed = False
    for i, row in enumerate(df_Param.index):
        # Path
        str_ID = str(df_Param.loc[row, 'ID'])
        str_FileName = fStr_generateFileName(df_Param, row, dte_date)
        str_folderRaw = fStr_generateFolderRaw(df_Param, row, str_folderRoot, dte_date)
        # Create the folder
        if not fBl_createFolder(str_folderRaw): 
            return 'ERROR: Could not Create Folder: ' + str_folderRaw, []
        
        # Try to get the data from files already dwld - (Add DATAFRAME in the dictionary)
        bl_forceDwld_local = bl_forceDwld
        if not bl_forceDwld_local:
            print('Searching for... ' + str_FileName)
            df_data = fDf_getDfFromDownloaded(df_Param, row, str_folderRaw, str_FileName)
            if df_data is None: bl_forceDwld_local = True
            else: d_result[str_ID] = df_data
        # Download
        if bl_forceDwld_local:
            print('Downloading... ' + str_FileName)
            bl_success = Act_DownFiles(df_Param, row, str_folderRaw, str_FileName, dte_date, str_folderRoot, bl_ArchiveMails)
            if not bl_success:
                bl_dwlFailed = True
                continue
            else:
                # In case of download files before, we need to update fileName
                str_FileName = fStr_generateFileName(df_Param, row, dte_date)
        # Get the data from files dwld - (Add DATAFRAME in the dictionary)
        if bl_forceDwld_local and bl_dfRequired:
            print('Searching again for... ' + str_FileName)
            df_data = fDf_getDfFromDownloaded(df_Param, row, str_folderRaw, str_FileName)
            if df_data is None: 
                bl_dwlFailed = True
                continue
            d_result[str_ID] = df_data
			
        #Add the folder for information || Careful, takes only the last one
        d_result['Folder'] = str_folderRaw.replace('\\raw','')
        l_PathOutput.append(str_folderRaw + str_FileName)
    # End of loop - Add Path of files downloaded
    d_result['files'] = l_PathOutput 
    
    if bl_dwlFailed: return False
    elif bl_dfRequired: return d_result
    else: return d_result

