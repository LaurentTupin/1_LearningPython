import pandas as pd
import sys
import os
import shutil
import time
from pandas.tseries.offsets import BDay
import win32com.client as win32
sys.path.append('../')
import fct_DB as db
import fct_Files as fl
import fct_outlook as out
import fct_Ftp as ftp
import fct_Date as dat
import fct_html as html
import fct_dataframe as dframe


#-----------------------------------------------------------------
# Variables
#-----------------------------------------------------------------
str_NewFileName = ''
str_dbAmundi = 'StagingDataFile'
str_dbSolaQC = 'SolaQC'
str_outlookAcc = 'sola@ihsmarkit.com'
str_outlookMailbox = 'Inbox'
str_outlookFolderToLookFor = 'PCF-Received'
str_outlookFolderToArchive = 'PCF-Treated'
#str_from = 'Markit ETF Management'
#str_from = 'Markit.ETFManagement@ihsmarkit.com'
str_from = ''
str_message = "Hello all, \r\n \r\n" +  \
            "Please find the files for today.\r\n" +  \
            "Please send any questions or feedback to DeltaOneSupport@ihsmarkit.com \r\n" +  \
            "Regards, \r\n \r\n" +  \
            "Markit ETF Management"


#-----------------------------------------------------------------
# Messages for the user to have information
#-----------------------------------------------------------------
def Initt(str_date = ''):
    str_return = '\n' + '------------------------------------------------'
    str_return += '\n' + 'Today is : ' + str_date
    str_return += '\n' + '------------------------------------------------'
    return str_return

#-----------------------------------------------------------------
# Compare files
#-----------------------------------------------------------------
    #def fdf_fileInDf(str_link):
    #    if '.xls' in str_link.split('\\')[-1]:
    #        df = pd.read_excel(str_link, sheet_name='Sheet1', header = None)
    #    else: df = pd.read_csv(str_link, header = None)
    #    return df
def fdf_compare2files(str_link1, str_link2, i_colToKeep = 0, v_sheetName = ''):
    bl_header = None
    
    if v_sheetName != '':
        df1 = fDf_getDfFromPCF(None, 0, '', str_link1, bl_header, v_sheetName)
        df2 = fDf_getDfFromPCF(None, 0, '', str_link2, bl_header, v_sheetName)
    else:
        df1 = fDf_getDfFromPCF(None, 0, '', str_link1, bl_header)
        df2 = fDf_getDfFromPCF(None, 0, '', str_link2, bl_header)
        # case of Text with Tabulator Sep...
        if '.txt' == str_link1[-4:] and len(df1.columns) == 1 and len(df2.columns) == 1:
            print(' WARNING: df had only 1 column, therefore, we will read the txt file with Sep = TAB')
            df1 = fDf_getDfFromPCF(None, 0, '', str_link1, bl_header, str_sep = '\t')
            df2 = fDf_getDfFromPCF(None, 0, '', str_link2, bl_header, str_sep = '\t')
            
    # FILL NA
    df1.fillna(value = '', inplace = True)
    df2.fillna(value = '', inplace = True)
    
    # Loop to put to void the same value
    df = df1
    int_df1NbRows = len(df.index)
    #int_df1NbCol = len(df.columns)
    int_df2NbRows = len(df2.index)
    int_df2NbCol = len(df2.columns)
    int_diffCount = 0
        
    for i_row, t_row in df1.iterrows():
        i_col = 0
        for value in t_row:
            # Keep the value of ID column
            if i_col == i_colToKeep:
                val = df.loc[i_row, i_col]
            
            # df1 is bigger than df2
            if i_row >= int_df2NbRows or i_col >= int_df2NbCol:
                df.loc[i_row, i_col] = str(df1.loc[i_row, i_col]) + ' || '
            # Same
            elif(df1.loc[i_row, i_col] == df2.loc[i_row, i_col]):
                df.loc[i_row, i_col] = ''
            # Remove NaN (null) and when its the same btw 2 df
            elif str(df1.loc[i_row, i_col]) == 'nan' and str(df2.loc[i_row, i_col]) == 'nan':
                df.loc[i_row, i_col] = ''
            # Difference
            else:
                try:
                    bl_ColToKeep = True
                    diff = float(df1.loc[i_row, i_col]) - float(df2.loc[i_row, i_col])
                    diffPourc = 100 * (diff / float(df2.loc[i_row, i_col]))
                    
                    # If difference is very small (to avoid rounding too small)
                    if abs(diff) < 0.001 and abs(diffPourc) < 0.001:
                        df.loc[i_row, i_col] = ''
                        bl_ColToKeep = False
                    else:
                        df.loc[i_row, i_col] = str(df1.loc[i_row, i_col]) + ' || ' + str(df2.loc[i_row, i_col]) \
                                            + ' | Diff: ' + str(round(diff,1)) + ' | Diff%: ' + str(round(diffPourc, 2))
                except:
                    df.loc[i_row, i_col] = str(df1.loc[i_row, i_col]) + ' || ' + str(df2.loc[i_row, i_col])                    
                
                # Keep the value of ID column
                if bl_ColToKeep and i_col > i_colToKeep:
                    int_diffCount += 1
                    df.loc[i_row, i_colToKeep] = val
            # End LOOP
            i_col += 1
    
    if int_df1NbRows < int_df2NbRows:
        for i_row in range(int_df1NbRows, int_df2NbRows):
            df.loc[i_row] = df2.loc[i_row].apply(lambda x: 'pty | {}'.format(str(x)))
            
    #    # 1. Remove rows which are exactly the same
    #    dfs_dictionary = {'DF1':df1,'DF2':df2}
    #    df = pd.concat(dfs_dictionary)
    #    df.drop_duplicates(keep=False, inplace = True)    
    #    # 2. Remove Void Rows & Columns
    #    df.dropna(how='all', inplace = True)
    #    df.dropna(axis='columns', how='all', inplace = True)
    
    return df, int_diffCount



#====================================================================================================
# SEND MAILS / FTP - Detailed Function
#====================================================================================================

#-----------------------------------------------------------------
# Send PCF by FTP
#-----------------------------------------------------------------
def pcf_sendFTP(dte_date, l_pathAttach, str_pcf):
    # From CSV Parameters
    try:
        df_Param = pd.read_csv('Seita_Param_Mail.csv')
        df_Param = df_Param.loc[df_Param['Perimeter'] == str_pcf]
        df_Param = df_Param.loc[df_Param['Type'] == 'FTP']
        df_Param.fillna('', inplace = True)
        if df_Param.empty:          return False, []
    except: 
        print(' ERROR pcf_sendFTP: Cannot read Seita_Param_Mail.csv')
        return False, []
    # LOOP on different Mail
    bl_success_final = True
    for x_FTP in df_Param['ID_Mail'].unique():
        df_FTP = df_Param.loc[df_Param['ID_Mail'] == x_FTP]
        # Files List
        try:
            df_filesList = df_FTP.loc[df_FTP['Field'] == 'FileNameInclude']
            if df_filesList.empty:     return False, []
            # Filter to compare with what has been selected
            l_pathAttach_Part = []
            for x_fileName in df_filesList['str_Value'].unique():
                str_fileName = str(x_fileName)
                str_DateFormat = df_filesList.loc[df_filesList['str_Value'] == x_fileName, 'str_DateFormat'].values[0]
                if not str_fileName == '':
                    if not str_DateFormat == '':    
                        str_fileName = str_fileName.replace('<DateFormat>', dte_date.strftime(str_DateFormat))
                    # Mettre les PJ en liste
                    l_pathAttach_Part += [path for path in l_pathAttach if str_fileName.upper() in path.upper()]
        except: 
            print(' ERROR: pcf_sendFTP: Files List')
            print(' - str_pcf: ', str_pcf, ' | dte_date: ', dte_date)
            print(' - x_FTP: ', x_FTP)
            print(' - df_FTP: ', df_FTP.head(2))
            return False, []
        # Other FTP Param
        try:
            # FTP Param
            str_FileUploadMode =    df_FTP.loc[df_FTP['Field'] == 'FileUploadMode', 'str_Value'].values[0]
            str_FTP_server =        df_FTP.loc[df_FTP['Field'] == 'FTP_server', 'str_Value'].values[0]
            str_FTP_uid =           df_FTP.loc[df_FTP['Field'] == 'FTP_uid', 'str_Value'].values[0]
            str_FTP_pwd =           df_FTP.loc[df_FTP['Field'] == 'FTP_pwd', 'str_Value'].values[0]
            str_FTP_directory =     df_FTP.loc[df_FTP['Field'] == 'FTP_directory', 'str_Value'].values[0]
            # Get folder
            l_ftpFolder = str_FTP_directory.split('/')
            if l_ftpFolder[0] == '': l_ftpFolder = l_ftpFolder[1:]
            elif l_ftpFolder[0] == 'nan': l_ftpFolder = []	
            # Keep only unique PJ
            l_pathAttach_Part = list(set(l_pathAttach_Part))
            if not l_pathAttach_Part:       return False, []
        except: 
            print(' ERROR: pcf_sendFTP: Files List')
            print(' - str_pcf: ', str_pcf, ' | dte_date: ', dte_date)
            print(' - x_FTP: ', x_FTP)
            print(' - df_FTP: ', df_FTP.head(2))
            return False, []
        # FTP Launch - LOOP
        try:
            for Path in l_pathAttach_Part:
                str_FileName = Path.split('\\')[-1]
                str_folder = '\\'.join(Path.split('\\')[:-1])
                if str_FileUploadMode == 'FTP':               
                    bl_success = ftp.fBl_ftpUpFile_Bi(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folder)
                elif str_FileUploadMode == 'FTP_SSL':         
                    bl_success = ftp.fBl_ftpUpFile_Bi(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folder, -1, True)
                elif str_FileUploadMode == 'SFTP_Paramiko':   
                    bl_success = ftp.ssh_upFile(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folder)
                #Store Result
                if not bl_success:          bl_success_final = False
        except:
            print(' ERROR: on UPLOAD file')
            print(' - str_pcf: ', str_pcf, ' | str_FileUploadMode', str_FileUploadMode)
            print(' - str_FileName: ', str_FileName)
        # Search in FTP to return if FIles has been well integrated
        try:
            l_ListFilesFTP = []
            if str_FileUploadMode == 'FTP':               
                l_fileInFtp = ftp.ftp_listFolder(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder)
            elif str_FileUploadMode == 'FTP_SSL':         
                l_fileInFtp = ftp.ftp_listFolder(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, -1, True)
            elif str_FileUploadMode == 'SFTP_Paramiko':   
                l_fileInFtp = ftp.ssh_listFilesInFolder(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder)            
            # LOOP
            for Path in l_pathAttach_Part:
                str_FileName = Path.split('\\')[-1]
                if str_FileName in l_fileInFtp:
                    l_ListFilesFTP.append('OK : {}'.format(str_FileName))
                else:
                    l_ListFilesFTP.append('KO : {}'.format(str_FileName))
        except:
            l_ListFilesFTP.append('NA : Cannot connect to FTP / SFTP')
            print(' ERROR: pcf_sendFTP: List the files')
            print(' - str_pcf: ', str_pcf, ' | dte_date: ', dte_date)
            try:
                print(' - str_FileUploadMode: ', str_FileUploadMode)
                print(' - str_FTP_server: ', str_FTP_server)
                print(' - str_FTP_uid: ', str_FTP_uid)
                print(' - str_FTP_pwd: ', str_FTP_pwd)
                print(' - str_FTP_directory: ', str_FTP_directory)
            except:     pass
    return bl_success_final, l_ListFilesFTP


#-----------------------------------------------------------------
# Send Mails
#-----------------------------------------------------------------
def pcf_sendMail(dte_date, l_pathAttach, str_pcf, str_MailType, bl_draft):
    # From CSV Parameters
    try:
        df_Param = pd.read_csv('Seita_Param_Mail.csv')
        df_Param = df_Param.loc[df_Param['Perimeter'] == str_pcf]
        if '1.' in str_MailType:            df_Param = df_Param.loc[df_Param['Type'] == 'outMail1']
        elif '2.' in str_MailType:          df_Param = df_Param.loc[df_Param['Type'] == 'outMail2_confirm']
        elif '3.' in str_MailType:          df_Param = df_Param.loc[df_Param['Type'] == 'outMail3_LateAlert']
        df_Param.fillna('', inplace = True)
    except: 
        print(' ERROR pcf_sendMail: Cannot read Seita_Param_Mail.csv')
        return False
    # Empty dataframe on perimeter: Send all Path selected before as ATTACH
    try:
        if df_Param.empty:
            bl_success = fBl_sendPcfMail(bl_draft, False, '', '', '', '', l_pathAttach)
            return bl_success
    except: 
        print(' ERROR pcf_sendMail: Send mail with CSV empty')
        print(' - str_pcf: ', str_pcf, ' | dte_date: ', dte_date)
        return False
    # LOOP on different Mail
    bl_success_final = True
    for x_mail in df_Param['ID_Mail'].unique():
        df_Mail = df_Param.loc[df_Param['ID_Mail'] == x_mail]
        # Subject
        try:
            str_DateFormat = df_Mail.loc[df_Mail['Field'] == 'Subject', 'str_DateFormat'].values[0]
            str_subject = df_Mail.loc[df_Mail['Field'] == 'Subject', 'str_Value'].values[0]
            if not str_DateFormat == '' and not str_subject == '': 
                str_subject = str_subject.replace('<DateFormat>', dte_date.strftime(str_DateFormat))
        except:
            print(' ERROR pcf_sendMail: Subject')
            print(' - str_pcf: ', str_pcf, ' | dte_date: ', dte_date)
            print(' - x_mail: ', x_mail)
            print(' - df_Mail: ', df_Mail.head(2))
            return False
        # Attachement
        try:
            df_Attach = df_Mail.loc[df_Mail['Field'] == 'Attachement']
            if not df_Attach.empty:
                l_pathAttach_Part = []
                for x_attach in df_Attach['str_Value'].unique():
                    str_DateFormat = df_Attach.loc[df_Attach['str_Value'] == x_attach, 'str_DateFormat'].values[0]
                    str_Attachement = str(x_attach)
                    if not str_Attachement == '':
                        if not str_DateFormat == '':    str_Attachement = str_Attachement.replace('<DateFormat>', dte_date.strftime(str_DateFormat))
                        # Mettre les PJ en liste
                        l_pathAttach_Part += [attach for attach in l_pathAttach if str_Attachement.upper() in attach.upper()]
            else:   l_pathAttach_Part = l_pathAttach        # Mettre tout si Attach n'est pas precise
        except: 
            print(' ERROR: pcf_sendMail: Attach')
            print(' - str_pcf: ', str_pcf, ' | dte_date: ', dte_date)
            print(' - x_mail: ', x_mail)
            print(' - df_Mail: ', df_Mail.head(2))
            return False
        # Destinataire
        try:
            df_To = df_Mail.loc[df_Mail['Field'] == 'To']
            df_Cc = df_Mail.loc[df_Mail['Field'] == 'Cc']
            df_Bcc = df_Mail.loc[df_Mail['Field'] == 'Bcc']
            str_to = '; '.join(df_To['str_Value'])
            str_cc = '; '.join(df_Cc['str_Value'])
            str_bcc = '; '.join(df_Bcc['str_Value'])
            # Send PCF by Mail
            if l_pathAttach_Part:          # Il faut au moins une PJ (eviter d'ouvrir plein de mails vide alors que user a select UNE PJ)
                # Keep only unique PJ
                l_pathAttach_Part = list(set(l_pathAttach_Part))
                bl_success = fBl_sendPcfMail (bl_draft, False, str_to, str_cc, str_bcc, str_subject, l_pathAttach_Part)
            elif not l_pathAttach and len(df_Param['ID_Mail'].unique()) == 1:              # (A  moins que tout soit vide)
                bl_success = fBl_sendPcfMail (bl_draft, False, str_to, str_cc, str_bcc, str_subject, [])
            #Store Result
            if not bl_success:          bl_success_final = False
        except: 
            print(' ERROR: pcf_sendMail: Final')
            print(' - str_pcf: ', str_pcf, ' | dte_date: ', dte_date)
            try:
                print(' - x_mail: ', x_mail)
                print(' - df_Mail: ', df_Mail.head(2))
                print(' - str_subject: ', str_subject)
                print(' - str_to: ', str_to)
                print(' - str_cc: ', str_cc)
                print(' - str_bcc: ', str_bcc [:20])
                print(' - l_pathAttach: ', l_pathAttach)
            except:     pass
            return False
    return bl_success_final
