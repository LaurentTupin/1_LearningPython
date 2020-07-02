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
def fDf_phillipCap_GetPivotCode_wDiv(df_Compo, str_colName, str_folder, str_fileName, str_date):
    try:
        # Pivot Code
        l_ric = df_Compo[str_colName].tolist()
        str_req =  """{0}{1} SELECT Ric AS [{2}],Isin,Bloomberg,Sedol,ISNULL(XdDate,'{4}'),ISNULL(Sum(GrossAmount), 0) as GrossAmount
                        {1} FROM tblCodePivot sp {1} LEFT JOIN tblDistribution d on d.ListingID = sp.ListingID 
                            and CorporateActionTypeID in (1,2,69) {1} and CorporateActionSetID = 1
                            and XdDate = '{4}'
                        {1} WHERE Ric in ('{3}') 
                        {1} GROUP BY Ric,Isin,Bloomberg,Sedol,sp.ListingID,XdDate {1} order by Isin
                        """.format('SET NOCOUNT ON;', '\n', str_colName, "','".join(l_ric), str_date)
        df_codePivot = db.fDf_GetRequest_or_fromCsvFile(str_req, str_fileName, 1, str_folder)
        df_codePivot.fillna(value = '', inplace = True)
    except: 
        print('ERROR fDf_phillipCap_GetPivotCode_wDiv')
        raise
    return df_codePivot