#___________________________________________________________________________________________









#-----------------------------------------------------------------
# Code Pivot
#-----------------------------------------------------------------
def WisdomTree_GetPivotCode(df_Compo, str_colName, str_folder, str_fileName):
    try:
        # Pivot Code
        l_bbg = df_Compo[str_colName].tolist()
        str_req =  "{0} SELECT Bloomberg AS [{1}], CurrentName, Mic, CurrencyCode, Ric ".format('SET NOCOUNT ON; \n', str_colName)
        str_req += "{0} FROM SolaDBServer..tblCodePivot ".format('\n')
        str_req += "{0} WHERE Bloomberg IN ('{1}') ".format('\n', "','".join(l_bbg))
        df_codePivot = db.fDf_GetRequest_or_fromCsvFile(str_req, str_fileName, 1, str_folder)
        df_codePivot.fillna(value = '', inplace = True)
    except: 
        print('ERROR WisdomTree_GetPivotCode')
        raise
    return df_codePivot


def EasyComo_GetPivotCode(df_Compo, str_colName, str_folder, str_fileName):
    try:
        # Pivot Code
        l_bbg = df_Compo[str_colName].tolist()
        str_req =  "{0} SELECT lc.Code AS [{1}], sl.Bloomberg, sl.Ric, sl.SecurityName,sl.CurrencyCode, sl.ListingID, sl.Isin".format('SET NOCOUNT ON; \n', str_colName)
        str_req += "{0} FROM SolaDBServer..tblListingCode lc {0}  INNER JOIN SolaDBServer..vwSecurityListing sl ON sl.ListingID=lc.ListingID".format('\n')
        str_req += "{0} WHERE lc.Code IN ('{1}') ".format('\n', "','".join(l_bbg))
        str_req += "{0} AND CURRENT_TIMESTAMP BETWEEN lc.StartDate AND lc.EndDate ".format('\n')
        df_codePivot = db.fDf_GetRequest_or_fromCsvFile(str_req, str_fileName, 1, str_folder)
        df_codePivot.fillna(value = '', inplace = True)
    except: 
        print('ERROR EasyComo_GetPivotCode')
        raise
    return df_codePivot

def fDf_EasyCom_NavToAdd(df_GSCUGSCE, dte_date, dte_NAVDate):
    # For Header
    df_GSCUGSCE['Ric'] = df_GSCUGSCE[19]
    df_GSCUGSCE['3Isin'] = df_GSCUGSCE[18]
    df_GSCUGSCE['4TargetNav'] = df_GSCUGSCE[7]
    df_GSCUGSCE['7IndexP'] = df_GSCUGSCE[29]
    
    # SQL Request - NAME
    str_req = """SELECT sl.Isin AS [Isin], sl.Ric, sl.SecurityName AS [3Name] FROM vwSecurityListing sl
                WHERE ((sl.Isin in ('LU1291109533', 'LU1481202775', 'LU1859444769', 'LU2008760592', 'LU2008761053') AND sl.Ric LIKE '%.PA')
                    OR (sl.Isin = 'LU1291109616'  AND sl.Ric LIKE '%.AS'))
                ORDER BY Ric"""
    df_NAME = db.db_SelectReq(str_req, 'D1PRDSOLADB.infocloud.local')
    l_Ric = df_NAME['Ric'].tolist()
    # SQL Request - NAV
    str_req = """SELECT sl.Isin, sl.Ric, sl.SecurityName, e.ETFID, ep.AsAtDate, ep.CurrencyCode, ep.NAV FROM tblETF e
                	join vwSecurityListing sl on sl.SecurityID = e.SecurityID
                	join tblETFPosition ep  on e.ETFID = ep.ETFID
                WHERE ep.AsAtDate >= DATEADD(DAY, -8, CURRENT_TIMESTAMP)
                	AND sl.Ric IN ('{}')
                ORDER BY AsAtDate DESC, ETFID asc""".format("','".join(l_Ric))
    df_NAV = db.db_SelectReq(str_req)
    df_NAV = dframe.fDf_GetFirst_onGroupBy(df_NAV[['Ric', 'AsAtDate', 'NAV']], 'Ric', 'NAV', False, ['AsAtDate'], False)
    # SQL Request - IndexPrice
    str_req = """SELECT sl.Isin,sl.Ric,sl.SecurityName, e.ETFID, ip.AsAtDate, ip.CurrencyCode, ip.VariantID, ip.Value AS [IndexPrice]
                FROM tblETF e
                	join vwSecurityListing sl on sl.SecurityID = e.SecurityID
                	LEFT join vwSecurityListing sl_0 on sl_0.ListingID = e.ReferenceIndexListingID
                	LEFT join tblIndex i on i.SecurityID = sl_0.SecurityID
                	LEFT join tblIndexPosition ip on i.IndexID = ip.IndexID
                WHERE AsAtDate >= DATEADD(DAY, -8, CURRENT_TIMESTAMP)
                	AND ip.CurrencyCode = 'EUR' and ip.VariantID in (102,103)  
                	AND sl.Ric IN ('{}')
                ORDER BY AsAtDate desc, VariantID asc, ETFID asc""".format("','".join(l_Ric))
    df_IndPrice = db.db_SelectReq(str_req)
    df_IndPrice = dframe.fDf_GetFirst_onGroupBy(df_IndPrice[['Ric', 'IndexPrice']], 'Ric', 'IndexPrice', False)
    # JOIN the DF
    df_NavToAdd = dframe.fDf_JoinDf(df_NAME, df_GSCUGSCE[['Ric', '3Isin', '4TargetNav', '7IndexP']], 'Ric', 'left')
    df_NavToAdd = dframe.fDf_JoinDf(df_NavToAdd, df_NAV, 'Ric', 'left')
    df_NavToAdd = dframe.fDf_JoinDf(df_NavToAdd, df_IndPrice, 'Ric', 'left')
    # Choose the columns
    df_NavToAdd = dframe.dDf_fillNaColumn(df_NavToAdd, '3Isin', 'Isin')
    df_NavToAdd = dframe.dDf_fillNaColumn(df_NavToAdd, '4TargetNav', 'NAV')
    df_NavToAdd = dframe.dDf_fillNaColumn(df_NavToAdd, '7IndexP', 'IndexPrice')
    # For ALL
    df_NavToAdd['1IndexDate'] = (dte_date-BDay(1)).strftime('%d/%m/%Y')
    df_NavToAdd['2Client'] = 'BNP'
    df_NavToAdd['5AdjustFactor'] = 1
    df_NavToAdd['6feeFactor'] = 1-(0.002/360 * dat.fInt_dateDifference(dte_date-BDay(1), dte_NAVDate)) 
    df_NavToAdd['8'] = df_NavToAdd['7IndexP']
    df_NavToAdd['9'] = df_NavToAdd['7IndexP']
    df_NavToAdd['10'] = df_NavToAdd['7IndexP']
    df_NavToAdd = df_NavToAdd[['1IndexDate', '2Client', '3Name', '3Isin', '4TargetNav', '5AdjustFactor', '6feeFactor', '7IndexP', '8', '9', '10']]
    return df_NavToAdd


#-----------------------------------------------------------------
# Functions
#-----------------------------------------------------------------
def Act_CopySheetExcel_fomCsv(str_pathWkDest, l_PathWkOrigin, l_SheetName = []):        
    # Loop on the different CSV
    l_sh = []
    for i in range(len(l_PathWkOrigin)):
        str_pathWkOrigin = l_PathWkOrigin[i]
        try:        df_data = pd.read_csv(str_pathWkOrigin, header = None)
        except:     
            print('  ERROR: Could not Take the CSV into DF ')
            print('  - str_pathWkOrigin: ', str_pathWkOrigin)
            raise
        # Get the sheet Name
        try:        str_SheetName = l_SheetName[i]
        except:     
            str_SheetName = str_pathWkOrigin.split('\\')[-1]
            str_SheetName = str_SheetName.split('.csv')[0]
            str_SheetName = str_SheetName[:15]
            while str_SheetName in l_sh:
                str_SheetName = str_SheetName[:len(str_SheetName - 1)] + '_' + str(i + 1)
            l_sh.append(str_SheetName)
        # Create the XLSX file
        try:
            if fl.fBl_FileExist(str_pathWkDest):    str_pathReturn = fl.fStr_fillExcel_InsertNewSheet(str_pathWkDest, '', df_data, str_SheetName)
            else:                                   str_pathReturn = fl.fStr_createExcel_1Sh(str_pathWkDest, '', df_data, str_SheetName)
        except: 
            print('  ERROR: Could not create / Fill the XLSX file')
            print('  - str_pathWkOrigin: ', str_pathWkOrigin)
            print('  - str_pathWkDest: ', str_pathWkDest)
            try:    print('  - str_pathReturn: ', str_pathReturn)
            except: pass
            raise
    return True


def Act_CopySheetExcel(str_pathWkDest, l_PathWkOrigin, l_SheetName = []):
    try:
        time.sleep(1)
        # Create the file
        try:
            if not fl.fBl_FileExist(str_pathWkDest):
                df = pd.DataFrame([['','',''], ['','',''], ['','','']],columns = ['1','2','3'])
                df.to_excel(str_pathWkDest, sheet_name = 'Sheet1', header = False, index = False)
        except: 
            print('Could not create the Excel')
            print(str_pathWkDest)
            return False
        # Create instance Excel
        xlApp = win32.Dispatch("Excel.Application")
        xlApp.Visible = True
        WkDest = xlApp.Workbooks.Open(Filename = str_pathWkDest)
        time.sleep(3)
        l_wsDest = [ws.name for ws in WkDest.Worksheets]
        # Copy Sheet - Loop
        for str_pathWkOrigin in l_PathWkOrigin:
            try:
                time.sleep(0.2)
                WkOrigin = xlApp.Workbooks.Open(Filename = str_pathWkOrigin)
                time.sleep(0.1)
                WSheet = WkOrigin.Worksheets(1)
                bl_SheetExist = WSheet.name in l_wsDest
                if bl_SheetExist:   print(WSheet.name + ' already exists in Workbook Destination')
                else:               WSheet.Copy(Before = WkDest.Worksheets(1))
                WkOrigin.Close(SaveChanges=False)
            except:
                print(' * Could not find the Excel Origin:   ', str_pathWkOrigin, '  || Try next one... ')
                try:    print('  - Sheet Name', WSheet.name)
                except: print('  - No sheet name detected')
                time.sleep(0.5)
        # Close the final Excel
        WkDest.Close(SaveChanges=True)
        xlApp.Visible = True
        #xlApp.Quit()
    except:
        print(' ERROR in Act_CopySheetExcel')
        xlApp.Visible = True
        xlApp.Quit()
        raise
    return True







#===========================================================================================================================
def fBl_sendPcfMail (bl_draft, bl_devEnv, str_to, str_cc, str_bcc, str_subject, l_pathAttach = [], str_messag = str_message):
    if bl_devEnv: 
        str_fromm, str_to, str_cc, str_bcc = 'Laurent.Tupin@ihsmarkit.com', 'Laurent.Tupin@ihsmarkit.com', '', ''
    else: str_fromm = str_from    
    bl_success = out.fBl_SendMail_outlook(bl_draft, str_fromm, str_to, str_cc, str_bcc, str_subject, l_pathAttach, str_messag)
    return bl_success


def fBl_sendErrorReport2(bl_noError, bl_devEnv, str_cc, str_message):
    if not bl_devEnv:
        if bl_noError:
            str_subject = 'OK'
            str_message = 'PCF are created successfully !'
        else:
            str_subject = 'KO'
            str_message = '!!!!!!! PCF are  NOT created successfully !!!!!!!' + '\n' + '\n' + '\n' + str_message
        try:
            str_to = 'Laurent.Tupin@ihsmarkit.com'
            str_subject = 'PCF automation: ' + str_subject 
            out.fBl_SendMail_outlook(False, '', str_to, str_cc, '', str_subject, [], str_message)
        except: 
            try: out.fBl_SendMail_outlook(True, '', str_to, str_cc, '', str_subject, [], str_message)
            except: return False
    return True


def fFlt_roundDown(num, rund = 0):
    int_div = int('1' + rund * '0')
    return ((num * int_div) // 1) / int_div
    

def fDte_dateFutures(dte_date, int_Month = 1):
    str_datFut = dat.fDte_formatMoisAn(dat.fDte_AddMonth(dte_date, int_Month))
    if str_datFut[:3] == 'JUL': 
        str_datFut = 'JLY' + str_datFut[3:]
    return str_datFut

def f2Flt_rollover(dte_date):
    i_day = dat.fInt_workingDay(dte_date)
    
    if i_day < 5:
        return 1.0, 0.0
    elif i_day > 10:
        return 0.0, 1.0
    elif i_day == 5:
        return 1.0, 0.0
    elif i_day == 6:
        return 0.8, 0.2
    elif i_day == 7:
        return 0.6, 0.4
    elif i_day == 8:
        return 0.4, 0.6
    elif i_day == 9:
        return 0.2, 0.8
    elif i_day == 10:
        return  0.0, 1.0
    else:
        print('f2Int_rollover did not work, i_day = ' + i_day)
        return -1, -1


def fStr_ZipFilePath(df_Param, row, dte_date, str_folderRoot):
    # Replace Date
    str_folderDate = str(df_Param.loc[row, 'folderDate'])
    folderDateOffset = df_Param.loc[row, 'folderDateOffset']
    CalendarID = df_Param.loc[row, 'DateCalendarID']
    str_Zip_Date = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, str_folderDate, int(folderDateOffset), str(CalendarID))
    str_ZipPath = df_Param.loc[row, 'Dir_Source'].replace('{folderDate}', str_Zip_Date)
    # Put root folder or not
    if not str_ZipPath[:2] == '\\\\': str_ZipPath = str_folderRoot + str_ZipPath
    # Replace the XXXX in the string
    str_folder = '\\'.join(str_ZipPath.split('\\')[:-1]) + '\\'
    str_fileName = str_ZipPath.split('\\')[-1]
    #str_fileName = fl.fStr_FindPath_byReplacingX(str_folder, str_fileName)
    str_fileName = fl.fStr_GetMostRecentFile_InFolder(str_folder, str_fileName)
    if str_fileName == '': raise
    str_ZipPath =  str_folder + str_fileName
    #print('str_ZipPath ', str_ZipPath)
    return str_ZipPath


#-----------------------------------------------------------------------------------------------------
# Main Function to download
#-----------------------------------------------------------------------------------------------------
def Act_DownFiles_outlook(df_Param, row, str_folderRaw, str_FileName, bl_ArchiveMails):
    # Param
    str_outlook_Acct = str(df_Param.loc[row, 'outlook_Acct'])
    str_outlook_mailBox = str(df_Param.loc[row, 'outlook_mailBox'])
    str_outlook_folder = str(df_Param.loc[row, 'outlook_folder'])
    str_outlook_folderToArchive = str(df_Param.loc[row, 'outlook_folderToArchive'])
    str_outlook_subject = str(df_Param.loc[row, 'outlook_subject'])
    str_to = str(df_Param.loc[row, 'outlook_To'])
    str_cc = str(df_Param.loc[row, 'outlook_Cc'])
    str_ExactName = str(df_Param.loc[row, 'File_ExactName'])
    int_File_startW = df_Param.loc[row, 'File_startW']
    int_File_endW = df_Param.loc[row, 'File_endW']
    l_files = []
    if not str_ExactName.lower() == 'true':
        str_File_startW = str_FileName[:int(int_File_startW)]
        if int_File_endW == 0:          str_File_endW = ''
        else:                           str_File_endW = str_FileName[-int(int_File_endW):]
    
    # Get Mails (ALL of them, can be very heavy)
    o_mails, o_folderToMove = out.fMail_getMails(str_outlook_Acct, str_outlook_mailBox, str_outlook_folder, str_outlook_folderToArchive)
    if o_mails == False: 
        print(' EMPTY: Cannot Get Mails')
        print(' - ', str_outlook_Acct, str_outlook_mailBox, str_outlook_folder, str_outlook_folderToArchive)
        return False
    
    # Filter the Mail: Filter with the criteria: SUbject + Name of Attach... + Sort more Recent
    if str_ExactName.lower() == 'true':
        l_mail = out.fMail_GetMailWithAttach(o_mails, str_outlook_subject, str_to, str_cc, str_FileName)
    else:
        l_mail = out.fMail_GetMailWithAttach(o_mails, str_outlook_subject, str_to, str_cc, '', str_File_startW, str_File_endW)
        #    # Filter on Subject and take most Recent mail
        #    if str_ExactName.lower() == 'true': 
        #        l_mail = out.fMail_getmail_mostRecent(o_mails, [str_outlook_subject], str_to, str_cc, str_FileName)
        #    else: l_mail = out.fMail_getmail_mostRecent(o_mails, [str_outlook_subject], str_to, str_cc, '')
    
    #==============================================================================================
    # If the Mail cannot be found, We search in Inbox (and move it to the right folder using the Archive functionality)
    if l_mail == False and str_outlook_folder!= '' :
        print(' EMPTY: Cannot Get Most Recent Mails')
        print(' -> We will search in MailBox: #', str_outlook_mailBox, '#')
        bl_ArchiveMails = True
        str_outlook_folderToArchive = str_outlook_folder
        str_outlook_folder = ''
        # Get Mails
        o_mails, o_folderToMove = out.fMail_getMails(str_outlook_Acct, str_outlook_mailBox, str_outlook_folder, str_outlook_folderToArchive)
        # Filter the Mail: Filter with the criteria: SUbject + Name of Attach... + Sort more Recent
        if str_ExactName.lower() == 'true': 
            l_mail = out.fMail_GetMailWithAttach(o_mails, str_outlook_subject, str_to, str_cc, str_FileName)
        else: 
            l_mail = out.fMail_GetMailWithAttach(o_mails, str_outlook_subject, str_to, str_cc, '', str_File_startW, str_File_endW)
        #        # Filter on Subject and take most Recent mail
        #        if str_ExactName.lower() == 'true': 
        #            l_mail = out.fMail_getmail_mostRecent(o_mails, [str_outlook_subject], str_to, str_cc, str_FileName)
        #        else: l_mail = out.fMail_getmail_mostRecent(o_mails, [str_outlook_subject], str_to, str_cc)       
    #==============================================================================================
    
    if not l_mail: 
        print(' EMPTY: Mails Filtrered this way returned empty, Subject: {}, Attach: {}'.format(str_outlook_subject, str_FileName))
        return False
    
    # Download PJ
    if str_ExactName.lower() == 'true':
        l_files = out.fBl_downMailAttch2(str_folderRaw, l_mail, str_FileName)
    else:
        l_files = out.fBl_downMailAttch2(str_folderRaw, l_mail, str_File_startW, str_File_endW)
    
    if not l_files:
        print(' EMPTY: Cannot download Attach from mail')
        print(' - Mail Subject: ' + str_outlook_subject)
        print(' - Outlook Folder: ' + str_outlook_folder)
        return False
        #    # Rename the file - RENAMING
        #    if not str_ExactName.lower() == 'true':
        #        str_file = str(l_files[0])
        #        fl.Act_Rename(str_folderRaw, str_file, str_FileName)
    # Archive PJ
    if bl_ArchiveMails:
        bl_success = out.fBl_archiveMail(l_mail, o_folderToMove)
        if not bl_success: print('Cannot Archive mail')
    return True


#------------------------------------------------------------------------------------------------------------------------------------
def Act_DownFiles_FTP(df_Param, row, str_folderRaw, str_FileName, str_FileDownloadMode, dte_date):
    # Param
    str_id = str(df_Param.loc[row, 'ID'])
    str_PCF = str(df_Param.loc[row, 'PCF'])
    str_FTP_server = str(df_Param.loc[row, 'FTP_server'])
    str_FTP_uid = str(df_Param.loc[row, 'FTP_uid'])
    str_FTP_pwd = str(df_Param.loc[row, 'FTP_pwd'])
    str_FTP_directory = str(df_Param.loc[row, 'FTP_directory'])
    
    str_fileDate = str(df_Param.loc[row, 'fileDate'])
    DateOffset = str(df_Param.loc[row, 'DateOffset'])
    CalendarID = df_Param.loc[row, 'DateCalendarID']
    
    str_ExactName = str(df_Param.loc[row, 'File_ExactName'])
    int_File_startW = df_Param.loc[row, 'File_startW']
    int_File_endW = df_Param.loc[row, 'File_endW']
    #    str_File_startW = str_FileName[:int(int_File_startW)]
    #    if int_File_endW == 0:      str_File_endW = ''
    #    else:                       str_File_endW = str_FileName[-int(int_File_endW):]
    
    global str_NewFileName
    str_NewFileName = ''
    
    # Get folder
    l_ftpFolder = str_FTP_directory.split('/')
    if l_ftpFolder[0] == '':        l_ftpFolder = l_ftpFolder[1:]
    elif l_ftpFolder[0] == 'nan':   l_ftpFolder = []
    
    
    #--------------------------------------------------------------------------
    # List all file that look like NameWithXXX and take the most recent one
    #--------------------------------------------------------------------------
    if not str_ExactName.lower() == 'true':
        if not int_File_startW == '' or not int_File_endW == '':
            try:
                if str_FileDownloadMode == 'FTP':               l_files = ftp.ftp_listFolder(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder)
                elif str_FileDownloadMode == 'FTP_SSL':         l_files = ftp.ftp_listFolder(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, -1, True)
                elif str_FileDownloadMode == 'SFTP_Paramiko':   l_files = ftp.ssh_listFilesInFolder(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder)
            except:
                print('     ERROR: We could list the files from ' + str_FileDownloadMode)
                return False
            # 1.b. FIlter only the one with the XXX
            l_files = fl.fL_GetFileList_withinModel(l_files, str_FileName)
            # 1.c. Sort by Alphabet because Time will be the only difference if several files
            l_files.sort(reverse = True)
            # 1.d. Final Name of the file
            str_FileName = l_files[0]
            print('  * We found in FTP the complete name: ', str_FileName)
            str_NewFileName = str_FileName
        
    #--------------------------------------------------------------------------
    # DOWNLOAD
    #--------------------------------------------------------------------------
    try:
        if str_FileDownloadMode == 'FTP':               ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folderRaw)
        elif str_FileDownloadMode == 'FTP_SSL':         ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folderRaw, -1, True)
        elif str_FileDownloadMode == 'SFTP_Paramiko':   ftp.ssh_downFile(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folderRaw)
    except:
        if str_ExactName.lower() == 'true':
            print('     ERROR: We could not download from ' + str_FileDownloadMode + '\n')
            return False
        if not int_File_startW == '' or not int_File_endW == '':
            print('     ERROR: We could not download from ' + str_FileDownloadMode + '\n')
            return False
        
        #----------------------------------------------------------
        # Try with another date
        #----------------------------------------------------------
        print('   ' + str_FileDownloadMode + ' did not find the file: ', str_FileName, '   || PCF: ' + str_PCF, '   || Download mode: ' + str_FileDownloadMode)
        print('   **Try Again : Offset was: ' + str(DateOffset) + ' | And is now: ' + str(int(DateOffset) - 1))
        
        str_NewDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, str_fileDate, int(DateOffset) - 1, str(CalendarID))
        str_FileName = df_Param.loc[row, 'fileName'].replace('{fileDate}', str_NewDate)
        str_NewFileName = str_FileName
        
        # Change df_Param for the next Offset (if d-1 become d-2, d-2 needs to become d-3)
        df_Param.loc[(df_Param.PCF == str_PCF) & (df_Param.ID == str_id), 'DateOffset'] = df_Param['DateOffset'] - 1
        #df_Param.loc[(df_Param.PCF == str_PCF) & (df_Param.FileDownloadMode == str_FileDownloadMode),'DateOffset'] = df_Param['DateOffset'] - 1
        #df_Param.loc[(df_Param.PCF==str_PCF) & (df_Param.FileDownloadMode==str_FileDownloadMode),'DateOffset'].apply(lambda x: x-1)
        
        try:
            if str_FileDownloadMode == 'FTP':
                ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folderRaw)
                print('   File Successfully downloaded... ' + str_FileName + '\n\n')
            elif str_FileDownloadMode == 'FTP_SSL':
                ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folderRaw, -1, True)
                print('   File Successfully downloaded (ftp + SSL)... ' + str_FileName + '\n\n')
            elif str_FileDownloadMode == 'SFTP_Paramiko':
                ftp.ssh_downFile(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_FileName, str_folderRaw)
                print('   File Successfully downloaded (sftp)... ' + str_FileName + '\n\n')
        except: 
            print('     ERROR * 2: We could not download from ' + str_FileDownloadMode + '\n\n')
            return False
    return True


#------------------------------------------------------------------------------------------------------------------------------------
def Act_DownFiles_SQL(df_Param, row, str_folderRaw, str_FileName,  dte_date):
    # Param
    str_PCF = str(df_Param.loc[row, 'PCF'])
    str_req = fStr_generateSQLReq(df_Param, row, dte_date)
    # Execute Req
    try:
        df_sql = db.db_SelectReq(str_req)
    except:
        print('     ERROR in Act_DownFiles_SQL: We could not execute the SQL in PCF: ', str_PCF)
        print('     - ', str_req)
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
def Act_DownFiles_ZIP(df_Param, row, str_folderRaw, str_FileName, dte_date, str_folderRoot):
    # Param
    str_PCF = str(df_Param.loc[row, 'PCF'])
    try:            str_ZipPath = fStr_ZipFilePath(df_Param, row, dte_date, str_folderRoot)
    except:
        print('  ERROR in Act_DownFiles_ZIP.   PCF: ', str_PCF)
        print('  Could not find the path of the ZIP (str_ZipPath)')
        return False
    # Extarct the right file
    try:            fl.ZipExtractFile(str_ZipPath, str_folderRaw, str_FileName)
    except:
        print('    ERROR in Act_DownFiles_ZIP.   PCF: ', str_PCF)
        print('    str_ZipPath: ' , str_ZipPath)
        return False
    return True

 
#------------------------------------------------------------------------------------------------------------------------------------		
def Act_DownFiles(df_Param, row, str_folderRaw, str_FileName, dte_date, str_folderRoot, bl_ArchiveMails):
    try:
        # Param
        str_path = fl.fStr_BuildPath(str_folderRaw, str_FileName)
        str_File_PrefixName = str(df_Param.loc[row, 'File_PrefixName'])
        str_FileDownloadMode = str(df_Param.loc[row, 'FileDownloadMode'])
        str_SheetName = str(df_Param.loc[row, 'SheetName'])
        str_fileDate = str(df_Param.loc[row, 'fileDate'])
        DateOffset = df_Param.loc[row, 'DateOffset']
        CalendarID = df_Param.loc[row, 'DateCalendarID']
        # URL Param
        str_url = str(df_Param.loc[row, 'URL'])
        str_url_keyword = str(df_Param.loc[row, 'url_keyword'])
        str_dateURL = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, str_fileDate, int(DateOffset), str(CalendarID))
        str_url_2 = str_url.replace('{fileDate}', str_dateURL)
        str_Translate = str(df_Param.loc[row, 'url_blTranslate'])
        if str_Translate.lower() == 'true': bl_waitTranslate = True
        else:                               bl_waitTranslate = False
        
        # Outlook
        if str_FileDownloadMode == 'OUTLOOK':
            bl_success = Act_DownFiles_outlook(df_Param, row, str_folderRaw, str_FileName, bl_ArchiveMails)
            if not bl_success: 
                return False
        # Folder
        elif str_FileDownloadMode == 'FOLDER':
            try:
                str_pathSource = df_Param.loc[row, 'Dir_Source'].replace('{folderDate}', 
                                             (dte_date + BDay(int(df_Param.loc[row, 'DateOffset']))).strftime(df_Param.loc[row, 'folderDate']))
                if not str_pathSource[:2] == '\\\\': str_pathSource = str_folderRoot + str_pathSource
                # Name of the file with XX
                try:
                    if str_FileName.count('{') and str_FileName.count('}') > 0 :
                        #str_FileName = fl.fStr_FindPath_byReplacingX(str_pathSource, str_FileName)
                        str_FileName = fl.fStr_GetMostRecentFile_InFolder(str_pathSource, str_FileName)
                except: print('  fStr_generateFileName: Could not find the File with XXXX ')
                # Copy
                shutil.copyfile(os.path.join(str_pathSource, str_FileName), str_path)
            except:
                print('   ERROR in Act_DownFiles: shutil.copy did not work')
                print('   - str_pathSource: ', str_pathSource)
                print('   - str_FileName: ', str_FileName)
                return False
        # FTP
        elif str_FileDownloadMode == 'FTP':
            bl_success = Act_DownFiles_FTP(df_Param, row, str_folderRaw, str_FileName, str_FileDownloadMode, dte_date)
            if str_NewFileName != '': str_FileName = str_NewFileName
            if not bl_success: return False
        # FTP
        elif str_FileDownloadMode == 'FTP_SSL':
            bl_success = Act_DownFiles_FTP(df_Param, row, str_folderRaw, str_FileName, str_FileDownloadMode, dte_date)
            if str_NewFileName != '': str_FileName = str_NewFileName
            if not bl_success: return False
        # FTP paramiko
        elif str_FileDownloadMode == 'SFTP_Paramiko':
            bl_success = Act_DownFiles_FTP(df_Param, row, str_folderRaw, str_FileName, str_FileDownloadMode, dte_date)
            if str_NewFileName != '': str_FileName = str_NewFileName
            if not bl_success: return False
        # SQL
        elif str_FileDownloadMode == 'SQL':
            bl_success = Act_DownFiles_SQL(df_Param, row, str_folderRaw, str_FileName, dte_date)
            if not bl_success: return False        
        # ZIP
        elif str_FileDownloadMode == 'ZIP':
            bl_success = Act_DownFiles_ZIP(df_Param, row, str_folderRaw, str_FileName, dte_date, str_folderRoot)
            # If its this file, do not return an error (as he is here only sometimes)
            if not 'HKGRFMHKSSET_ST-FM-TX' in str_FileName:
                if not bl_success: return False
        # HTML
        elif str_FileDownloadMode == 'HTML_JSON':
            df_fut = html.fDf_htmlGetArray_json(str_url_2, str_url_keyword)
            #----------------------------------------------------------------------
            # In case of Holiday not accounted or else, date must bu offset until we found data
            i_offset = 1
            while len(df_fut) == 0:
                str_dateURL = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, str_fileDate, int(DateOffset) -i_offset, str(CalendarID))
                str_url_2 = str_url.replace('{fileDate}', str_dateURL)
                print(' Careful the URL was not found, we needed to search the URL: \n', str_url_2)
                df_fut = html.fDf_htmlGetArray_json(str_url_2, str_url_keyword)
                i_offset += 1
                if i_offset > 10: break
            #----------------------------------------------------------------------
            if len(df_fut) > 0:
                fl.fStr_CreateTxtFile(str_folderRaw, str_FileName, df_fut, '', True)
            #str_url = "https://www.cmegroup.com/trading/energy/crude-oil/light-sweet-crude_quotes_settlements_futures.html"
            #str_url = f'https://www.cmegroup.com/CmeWS/mvc/Settlements/Futures/Settlements/425/FUT?tradeDate={str_date}'
        elif str_FileDownloadMode == 'HTML_JSON_YUANTA':
            d_listUrl = {}
            str_url_Root = str_url_2.replace('api/Orders?fundid=', '#/Orders/')
            df_html = html.fDf_htmlGetArray_json(str_url_2)
            if len(df_html) == 0:       print(' INFORMATION: No Orders on URL: ', str_url_2)
            #--------------------------------------------------------------
            # Special treatment on str_url_keyword which is a dico from here
            l_coupleDico = str_url_keyword.split('||')
            for str_couple in l_coupleDico:
                str_couple = str_couple.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
                str_key = str_couple.split(':')[0]
                str_value = str_couple.split(':')[1]
                d_listUrl[str_key] = list(str_value.split(','))
            #--------------------------------------------------------------
            for i_Key, i_List in d_listUrl.items():
                df_html_1 = []
                for i_urlPart in i_List:
                    str_url_3 = str_url_2.replace(i_Key, i_urlPart)
                    df_html_3 = html.fDf_htmlGetArray_json(str_url_3)
                    if len(df_html_3) > 0:
                        if len(df_html_1) > 0:  df_html_1 = dframe.fDf_Concat_wColOfDf1(df_html_1, df_html_3, True, 1)
                        else:                   df_html_1 = df_html_3.copy()
                    else:
                        print(' INFORMATION: there is no data on URL: {}'.format( str_url_3))
                        print(' - URL root to look for other data: {}'.format(str_url_Root))
                df_html = dframe.fDf_Concat_wColOfDf1(df_html, df_html_1, True, 2)
            # Create CSV
            if len(df_html) > 0:
                df_html.to_csv(str_path, header = True, index = False)
        elif str_FileDownloadMode == 'HTML_SOUP':
            df_result = html.fDf_htmlGetArray_Soup(str_url_2, False, bl_waitTranslate)
            df_result.fillna(value = '', inplace = True)
            df_result.loc[0, 2] = ''
            fl.fStr_createExcel_1Sh(str_folderRaw, str_FileName, df_result, str_SheetName, False)
        elif str_FileDownloadMode == 'HTML_csv_SOUP':
            df_result = html.fDf_htmlGetArray_Soup(str_url_2, True, bl_waitTranslate)
            df_result.to_csv(str_path, header = False, index = False)
        elif str_FileDownloadMode == 'NO_DOWNLOAD':
            print(' - Is is FINE: No file to download - Only to load')
            
        # Renaming the INPUT Files
        if not str_File_PrefixName == '':
            try: fl.Act_Rename(str_folderRaw, str_FileName, str_File_PrefixName + str_FileName)
            except: print(' ERROR: Act_Rename')
    except: 
        print(' ERROR: in Act_DownFiles')
        return False
    return True
    
    