def WisdomTree_GetPivotCode(df_Compo, str_colName, str_folder, str_fileName):
    try:
        # Pivot Code
        l_bbg = df_Compo[str_colName].tolist()
        str_req =  """{0}{1} SELECT Bloomberg AS [{2}], CurrentName, Mic, CurrencyCode, Ric 
                        {1} FROM SolaDBServer..tblCodePivot {1} WHERE Bloomberg IN ('{3}') 
                        """.format('SET NOCOUNT ON;', '\n', str_colName, "','".join(l_bbg))
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
    str_folderDateFormat = str(df_Param.loc[row, 'folderDate'])
    str_dteFormat_DirSource = str(df_Param.loc[row, 'dteFormat_DirSource'])
    folderDateOffset = df_Param.loc[row, 'folderDateOffset']
    CalendarID = df_Param.loc[row, 'DateCalendarID']
    str_Zip_Date = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, str_dteFormat_DirSource, int(folderDateOffset), str(CalendarID))
    str_folderDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, str_folderDateFormat, int(folderDateOffset), str(CalendarID))
    str_ZipPath = df_Param.loc[row, 'Dir_Source']
    str_ZipPath = str_ZipPath.replace('{dteFormat_DirSource}', str_Zip_Date)
    str_ZipPath = str_ZipPath.replace('{folderDate}', str_folderDate)
    # Put root folder or not
    str_ZipPath = fl.fStr_BuildFolder_wRoot(str_ZipPath, str_folderRoot)
    #if not str_ZipPath[:2] == '\\\\': str_ZipPath = str_folderRoot + str_ZipPath
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
    str_outlkAcctName = str(df_Param.loc[row, 'outlook_Acct'])
    str_outlkMailbox = str(df_Param.loc[row, 'outlook_mailBox'])
    str_folder = str(df_Param.loc[row, 'outlook_folder'])
    str_folderToArchive = str(df_Param.loc[row, 'outlook_folderToArchive'])
    str_mailSubject = str(df_Param.loc[row, 'outlook_subject'])
    str_to = str(df_Param.loc[row, 'outlook_To'])
    str_cc = str(df_Param.loc[row, 'outlook_Cc'])
    str_ExactName = str(df_Param.loc[row, 'File_ExactName'])
    int_File_startW = df_Param.loc[row, 'File_startW']
    int_File_endW = df_Param.loc[row, 'File_endW']
    if str_ExactName.lower() == 'true':
        str_File_startW = str_FileName
        str_File_endW = ''
    else:
        str_File_startW = str_FileName[:int(int_File_startW)]
        if int_File_endW == 0:          str_File_endW = ''
        else:                           str_File_endW = str_FileName[-int(int_File_endW):]
    
    # With Class, version Jun 2020
    inst_outlookMail = out.c_outlookMail()
    inst_outlookMail.outlk_DefineOutlook('MAPI')
    inst_outlookMail.outlk_getAccount(str_outlkAcctName)
    inst_outlookMail.outlk_DefineFolder(str_outlkMailbox, [str_folder])
    inst_outlookMail.outlk_GetMails()
    inst_outlookMail.outlk_FilterMails(str_mailSubject, str_to, str_cc, str_File_startW, str_File_endW)
    #==============================================================================================
    # If the Mail cannot be found, We search in Inbox (and move it to the right folder using the Archive functionality)
    if inst_outlookMail.o_mails == False and str_folder != '':
        print(' EMPTY: Cannot Get the Mail in the folder {}'.format(str_folder))
        print(' -> We will search in MailBox: #', str_outlkMailbox, '#')
        bl_ArchiveMails = True
        str_folderToArchive = str_folder
        str_folder = ''
        inst_outlookMail.outlk_DefineFolder(str_outlkMailbox, [str_folder])
        inst_outlookMail.outlk_GetLastMails()
        inst_outlookMail.outlk_FilterMails(str_mailSubject, str_to, str_cc, str_File_startW, str_File_endW)
    #==============================================================================================
    inst_outlookMail.outlk_GetLatestMail()
    inst_outlookMail.outlk_DownloadEmailsPJ(str_folderRaw, str_File_startW, str_File_endW)
    # Archive PJ
    if bl_ArchiveMails:
        inst_outlookMail.outlk_DefineArchiveFolder([str_folderToArchive])
        inst_outlookMail.outlk_ArchiveEmail()
    # END
    if inst_outlookMail.l_docDownloaded == []:
        return False
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
def Act_DownFiles_SQL(df_Param, row, str_folderRaw, str_FileName, dte_date, bl_EmptyMessage = True):
    # Param
    str_PCF = str(df_Param.loc[row, 'PCF'])
    str_req = fStr_generateSQLReq(df_Param, row, dte_date)
    # Execute Req
    try:
        df_sql = db.db_SelectReq(str_req, bl_EmptyMessage = bl_EmptyMessage)
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
                str_pathSource = df_Param.loc[row, 'Dir_Source'].replace('{dteFormat_DirSource}', 
                                             (dte_date + BDay(int(df_Param.loc[row, 'DateOffset']))).strftime(df_Param.loc[row, 'dteFormat_DirSource']))
                str_pathSource = fl.fStr_BuildFolder_wRoot(str_pathSource, str_folderRoot)
                #if not str_pathSource[:2] == '\\\\': str_pathSource = str_folderRoot + str_pathSource
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
        # SQL
        elif str_FileDownloadMode == 'SQL_noMsg':
            bl_success = Act_DownFiles_SQL(df_Param, row, str_folderRaw, str_FileName, dte_date, bl_EmptyMessage = False)
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
            elif 'FX 5.30PM' in str_FileName.upper():
                df_data = pd.read_csv(str_path, header = bl_header, skiprows = 1)
            elif 'WISDOMTREEUCITS_BSKT' in str_FileName.upper():
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
    str_folderRaw = fl.fStr_BuildFolder_wRoot(str_folderRaw, str_folderRoot)
    #if str_Dir_Dest[:2] != '\\\\': str_folderRaw = str_folderRoot + str_folderRaw
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


#------------------------------------------------------------------------------
# Function for SG Easy Msci
#------------------------------------------------------------------------------
def fDf_loopOnRic_SqlReq_SaveCsv(df_lConfig, str_req, dte_date, str_folder, str_filenameExtension = ''):
    inst_db = db.c_sqlDB()
    inst_db.server = 'D1PRDSOLADB.infocloud.local'
    str_cloudPathForCsv = inst_db.cloudPathForCsv
    #inst_db.cloudPathForCsv = str_folder + r'\raw'
    d_Df = {}
    for i_row, t_row in df_lConfig.iterrows():
        str_IndexRic = t_row['IndexRic']
        if not str_IndexRic in d_Df:        #Avoid Double
            str_fileName =  '{}{}.txt'.format(t_row['Pcf_FileName'].replace('PCF',''), str_filenameExtension)
            str_req_loop = str_req.replace('<RIC>', str_IndexRic).replace('<DATE>', dte_date.strftime('%Y%m%d'))
            df_sqlResult = db.fDf_GetRequest_or_fromCsvFile(str_req_loop, str_fileName, 30, str_folder + r'raw', bl_EmptyMessage = False)
            #            df_sqlResult = db.db_SelectReq(str_req_loop, 'D1PRDSOLADB.infocloud.local', bl_EmptyMessage = False)
            #            # Save a CSV to keep it
            #            fl.fStr_CreateTxtFile(fl.fStr_BuildPath(str_folder + r'\raw', str_fileName), '', df_sqlResult)
            # Save into dictionary
            d_Df[str_IndexRic] = df_sqlResult
        else:   pass
    inst_db.cloudPathForCsv = str_cloudPathForCsv
    return d_Df