#------------------------------------------------------------------------------------------------------------------------------------
def fDf_getDfFromPCF(df_Param, row, str_folder, str_FileName, bl_header = 0, v_sheetName = '', str_sep = ',', l_names = None, str_encoding = None):
    str_path = os.path.join(str_folder, str_FileName)
    # Test if the file exist
    if not fl.fBl_FileExist(str_path):
        print('   File does not exist (fDf_getDfFromPCF)')
        print('   - Path: ', str_path)
        return None
    # Try to read
    try:        
        # ------- XLSX -------
        if '.XLSX' in str_FileName.upper() or '.XLS' in str_FileName.upper():
            if v_sheetName == '':   df_data = pd.read_excel(str_path, header = bl_header)
            else:                   df_data = pd.read_excel(str_path, header = bl_header, sheet_name = v_sheetName)
        # ------- FLat File -------
        elif '.ETF' in str_FileName.upper() or '.XML' in str_FileName.upper() or '.XSD' in str_FileName.upper() or '718708NETRCNH' in str_FileName.upper():
            df_data = pd.read_csv(str_path, header = bl_header)
        elif '.CSV' in str_FileName.upper() or '.TXT' in str_FileName.upper() or '.HDX' in str_FileName.upper():
            if '.HDX' in str_FileName.upper():
                df_data = pd.read_csv(str_path, header = 1, sep='\t')
            else:
                df_data = dframe.fDf_readCsv_enhanced(str_path, bl_header, str_sep)
        # ------- ZIP -------
        elif '.ZIP' in str_FileName.upper():
            df_data = 1
        else:
            print('---------------------------')
            print('  (**) We do not know how to take DF from this kind of files | We need to define a type in fDf_getDfFromPCF...')
            print('  - str_FileName: ', str_FileName)
            print('---------------------------')
            return None
    except Exception as err:
        print('   ERROR in fDf_getDfFromPCF : df_data could not be read')
        print('   - Error: ', str(err))
        print('   - str_folder', str_folder)
        print('   - str_FileName', str_FileName)
        print('   - bl_header', bl_header)
        print('   - v_sheetName', v_sheetName)
        print('   - str_sep', str_sep)
        return None
    return df_data



##str_path = r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Manual_py\HK_Easy\Easy 20200528\Easy FI - open\PCFSRIC520200528.txt'
##df_data = pd.read_csv(str_path, header = None, sep = ",", names = None, encoding = None)
##print(df_data )

#str_path = r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Auto_py\HK_Global X\Global X 20200601\raw\ESTIMATE_PCFOIL_20200601.xls'
##str_path = r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Auto_py\HK_Global X\Global X 20200601\raw\GLOBAL_X_ETF_NAV_200601.XLS'
##df_data = pd.read_excel(str_path, header = None)
#df_data = fl.fDf_convertToXlsx(str_path, '', None)
#print(df_data)
#df_data.to_csv(str_path.replace('.xls', '.csv'), index = False, header = None) 




#------------------------------------------------------------------------------------------------------------------------------------
def fDf_getDfFromDownloaded(df_Param, row, str_folderRaw, str_FileName, bl_header = 0):
    # Renaming the INPUT Files
    try:
        str_SheetName = str(df_Param.loc[row, 'SheetName'])
        str_File_PrefixName = str(df_Param.loc[row, 'File_PrefixName'])
        if not str_File_PrefixName == '': 
            str_FileName = str_File_PrefixName + str_FileName
    except: print('  Renaming did not work in fDf_getDfFromDownloaded !!!')
    
    print('Searching for... ' + str_FileName)
    str_path = os.path.join(str_folderRaw, str_FileName)
    
    # Test if the file exist
    if not fl.fBl_FileExist(str_path):
        print('   File does not exist (fDf_getDfFromDownloaded)')
        print('   - Path: ', str_path)
        return None, False
    
    # Get the DataFrame from the file
    try:        
        # ------- XLSX -------
        if '.XLSX' in str_FileName.upper() or '.XLS' in str_FileName.upper():
            if 'NQ100' in str_FileName.upper() and 'DEALING ' in str_FileName.upper():
                df_data = pd.read_excel(str_path, header = 1)            
            elif 'LAST-VALUATION-MARKIT' in str_FileName.upper():
                df_data = pd.read_excel(str_path, header = 3)
            elif '_SOLCBTT_' in str_FileName.upper() or '_SOLCCCT_' in str_FileName.upper():
                df_data = pd.read_excel(str_path, header = 4)
            elif 'ETF_PCFREPORT_MIRAE' in str_FileName.upper() :
                df_data = pd.read_excel(str_path, header = None)
            elif 'ESTIMATE_PCFOIL_' in str_FileName.upper() or 'ESTIMATE_PCFSPX_' in str_FileName.upper() or 'PCFHSIHSCEI_' in str_FileName.upper():
                df_data = fl.fDf_convertToXlsx(str_path, str_SheetName, None)
            elif 'PCF_CAM CTPB BOND ETF_' in str_FileName.upper():
                df_data = 1
            else:
                if str_SheetName == '':     df_data = pd.read_excel(str_path, header = bl_header)
                else:                       df_data = pd.read_excel(str_path, header = bl_header, sheet_name = str_SheetName)
                #, skiprows = range(2), nrows = 6, l_names = range(7), encoding = 'cp1252'
        # ------- HDX -------
        elif '.HDX' in str_FileName.upper():
            if '_SPGSCI_FIN_STD' in str_FileName.upper() :
                df_data = pd.read_csv(str_path, header = 1, sep='\t')
            else:
                print(' HDX in fDf_getDfFromDownloaded: Case not taken into account')
                return None, True
            
        # ------- CSV -------
        elif '.CSV' in str_FileName.upper():
            if 'GMO' in str_FileName.upper() or 'fcnacl2v' in str_FileName.lower() or 'fdccc' in str_FileName.lower() \
            or 'fdcco' in str_FileName.lower() or 'navau' in str_FileName.lower():
                df_data = pd.read_csv(str_path, header = 2)
                # If it has been opened manually, it should take the 4th row
                l_colUnamed = ['Unnamed' for colName in df_data.columns if 'Unnamed' in colName]
                if l_colUnamed:
                    print(df_data.iloc[0:4, 0:3])
                    df_data = pd.read_csv(str_path, header = 3)
                    print('-------- After, header on 4th row ---------')
                    print(df_data.iloc[0:4, 0:3])
                # GMO treat
                if 'GMO' in str_FileName.upper():
                    df_data.dropna(axis = 'index', subset = ['ISIN'], inplace = True)
            elif 'DF_LIGHT_INV_S02' in str_FileName.upper() or 'DF_NAV_S02' in str_FileName.upper():
                df_data = pd.read_csv(str_path, header = bl_header, sep=';', index_col=False) 
            elif 'PINGAN_PCF_' in str_FileName.upper():
                ## Do note that this will cause the offending lines to be skipped.
                #df_data = pd.read_csvstr_path, header = bl_header, error_bad_lines = False)
                df_data = 1
            elif 'WISDOMTREEUCITS_BSKT' in str_FileName.upper() :
                df_data = pd.read_csv(str_path, header = bl_header, skiprows = 8)
            else:
                df_data = pd.read_csv(str_path, header = bl_header)
                
        # ------- TXT -------
        elif '.TXT' in str_FileName.upper():
            if 'ELQC' in str_FileName.upper() or 'GOMA' in str_FileName.upper() \
            or 'PCFGSCE' in str_FileName.upper() or 'PCFGSCU' in str_FileName.upper() \
            or 'COGSDE_GSCE_' in str_FileName.upper() or 'COGSCU' in str_FileName.upper(): # \
            #or 'DIREXION_HSBC.T' in str_FileName.upper() :
                df_data = pd.read_csv(str_path, header = bl_header, sep='\t')
            elif 'COEEEH_' in str_FileName.upper() or 'COEMEH_' in str_FileName.upper() or 'COJBEM_' in str_FileName.upper():
                # we just forward so we do not need the data: Check out PINGAN_PCF_
                df_data = 1
            else:
                df_data = pd.read_csv(str_path, header = bl_header)
                
        # ------- Other Flat files -------
        elif '.ETF' in str_FileName.upper():
            df_data = pd.read_csv(str_path, header = bl_header)
        
        elif '718708NETRCNH' in str_FileName.upper():
            df_data = dframe.fDf_readCsv_enhanced(str_path, None, str_sep = '|', l_names = range(33))
            
        # ------- ZIP -------
        elif '.ZIP' in str_FileName.upper():
            df_data = 1
        
        else:
            print('---------------------------')
            print('  (**) We do not know how to take DF from this kind of files | We need to define a type in fDf_getDfFromDownloaded...')
            print('  - str_FileName: ', str_FileName)
            print('---------------------------')
            return None, True
    except Exception as err:
        print('   ERROR in fDf_getDfFromDownloaded : df_data could not be read ')
        print('   - Error: ', str(err))
        print('   - Path: ', str_path)
        print('   - bl_header: ', bl_header)
        return None, True
    return df_data, True



#------------------------------------------------------------------------------------------------------------------------------------
def fStr_generateFileName(df_Param, row, str_folderRaw, dte_date):
    str_fileName = str(df_Param.loc[row, 'fileName'])
    str_fileDate = str(df_Param.loc[row, 'fileDate'])
    DateOffset = df_Param.loc[row, 'DateOffset']
    CalendarID = df_Param.loc[row, 'DateCalendarID']
    str_NewDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, str_fileDate, int(DateOffset), str(CalendarID))
    str_fileName = str_fileName.replace('{fileDate}', str_NewDate)
    # Name of the file with XX
    try:
        if str_fileName.count('{') and str_fileName.count('}') > 0 :
            if str_fileName.count('{X}') > 0 :
                str_fileName = fl.fStr_GetMostRecentFile_InFolder(str_folderRaw, str_fileName, True, bl_exactNumberX = False)
            else:
                str_fileName = fl.fStr_GetMostRecentFile_InFolder(str_folderRaw, str_fileName, True, bl_exactNumberX = True)
    except: print('  fStr_generateFileName: Error, should not Happen !!!!! ')
    return str_fileName
def fStr_generateFolderRaw(df_Param, row, str_folderRoot, dte_date):
    str_Dir_Dest = str(df_Param.loc[row, 'Dir_Dest'])
    str_folderDate = str(df_Param.loc[row, 'folderDate'])
    folderDateOffset = df_Param.loc[row, 'folderDateOffset']
    CalendarID = df_Param.loc[row, 'DateCalendarID']
    str_NewDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, str_folderDate, int(folderDateOffset), str(CalendarID))
    # Build the Folder
    str_folderRaw = str_Dir_Dest.replace('{folderDate}', str_NewDate)
    if str_Dir_Dest[:2] != '\\\\': str_folderRaw = str_folderRoot + str_folderRaw
    if str_Dir_Dest[-1] != '\\' : str_folderRaw = str_folderRaw + '\\'
    return str_folderRaw
def fStr_generateSQLReq(df_Param, row, dte_date):
    try:
        str_sqlReq = str(df_Param.loc[row, 'sqlReq'])
        if '{sql_Date}' in str_sqlReq:
            str_sqlDateFormat = str(df_Param.loc[row, 'sqlDateFormat'])
            sqlDateOffset = df_Param.loc[row, 'sqlDateOffset']
            str_sqlDateOffsetType = str(df_Param.loc[row, 'sqlDateOffsetType'])
            CalendarID = df_Param.loc[row, 'DateCalendarID']
            # Condition to offset the date and input into the QL req
            if str_sqlDateOffsetType == 'Month':
                dte_NewDate = dat.fDte_AddMonth(dte_date, int(sqlDateOffset))
                #Do not use the function #fDat_GetCorrectOffsetDate_Calendar# because that change month in case EOM is Saturday or Sunday...
                str_NewDate = dte_NewDate.strftime(str_sqlDateFormat)
            else:
                str_NewDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, str_sqlDateFormat, int(sqlDateOffset), str(CalendarID))
            str_NewDate = str_NewDate.upper()
            str_sqlReq = str_sqlReq.replace('{sql_Date}', str_NewDate)
    except Exception as err: print(' ERROR in fStr_generateSQLReq: {}'.format(str(err)))
    return str_sqlReq




#------------------------------------------------------------------------------------------------------------------------------------	
def fDic_pcfAutomate_GetFiles2(df_Param, str_folderRoot, dte_date, bl_ArchiveMails, bl_dfRequired = True, bl_forceDwld = False):
    # Take parameters from CSV
    d_result = {}
    l_PathOutput = []
    bl_dwlFailed = False
    
    for i, row in enumerate(df_Param.index):
        bl_forceDwld_local = bl_forceDwld
        # Variables in Param CSV
        str_ID = str(df_Param.loc[row, 'ID'])
        str_folderRaw = fStr_generateFolderRaw(df_Param, row, str_folderRoot, dte_date)
        str_FileName = fStr_generateFileName(df_Param, row, str_folderRaw, dte_date)
        bl_Optional = False
        if str(df_Param.loc[row, 'bl_Optional']).lower() == 'true':     bl_Optional = True
        
        # Create the folder
        try:        fl.fBl_createDir(str_folderRaw)
        except:     return 'ERROR in GenProcess. _GetFiles2: Could not Create Folder: ' + str_folderRaw
        
        
        #======================================================================================
        # SEARCH: Try to get the data from files already dwld - (Add DATAFRAME in the dictionary)
        #======================================================================================
        if not bl_forceDwld_local:
            df_data, bl_exist = fDf_getDfFromDownloaded(df_Param, row, str_folderRaw, str_FileName)
            # bl_exist = False: File not downloaded ==> will go download it
            if not bl_exist:
                bl_forceDwld_local = True
            # bl_exist = True + df_data is None: File not readable => Useless to even try to download it
            elif df_data is None:
                if not bl_Optional: bl_dwlFailed = True
                else:               print('   (*) File could not be read but the file is optional => Process continue without raising issues')
                print('')
                continue
            else:                   d_result[str_ID] = df_data
        
        #======================================================================================
        # Download
        #======================================================================================
        if bl_forceDwld_local:
            print('Downloading... ' + str_FileName)
            bl_success = Act_DownFiles(df_Param, row, str_folderRaw, str_FileName, dte_date, str_folderRoot, bl_ArchiveMails)
            # In case of download files before, we need to update fileName
            if bl_success:              str_FileName = fStr_generateFileName(df_Param, row, str_folderRaw, dte_date)
            else:
                if not bl_Optional:     bl_dwlFailed = True
                else:                   print('   (*) File could not be downloaded but the file is optional => Process continue without raising issues')
                print('')
                continue
            #-------------------------------------------
            # Re-Search after Download
            # Get the DF in case of download after Search not successful (not if Download PJ only (bl_dfRequired = False)) ()
            if bl_dfRequired:
                #print('Searching again for... ' + str_FileName)
                df_data, bl_exist = fDf_getDfFromDownloaded(df_Param, row, str_folderRaw, str_FileName)
                if not bl_exist:
                    print('   ERROR: File  has been downloaded even if it pass the download check. Please report the issue in detail with LT: {}'.format(str_ID))
                    if not bl_Optional: bl_dwlFailed = True
                    else:               print('   (*) However the file is optional => Process continue')
                    print('')
                    continue
                elif df_data is None:
                    if not bl_Optional: bl_dwlFailed = True
                    else:               print('   (*) File could not be read after success download but file = optional => Process continue')
                    print('')
                    continue
                # Add DATAFRAME in the dictionary
                print('')
                d_result[str_ID] = df_data
                
            else:   pass
        #======================================================================================
        
        #Add the folder for information || Careful, takes only the last one
        d_result['Folder'] = str_folderRaw.replace('\\raw','')
        l_PathOutput.append(str_folderRaw + str_FileName)
    # End of loop - Add Path of files downloaded
    d_result['files'] = l_PathOutput 
    
    if bl_dwlFailed:        return False
    elif bl_dfRequired:     return d_result
    else:                   return d_result






########################################################################################################################################
########################################################################################################################################

#-----------------------------------------------------------------
# WisdomTree etf file creation
#-----------------------------------------------------------------
def fStr_CreateEtfFile(str_folder, str_fileName, dte_date, str_Isin1, str_id, str_IsinFinal, str_ccy, flt_nav):
    str_text = '#@!ETF {0}{1}'.format(dte_date.strftime('%d%m%y'), '\n')
    str_text += '{0}'.format('\n')
    str_text += '[INDEX]{0}'.format('\n')
    str_text += 'ISIN={0}{1}'.format(str_Isin1, '\n')
    str_text += 'ALPHA={0}{1}'.format(str_id, '\n')
    str_text += 'CASH=0{0}'.format('\n')
    str_text += 'FUNDSHARES=1{0}'.format('\n')
    str_text += 'NAME=INAV WISDOMTREE ENHANCED COMMODITY UCITS ACC{0}'.format('\n')
    str_text += '#MAILADDRESS=mk_index_production@markit.com{0}'.format('\n')
    str_text += '#MAILADDRESS=Data.eu@wisdomtree.com{0}'.format('\n')
    str_text += '#MAILADDRESS=Sola@ihsmarkit.com{0}'.format('\n')
    str_text += '{0}'.format('\n')
    str_text += '[UNDERLYING]{0}'.format('\n')
    str_text += 'COUNT=1{0}'.format('\n')
    str_text += '{0}'.format('\n')
    str_text += 'ENTRY={0} +{1}={2} 1 RER 1'.format(str_IsinFinal, str(round(flt_nav, 4)), str_ccy)
    # Create Txt file And rename it
    fl.act_createFile(False, str_folder, str_fileName, str_text)
    #    fl.act_createFile(False, str_folder, str_fileName.replace('.etf', '.txt'), str_text)
    #    fl.Act_Rename(str_folder, str_fileName.replace('.etf', '.txt'), str_fileName)
    return os.path.join(str_folder, str_fileName)





#-----------------------------------------------------------------
# AMUNDI
#-----------------------------------------------------------------
def fDf_getFut_inDb(dte_futDate):
    str_req = """SELECT Column5, Column6, Column7, Column9, Column10
        FROM vwSTOXXEurope600FuturesRollIndexFile
        WHERE Column1 = '""" + dte_futDate + "'"
    df_futures = db.db_SelectReq(str_req, '', str_dbAmundi, '', '', True)
    return df_futures

def fFl_getFutCode(int_weekday, RollOverWeek, FuturesCode, FuturesCode2, Future1Percentage, futuresvalue2):
    futyear=FuturesCode[:4]
    futmonth=FuturesCode[-2:]
    # Change the condition
    if RollOverWeek:
        futmonth = int(futmonth)+3
        if (futmonth > 12):
            futmonth = futmonth - 12
            futyear = str(int(futyear) + 1)
        Future1Percentage = 1 - (int_weekday / 4)
        futmonth = '0' + str(futmonth) [-2:]
    elif futuresvalue2 is not None and Future1Percentage == 0:
        futyear = FuturesCode2[:4]
        futmonth = FuturesCode2[-2:]
        Future1Percentage = 1
    # Return the code 
    if futmonth == '03':
        mID = 'H'
        futmonth = 'Mar'
    elif futmonth == '06':
        mID = 'M'
        futmonth = 'Jun'
    elif futmonth == '09':
        mID = 'U'
        futmonth = 'Sep'
    elif futmonth == '12':
        mID = 'Z'
        futmonth = 'Dec'
    # Return 
    return 'SXO' + mID + futyear[-1:], futmonth, futyear, Future1Percentage

def fBl_RollOverWeek(dte_date):
    str_currentMonth = dte_date.strftime("%m")
    dte_last_friday = dat.fDte_lastFriday(dte_date)
    if ((dat.is_second_friday(dte_last_friday)) and (str_currentMonth in ('3','6','9','12'))):
        print("Today is rollover week - week after 2nd Friday of the quarter: ", dte_last_friday)
        return True
    else: return False
    
def fFl_getFutValue(futuresvalue, futuresvalue2, RollOverWeek, d, FutureCode2, dte_dm1, Future1Percentage):
    if (RollOverWeek and d > 0):
        str_req = """SELECT * 
                FROM tblPriceException pe 
                JOIN tblListingCode sl ON pe.ListingID = sl.ListingID 
                WHERE CodeTypeID = 15 AND FamilyID = 1394 AND Code = '""" + FutureCode2 + "' AND AsAtDate = '" + dte_dm1 + "'"
        df_futures = db.db_SelectReq(str_req)
        #df_futures = df_futures.loc[df_futures['AsAtDate'] == dte_dm1]
        futuresvalue2 = df_futures['Value'].iloc[0]
    elif (RollOverWeek and d == 0):
        futuresvalue2 = 1
    elif futuresvalue2 is not None and Future1Percentage == 0:
        futuresvalue = futuresvalue2
    # Put to Float
    if futuresvalue is not None:
        futuresvalue = float(futuresvalue)
    if futuresvalue2 is not None:
        futuresvalue2 = float(futuresvalue2)
     # Return   
    return futuresvalue, futuresvalue2


def fDf_GetHoliday():
    str_req = """SELECT * FROM tblHoliday Where CalendarID = '60'"""
    df_Holiday = db.db_SelectReq(str_req)
    return df_Holiday

def fDf_GetPosition(str_ric):
    str_req = "DECLARE @IndexRic varchar(30) = '" + str_ric + """'
              SELECT lc.Code, v.Name as Variant, l.CurrencyCode, ip.AsAtDate, ip.Value 
              FROM tblListingCode lc
                  JOIN tblListing l on lc.ListingID=l.ListingID
                  JOIN tblVariant v on l.VariantID=v.VariantID 
                  JOIN tblIndex i on l.SecurityID=i.SecurityID
                  JOIN tblIndexPosition ip on i.IndexID=ip.IndexID 
                      AND ip.AsAtDate >= getdate()-10 
                      AND ip.AsAtDate <= getdate()
                      AND ip.VariantID=l.VariantID 
                      AND ip.CurrencyCode = l.CurrencyCode 
                      AND IsOpen=0 
              WHERE lc.StartDate<= cast(getdate() as date) 
                  AND lc.EndDate > cast(getdate() as date) 
                  AND lc.Code = @IndexRic
              ORDER BY AsAtDate desc """    
    df_Position = db.db_SelectReq(str_req)
    return df_Position

def fDf_GetComposition(str_ric, IndexDate):
    str_req = "exec spExcelGetComposition '" + str_ric + "', '" + IndexDate + "', 'Index', 'Tracking', 'Open'"
    df_Composition = db.db_SelectReq(str_req)
    return df_Composition

def fDf_GetBeta(int_listingId):
    str_req = "DECLARE @IndexListingID int = " + str(int_listingId) + """
              SELECT v.Name as Variant, l.CurrencyCode, ip.AsAtDate, ip.Value 
              FROM tblListing l 
                  JOIN tblVariant v on l.VariantID=v.VariantID 
                  JOIN tblIndex i on l.SecurityID=i.SecurityID 
                  JOIN tblIndexPosition ip on i.IndexID=ip.IndexID 
                      AND ip.AsAtDate >= getdate()-10 
                      AND ip.AsAtDate <= getdate() 
                      AND ip.VariantID=l.VariantID 
                      AND ip.CurrencyCode = l.CurrencyCode 
                      AND IsOpen=0 
              WHERE l.ListingID = @IndexListingID
              ORDER BY AsAtDate desc """
    df_Beta = db.db_SelectReq(str_req)
    return df_Beta

def fDf_GetCreationUnit(str_secId):
    str_req = "SELECT * from tblSecurityExtendedProperty Where SecurityID = '" + str_secId + "' and PropertyTypeID = '378'"
    df_Composition = db.db_SelectReq(str_req)
    return df_Composition

def fDf_GetFeesSpread(str_secId):
    str_req = "SELECT DaysInYear, DailySwapRate, AnnualManagementFeeRate from tblETF e Where SecurityID = '" + str_secId + "'"
    df_Composition = db.db_SelectReq(str_req)
    return df_Composition
















#====================================================================================================
# DEPRECATED
#====================================================================================================




#-----------------------------------------------------------------
# DEPREACTED - To delete when all is cleaned
#-----------------------------------------------------------------
def fL_downFTP(str_host, str_uid, str_pwd, l_folder, str_fileName, str_filePathDest):
    print('DEPREACTED fL_downFTP')
    bl_success = ftp.fBl_ftpDownFileBinary(str_host, str_uid, str_pwd,l_folder, str_fileName, str_filePathDest)
    if not bl_success: return False    
    return True


def fDf_sqlFx(l_where = ["FXRateSetID = '1'", "FromCurrencyCode = 'USD'"]):
    print('DEPREACTED fDf_sqlFx')
    return db.fDf_sqlBuildSelect('tblFXRate', '*', l_where)


def fDf_sqlMapping(str_from, str_select = '*', l_where = [], str_orderBy = ''):
    print('DEPREACTED fDf_sqlMapping')
    return db.fDf_sqlBuildSelect(str_from, str_select, l_where, '', str_orderBy)


def fDte_dateFutures2(dte_date, int_Month = 1):
    print('DEPREACTED fDte_dateFutures2')
    a = dat.fDte_AddMonth(dte_date, int_Month)
    print(a)
    b = dat.fDte_formatMoisAnnee(a)
    print(b)
    return b

def fBl_createFolder(str_folder):
    print('  DEPRECATED: replace fBl_createFolder by fl.fBl_createDir')
    #    str_folderShortName = '\\' + '\\'.join(str_folder.split('\\')[-5:])
    bl_success = fl.fBl_createDir(str_folder)
    return bl_success

def fL_CreateTxtFile_v2(str_folder, str_FileName, df_data, bl_header = False, str_sep = ','):
    print('  DEPRECATED: replace fL_CreateTxtFile_v2 by fl.fStr_CreateTxtFile')
    str_PcfPath = fl.fStr_CreateTxtFile(str_folder, str_FileName, df_data, str_sep, bl_header) 
    #    try:
    #        if str_FileName == '':      str_PcfPath = str_folder
    #        else:                       str_PcfPath = os.path.join(str_folder, str_FileName)
    #        df_data.to_csv(str_PcfPath, index = False, header = bl_header, sep = str_sep) 
    #    except:
    #        print('  ERROR in fL_CreateTxtFile_v2: Could not create the file: ')
    #        print('  - str_folder :',str_folder, 'str_FileName :', str_FileName, 'bl_header :',  bl_header, 'str_sep :',  str_sep)
    #        return False
    return str_PcfPath

def fL_CreateTxtFile_RetunPath(str_pathPcf, l_pcfFileName, df_data, bl_header = False, str_sep = ','):
    print('  DEPRECATED: replace fL_CreateTxtFile_RetunPath by fl.fStr_CreateTxtFile')
    str_Path = fl.fStr_CreateTxtFile(str_pathPcf, l_pcfFileName[0], df_data, str_sep, bl_header) 
    #    try:
    #        l_pathPcf = [str_pathPcf + file for file in l_pcfFileName]
    #        for str_Pcf in l_pathPcf:
    #            df_data.to_csv(str_Pcf, index = False, header = bl_header, sep = str_sep) 
    ##            #For Amundi 
    ##            if 'PCFMKTN' in str_Pcf:
    ##                df_data.to_csv(str_Pcf.replace('PCFMKTN', 'PCFMKTN_2'), index=False, header = None, sep='\t')
    #    except:
    #        print('  ERROR: Could not create the file: ')
    #        print('  - str_pathPcf :',str_pathPcf, 'l_pcfFileName :', l_pcfFileName, 'bl_header :',  bl_header)
    #        return False
    return [str_Path]

# 1 file out - 1 Dataframe - 1 Sheet (INSERT SHEET - Not insert rows in existing sheet)
def fL_fillExcel_v3(str_folder, str_FileName, df_data, str_SheetName = '', bl_header = False):
    print('  DEPRECATED: replace fL_fillExcel_v3 by fl.fStr_fillExcel_InsertNewSheet')
    str_path = fl.fStr_fillExcel_InsertNewSheet(str_folder, str_FileName, df_data, str_SheetName, bl_header)
    #    try:
    #        if str_FileName == '':  str_path = str_folder
    #        else:                   str_path = os.path.join(str_folder, str_FileName)
    #        # Define Book
    #        xl_book = openpyxl.load_workbook(filename = str_path)
    #        #xl_writer = pd.ExcelWriter(str_path, engine = 'openpyxl')
    #        with pd.ExcelWriter(str_path, engine = 'openpyxl') as xl_writer:
    #            xl_writer.book = xl_book
    #            xl_writer.sheets = dict((ws.title, ws) for ws in xl_book.worksheets)
    #            # Add the Sheet
    #            if str_SheetName == '':     str_SheetName = 'Sh1'
    #            if str_SheetName in list(xl_writer.sheets):
    #                print(" The sheet '{}' alrdeay exist".format(str_SheetName))
    #                while str_SheetName in list(xl_writer.sheets):
    #                    str_SheetName = str_SheetName[1:] + str_SheetName[0] + 'x'
    #                print(" We replace the sheet name: '{}'  but you need to improve the management of name".format(str_SheetName))
    #            df_data.to_excel(xl_writer, header = bl_header, index = False, sheet_name = str_SheetName)
    #            #SAVE
    #            xl_writer.save()
    #    except:
    #        print('  ERROR in fL_fillExcel_vv3: Could not fill the file')
    #        print('  - str_path', str_path)
    #        print('  - str_SheetName', str_SheetName)
    #        return False
    return str_path


# n file out - 1 Dataframe - 1 Sheet - MEANT TO DISAPEAR as it makes no sense
def fL_fillExcel_RetunPath(str_pathPcf, l_pcfFileName, df_data, bl_header = False, 
                           bl_insertRows = False, int_nbRows = 0, int_rowsWhere = 1):
    print('  DEPRECATED: replace fL_fillExcel_RetunPath by fl.fStr_fillXls_celByCel')
    str_path = str_pathPcf + l_pcfFileName[0]
    fl.fStr_fillXls_celByCel(str_path, df_data, '', 0, int_nbRows, int_rowsWhere)
    #    try:
    #        l_pathPcf = [str_pathPcf + file for file in l_pcfFileName]
    #        for str_Pcf in l_pathPcf:
    #            xlApp = win32.Dispatch('Excel.Application')
    #            xlApp.Visible = True 
    #            xlWb = xlApp.Workbooks.Open(str_Pcf)
    #            xlWs = xlWb.ActiveSheet
    #            # ------ Insert or delete ROWS ------
    #            if bl_insertRows:
    #                if int_nbRows > 0:
    #                    #xlWs.getCells().insertRows(int_rowsWhere, int_nbRows)
    #                    #xlWs.insert_rows(int_rowsWhere, int_nbRows)
    #                    for i in range(0, int_nbRows): xlWs.Rows(int_rowsWhere).EntireRow.Insert()
    #                elif int_nbRows < 0:
    #                    #xlWs.getCells().deleteRows(int_rowsWhere, -int_nbRows, True) 
    #                    for i in range(0, -int_nbRows): xlWs.Rows(int_rowsWhere).EntireRow.Delete()                    
    #            # -----------------------------------
    #            for i, row in enumerate(df_data.index):
    #                for j, col in enumerate(df_data.columns):
    #                    xlWs.Cells(i+1, j+1).Value = str(df_data.iat[i, j])
    #            xlApp.Visible = True
    #            xlWb.Close(True)
    #            #xlApp.Application.Quit()
    #    except:
    #        try: xlApp.Visible=True
    #        except: print('  ERROR: xlApp visible did not work')
    #        try: xlWb.Close(False)
    #        except: print('  ERROR: Excel workbook could not be closed')
    #        #try: xlApp.Application.Quit()
    #        #except: print('  ERROR: Excel could not be closed')
    #        print('  ERROR: Could not create the PCF: ' + str_Pcf)
    #        return False
    return l_pcfFileName