def fDf_loopOnRic_CreateFile(d_param):
    df_lConfig =    d_param['df_lConfig']
    df_1NavIndic =  d_param['df_1NavIndic']
    df_2Val_Dmc =   d_param['df_2Val_Dmc']
    d_CompoDf =     d_param['d_CompoDf']
    d_CorpActDf =   d_param['d_CorpActDf']
    dte_date =      d_param['dte_date']
    dte_navDate =   d_param['dte_navDate']
    str_folder =    d_param['str_folder']
    l_pathAttach = []
    for i_row, t_row in df_lConfig.iterrows():
        # GET INPUT
        str_IndexRic =  t_row['IndexRic']
        str_ric =       t_row['ETF_RIC']
        str_isin =      t_row['Isin']
        int_divisor =   t_row['Divisor']
        # NAV Df
        flt_nav = df_1NavIndic[df_1NavIndic['Fund Code'] == str_isin]['Calculated Target Nav'].values[0]
        flt_TotalNav = flt_nav * int_divisor
        flt_shareNb = df_2Val_Dmc[df_2Val_Dmc['ISIN Code'] == str_isin]['Share Nb'].values[0]
        flt_indexReturn = df_1NavIndic[df_1NavIndic['Fund Code'] == str_isin]['Index Return Converted'].values[0]
        # Dataframe from dico
        df_compo =  d_CompoDf[str_IndexRic].copy()
        df_CA =     d_CorpActDf[str_IndexRic][['Isin','NetAmount']].copy()
        df_compo =  dframe.fDf_JoinDf(df_compo, df_CA, 'Isin', str_how = 'left')
        # Calculate WEIGHT
        df_compo['Weight'] = df_compo['IndexQuantity'] * df_compo['UnadjustedPrice'] * df_compo['FXRate']
        flt_sumProduct = df_compo['Weight'].sum()
        df_compo['Weight'] = df_compo['Weight'] / flt_sumProduct
        
        #-------------------
        # PCF - COMPO
        #-------------------
        df_compo['1col'] = 'B'
        df_compo['2col'] = t_row['Isin']
        df_compo['3col'] = 'Equity'
        df_compo['6col'] = '-'
        df_compo = dframe.fDf_InsertColumnOfIndex(df_compo, l_colSort = ['Ric'])
        df_compo['15col'] = 'T'
        df_compo.fillna({'NetAmount' : 0}, inplace = True)
        df_compo['PRICE'] = (df_compo['UnadjustedPrice'] - df_compo['NetAmount']) * df_compo['FXRate']
        df_compo['PRICE_r'] = df_compo['PRICE'].apply(lambda x:round(x, 4))
        df_compo['FXRate_r'] = df_compo['FXRate'].apply(lambda x:round(x, 4))
        df_compo['UNIT'] = flt_TotalNav * df_compo['Weight'] / df_compo['UnadjustedPrice']
        df_compo['UNIT_r'] = df_compo['UNIT'].apply(lambda x:round(x, 4))
        # Get the cash
        df_compo['CASH']  = df_compo['UNIT'] * df_compo['FXRate'] * df_compo['NetAmount']
        flt_cash = df_compo['CASH'].sum() / int_divisor
        t_row['flt_cash'] = flt_cash
        # Get Number of rows in Composition
        int_nbCompo = len(df_compo)
        t_row['int_nbCompo'] = int_nbCompo
        # FINAL COMPO
        df_compo_pcf = df_compo[['1col','2col','3col','Isin','Ric','6col','MIC','SecurityName', 'UNIT_r','6col','6col',
                                 'ind','PRICE_r','FXRate_r','15col','Isin']].copy()
        #-------------------
        # PCF - Header
        #-------------------
        df_header = pd.DataFrame([['H', t_row['ISINiNAV'], t_row['EuronextCategory'], int(int_nbCompo), '1',
                                  dte_date.strftime('%Y%m%d'), dte_navDate.strftime('%Y%m%d'), round(flt_nav, 4),
                                  '-','-', round(flt_cash, 13),'-', int(flt_shareNb), round(flt_nav * int_divisor, 4),
                                  str(int_divisor), t_row['ETF CCY'], t_row['Underlying index CCY'], t_row['ETF CCY'],
                                  str_isin, str_ric, t_row['ETF BBG Code'],t_row['UnderlyingIndexRIC'],
                                  t_row['Indicative NAV ID'],'-','-','-','-','-','-',flt_indexReturn]]
                                , columns = range(30))
        # CONCAT
        df_pcf = dframe.fDf_Concat_wColOfDf1(df_header, df_compo_pcf)
        # Create PCF Files
        str_pcfFilename =  '{}{}.txt'.format(t_row['Pcf_FileName'], dte_date.strftime('%Y%m%d'))
        str_path = fl.fStr_CreateTxtFile(str_folder, str_pcfFilename, df_pcf)
        l_pathAttach.append(str_path)
        
        #-------------------
        # CO - COMPO
        #-------------------
        df_compo['1col'] = '3'
        df_compo['SHARES'] = df_compo['UNIT'].apply(lambda x:round(x, 0))
        df_compo['MCap'] = df_compo['SHARES'] * df_compo['PRICE_r']
        df_compo['Weight_100'] = df_compo['Weight'] * 100
        df_compo['CO'] = df_compo['Isin'].apply(lambda str_isin : str_isin[:2])
        # FINAL COMPO
        df_compo_CO = df_compo[['1col','ind','2col','Isin','SecurityName','SHARES','PRICE_r','MCap', 'Weight_100','CO','6col']].copy()
        #-------------------
        # CO - Header
        #-------------------
        df_compo['CASH'] = (df_compo['UNIT_r'] - df_compo['SHARES']) * df_compo['PRICE_r']
        flt_cash = df_compo['CASH'].sum()
        df_header_1 = pd.DataFrame([['1','-', str_isin, t_row['TrackerMnemoCode'], t_row['ETF Name'], '-', t_row['UnderlyingName'],
                                     t_row['ISINiNAV'], '-', t_row['iNAVName'], t_row['ManagementStyle'], t_row['Category'], t_row['Region'], 
                                     '-', t_row['InvestableUniverse'], '-', str_isin, '-', '-','']]
                                , columns = range(20))
        df_header_2 = pd.DataFrame([['2', dte_date.strftime('%Y%m%d'), str_isin, str(int_divisor), int_divisor*round(flt_nav, 4),
                                     round(int_divisor * flt_nav - flt_cash, 2), round(flt_nav, 4), flt_cash, 100*flt_cash / (int_divisor*flt_nav), 
                                     t_row['ETF CCY'], int(flt_shareNb), round(flt_shareNb * flt_nav, 2), '-', '-', '-', t_row['ManagementFee'],
                                     round(flt_nav, 4), dte_navDate.strftime('%Y%m%d'), flt_indexReturn, dte_date.strftime('%Y%m%d')]]
                                , columns = range(20))
        # CONCAT
        df_pcf = dframe.fDf_Concat_wColOfDf1(df_header_1, df_header_2)
        df_pcf = dframe.fDf_Concat_wColOfDf1(df_pcf, df_compo_CO)
        # Create PCF Files
        str_COfilename =  '{}_{}.txt'.format(t_row['CO_FileName'], dte_date.strftime('%Y%m%d'))
        str_path = fl.fStr_CreateTxtFile(str_folder, str_COfilename, df_pcf)
        l_pathAttach.append(str_path)
        
    return l_pathAttach



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