# 1 file out - n Dataframe - n Sheet
def fL_fillExcel_v2(str_folder, str_FileName, l_dfData, l_SheetName = [], bl_insertRows = False, 
                    l_nbRows = [], l_rowsWhere = []):
    print('  DEPRECATED: replace fL_fillExcel_v2 by fl.fStr_fillXls_celByCel_plsSheets')
    str_path = fl.fStr_fillXls_celByCel_plsSheets(str_folder,str_FileName,l_dfData,l_SheetName,l_nbRows,l_rowsWhere)
    #    try:
    #        if str_FileName == '':      str_path = str_folder
    #        else:                       str_path = os.path.join(str_folder, str_FileName)
    #		
    #        # Open the file (win32)
    #        xlApp = win32.Dispatch('Excel.Application')
    #        xlApp.Visible = True 
    #        xlWb = xlApp.Workbooks.Open(str_path)
    #		
    #        # Dataframe
    #        for i in range(len(l_dfData)):
    #            df_data = l_dfData[i]
    #            try:        str_SheetName = l_SheetName[i]
    #            except:     str_SheetName = ''
    #            #Sheet Name
    #            try:                            xlWs = xlWb.Sheets(str_SheetName)
    #            except:
    #                if xlWb.Sheets(i + 1).name not in l_SheetName:  xlWs = xlWb.Sheets(i + 1)
    #                elif str_SheetName != '':                       xlWs = xlWb.add_worksheet(str_SheetName)
    #                else:	                                          xlWs = xlWb.add_worksheet()
    #            xlWs.Select
    #            # ------ Insert or delete ROWS ------
    #            if bl_insertRows:
    #                try:        int_nbRows = l_nbRows[i]
    #                except:     int_nbRows = 0
    #                
    #                print('int_nbRows: ', int_nbRows)
    #                
    #                try:        int_rowsWhere = l_rowsWhere[i]
    #                except:     int_rowsWhere = 1
    #                
    #                print('int_rowsWhere: ', int_rowsWhere)
    #                
    #                if int_nbRows > 0:
    #                    for i in range(0, int_nbRows):      xlWs.Rows(int_rowsWhere).EntireRow.Insert()
    #                elif int_nbRows < 0:
    #                    for i in range(0, -int_nbRows): 		xlWs.Rows(int_rowsWhere).EntireRow.Delete()                    
    #            # -----------------------------------
    #            for i, row in enumerate(df_data.index):
    #                for j, col in enumerate(df_data.columns):	xlWs.Cells(i+1, j+1).Value = str(df_data.iat[i, j])
    #        #xlApp.Visible = True
    #        xlWb.Close(True)
    #        #xlApp.Application.Quit()
    #    except:
    #        try: 		xlApp.Visible=True
    #        except: 	print('  ERROR: xlApp visible did not work')
    #        try: 		xlWb.Close(False)
    #        except: 	print('  ERROR: Excel workbook could not be closed')
    #        #try: 		xlApp.Application.Quit()
    #        #except: 	print('  ERROR: Excel could not be closed')
    #        print('  ERROR: Could not create the PCF: ' + str_path)
    #        return False
    return str_path


# 1 file out - 1 Dataframe - 1 Sheet
def fL_createExcel_v3(str_folder, str_FileName, df_Data, str_SheetName = '', bl_header = False):
    print('  DEPRECATED: replace fL_createExcel_v3 by fl.fStr_createExcel_1Sh')
    str_path = fl.fStr_createExcel_1Sh(str_folder, str_FileName, df_Data, str_SheetName, bl_header)
    #    try:        
    #        if str_FileName == '':      str_path = str_folder
    #        else:                       str_path = os.path.join(str_folder, str_FileName)
    #        
    #        if str_SheetName != '':     df_Data.to_excel(str_path, header = bl_header, index = False, sheet_name = str_SheetName)
    #        else:                       df_Data.to_excel(str_path, header = bl_header, index = False)
    #    except:
    #        print('  ERROR: fL_createExcel_v3 did not work ')
    #        print('  - str_path: ', str_path)
    #        print('  - str_SheetName: ', str_SheetName)
    #        return False
    return str_path


# n file out - 1 Dataframe - 1 Sheet - MEANT TO DISAPEAR as it makes no sense
def fL_createExcel_RetunPath(str_folder, l_pcfFileName, df_Data, bl_header = False, str_SheetName = ''):
    print('  DEPRECATED: replace fL_createExcel_RetunPath by fl.fStr_createExcel_1Sh')
    str_path = fl.fStr_createExcel_1Sh(str_folder, l_pcfFileName[0], df_Data, str_SheetName, bl_header)
    #    try:
    #        l_pathPcf = [str_pathPcf + file for file in l_pcfFileName]
    #        for str_Pcf in l_pathPcf:
    #            # Create the file (xlsxwriter cannot modify files)
    #            xlWb = xlsxwriter.Workbook(str_Pcf)
    #            #Sheet Name
    #            if str_SheetName != '':     xlWs = xlWb.add_worksheet(str_SheetName)             
    #            else:                       xlWs = xlWb.add_worksheet()   
    #            # fill in
    #            for i, row in enumerate(df_data.index):
    #                for j, col in enumerate(df_data.columns):
    #                    xlWs.write(i, j, str(df_data.iat[i, j]))
    #                    #xlWs.Cells(i+1, j+1).Value = str(df_data.iat[i, j])
    #        xlWb.close()
    #    except:
    #        try:        xlWb.close()
    #        except:     print('Could not close the file')
    #        print('  ERROR: fL_createExcel_RetunPath did not work ')
    #        print(str_pathPcf, l_pcfFileName)
    #        print('str_SheetName: ', str_SheetName)
    #        return False
    return [str_path]


# 1 file out - n Dataframe - n Sheet
def fL_createExcel_v2(str_folder, str_FileName, l_dfData, l_SheetName = [], bl_header = False):
    print('  DEPRECATED: replace fL_createExcel_v2 by fl.fStr_createExcel_SevSh')
    str_path = fl.fStr_createExcel_SevSh(str_folder, str_FileName, l_dfData, l_SheetName, bl_header)
    #    try:        
    #        if str_FileName == '':      str_path = str_folder
    #        else:                       str_path = os.path.join(str_folder, str_FileName)
    #        # Create the file (xlsxwriter cannot modify files)
    #        xlWb = xlsxwriter.Workbook(str_path)
    #        # Dataframe
    #        for i in range(len(l_dfData)):
    #            df_data = l_dfData[i]
    #            try:        str_SheetName = l_SheetName[i]
    #            except:     str_SheetName = ''
    #            #Sheet Name
    #            if str_SheetName != '':     xlWs = xlWb.add_worksheet(str_SheetName)             
    #            else:                       xlWs = xlWb.add_worksheet()   
    #            # fill in
    #            for i, row in enumerate(df_data.index):
    #                for j, col in enumerate(df_data.columns):
    #                    xlWs.write(i, j, str(df_data.iat[i, j]))
    #                    #xlWs.Cells(i+1, j+1).Value = str(df_data.iat[i, j])
    #        xlWb.close()
    #    except:
    #        try:        xlWb.close()
    #        except:     print('Could not close the file')
    #        print('  ERROR: fL_createExcel_v2 did not work ')
    #        print('  - ', str_folder, str_FileName)
    #        print('  - l_SheetName: ', l_SheetName)
    #        return False
    return str_path



#-----------------------------------------------------------------
# DB_AM
#-----------------------------------------------------------------
def fDf_DB_AM_Proc():
    print('DEPREACTED')
    return -1
    str_req = """SET NOCOUNT ON; 
        IF OBJECT_ID ('tempdb..#tmpInterim') IS NOT NULL DROP TABLE #tmpInterim
        BEGIN
        	SELECT distinct '' [Fund Code]
        		,CASE WHEN sc.Code='XD00BQXKVQ19' 
        			THEN  'IE'+substring(sc.Code,3,10)
        			ELSE  'LU'+substring(sc.Code,3,10)
        			END AS Isin
        		,sp.Name as [Fund Name]
        		, '' [Share Class]
        		,ep.CurrencyCode as [Currency]
        		,ep.AsAtDate as [NAV Date]
        		,CAST(0.0 AS DECIMAL(25,13)) as [NAV Per Share]
        		,ep.SharesOutstanding as [Total Shares In Issue]
        		,CAST(0.0 AS DECIMAL(25,13)) as [Total Fund NAV]
        		,'' [Price equivalent in EUR]
        		,'' [Price equivalent in GBP]	
        		,'' [Price equivalent in JPY]	
        		,'' [Price equivalent in HKD]	
        		,'' [(No column name)]	
        		,'' [Price equivalent in USD]
        		,'' [(No column name2)]
        		,'' [Aktien gewinn]
        		,'' [Zwischen gewinn]	
        		,'' [Zwischen gewinn in EUR]	
        		,'' [Zwischen gewinn in EUR2]
        		,'' [TID]	
        		,'' [WKN (Germany)]
        		,'' [Valoren (Switzerland)]
        		,'' [Reuters Code]	
        		,'' [Bloomberg code]
        		,'' [Fees]	
        		,'' [Quantity]
        		,CAST(0.0 AS DECIMAL(25,13)) as MTM	
        		,ep.AsAtDate as NAVDate
        		,ep.SharesOutstanding as TotalSharesInIssue
        		,eprice.CustodianDate as SSNAVDate
        		,eprice.PreviousNAV as SSNAV
        		,ep.SharesOutstanding as SSSO
        		,ep.AUM as SSAUM
        		,CAST(eprice.CustodianMTM AS DECIMAL(25,13)) as SSMTM
        		,CASE WHEN lc.Code IS NULL THEN s.CurrentName ELSE s.CurrentName + ' - ' + lc.Code END as Benchmark
        		,cd.OpenDate as BenchmarkCurrentDate
        		,ip.CurrencyCode as BenchMarkCurrency
        		,ip.Value as BenchMarkValueOpen
        		,CAST(CASE WHEN ip.CurrencyCode = ep.CurrencyCode THEN ip.Value ELSE ip.Value * fxe.Value / fxb.Value END AS DECIMAL(25,13)) AS BenchMarkValueOpenBase
        		,eprice.CustodianDate as BenchmarkPrevDate
        		,ipc.Value as BenchMarkValueClose
        		,CAST(CASE WHEN ip.CurrencyCode = ep.CurrencyCode THEN ipc.Value ELSE ipc.Value * fxec.Value / fxbc.Value END AS DECIMAL(25,13)) AS BenchMarkValueCloseBase
        		,CAST(0.0 AS DECIMAL(25,13)) as BMPerformance
        		,round(CAST(e.DailySwapRate AS DECIMAL(25,25)) * 10000 * 360,2) as Spread
        		,CAST(e.AnnualManagementFeeRate AS DECIMAL(25,13)) *10000 as TER
        		,d.GrossAmount as Distribution
        		,ca.SharesAdjustmentFactor as Split
        	INTO #tmpInterim
        	FROM tblSecurityCode sc  
        		inner join tblETF e on e.SecurityID = sc.SecurityID 
        		left join tblFamily f On f.FamilyID = e.FamilyID
        		left join tblSecurityProperty sp on sp.SecurityID = sc.SecurityID and sp.StartDate <= f.OpenDate and sp.EndDate > f.OpenDate
        		left join tblETFPosition ep on ep.ETFID = e.ETFID and ep.AsAtDate = f.OpenDate
        		left join tblBasket b on b.ETFID = e.ETFID
        		left join tblBasketType bt on bt.BasketTypeID = b.BasketTypeID
        		left join tblBasketPosition bp on bp.BasketID = b.BasketID and bp.AsAtDate = f.OpenDate   
        		left join tblListing l on l.ListingID = e.ReferenceIndexListingID        
        		left join tblSecurity s on s.SecurityID = l.SecurityID      
        		left outer join tblListingCode lc on lc.ListingID = l.ListingID and lc.CodeTypeID = 10 and lc.StartDate <= f.OpenDate and lc.EndDate > f.OpenDate
        		left outer join tblIndex i on i.SecurityID = s.SecurityID
        		left join tblFamily fi on fi.FamilyID = i.FamilyID
        		left join tblCalendarDate cd on cd.CalendarID = fi.CalendarID and f.CurrentDate = cd.OpenDate
        		left join tblETFPricing eprice on eprice.ETFID = e.ETFID and eprice.AsAtDate = f.CurrentDate 
        		left join tblDistribution d on d.ListingID = l.ListingID and d.XdDate = f.OpenDate
        		left join tblCorporateAction ca on ca.ListingID = l.ListingID and ca.CorporateActionTypeID = 9 and ca.XdDate = f.OpenDate
        		left join tblRate r on r.RateSetID = e.FundingSpreadRateSetID and r.AsAtDate = f.CurrentDate
        		left join tblIndexPosition ip on ip.IndexID = i.IndexID and ip.CurrencyCode = l.CurrencyCode and ip.VariantID = l.VariantID and ip.AsAtDate = cd.OpenDate  
        		left join tblIndexPosition ipc on ipc.IndexID = i.IndexID and ipc.CurrencyCode = l.CurrencyCode and ipc.VariantID = l.VariantID 
                and ipc.AsAtDate = eprice.CustodianDate
        		LEFT JOIN tblFXRate fxe on fxe.FXRateSetID = f.FXRateSetID and fxe.AsAtDate = cd.OpenDate and fxe.FromCurrencyCode = 'USD' 
                and fxe.ToCurrencyCode = ep.CurrencyCode
        		LEFT JOIN tblFXRate fxb on fxb.FXRateSetID = f.FXRateSetID and fxb.AsAtDate = cd.OpenDate and fxb.FromCurrencyCode = 'USD' 
                and fxb.ToCurrencyCode = ip.CurrencyCode
        		LEFT JOIN tblFXRate fxec on fxec.FXRateSetID = f.FXRateSetID and fxec.AsAtDate = eprice.CustodianDate and fxec.FromCurrencyCode = 'USD' 
                and fxec.ToCurrencyCode = ep.CurrencyCode
        		LEFT JOIN tblFXRate fxbc on fxbc.FXRateSetID = f.FXRateSetID and fxbc.AsAtDate = eprice.CustodianDate and fxbc.FromCurrencyCode = 'USD' 
                and fxbc.ToCurrencyCode = ip.CurrencyCode
        		WHERE e.FamilyID IN(
                     SELECT f.FamilyID FROM tblFamily f
        				JOIN tblFamilyTask ft ON ft.FamilyID  = f.FamilyID
        				JOIN tblTask t ON t.TaskID = ft.TaskID
        				JOIN tblProcess p ON p.ProcessID = t.ProcessID
                     WHERE p.ProcessID in (33, 34))
        		AND b.BasketTypeID = 5
        		and sc.Code in ('XD00BQXKVQ19','XD0274208692','XD0274210672','XD0292096186','XD0292107645','XD0292107991','XD0292109690','XD0322251520','XD0322252171',
        			'XD0322252502','XD0322252924','XD0432553047','XD0455008887','XD0455009265','XD0455009851','XD0476289623','XD0476289896','XD0490618542',	'XD0514695187')		
        	UPDATE #tmpInterim
        	SET BMPerformance = (BenchMarkValueOpenBase - BenchMarkValueCloseBase) / BenchMarkValueCloseBase
        	WHERE BenchMarkValueCloseBase IS NOT NULL
        	UPDATE #tmpInterim
        	SET MTM = SSMTM * (1 + BMPerformance)
        		   ,[NAV Per Share] = SSNAV * (1 + BMPerformance) - ((( CAST(DATEDIFF(DAY,SSNAVDate,NAVDate) AS DECIMAL(38,34))) / CAST(360 AS DECIMAL(25,13))) * 
                   ((ISNULL(Spread,0.00000000000000) + TER) / 10000) * SSNAV * (1 + BMPerformance))
        	UPDATE #tmpInterim
        	SET [Total Fund NAV] = [NAV Per Share] * TotalSharesInIssue
        
        	select * from #tmpInterim          
        	order by 6 asc
        	DROP TABLE #tmpInterim
        END"""
    df_proc = db.db_SelectReq(str_req)
    return df_proc


#-----------------------------------------------------------------
# EASY_FI
#-----------------------------------------------------------------
def fDf_EasyFi_COELQC1_Proc(str_bbg):
    print('DEPREACTED')
    return -1
    str_req = """SET NOCOUNT ON; 
        DECLARE @Code VARCHAR (30) = '""" + str_bbg + """'
        DECLARE @BasketType VARCHAR (20) = 'Creation'
        
        SELECT  '1' AS [Structure Line Counting Unit]
        	,'-' AS [Counter Line]
        	,sc.Code AS [ETF ISIN code] 
        	,lc2.Code AS [Listing ID]
        	,s.CurrentName  AS [Sec Name]
        	,'-' AS [6]
        	,Isp.Name AS [Index Name]
        	,Isc.Code AS [index iNAV Isin]
        	,'-' AS [9],'-' AS [10],'P' AS [11],'S' AS [12],'-' AS [13]
          ,'-' AS [14],'-' AS [15],'-' AS [16],'-' AS [17],'-' AS [18],'-' AS [19]
        FROM tblListingCode lc
        	INNER JOIN tblListingCode lc2 ON lc2.ListingID = lc.ListingID AND lc2.CodeTypeID = 23
        	INNER JOIN tblListing l ON l.ListingID = lc.ListingID
        	INNER JOIN tblSecurity s ON s.SecurityID = l.SecurityID
        	INNER JOIN tblETF e ON e.SecurityID = l.SecurityID
        	INNER JOIN tblSecurityCode sc ON  sc.SecurityID = l.SecurityID
        		AND sc.CodeTypeID = (SELECT CodeTypeID FROM tblCodeType WHERE Name = 'Isin')
        	LEFT JOIN tblSecurityCode Isc ON  Isc.SecurityID = l.SecurityID
        		AND Isc.CodeTypeID = (SELECT CodeTypeID FROM tblCodeType WHERE Name = 'iNAV ISIN')
        	INNER JOIN tblListing Il ON Il.ListingID = e.ReferenceIndexListingID
        	INNER JOIN tblSecurityProperty Isp ON Isp.SecurityID = Il.SecurityID
        WHERE lc.Code = @Code"""
    df_proc = db.db_SelectReq(str_req)
    return df_proc


def fDf_EasyFi_COELQC2_Proc(str_bbg):
    print('DEPREACTED')
    return -1
    str_req = """DECLARE @RefFamilyID INT, @Filter VARCHAR(100), @ListingID INT, @PCFCurrency VARCHAR(255), @RIC VARCHAR(25), 
    	@CalculationMask INT, @ETFID INT, @BasketID INT, @BasketTypeID INT, @BasketName VARCHAR (20), @CloseDate DATE, 
    	@UnderlyingIndexCurrency char (3), @AsAtDate DATE, @BasketType VARCHAR (20) = 'Creation', @Bloomberg varchar(50), 
    	@Code VARCHAR (30) = '""" + str_bbg + """'
        
        SELECT
        	@RefFamilyID = RefFamilyID,
        	@Filter = bp.Filter,
        	@ListingID = l.ListingID,
        	@PCFCurrency = l.CurrencyCode,
        	@RIC = lc.Code,
        	@CalculationMask = bp.CalculationMask,
        	@ETFID = e.ETFID,
        	@BasketID = b.BasketID,
        	@BasketTypeID = bt.BasketTypeID,
        	@BasketName = bt.Name,
        	@AsAtDate =f.OpenDate,
        	@CloseDate=f.CurrentDate
        FROM tblFamily f
        	INNER JOIN tblETF e ON e.FamilyID = f.FamilyID
        	INNER JOIN tblSecurity s ON s.SecurityID = e.SecurityID
        	INNER JOIN tblBasket b ON b.ETFID = e.ETFID
        	INNER JOIN tblBasketProperty bp ON bp.BasketID = b.BasketID AND bp.StartDate <= f.CurrentDate AND bp.EndDate > f.CurrentDate
        	INNER JOIN tblBasketType bt on bt.BasketTypeID = b.BasketTypeID
        	INNER JOIN tblListing l ON l.SecurityID = s.SecurityID
        	INNER JOIN tblListingCode lc ON lc.ListingID = l.ListingID AND lc.StartDate <=f.CurrentDate AND lc.EndDate >f.CurrentDate
        WHERE  lc.Code = @Code AND UPPER(bt.Name) = UPPER(@BasketType)	
        
        SELECT @Bloomberg = Code 
        FROM tblListingCode GG 
        WHERE  GG.ListingID = @ListingID 
        	AND GG.StartDate <= @AsAtDate 
        	AND GG.EndDate > @AsAtDate 
        	AND GG.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'Bloomberg')
        
        SELECT '2' AS [Structure Line Counting Unit], 
        	CONVERT(VARCHAR(10), CL.OpenDate, 112) AS [iNAV Calculation Date], 
        	G.Code AS [ETF ISIN Code],
        	cast(A.Divisor as float) AS [Number of Shares of a Creation Unit], 
        	A.NAV*A.Divisor AS [Value of One Creation Unit],
        	A.NAV*A.Divisor-H.EstimatedCash AS [Value of Equity],
        	A.NAV AS [NAV], 
        	H.EstimatedCash AS [Cash Component of the NAV],
        	100*H.EstimatedCash/(A.NAV*A.Divisor) AS [Cash in Percentage],
        	B.CurrencyCode AS [Currency Used to Value the Fund],
        	A.SharesOutstanding AS [Outstanding Shares],
        	A.NAV*A.Divisor AS [NAV of the Fund],
        	d.GrossAmount AS [Dividend Amount], 
        	d.XdDate AS [Ex Date], 
        	'' AS [Dividend Frequency],
        	B.TotalExpenseRatio AS [Management Fees],
        	A.NAV AS [NAV 2],
        	CONVERT(VARCHAR(10),A.AsAtDate, 112) AS [NAV Valuation Date], 
        	L.Value AS [Underlying Index Level], 
        	CONVERT(VARCHAR(10),A.AsAtDate, 112) AS [Effective Date of the C/R File], 
        	'-' AS [Exposure to Risky Assets],
        	'-' AS [Reference Basket Level], 
        	'-' AS [NAV Floor], 
        	'-' AS [Multiplier] 
        FROM tblETFPosition A
        	INNER JOIN tblETF B ON B.ETFID = A.ETFID
        	INNER JOIN tblFamily C ON C.FamilyID = B.FamilyID
        	INNER JOIN tblSecurity D ON D.SecurityID = B.SecurityID
        	INNER JOIN tblSecurityProperty E ON E.SecurityID = D.SecurityID AND E.StartDate <= @AsAtDate AND E.EndDate > @AsAtDate
        	LEFT JOIN tblListing F ON F.SecurityID = D.SecurityID  
        	LEFT JOIN tblSecurityCode G ON  G.SecurityID = D.SecurityID AND G.StartDate <= @AsAtDate AND G.EndDate > @AsAtDate AND G.CodeTypeID = (SELECT CodeTypeID 
            FROM tblCodeType WHERE Name = 'Isin')
        	LEFT JOIN tblSecurityCode II ON II.SecurityID = F.SecurityID AND II.StartDate <= @AsAtDate AND II.EndDate > @AsAtDate AND II.CodeTypeID = (select CodeTypeID 
            from tblCodeType WHERE Name = 'iNAV ISIN')
        	INNER JOIN tblBasketPosition H ON H.BasketID = @BasketID AND H.AsAtDate = A.AsAtDate
        	INNER JOIN tblBasketPosition I ON I.BasketID = @BasketID AND I.AsAtDate IN (SELECT MAX(I2.AsAtDate) FROM tblBasketPosition I2 WHERE I2.BasketID = I.BasketID 
            AND I2.AsAtDate < H.AsAtDate)
        	INNER JOIN tblListing UI ON UI.ListingID = B.ReferenceIndexListingID
        	INNER JOIN tblCalendarDateLite CL ON CL.CalendarID = C.CalendarID AND CL.AsAtDate = @CloseDate
        	JOIN tblIndex K ON K.SecurityID = UI.SecurityID
        	JOIN tblIndexPosition L ON L.IndexID = K.IndexID AND L.AsAtDate = A.AsAtDate AND L.VariantID = UI.VariantID AND L.CurrencyCode = UI.CurrencyCode
        	LEFT JOIN tblSecurityCode M ON M.SecurityID = UI.SecurityID AND M.StartDate <= @AsAtDate AND M.EndDate > @AsAtDate AND M.CodeTypeID = 4   
        	JOIN tblSecurityProperty sp ON sp.SecurityID = UI.SecurityID AND sp.StartDate < @AsAtDate AND sp.EndDate > @AsAtDate                                                                                                                             
        	LEFT JOIN tblDistribution d ON d.ListingID = F.ListingID AND d.XdDate = CL.OpenDate AND d.CorporateActionSetID = 1
        WHERE  F.ListingID = @ListingID AND A.AsAtDate = @AsAtDate   
        ORDER BY A.AsAtDate DESC"""
    df_proc = db.db_SelectReq(str_req)
    return df_proc


def fDf_EasyFi_COELQC3_Proc(str_bbg):
    print('DEPREACTED')
    return -1
    str_req = """SET NOCOUNT ON; 
       DECLARE @RefFamilyID INT, @Filter VARCHAR(100), @ListingID INT, @PCFCurrency VARCHAR(255),
           @RIC VARCHAR(25), @CalculationMask INT, @ETFID INT, @BasketID INT, @BasketTypeID INT,
           @BasketName VARCHAR (20), @UnderlyingIndexCurrency char (3), @AsAtDate DATE, 
           @BasketType VARCHAR (20) = 'Creation', @CloseDate DATE, @Bloomberg varchar(50),
           @Code VARCHAR (30) = '""" + str_bbg + """'
        SELECT
        	@RefFamilyID = RefFamilyID,
        	@Filter = bp.Filter,
        	@ListingID = l.ListingID,
        	@PCFCurrency = l.CurrencyCode,
        	@RIC = lc.Code,
        	@CalculationMask = bp.CalculationMask,
        	@ETFID = e.ETFID,
        	@BasketID = b.BasketID,
        	@BasketTypeID = bt.BasketTypeID,
        	@BasketName = bt.Name,
        	@AsAtDate =f.OpenDate,
        	@CloseDate = f.CurrentDate
        FROM tblFamily f
        	INNER JOIN tblETF e ON e.FamilyID = f.FamilyID
        	INNER JOIN tblSecurity s ON s.SecurityID = e.SecurityID
        	INNER JOIN tblBasket b ON b.ETFID = e.ETFID
        	INNER JOIN tblBasketProperty bp ON bp.BasketID = b.BasketID AND bp.StartDate <= f.CurrentDate AND bp.EndDate > f.CurrentDate
        	INNER JOIN tblBasketType bt on bt.BasketTypeID = b.BasketTypeID
        	INNER JOIN tblListing l ON l.SecurityID = s.SecurityID
        	INNER JOIN tblListingCode lc ON lc.ListingID = l.ListingID AND lc.StartDate <=f.CurrentDate AND lc.EndDate >f.CurrentDate
        WHERE  lc.Code = @Code AND UPPER(bt.Name) = UPPER(@BasketType)
        
        SELECT '3' AS [Structure Line Counting Unit],
        	ROW_NUMBER () OVER (ORDER BY si.Code) AS [Counter Line],
        	sc.Code AS [ETF ID],
        	si.Code AS [Constituent ISIN], 
        	s.Name AS [Constituent Name], 
        	c.NumberOfUnits AS [Constituent Shares in the Creation Unit],
        	ISNULL(pe.Value,p.Value) AS [Dirty Price], 
        	c.NumberOfUnits * IsNull(c.PriceAdjustmentFactor, 1.0) *    
        		   CASE WHEN @CalculationMask & 1 > 0 THEN c.Factor1 ELSE 1 END *  
        		   CASE WHEN @CalculationMask & 2 > 0 THEN c.Factor2 ELSE 1 END *  
        		   CASE WHEN @CalculationMask & 4 > 0 THEN c.Factor3 ELSE 1 END *  
        		   CASE WHEN @CalculationMask & 8 > 0 THEN c.Factor4 ELSE 1 END *  
        		   CASE WHEN @CalculationMask & 16 > 0 THEN c.Factor5 ELSE 1 END *  
        		   CASE WHEN @CalculationMask & 32 > 0 THEN c.Factor6 ELSE 1 END *  
        		   CASE WHEN @CalculationMask & 64 > 0 THEN c.Factor7 ELSE 1 END *  
        		   CASE WHEN @CalculationMask & 128 > 0 THEN c.Factor8 ELSE 1 END *  
        		   CASE WHEN @CalculationMask & 256 > 0 THEN c.Factor9 ELSE 1 END * ISNULL(pe.Value,p.Value)   
        	AS [Market Value],  
        	CAST(NULL AS DECIMAL(28,14)) AS [Weighting in Percentage], 
        	'-' AS [Market Origin of Company],
        	'-' AS [Company Sector],
        	cu.MajorCurrencyCode AS [CCY],
        	bp.CleanPrice AS [CleanPrice], 
          bp.AccruedInterest AS [AccruedInterest]
        FROM tblConstituent c
        	INNER JOIN tblListing l ON l.ListingID = c.ListingID
        	INNER JOIN tblSecurity se ON se.SecurityID = l.SecurityID
        	INNER JOIN tblSecurityType st ON st.SecurityTypeID = se.SecurityTypeID
        	INNER JOIN tblSecurityProperty s ON s.SecurityID = l.SecurityID AND s.StartDate <= @AsAtDate AND s.EndDate > @AsAtDate
        	LEFT JOIN tblListingCode lcr ON lcr.ListingID = l.ListingID AND lcr.StartDate <= @AsAtDate AND lcr.EndDate > @AsAtDate 
        		AND lcr.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'Ric')
        	LEFT JOIN tblListingCode lcb ON lcb.ListingID = l.ListingID AND lcb.StartDate <= @AsAtDate AND lcb.EndDate > @AsAtDate 
        		AND lcb.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'Bloomberg')
        	LEFT JOIN tblListingCode lcs ON lcs.ListingID = l.ListingID AND lcs.StartDate <= @AsAtDate AND lcs.EndDate > @AsAtDate 
        		AND lcs.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'Sedol')
        	LEFT JOIN tblSecurityCode si ON si.SecurityID = l.SecurityID AND si.StartDate <= @AsAtDate AND si.EndDate > @AsAtDate 
        		AND si.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'Isin')
        	INNER JOIN tblExchange ex ON ex.ExchangeID = l.ExchangeID
        	INNER JOIN tblCurrency cu ON cu.CurrencyCode = l.CurrencyCode
        	LEFT JOIN tblPrice p ON p.ListingID = c.ListingID AND p.AsAtDate = @CloseDate
        	LEFT JOIN tblPriceException pe ON pe.ListingID = c.ListingID AND pe.FamilyID = c.FamilyID AND pe.AsAtDate = @CloseDate
        	JOIN tblETF e ON e.FamilyID = c.FamilyID
        	JOIN tblSecurityCode sc ON sc.SecurityID = e.SecurityID AND sc.StartDate <= @AsAtDate AND sc.EndDate > @AsAtDate AND sc.CodeTypeID = 4
        	LEFT JOIN [PRDCOB001WI].SolaFixedIncome.dbo.tblBondPrice bp on bp.FamilyID = c.FamilyID and bp.AsAtDate = @AsAtDate and bp.ListingID = c.ListingID
        WHERE c.StartDate <=@AsAtDate AND c.EndDate > @AsAtDate AND c.FamilyID = @RefFamilyID 
        	AND c.ConstituentType = (SELECT ConstituentType FROM tblConstituentType WHERE Name = 'Normal') AND c.FilterValue LIKE @Filter"""
    df_proc = db.db_SelectReq(str_req)
    return df_proc


def fDf_EasyFi_PCFELQC1_Proc(str_bbg):
    print('DEPREACTED')
    return -1
    str_req = """SET NOCOUNT ON; 
       DECLARE @Ric VARCHAR(30) ='""" + str_bbg + """',
          @BasketType VARCHAR (20) = 'Creation',
        	@RefFamilyID INT,
        	@Filter VARCHAR(100),
        	@ListingID INT,
        	@PCFCurrency VARCHAR(255),
        	@RIC VARCHAR(25),
        	@CalculationMask INT,
        	@ETFID INT,
        	@BasketID INT,
        	@BasketTypeID INT,
        	@BasketName VARCHAR (20),
        	@UnderlyingIndexCurrency char (3),
        	@ProductType varchar(50),
        	@ClassificationSchemeID int= 71,
        	@ETF_ISIN varchar(12),
        	@AsAtDate   DATE ,
        	@SecurityID int,
        	@iNavTicker varchar(50),
        	@Bloomberg varchar(50),
        	@GrossAmount numeric(28,12),
        	@OpenDate date, 
        	@PriceDate DATE
        
        SELECT
        	@RefFamilyID = RefFamilyID,
        	@Filter = bp.Filter,
        	@ListingID = l.ListingID,
        	@PCFCurrency = l.CurrencyCode,
        	@RIC = lc.Code,
        	@CalculationMask = bp.CalculationMask,
        	@ETFID = e.ETFID,
        	@BasketID = b.BasketID,
        	@BasketTypeID = bt.BasketTypeID,
        	@BasketName = bt.Name,
        	@AsAtDate =f.OpenDate,
        	@ETF_ISIN =  sc.Code
        FROM tblFamily f
        	INNER JOIN tblETF e ON e.FamilyID = f.FamilyID
        	INNER JOIN tblSecurity s ON s.SecurityID = e.SecurityID
        	INNER JOIN tblBasket b ON b.ETFID = e.ETFID
        	INNER JOIN tblBasketProperty bp ON bp.BasketID = b.BasketID AND bp.StartDate <= GETDATE() AND bp.EndDate > GETDATE()
        	INNER JOIN tblBasketType bt on bt.BasketTypeID = b.BasketTypeID
        	INNER JOIN tblListing l ON l.SecurityID = s.SecurityID
        	INNER JOIN tblListingCode lc ON lc.ListingID = l.ListingID 
        		AND lc.StartDate <= GETDATE() 
        		AND lc.EndDate > GETDATE() 
        		AND lc.CodeTypeID =10 
        	LEFT JOIN tblSecurityCode sc ON sc.SecurityID = s.SecurityID 
        		AND sc.StartDate <= GETDATE() 
        		AND	sc.EndDate > GETDATE() 
        		AND sc.CodeTypeID = 4
        WHERE  lc.Code = @Ric AND UPPER(bt.Name) = UPPER(@BasketType)
        		
        SELECT @ProductType=c.Code
        FROM tblListing l 
        	JOIN tblSecurity s On s.SecurityID = l.SecurityID
        	JOIN tblSecurityClassification sl On sl.SecurityID = l.SecurityID AND sl.StartDate <=@AsAtDate AND sl.EndDate >@AsAtDate
        	JOIN tblClassification c On c.ClassificationID = sl.ClassificationID
        WHERE ListingID = @ListingID AND c.ClassificationSchemeID=@ClassificationSchemeID
        
        SELECT @Bloomberg = Code 
        FROM tblListingCode GG 
        WHERE GG.ListingID = @ListingID 
        	AND GG.StartDate <= @AsAtDate 
        	AND GG.EndDate > @AsAtDate 
        	AND GG.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'Bloomberg')
        
        SELECT @iNavTicker = Code 
        FROM tblListingCode GG 
        WHERE  GG.ListingID = @ListingID 
        	AND GG.StartDate <= @AsAtDate 
        	AND GG.EndDate > @AsAtDate 
        	AND GG.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'iNavTicker') 
        
        ---- Assume dividend currency is the same as the base currency																				    
        SELECT @GrossAmount  = GrossAmount 
        FROM  tblDistribution d 
        WHERE d.ListingID = @ListingID AND d.XdDate = @OpenDate AND d.CorporateActionSetID = 1
        
        SELECT 'H' AS [Record Type]
        	,ISNULL(HH.Code,'') AS [iNAV ISIN Code]
        	,@ProductType AS [Category (Product Type)]
        	,H.ConstituentCount
        	,'1' AS [Update Count]
        	,C.OpenDate AS [iNAV Calculation Date]
        	,C.CurrentDate AS [NAV Valuation Date]
        	,A.NAV AS [NAV]
        	,'-' AS [Estimated NAV]
        	,'-' AS [Estimated NAV Valuation Date]
        	,H.EstimatedCash/A.Divisor AS [Cash Component of the NAV]
        	,'-' AS [Estimated Cash of the Next Trading Day NAV]
        	,A.SharesOutstanding AS [ETF Total Number of Outstanding Shares]
        	,A.NAV*A.Divisor AS [Value of One Creation Unit]
        	,A.Divisor AS [Number Shares of a Creation Unit]
        	,B.CurrencyCode AS [Trading Currency]
        	,UI.CurrencyCode AS [Underlying Index Currency] 
        	,A.CurrencyCode AS [NAV (base) Currency]
        	,G.Code AS [ETF ISIN Code]
        	,@RIC AS [ETF RIC Code]
        	,GG.Code AS [ETF BBG Code]
        	,M.Code AS [Underlying Index ID]
        	,II.Code [Indicative NAV ID]
        	,CASE WHEN d.GrossAmount IS NULL THEN '-' 
        		ELSE CAST(d.GrossAmount AS VARCHAR) END [Dividend Amount of One ETF Share]
        	,CASE WHEN d.XdDate IS NULL THEN '-' 
        		ELSE CAST(d.XdDate AS VARCHAR) END  [Dividend Ex-Date]	
        	,'-' AS [Exposure to Risky Assets]
        	,'-' AS [Reference Basket Level]
        	,'-' AS [NAV Floor]
        	,'-' AS [Multiplier]
        	,L.Value [Underlying Index Level] 
        FROM tblETFPosition A
        	INNER JOIN tblETF B ON B.ETFID = A.ETFID
        	INNER JOIN tblFamily C ON C.FamilyID = B.FamilyID
        	INNER JOIN tblSecurity D ON D.SecurityID = B.SecurityID
        	INNER JOIN tblSecurityProperty E ON E.SecurityID = D.SecurityID 
        		AND E.StartDate <= @AsAtDate 
        		AND E.EndDate > @AsAtDate
        	INNER JOIN tblListing F ON F.SecurityID = D.SecurityID
        	LEFT JOIN tblSecurityCode G ON G.SecurityID = D.SecurityID 
        		AND G.StartDate <= @AsAtDate 
        		AND G.EndDate > @AsAtDate 
        		AND G.CodeTypeID = (SELECT CodeTypeID FROM tblCodeType WHERE Name = 'Isin')
        	LEFT JOIN tblSecurityCode HH ON    HH.SecurityID = D.SecurityID 
        		AND HH.StartDate <= @AsAtDate 
        		AND HH.EndDate > @AsAtDate 
        		AND HH.CodeTypeID = (SELECT CodeTypeID FROM tblCodeType WHERE Name = 'iNAV ISIN')
        	LEFT JOIN tblListingCode GG ON GG.ListingID = F.ListingID 
        		AND GG.StartDate <= @AsAtDate 
        		AND GG.EndDate > @AsAtDate 
        		AND GG.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'Bloomberg')
        	LEFT JOIN tblListingCode II ON II.ListingID = F.ListingID 
        		AND II.StartDate <= @AsAtDate 
        		AND II.EndDate > @AsAtDate 
        		AND II.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'iNavTicker')
        	INNER JOIN tblBasketPosition H ON H.BasketID = @BasketID AND H.AsAtDate = A.AsAtDate
        	INNER JOIN tblListing UI ON UI.ListingID = B.ReferenceIndexListingID
        	INNER JOIN tblCalendarDateLite CL ON CL.CalendarID = C.CalendarID AND CL.AsAtDate = @AsAtDate
        	JOIN tblIndex K ON K.SecurityID = UI.SecurityID
        	JOIN tblIndexPosition L ON L.IndexID = K.IndexID AND L.AsAtDate = A.AsAtDate AND L.VariantID = UI.VariantID AND L.CurrencyCode = UI.CurrencyCode
        	LEFT JOIN tblListingCode M ON M.ListingID = B.ReferenceIndexListingID 
        		AND M.StartDate <= GETDATE () 
        		AND M.EndDate > GETDATE () 
        		AND M.CodeTypeID = 10																					  																		    
        	LEFT JOIN tblDistribution d ON d.ListingID = F.ListingID 
        		AND d.XdDate = CL.OpenDate 
        		AND d.CorporateActionSetID = 1
        WHERE  F.ListingID = @ListingID AND A.AsAtDate = @AsAtDate 
        ORDER BY A.AsAtDate DESC"""
    df_proc = db.db_SelectReq(str_req)
    return df_proc




def fDf_EasyFi_PCFELQC2_Proc(str_bbg):
    print('DEPREACTED')
    return -1
    str_req = """SET NOCOUNT ON; 
       DECLARE @Ric VARCHAR(30) ='""" + str_bbg + """',
          @BasketType VARCHAR (20) = 'Creation',
        	@RefFamilyID INT,
        	@Filter VARCHAR(100),
        	@ListingID INT,
        	@PCFCurrency VARCHAR(255),
        	@RIC VARCHAR(25),
        	@CalculationMask INT,
        	@ETFID INT,
        	@BasketID INT,
        	@BasketTypeID INT,
        	@BasketName VARCHAR (20),
        	@UnderlyingIndexCurrency char (3),
        	@ProductType varchar(50),
        	@ClassificationSchemeID int= 71,
        	@ETF_ISIN varchar(12),
        	@AsAtDate   DATE ,
        	@SecurityID int,
        	@iNavTicker varchar(50),
        	@Bloomberg varchar(50),
        	@GrossAmount numeric(28,12),
        	@OpenDate date, 
        	@PriceDate DATE
        
        SELECT
        	@RefFamilyID = RefFamilyID,
        	@Filter = bp.Filter,
        	@ListingID = l.ListingID,
        	@PCFCurrency = l.CurrencyCode,
        	@RIC = lc.Code,
        	@CalculationMask = bp.CalculationMask,
        	@ETFID = e.ETFID,
        	@BasketID = b.BasketID,
        	@BasketTypeID = bt.BasketTypeID,
        	@BasketName = bt.Name,
        	@AsAtDate =f.OpenDate,
        	@PriceDate=f.CurrentDate,
        	@ETF_ISIN =  sc.Code
        FROM tblFamily f
        	INNER JOIN tblETF e ON e.FamilyID = f.FamilyID
        	INNER JOIN tblSecurity s ON s.SecurityID = e.SecurityID
        	INNER JOIN tblBasket b ON b.ETFID = e.ETFID
        	INNER JOIN tblBasketProperty bp ON bp.BasketID = b.BasketID 
        		AND bp.StartDate <= GETDATE() 
        		AND bp.EndDate > GETDATE()
        	INNER JOIN tblBasketType bt on bt.BasketTypeID = b.BasketTypeID
        	INNER JOIN tblListing l ON l.SecurityID = s.SecurityID
        	INNER JOIN tblListingCode lc ON lc.ListingID = l.ListingID 
        		AND lc.StartDate <= GETDATE() 
        		AND lc.EndDate > GETDATE()  
        		AND lc.CodeTypeID =10 
        	LEFT JOIN tblSecurityCode sc ON sc.SecurityID = s.SecurityID 
        		AND sc.StartDate <= GETDATE() 
        		AND sc.EndDate > GETDATE() 
        		AND sc.CodeTypeID = 4
        WHERE  lc.Code = @Ric AND UPPER(bt.Name) = UPPER(@BasketType)
        
        SELECT 'B' AS [Record Type]
        	,@ETF_ISIN AS [ETF ID]
        	,st.Name AS [Constituent Type]
        	,si.Code AS [Constituent ISIN]
        	,lcr.Code AS [RIC]
        	,ISNULL(lcb.Code,'-') AS [Bloomberg]
        	,CASE WHEN ex.MIC ='NONE' THEN '-' ELSE '' END AS [Mic]
        	,s.Name AS [Constituent Name]
        	,c.NumberOfUnits AS [Constituent Shares in the Creation Unit]
        	,'-' AS [Corresponding Correlated Index Ric Code]
        	,'-' AS [Corresponding Correlated Index Factor]
        	,ROW_NUMBER () OVER(ORDER BY s.Name) AS [Counter line]
        	,ISNULL(pe.Value,p.Value) AS [Closing Price of the Constituent]
        	,'-' AS [Forex rate used to calculate the closing price used in NAV calculation]
        	,'T' AS [Trailer Record]
        	,@ETF_ISIN AS [ETF ID 2]
        	,c.NumberOfUnits * IsNull(c.PriceAdjustmentFactor, 1.0) *    
        		CASE WHEN @CalculationMask & 1 > 0 THEN c.Factor1 ELSE 1 END *  
        		CASE WHEN @CalculationMask & 2 > 0 THEN c.Factor2 ELSE 1 END *  
        		CASE WHEN @CalculationMask & 4 > 0 THEN c.Factor3 ELSE 1 END *  
        		CASE WHEN @CalculationMask & 8 > 0 THEN c.Factor4 ELSE 1 END *  
        		CASE WHEN @CalculationMask & 16 > 0 THEN c.Factor5 ELSE 1 END *  
        		CASE WHEN @CalculationMask & 32 > 0 THEN c.Factor6 ELSE 1 END *  
        		CASE WHEN @CalculationMask & 64 > 0 THEN c.Factor7 ELSE 1 END *  
        		CASE WHEN @CalculationMask & 128 > 0 THEN c.Factor8 ELSE 1 END *  
        		CASE WHEN @CalculationMask & 256 > 0 THEN c.Factor9 ELSE 1 END * ISNULL(pe.Value,p.Value) 
        	AS [Market Value]
        	,CAST(NULL AS DECIMAL(28,14)) AS [Weighting in Percentage]
        	,bp.CleanPrice AS [18]
        	,bp.AccruedInterest AS [19]
        FROM tblConstituent c
        	INNER JOIN tblListing l ON l.ListingID = c.ListingID
        	INNER JOIN tblSecurity se ON se.SecurityID = l.SecurityID
        	INNER JOIN tblSecurityType st ON st.SecurityTypeID = se.SecurityTypeID
        	INNER JOIN tblSecurityProperty s ON s.SecurityID = l.SecurityID 
        		AND s.StartDate <= @AsAtDate 
        		AND s.EndDate > @AsAtDate
        	LEFT JOIN tblListingCode lcr ON lcr.ListingID = l.ListingID 
        		AND lcr.StartDate <= @AsAtDate 
        		AND lcr.EndDate > @AsAtDate 
        		AND lcr.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'Ric')
        	LEFT JOIN tblListingCode lcb ON lcb.ListingID = l.ListingID 
        		AND lcb.StartDate <= @AsAtDate 
        		AND lcb.EndDate > @AsAtDate 
        		AND lcb.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'Bloomberg')
        	LEFT JOIN tblListingCode lcs ON lcs.ListingID = l.ListingID 
        		AND lcs.StartDate <= @AsAtDate 
        		AND lcs.EndDate > @AsAtDate 
        		AND lcs.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'Sedol')
        	LEFT JOIN tblSecurityCode si ON si.SecurityID = l.SecurityID 
        		AND si.StartDate <= @AsAtDate 
        		AND si.EndDate > @AsAtDate 
        		AND si.CodeTypeID = (select CodeTypeID from tblCodeType WHERE Name = 'Isin')
        	INNER JOIN tblExchange ex ON ex.ExchangeID = l.ExchangeID
        	INNER JOIN tblCurrency cu ON cu.CurrencyCode = l.CurrencyCode
        	LEFT JOIN tblPrice p ON p.ListingID = c.ListingID 
        		AND p.AsAtDate =@PriceDate 
        	LEFT JOIN tblPriceException pe ON pe.ListingID = c.ListingID 
        		AND pe.FamilyID = c.FamilyID 
        		AND pe.AsAtDate = @PriceDate
        	LEFT JOIN [PRDCOB001WI].SolaFixedIncome.dbo.tblBondPrice bp on bp.FamilyID = c.FamilyID 
        		and bp.AsAtDate = @AsAtDate 
        		and bp.ListingID = c.ListingID
        WHERE c.StartDate <=@AsAtDate 
        	AND c.EndDate > @AsAtDate 
        	AND c.FamilyID = @RefFamilyID 
        	AND c.FilterValue LIKE @Filter"""
    df_proc = db.db_SelectReq(str_req)
    return df_proc
