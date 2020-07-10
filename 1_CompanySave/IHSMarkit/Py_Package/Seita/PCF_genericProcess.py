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
    df = df1.copy()
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
                    flt_1 = dframe.round_Correction(float(df1.loc[i_row, i_col]), 10)
                    flt_2 = dframe.round_Correction(float(df2.loc[i_row, i_col]), 10)
                    flt_diff = flt_1 - flt_2
                    if flt_diff == 0:   flt_diffPourc = 0
                    elif flt_2 == 0:    flt_diffPourc = 100
                    else:               flt_diffPourc = 100 * (flt_diff / flt_2)
                    
                    # If difference is very small (to avoid rounding too small)
                    if abs(flt_diff) < 0.001 and abs(flt_diffPourc) < 0.001:
                        df.loc[i_row, i_col] = ''
                        bl_ColToKeep = False
                    else:
                        df.loc[i_row, i_col] = str(flt_1) + ' || ' + str(flt_2) \
                                            + ' | Diff: ' + str(dframe.round_Correction(flt_diff,1)) \
                                            + ' | Diff%: ' + str(dframe.round_Correction(flt_diffPourc, 2))
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
                str_fileName = Path.split('\\')[-1]
                str_folder = '\\'.join(Path.split('\\')[:-1])
                if str_FileUploadMode == 'FTP':               
                    bl_success = ftp.fBl_ftpUpFile_Bi(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_fileName, str_folder)
                elif str_FileUploadMode == 'FTP_SSL':         
                    bl_success = ftp.fBl_ftpUpFile_Bi(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_fileName, str_folder, -1, True)
                elif str_FileUploadMode == 'SFTP_Paramiko':   
                    bl_success = ftp.ssh_upFile(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_fileName, str_folder)
                #Store Result
                if not bl_success:          bl_success_final = False
        except:
            print(' ERROR: on UPLOAD file')
            print(' - str_pcf: ', str_pcf, ' | str_FileUploadMode', str_FileUploadMode)
            print(' - str_fileName: ', str_fileName)
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
                str_fileName = Path.split('\\')[-1]
                if str_fileName in l_fileInFtp:
                    l_ListFilesFTP.append('OK : {}'.format(str_fileName))
                else:
                    l_ListFilesFTP.append('KO : {}'.format(str_fileName))
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




def fStr_GetSourceDirectory(df_Param, row, dte_date, str_folderRoot):
    # Get the Dir Source
    str_DirSource = df_Param.loc[row, 'Dir_Source']
    CalendarID = df_Param.loc[row, 'DateCalendarID']
    
    # Replace Date with Date of Folder
    dteFormat_folder = str(df_Param.loc[row, 'folderDate'])
    folderDateOffset = str(df_Param.loc[row, 'folderDateOffset'])
    str_folderDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, dteFormat_folder, int(folderDateOffset), str(CalendarID))
    str_DirSource = str_DirSource.replace('{folderDate}', str_folderDate)
    
    # Replace Date with specific Date of Directory Source
    dteFormat_DirSource = str(df_Param.loc[row, 'dteFormat_DirSource'])
    DateOffset_DirSouce = df_Param.loc[row, 'DateOffset_DirSouce']
    str_DirSourceDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, dteFormat_DirSource, int(DateOffset_DirSouce), str(CalendarID))
    str_DirSource = str_DirSource.replace('{dteFormat_DirSource}', str_DirSourceDate)
    
    # Put root folder or not
    str_DirSource = fl.fStr_BuildFolder_wRoot(str_DirSource, str_folderRoot)
    #if not str_DirSource[:2] == '\\\\': str_DirSource = str_folderRoot + str_DirSource
    return str_DirSource


def fStr_ZipFilePath(df_Param, row, dte_date, str_folderRoot):
    str_ZipPath = fStr_GetSourceDirectory(df_Param, row, dte_date, str_folderRoot)
    
    # Replace the XXXX in the string
    if str_ZipPath.count('{') and str_ZipPath.count('}') > 0:
        str_folder = '\\'.join(str_ZipPath.split('\\')[:-1]) + '\\'
        str_fileName = str_ZipPath.split('\\')[-1]
        if str_fileName.count('{X}') > 0:   bl_exactNumberX = False
        elif str_fileName.count('{*}') > 0: bl_exactNumberX = False
        else:                               bl_exactNumberX = True
        str_fileName = fl.fStr_GetMostRecentFile_InFolder(str_folder, str_fileName, bl_exactNumberX = bl_exactNumberX)
        if str_fileName == '': raise
        str_ZipPath =  str_folder + str_fileName
    return str_ZipPath


#-----------------------------------------------------------------------------------------------------
# Main Function to download
#-----------------------------------------------------------------------------------------------------
def Act_DownFiles_outlook(df_Param, row, str_folderRaw, str_fileName, bl_ArchiveMails):
    # Param
    str_outlkAcctName = str(df_Param.loc[row, 'outlook_Acct'])
    str_outlkMailbox = str(df_Param.loc[row, 'outlook_mailBox'])
    str_folder = str(df_Param.loc[row, 'outlook_folder'])
    str_folderToArchive = str(df_Param.loc[row, 'outlook_folderToArchive'])
    str_mailSubject = str(df_Param.loc[row, 'outlook_subject'])
    str_to = str(df_Param.loc[row, 'outlook_To'])
    str_cc = str(df_Param.loc[row, 'outlook_Cc'])
    str_File_startW, str_File_endW = fStr_SplitFileName_startEnd(str_fileName, str(df_Param.loc[row, 'File_ExactName']),
                                                                 df_Param.loc[row, 'File_startW'],df_Param.loc[row, 'File_endW'])
    #    str_ExactName = str(df_Param.loc[row, 'File_ExactName'])
    #    int_File_startW = df_Param.loc[row, 'File_startW']
    #    int_File_endW = df_Param.loc[row, 'File_endW']
    #    if str_ExactName.lower() == 'true':
    #        str_File_startW = str_fileName
    #        str_File_endW = ''
    #    else:
    #        str_File_startW = str_fileName[:int(int_File_startW)]
    #        if int_File_endW == 0:          str_File_endW = ''
    #        else:                           str_File_endW = str_fileName[-int(int_File_endW):]
    
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
def Act_DownFiles_FTP(df_Param, row, str_folderRaw, str_fileName, str_FileDownloadMode, dte_date):
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
    #    str_File_startW = str_fileName[:int(int_File_startW)]
    #    if int_File_endW == 0:      str_File_endW = ''
    #    else:                       str_File_endW = str_fileName[-int(int_File_endW):]
    
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
            l_files = fl.fL_GetFileList_withinModel(l_files, str_fileName)
            # 1.c. Sort by Alphabet because Time will be the only difference if several files
            l_files.sort(reverse = True)
            # 1.d. Final Name of the file
            str_fileName = l_files[0]
            print('  * We found in FTP the complete name: ', str_fileName)
            str_NewFileName = str_fileName
        
    #--------------------------------------------------------------------------
    # DOWNLOAD
    #--------------------------------------------------------------------------
    try:
        if str_FileDownloadMode == 'FTP':               ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_fileName, str_folderRaw)
        elif str_FileDownloadMode == 'FTP_SSL':         ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_fileName, str_folderRaw, -1, True)
        elif str_FileDownloadMode == 'SFTP_Paramiko':   ftp.ssh_downFile(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_fileName, str_folderRaw)
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
        print('   ' + str_FileDownloadMode + ' did not find the file: ', str_fileName, '   || PCF: ' + str_PCF, '   || Download mode: ' + str_FileDownloadMode)
        print('   **Try Again : Offset was: ' + str(DateOffset) + ' | And is now: ' + str(int(DateOffset) - 1))
        
        str_NewDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, str_fileDate, int(DateOffset) - 1, str(CalendarID))
        str_fileName = df_Param.loc[row, 'fileName'].replace('{fileDate}', str_NewDate)
        str_NewFileName = str_fileName
        
        # Change df_Param for the next Offset (if d-1 become d-2, d-2 needs to become d-3)
        df_Param.loc[(df_Param.PCF == str_PCF) & (df_Param.ID == str_id), 'DateOffset'] = df_Param['DateOffset'] - 1
        #df_Param.loc[(df_Param.PCF == str_PCF) & (df_Param.FileDownloadMode == str_FileDownloadMode),'DateOffset'] = df_Param['DateOffset'] - 1
        #df_Param.loc[(df_Param.PCF==str_PCF) & (df_Param.FileDownloadMode==str_FileDownloadMode),'DateOffset'].apply(lambda x: x-1)
        
        try:
            if str_FileDownloadMode == 'FTP':
                ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_fileName, str_folderRaw)
                print('   File Successfully downloaded... ' + str_fileName + '\n\n')
            elif str_FileDownloadMode == 'FTP_SSL':
                ftp.fBl_ftpDownFileBinary(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_fileName, str_folderRaw, -1, True)
                print('   File Successfully downloaded (ftp + SSL)... {}\n\n').format(str_fileName)
            elif str_FileDownloadMode == 'SFTP_Paramiko':
                ftp.ssh_downFile(str_FTP_server, str_FTP_uid, str_FTP_pwd, l_ftpFolder, str_fileName, str_folderRaw)
                print('   File Successfully downloaded (sftp)... {}\n\n').format(str_fileName)
        except: 
            print('     ERROR * 2: We could not download from ' + str_FileDownloadMode + '\n\n')
            return False
    return True


#------------------------------------------------------------------------------------------------------------------------------------
def Act_DownFiles_SQL(df_Param, row, str_folderRaw, str_fileName, dte_date, bl_EmptyMessage = True):
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
        str_Path = os.path.join(str_folderRaw, str_fileName)
        df_sql.to_csv(str_Path, index = False, header = True)
    except:
        print('     ERROR in Act_DownFiles_SQL: We could not save the DF in PCF: ', str_PCF)
        print('     ', str_Path)
        return False
    return True
	
#------------------------------------------------------------------------------------------------------------------------------------
def Act_DownFiles_ZIP(df_Param, row, str_folderRaw, str_fileName, dte_date, str_folderRoot):
    str_zipPwd = str(df_Param.loc[row, 'zipPassword'])
    try:        str_ZipPath = fStr_ZipFilePath(df_Param, row, dte_date, str_folderRoot)
    except:
        print('  ERROR in Act_DownFiles_ZIP')
        print('  Could not find the path of the ZIP (str_ZipPath)')
        return False
    # Extarct the right file
    try:        fl.ZipExtractFile(str_ZipPath, str_folderRaw, str_fileName, str_zipPassword = str_zipPwd)
    except:
        print('    ERROR in Act_DownFiles_ZIP')
        print('    str_ZipPath: ' , str_ZipPath)
        return False
    return True

 
#------------------------------------------------------------------------------------------------------------------------------------		
def Act_DownFiles(df_Param, row, str_folderRaw, str_fileName, dte_date, str_folderRoot, bl_ArchiveMails):
    try:
        # Param
        str_path = fl.fStr_BuildPath(str_folderRaw, str_fileName)
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
            bl_success = Act_DownFiles_outlook(df_Param, row, str_folderRaw, str_fileName, bl_ArchiveMails)
            if not bl_success: 
                return False
        # Folder
        elif str_FileDownloadMode == 'FOLDER':
            try:
                str_pathSource = fStr_GetSourceDirectory(df_Param, row, dte_date, str_folderRoot)
                # in case of undefined Name like {X}: We want to deal with the list of files
                if str_fileName.count('{') and str_fileName.count('}') > 0:
                    if str_fileName.count('{X}') > 0:   bl_exactNumberX = False
                    elif str_fileName.count('{*}') > 0: bl_exactNumberX = False
                    else:                               bl_exactNumberX = True
                    l_FileInFolder = fl.fL_GetFileListInFolder(str_pathSource, str_fileName.replace('{*}','{X}'), bl_exactNumberX = bl_exactNumberX)
                    # Copy all the files
                    for pathSource in l_FileInFolder:
                        fileName = pathSource.split('\\')[-1]
                        shutil.copyfile(pathSource, fl.fStr_BuildPath(str_folderRaw, fileName))
                else:
                    shutil.copyfile(os.path.join(str_pathSource, str_fileName), str_path)
            except Exception as err:
                print('   ERROR in Act_DownFiles: {}'.format(str(err)))
                print('   - str_pathSource: ', str_pathSource)
                print('   - str_fileName: ', str_fileName)
                return False
        # FTP
        elif str_FileDownloadMode == 'FTP':
            bl_success = Act_DownFiles_FTP(df_Param, row, str_folderRaw, str_fileName, str_FileDownloadMode, dte_date)
            if str_NewFileName != '': str_fileName = str_NewFileName
            if not bl_success: return False
        # FTP
        elif str_FileDownloadMode == 'FTP_SSL':
            bl_success = Act_DownFiles_FTP(df_Param, row, str_folderRaw, str_fileName, str_FileDownloadMode, dte_date)
            if str_NewFileName != '': str_fileName = str_NewFileName
            if not bl_success: return False
        # FTP paramiko
        elif str_FileDownloadMode == 'SFTP_Paramiko':
            bl_success = Act_DownFiles_FTP(df_Param, row, str_folderRaw, str_fileName, str_FileDownloadMode, dte_date)
            if str_NewFileName != '': str_fileName = str_NewFileName
            if not bl_success: return False
        # SQL
        elif str_FileDownloadMode == 'SQL':
            bl_success = Act_DownFiles_SQL(df_Param, row, str_folderRaw, str_fileName, dte_date)
            if not bl_success: return False
        # SQL
        elif str_FileDownloadMode == 'SQL_noMsg':
            bl_success = Act_DownFiles_SQL(df_Param, row, str_folderRaw, str_fileName, dte_date, bl_EmptyMessage = False)
            if not bl_success: return False
        # ZIP
        elif str_FileDownloadMode == 'ZIP':
            bl_success = Act_DownFiles_ZIP(df_Param, row, str_folderRaw, str_fileName, dte_date, str_folderRoot)
            # If its this file, do not return an error (as he is here only sometimes)
            if not 'HKGRFMHKSSET_ST-FM-TX' in str_fileName:
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
                fl.fStr_CreateTxtFile(str_folderRaw, str_fileName, df_fut, '', True)
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
            fl.fStr_createExcel_1Sh(str_folderRaw, str_fileName, df_result, str_SheetName, False)
        elif str_FileDownloadMode == 'HTML_csv_SOUP':
            df_result = html.fDf_htmlGetArray_Soup(str_url_2, True, bl_waitTranslate)
            df_result.to_csv(str_path, header = False, index = False)
        elif str_FileDownloadMode == 'NO_DOWNLOAD':
            print(' - Is is FINE: No file to download - Only to load')
            
        # Renaming the INPUT Files
        if not str_File_PrefixName == '':
            try: fl.Act_Rename(str_folderRaw, str_fileName, str_File_PrefixName + str_fileName)
            except: print(' ERROR: Act_Rename')
    except: 
        print(' ERROR: in Act_DownFiles')
        return False
    return True
    
    
#------------------------------------------------------------------------------------------------------------------------------------
def fDf_getDfFromPCF(df_Param, row, str_folder, str_fileName, bl_header = 0, v_sheetName = '', str_sep = ',', l_names = None, str_encoding = None):
    str_path = os.path.join(str_folder, str_fileName)
    # Test if the file exist
    if not fl.fBl_FileExist(str_path):
        print('   File does not exist (fDf_getDfFromPCF)')
        print('   - Path: ', str_path)
        return None
    # Try to read
    try:        
        # ------- XLSX -------
        if '.XLSX' in str_fileName.upper() or '.XLS' in str_fileName.upper():
            if v_sheetName == '':   df_data = pd.read_excel(str_path, header = bl_header)
            else:                   df_data = pd.read_excel(str_path, header = bl_header, sheet_name = v_sheetName)
            
        # ------- FLat File -------
        elif [x for x in ['.CSV', '.TXT', '.HDX', '.ETF', '.XML', '.XSD', '718708NETRCNH'] if x in str_fileName.upper() or x in str_folder.upper()]:
            if '.HDX' in str_fileName.upper():          
                bl_header = 1
                str_sep = '\t'
            elif [x for x in ['SG_EASY', 'Easy Commodity - open'] if x in str_fileName.upper() or x in str_folder.upper()]:
                str_sep = '\t'
                str_encoding = 'cp1252'
            #df_data = pd.read_csv(str_path, header = bl_header, sep = str_sep)
            df_data = dframe.fDf_readCsv_enhanced(str_path, bl_header = bl_header, str_sep = str_sep, str_encoding = str_encoding)
            
        # ------- ZIP -------
        elif '.ZIP' in str_fileName.upper():
            df_data = 1
        else:
            print('---------------------------')
            print('  (**) We do not know how to take DF from this kind of files | We need to define a type in fDf_getDfFromPCF...')
            print('  - str_fileName: ', str_fileName)
            print('---------------------------')
            return None
    except Exception as err:
        print('   ERROR in fDf_getDfFromPCF : df_data could not be read')
        print('   - Error: ', str(err))
        print('   - str_folder', str_folder)
        print('   - str_fileName', str_fileName)
        print('   - bl_header', bl_header)
        print('   - v_sheetName', v_sheetName)
        print('   - str_sep', str_sep)
        return None
    return df_data




#------------------------------------------------------------------------------------------------------------------------------------
def fDf_getDfFromDownloaded(df_Param, row, str_folderRaw, str_fileName, bl_header = 0):
    # Renaming the INPUT Files
    try:
        str_SheetName = str(df_Param.loc[row, 'SheetName'])
        str_File_PrefixName = str(df_Param.loc[row, 'File_PrefixName'])
        if not str_File_PrefixName == '': 
            str_fileName = str_File_PrefixName + str_fileName
    except: print('  Renaming did not work in fDf_getDfFromDownloaded !!!')
    
    print('Searching for... ' + str_fileName)
    str_path = os.path.join(str_folderRaw, str_fileName)
    
    # Test if the file exist
    if not fl.fBl_FileExist(str_path):
        print('   File does not exist (fDf_getDfFromDownloaded)')
        print('   - Path: ', str_path)
        return None, False
    
    # Get the DataFrame from the file
    try:        
        # ------- XLSX -------
        if '.XLSX' in str_fileName.upper() or '.XLS' in str_fileName.upper():
            if 'NQ100' in str_fileName.upper() and 'DEALING ' in str_fileName.upper():
                df_data = pd.read_excel(str_path, header = 1)            
            elif 'LAST-VALUATION-MARKIT' in str_fileName.upper():
                df_data = pd.read_excel(str_path, header = 3)
            elif '_SOLCBTT_' in str_fileName.upper() or '_SOLCCCT_' in str_fileName.upper():
                df_data = pd.read_excel(str_path, header = 4)
            elif 'ETF_PCFREPORT_MIRAE' in str_fileName.upper() :
                df_data = pd.read_excel(str_path, header = None)
            elif 'ESTIMATE_PCFOIL_' in str_fileName.upper() or 'ESTIMATE_PCFSPX_' in str_fileName.upper() or 'PCFHSIHSCEI_' in str_fileName.upper():
                df_data = fl.fDf_convertToXlsx(str_path, str_SheetName, None)
            elif 'PCF_CAM CTPB BOND ETF_' in str_fileName.upper():
                df_data = 1
            else:
                if str_SheetName == '':     df_data = pd.read_excel(str_path, header = bl_header)
                else:                       df_data = pd.read_excel(str_path, header = bl_header, sheet_name = str_SheetName)
                #, skiprows = range(2), nrows = 6, l_names = range(7), encoding = 'cp1252'
        # ------- HDX -------
        elif '.HDX' in str_fileName.upper():
            if '_SPGSCI_FIN_STD' in str_fileName.upper() :
                df_data = pd.read_csv(str_path, header = 1, sep='\t')
            else:
                print(' HDX in fDf_getDfFromDownloaded: Case not taken into account')
                return None, True
            
        # ------- CSV -------
        elif '.CSV' in str_fileName.upper():
            if 'GMO' in str_fileName.upper() or 'fcnacl2v' in str_fileName.lower() or 'fdccc' in str_fileName.lower() \
            or 'fdcco' in str_fileName.lower() or 'navau' in str_fileName.lower():
                df_data = pd.read_csv(str_path, header = 2)
                # If it has been opened manually, it should take the 4th row
                l_colUnamed = ['Unnamed' for colName in df_data.columns if 'Unnamed' in colName]
                if l_colUnamed:
                    print(df_data.iloc[0:4, 0:3])
                    df_data = pd.read_csv(str_path, header = 3)
                    print('-------- After, header on 4th row ---------')
                    print(df_data.iloc[0:4, 0:3])
                # GMO treat
                if 'GMO' in str_fileName.upper():
                    df_data.dropna(axis = 'index', subset = ['ISIN'], inplace = True)
            elif 'DF_LIGHT_INV_S02' in str_fileName.upper() or 'DF_NAV_S02' in str_fileName.upper():
                df_data = pd.read_csv(str_path, header = bl_header, sep=';', index_col=False) 
            elif 'PINGAN_PCF_' in str_fileName.upper():
                ## Do note that this will cause the offending lines to be skipped.
                #df_data = pd.read_csvstr_path, header = bl_header, error_bad_lines = False)
                df_data = 1
            elif 'FX 5.30PM' in str_fileName.upper():
                df_data = pd.read_csv(str_path, header = bl_header, skiprows = 1)
            elif 'WISDOMTREEUCITS_BSKT' in str_fileName.upper():
                df_data = pd.read_csv(str_path, header = bl_header, skiprows = 8)
            else:
                df_data = pd.read_csv(str_path, header = bl_header)
                
        # ------- TXT -------
        elif '.TXT' in str_fileName.upper():
            if 'ELQC' in str_fileName.upper() or 'GOMA' in str_fileName.upper() \
            or 'PCFGSCE' in str_fileName.upper() or 'PCFGSCU' in str_fileName.upper() \
            or 'COGSDE_GSCE_' in str_fileName.upper() or 'COGSCU' in str_fileName.upper(): # \
            #or 'DIREXION_HSBC.T' in str_fileName.upper() :
                df_data = pd.read_csv(str_path, header = bl_header, sep='\t')
            elif 'COEEEH_' in str_fileName.upper() or 'COEMEH_' in str_fileName.upper() or 'COJBEM_' in str_fileName.upper():
                # we just forward so we do not need the data: Check out PINGAN_PCF_
                df_data = 1
            else:
                df_data = pd.read_csv(str_path, header = bl_header)
                
        # ------- Other Flat files -------
        elif '.ETF' in str_fileName.upper():
            df_data = pd.read_csv(str_path, header = bl_header)
        
        elif '718708NETRCNH' in str_fileName.upper():
            df_data = dframe.fDf_readCsv_enhanced(str_path, None, str_sep = '|', l_names = range(33))
            
        # ------- ZIP -------
        elif '.ZIP' in str_fileName.upper():
            df_data = 1
        
        else:
            print('---------------------------')
            print('  (**) We do not know how to take DF from this kind of files | We need to define a type in fDf_getDfFromDownloaded...')
            print('  - str_fileName: ', str_fileName)
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
def fStr_SplitFileName_startEnd(str_fileName, str_ExactName, int_File_startW, int_File_endW):
    if str_ExactName.lower() == 'true':
        str_File_startW = str_fileName
        str_File_endW = ''
    else:
        str_File_startW = str_fileName[:int(int_File_startW)]
        if int_File_endW == 0:          str_File_endW = ''
        else:                           str_File_endW = str_fileName[-int(int_File_endW):]
    return str_File_startW, str_File_endW

def fStr_generateFileName(df_Param, row, str_folderRaw, dte_date, bl_tryReplaceTheX = True):
    str_fileName = str(df_Param.loc[row, 'fileName'])
    str_fileDate = str(df_Param.loc[row, 'fileDate'])
    DateOffset = df_Param.loc[row, 'DateOffset']
    CalendarID = df_Param.loc[row, 'DateCalendarID']
    str_NewDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, str_fileDate, int(DateOffset), str(CalendarID))
    str_fileName = str_fileName.replace('{fileDate}', str_NewDate)
    # Name of the file with XX
    try:
        if bl_tryReplaceTheX and str_fileName.count('{') and str_fileName.count('}') > 0 :
            if str_fileName.count('{X}') > 0:   bl_exactNumberX = False
            elif str_fileName.count('{*}') > 0: bl_exactNumberX = False
            else:                               bl_exactNumberX = True
            str_fileName = fl.fStr_GetMostRecentFile_InFolder(str_folderRaw, str_fileName.replace('{*}','{X}'), 
                                                              bl_searchOnlyIfPossible = True, bl_exactNumberX = bl_exactNumberX)
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
    l_ID_alreadyDone = []
    bl_dwlFailed = False
    
    for i, row in enumerate(df_Param.index):
        bl_forceDwld_local = bl_forceDwld
        
        #-------------------------------------------------------------
        # Is ID already has been done (Dowloaded or Saved into DF) ??
        #-------------------------------------------------------------
        str_ID = str(df_Param.loc[row, 'ID'])
        if str_ID in l_ID_alreadyDone:  continue        # Go back to the start of the loop (next file)
        else:                           l_ID_alreadyDone.append(str_ID)
        #-------------------------------------------------------------
        
        # Variables in Param CSV
        str_folderRaw = fStr_generateFolderRaw(df_Param, row, str_folderRoot, dte_date)
        str_fileName = fStr_generateFileName(df_Param, row, str_folderRaw, dte_date, bl_tryReplaceTheX = not bl_forceDwld_local)
        # Is File Optional for Download ???
        bl_Optional = False
        if str(df_Param.loc[row, 'bl_Optional']).lower() == 'true':     bl_Optional = True
        
        # Create the folder
        try:        fl.fBl_createDir(str_folderRaw)
        except:     return 'ERROR in GenProcess. _GetFiles2: Could not Create Folder: ' + str_folderRaw
        
        #======================================================================================
        # SEARCH: Try to get the data from files already dwld - (Add DATAFRAME in the dictionary)
        #======================================================================================
        if not bl_forceDwld_local:
            df_data, bl_exist = fDf_getDfFromDownloaded(df_Param, row, str_folderRaw, str_fileName)
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
            print('Downloading... {}'.format(str_fileName))
            bl_success = Act_DownFiles(df_Param, row, str_folderRaw, str_fileName, dte_date, str_folderRoot, bl_ArchiveMails)
            # In case of download files before, we need to update fileName
            if bl_success:              str_fileName = fStr_generateFileName(df_Param, row, str_folderRaw, dte_date)
            else:
                if not bl_Optional:     bl_dwlFailed = True
                else:                   print('   (*) File could not be downloaded but the file is optional => Process continue without raising issues')
                # Download has failed, bl_dwlFailed can be TRUE or FALSE depending if it's Optional or not.
                # But Either way, we need to remove str_ID form the list so it can try again to download (Multiple same str_ID, for multiple try)
                try:    l_ID_alreadyDone.remove(str_ID)
                except: print(' WARNING in fDic_pcfAutomate_GetFiles2 : Could not remove ID from List. ID= {0} || Liste= {1}'.format(str_ID, l_ID_alreadyDone))
                print('')
                continue
            #-------------------------------------------
            # Re-Search after Download
            # Get the DF in case of download after Search not successful (not if Download PJ only (bl_dfRequired = False)) ()
            if bl_dfRequired:
                #print('Searching again for... ' + str_fileName)
                df_data, bl_exist = fDf_getDfFromDownloaded(df_Param, row, str_folderRaw, str_fileName)
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
        l_PathOutput.append(str_folderRaw + str_fileName)
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
    str_text += 'ENTRY={0} +{1}={2} 1 RER 1'.format(str_IsinFinal, str(dframe.round_Correction(flt_nav, 4)), str_ccy)
    # Create Txt file And rename it
    fl.act_createFile(False, str_folder, str_fileName, str_text)
    #    fl.act_createFile(False, str_folder, str_fileName.replace('.etf', '.txt'), str_text)
    #    fl.Act_Rename(str_folder, str_fileName.replace('.etf', '.txt'), str_fileName)
    return os.path.join(str_folder, str_fileName)



def act_CreateSecurityNameFile():
    str_folder = r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Manual_py\SG_Easy\Easy MSCI 20200706'
    str_folder_Final = r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Manual_py\SG_Easy'
    l_files = fl.fList_FileInDir(str_folder)
    df_pcf_Final = None
    
    for file in l_files:
        df_pcf = dframe.fDf_readCsv_enhanced(fl.fStr_BuildPath(str_folder, file), bl_header = None, str_sep='\t', str_encoding = 'cp1252')
        l_col = list(range(50)[:len(df_pcf.columns)])
        df_pcf.columns = [str(x) for x in l_col]
        df_pcf = df_pcf[['3','4','7']]
        if df_pcf_Final is None:
            df_pcf_Final = df_pcf.copy()
        else:
            df_pcf_Final = dframe.fDf_Concat_wColOfDf1(df_pcf_Final, df_pcf)
        
    fl.fStr_CreateTxtFile(str_folder_Final, 'SgEasy_SecurityName.txt', df_pcf_Final)
#act_CreateSecurityNameFile()
    

#------------------------------------------------------------------------------
# Function for SG Easy Msci
#------------------------------------------------------------------------------
def Act_OrderByIsin_Easy(df_lConfig, str_folder, dte_date):
    str_folder = str_folder.replace('Auto_py', 'Manual_py')
    # Loop on parameters
    for i_row, t_row in df_lConfig.iterrows():
        df_pcf = None
        df_compo = None
        df_header = None
        try:
            str_pcfFilename =  '{}{}.txt'.format(t_row['Pcf_FileName'], dte_date.strftime('%Y%m%d'))
            df_pcf = dframe.fDf_readCsv_enhanced(fl.fStr_BuildPath(str_folder, str_pcfFilename), bl_header = None, str_sep='\t', str_encoding = 'cp1252')
            df_header = df_pcf.iloc[0:1].copy()
            df_compo = df_pcf.iloc[1:].copy()
            l_col = list(range(50)[:len(df_compo.columns)])
            df_compo.columns = [str(x) for x in l_col]
            df_compo.rename(columns = {'3':'Isin'}, inplace = True)
            df_compo.sort_values(by = ['Isin'], ascending = True, inplace = True)
            # index
            l_col = df_compo.columns
            df_compo = dframe.fDf_InsertColumnOfIndex(df_compo)
            df_compo['11'] = df_compo['ind']
            df_compo = df_compo[l_col]
            # Concat
            df_pcf = dframe.fDf_Concat_wColOfDf1(df_header, df_compo)
            fl.fStr_CreateTxtFile(str_folder, str_pcfFilename, df_pcf, str_sep = '\t')
        except Exception as err:
            print(' ERROR on Act_OrderByIsin_Easy - PCF | {}'.format(str(err)))
            print(' - str_pcfFilename', str_pcfFilename)
        try:
            str_COfilename =  '{}_{}.txt'.format(t_row['CO_FileName'], dte_date.strftime('%Y%m%d'))
            df_CO = dframe.fDf_readCsv_enhanced(fl.fStr_BuildPath(str_folder, str_COfilename), bl_header = None, str_sep='\t', str_encoding = 'cp1252')
            df_header = df_CO.iloc[:2].copy()
            df_compo = df_CO.iloc[2:].copy()
            l_col = list(range(50)[:len(df_compo.columns)]) 
            df_compo.columns = [str(x) for x in l_col]
            df_compo.rename(columns = {'3':'Isin'}, inplace = True)
            df_compo.sort_values(by = ['Isin'], ascending = True, inplace = True)
            # index
            l_col = df_compo.columns
            df_compo = dframe.fDf_InsertColumnOfIndex(df_compo)
            df_compo['1'] = df_compo['ind']
            df_compo = df_compo[l_col]
            # Concat
            df_CO = dframe.fDf_Concat_wColOfDf1(df_header, df_compo)
            fl.fStr_CreateTxtFile(str_folder, str_COfilename, df_CO, str_sep = '\t')
        except Exception as err:
            print(' ERROR on Act_OrderByIsin_Easy - CO | {}'.format(str(err)))
            print(' - str_COfilename', str_COfilename)
    return True

    
def fDdf_loopOnRic_SqlReq_SaveCsv(df_lConfig, str_req, dte_date, str_folder, str_filenameExtension = ''):
    inst_db = db.c_sqlDB()
    inst_db.server = 'D1PRDSOLADB.infocloud.local'
    str_cloudPathForCsv = inst_db.cloudPathForCsv
    #inst_db.cloudPathForCsv = str_folder + r'\raw'
    d_Df = {}
    for i_row, t_row in df_lConfig.iterrows():
        str_IndexRic = t_row['IndexRic']
        if not str_IndexRic in d_Df:        #Avoid Double
            str_fileName =  '{}{}.csv'.format(t_row['Pcf_FileName'].replace('PCF',''), str_filenameExtension)
            str_req_loop = str_req.replace('<RIC>', str_IndexRic).replace('<DATE>', dte_date.strftime('%Y%m%d'))
            df_sqlResult = db.fDf_GetRequest_or_fromCsvFile(str_req_loop, str_fileName, 30, r'{}raw'.format(str_folder), bl_EmptyMessage = False)
            # Save into dictionary
            d_Df[str_IndexRic] = df_sqlResult
        else:   pass
    inst_db.cloudPathForCsv = str_cloudPathForCsv
    return d_Df


def fLpath_loopOnRic_CreateFile(d_param):
    try:
        int_DivMethod = d_param['DivMethod']
        df_lConfig =    d_param['df_lConfig']
        df_1NavIndic =  d_param['df_1NavIndic']
        df_2Val_Dmc =   d_param['df_2Val_Dmc']
        df_FX =         d_param['df_FX']
        df_SecurityName=d_param['df_SecurityName']
        d_CompoDf =     d_param['d_CompoDf'] 
        dte_date =      d_param['dte_date']
        dte_navDate =   d_param['dte_navDate']
        str_folder =    d_param['str_folder']
        l_pathAttach = []
    except Exception as err:    
        print('  ERROR in fLpath_loop, 0. Grab the db | {}'.format(str(err)))
        raise
        
    # Loop on parameters
    for i_row, t_row in df_lConfig.iterrows():
        try:
            # GET INPUT
            str_IndexRic =  t_row['IndexRic']
            str_ric =       t_row['ETF_RIC']
            str_isin =      t_row['Isin']
            int_divisor =   t_row['Divisor']
            flt_divFactor = t_row['divFactor']
            str_idLoop =    t_row['TrackerMnemoCode']
            str_etfCcy =    t_row['ETF CCY']
            str_indexCcy =  t_row['Underlying index CCY']
            
            # NAV Df
            if len(df_1NavIndic[df_1NavIndic['Fund Code'] == str_isin]) == 0:
                print(" WARNING: the ETF (Isin = {} , Name = {} ) is not in the 1.NavIndic File: 'NavCalcOutputs_'".format(str_isin, t_row['Pcf_FileName']))
                continue
            elif len(df_2Val_Dmc[df_2Val_Dmc['ISIN Code'] == str_isin]) == 0:
                print(" WARNING: the ETF (Isin = {} , Name = {} ) is not in the 2.Val_Dmc File: 'Last-Valuation-MARKIT-'".format(str_isin, t_row['Pcf_FileName']))
                continue
            flt_nav = df_1NavIndic[df_1NavIndic['Fund Code'] == str_isin]['Calculated Target Nav'].values[0]
            flt_nav_G2 = dframe.round_Correction(flt_nav, 4) 
            flt_TotalNav = flt_nav * int_divisor
            flt_shareNb = df_2Val_Dmc[df_2Val_Dmc['ISIN Code'] == str_isin]['Share Nb'].values[0]
            flt_indexReturn = df_1NavIndic[df_1NavIndic['Fund Code'] == str_isin]['Index Return Converted'].values[0]
            # COMPO Dataframe from dico
            df_compo =  d_CompoDf[str_IndexRic].copy()
        except Exception as err:    
            print('  ERROR in fLpath_loop, 1. Compo | {} || {}'.format(str_idLoop, str(err)))
            raise
        
        try:
            # Hedged with FX
            flt_fx_UsdToEtf = df_FX.loc[df_FX['ToCurrencyCode'] == str_etfCcy, 'Value'].values[0]
            if str_etfCcy == str_indexCcy:      flt_fx_IndexToEtf = 1
            elif str_indexCcy == 'USD':         flt_fx_IndexToEtf = flt_fx_UsdToEtf
            else:
                flt_fx_UsdToIndex = df_FX.loc[df_FX['ToCurrencyCode'] == str_indexCcy, 'Value'].values[0]
                flt_fx_IndexToEtf = flt_fx_UsdToEtf / flt_fx_UsdToIndex
            df_compo['FXRate_toEtf'] = df_compo['FXRate'] * flt_fx_IndexToEtf
            df_compo['UnadjustedPrice_fxH'] = df_compo['UnadjustedPrice'] * df_compo['FXRate_toEtf']
            # SecurityName
            df_compo = dframe.fDf_JoinDf(df_compo, df_SecurityName, 'Isin', str_how = 'left')
            df_compo['Security_Name'].fillna(df_compo['SecurityName'], inplace = True)
            #df_compo['Country_code'] = df_compo['Isin'].apply(lambda str_isin : str_isin[:2])
            df_compo['Country_code'] = df_compo['DomicileCountryCode']
            # Calculate WEIGHT + UNIT (or SHARES)
            df_compo['Weight'] = df_compo['IndexQuantity'] * df_compo['UnadjustedPrice_fxH']
            flt_MaketCap = df_compo['Weight'].sum()
            df_compo['Weight'] = df_compo['Weight'] / flt_MaketCap
            df_compo['UNIT'] = flt_TotalNav * df_compo['Weight'] / (df_compo['UnadjustedPrice_fxH'])
        except Exception as err:    
            print('  ERROR in fLpath_loop, 2. Weight | {} || {}'.format(str_idLoop, str(err)))
            raise        
        #----------------------------------------------------------------------
        # Particularity according to Div Method
        #----------------------------------------------------------------------
        try:
            if int_DivMethod == 1:
                df_EPRAtax_perMic = d_param['d_CorpActDf'].copy()
                df_compo =  dframe.fDf_JoinDf(df_compo, df_EPRAtax_perMic, 'MIC', str_how = 'left')
                df_compo.fillna({'Tax_rate' : 0}, inplace = True)
                df_compo['div_NetAmount'] = df_compo['DivAmount'] * (1-df_compo['Tax_rate'])
                df_compo['NetAmount_fxH'] = df_compo['div_NetAmount'] * df_compo['FXRate_toEtf']
                df_compo['AdjustedPrice_fxH'] = df_compo['UnadjustedPrice_fxH'] - df_compo['NetAmount_fxH']
                # Calculate WEIGHT + UNIT (or SHARES)
                df_compo['Weight'] = df_compo['IndexQuantity'] * df_compo['AdjustedPrice_fxH']
                flt_MaketCap = df_compo['Weight'].sum()
                df_compo['Weight'] = df_compo['Weight'] / flt_MaketCap
                df_compo['UNIT'] = flt_TotalNav * df_compo['Weight'] / df_compo['AdjustedPrice_fxH']
                # Get the cash
                flt_cash = 0
            elif int_DivMethod == 2 or int_DivMethod == 4:
                df_CA = d_param['d_CorpActDf'][str_IndexRic][['Isin','GrossAmount','NetAmount', 'CurrencyCode']].copy()
                df_CA.columns = ['Isin','div_GrossAmount','div_NetAmount','div_ccy']
                # Convert DIVIDEND to EUR
                df_FX_div = df_FX[['ToCurrencyCode','Value']].copy()
                df_FX_div.columns = ['div_ccy','FXRate_toDiv']
                df_FX_div['FXRate_DivToUsd'] = 1/df_FX_div['FXRate_toDiv']
                df_FX_div['FXRate_DivToEtf'] = df_FX_div['FXRate_DivToUsd'] * flt_fx_UsdToEtf
                df_CA = dframe.fDf_JoinDf(df_CA, df_FX_div, 'div_ccy')
                df_CA['div_GrossAmount_fxH'] =  df_CA['div_GrossAmount'] * df_CA['FXRate_DivToEtf']
                df_CA['div_NetAmount_fxH'] =    df_CA['div_NetAmount'] * df_CA['FXRate_DivToEtf']
                df_CA = df_CA[['Isin','div_GrossAmount_fxH','div_NetAmount_fxH']].copy()
                # Put Dividenc into Compo
                df_compo = dframe.fDf_JoinDf(df_compo, df_CA, 'Isin', str_how = 'left')
                df_compo.fillna({'div_NetAmount_fxH' : 0}, inplace = True)
                
                # Only for DIV Methode 2 
                if int_DivMethod == 2:
                    df_compo['AdjustedPrice_fxH'] = df_compo['UnadjustedPrice_fxH'] - df_compo['div_NetAmount_fxH']
                    # Get the cash
                    df_compo['CASH']  = df_compo['UNIT'] * df_compo['div_NetAmount_fxH']
                    flt_cash = df_compo['CASH'].sum() / int_divisor
                    t_row['flt_cash'] = flt_cash
                elif int_DivMethod == 4:
                    # PCF:
                    df_compo['AdjustedPrice_fxH'] = df_compo['UnadjustedPrice_fxH']
                    flt_cash = 0
                    # CO: Find the NAV other then indicative NAV (G2: only for StoxxCalc = True)
                    df_compo.fillna({'div_GrossAmount_fxH' : 0}, inplace = True)
                    df_compo['div_fxH'] = df_compo['div_NetAmount_fxH']
                    df_compo = dframe.fDf_fillColUnderCondition(df_compo, 'div_fxH', df_compo['div_GrossAmount_fxH'], 'Country_code', 'FR')
                    df_compo['div_Ratio'] = df_compo['div_fxH'] * df_compo['Weight'] / df_compo['UnadjustedPrice_fxH']
                    flt_div_Ratio = df_compo['div_Ratio'].sum()
                    flt_nav_G2 = flt_nav * (1 + flt_div_Ratio) * (1 + flt_divFactor)
                    # Calculate UNIT specific for CO on Method 4:
                    flt_CO_TotalNav = (flt_nav_G2 - flt_nav) * int_divisor
                    df_compo['Additional_Shares'] = flt_CO_TotalNav * df_compo['Weight'] / df_compo['AdjustedPrice_fxH']
                    df_compo['Additional_Shares_r'] = df_compo['Additional_Shares'].apply(lambda x:dframe.round_Correction(x, 0))
                    df_compo['CO_UNIT'] = df_compo['UNIT'] + df_compo['Additional_Shares_r']
            elif int_DivMethod == 3:
                df_compo['AdjustedPrice_fxH'] = df_compo['UnadjustedPrice'] * df_compo['FXRate_toEtf']
                flt_cash = 0
        except Exception as err:    
            print('  ERROR in fLpath_loop, 3. Particularity of Div Calculus | {} || {}'.format(str_idLoop, str(err)))
            raise        
        #-------------------
        # PCF - COMPO
        #-------------------
        try:
            df_compo['1col'] = 'B'
            df_compo['2_EtfIsin'] = t_row['Isin']
            df_compo['3col'] = 'Equity'
            df_compo['6col'] = '-'
            df_compo = dframe.fDf_InsertColumnOfIndex(df_compo, l_colSort = ['Isin'])
            df_compo['15col'] = 'T'
            df_compo['PRICE_r'] = df_compo['AdjustedPrice_fxH'].apply(lambda x:dframe.round_Correction(x, 4))
            df_compo['FXRate_toEtf_r'] = df_compo['FXRate_toEtf'].apply(lambda x:dframe.round_Correction(x, 4))
            df_compo['UNIT_r'] = df_compo['UNIT'].apply(lambda x:dframe.round_Correction(x, 4))
                
            # Get Number of rows in Composition
            int_nbCompo = len(df_compo)
            t_row['int_nbCompo'] = int_nbCompo
            # FINAL COMPO
            df_compo_pcf = df_compo[['1col','2_EtfIsin','3col','Isin','Ric','6col','MIC','Security_Name', 'UNIT_r','6col','6col',
                                     'ind','PRICE_r','FXRate_toEtf_r','15col','2_EtfIsin']].copy()
        except Exception as err:    
            print('  ERROR in fLpath_loop, 4. PCF COMPO | {} || {}'.format(str_idLoop, str(err)))
            raise        
        #-------------------
        # PCF - Header
        #-------------------
        try:
            if flt_cash == 0:   flt_cash = int(flt_cash)
            
            df_header = pd.DataFrame([['H', t_row['ISINiNAV'], t_row['EuronextCategory'], int(int_nbCompo), '1',
                                      dte_date.strftime('%Y%m%d'), dte_navDate.strftime('%Y%m%d'), dframe.round_Correction(flt_nav, 4),
                                      '-','-', dframe.round_Correction(flt_cash, 13),'-', int(flt_shareNb), 
                                      dframe.round_Correction(flt_nav * int_divisor, 4),
                                      str(int_divisor), str_etfCcy, str_etfCcy, str_etfCcy,
                                      str_isin, str_ric, t_row['ETF BBG Code'],t_row['UnderlyingIndexRIC'],
                                      t_row['Indicative NAV ID'],'-','-','-','-','-','-',flt_indexReturn]]
                                    , columns = range(30))
            # CONCAT
            df_pcf = dframe.fDf_Concat_wColOfDf1(df_header, df_compo_pcf)
            # Create PCF Files
            str_pcfFilename =  '{}{}.txt'.format(t_row['Pcf_FileName'], dte_date.strftime('%Y%m%d'))
            str_path = fl.fStr_CreateTxtFile(str_folder, str_pcfFilename, df_pcf, str_sep = '\t')
            l_pathAttach.append(str_path)
        except Exception as err:    
            print('  ERROR in fLpath_loop, 5. Create PCF | {} || {}'.format(str_idLoop, str(err)))
            raise
        
        #-------------------
        # CO - COMPO
        #-------------------
        try:
            df_compo['1col'] = '3'
            if int_DivMethod == 4:      df_compo['SHARES'] = df_compo['CO_UNIT'].apply(lambda x:dframe.round_Correction(x, 0))
            else:                       df_compo['SHARES'] = df_compo['UNIT'].apply(lambda x:dframe.round_Correction(x, 0))
            df_compo['MCap'] = df_compo['SHARES'] * df_compo['PRICE_r']
            df_compo['Weight_100'] = df_compo['Weight'] * 100
            df_compo['Weight_100'] = df_compo['Weight_100'].apply(lambda x:dframe.round_Correction(x, 9))
            # FINAL COMPO
            df_compo_CO = df_compo[['1col','ind','2_EtfIsin','Isin','Security_Name','SHARES','PRICE_r','MCap',
                                    'Weight_100','Country_code','6col']].copy()
        except Exception as err:    
            print('  ERROR in fLpath_loop, 6. CO COMPO | {} || {}'.format(str_idLoop, str(err)))
            raise
        #-------------------
        # CO - Header
        #-------------------
        try:
            df_compo['CASH'] = (df_compo['UNIT_r'] - df_compo['SHARES']) * df_compo['PRICE_r']
            flt_cash = df_compo['CASH'].sum()
            df_header_1 = pd.DataFrame([['1','-', str_isin, str_idLoop, t_row['ETF Name'], '-', t_row['UnderlyingName'],
                                         t_row['ISINiNAV'], '-', t_row['iNAVName'], t_row['ManagementStyle'], t_row['Category'], t_row['Region'], 
                                         '-', t_row['InvestableUniverse'], '-', str_isin, '-', '-','']]
                                    , columns = range(20))
            df_header_2 = pd.DataFrame([['2', dte_date.strftime('%Y%m%d'), str_isin, str(int_divisor), int_divisor*dframe.round_Correction(flt_nav, 4),
                                         dframe.round_Correction(int_divisor * flt_nav - flt_cash, 2), 
                                         dframe.round_Correction(flt_nav_G2, 8), 
                                         flt_cash, 100*flt_cash / (int_divisor*flt_nav), str_etfCcy, int(flt_shareNb), 
                                         dframe.round_Correction(flt_shareNb * flt_nav, 2), '-', '-', '-', t_row['ManagementFee'],
                                         dframe.round_Correction(flt_nav, 4), dte_navDate.strftime('%Y%m%d'), flt_indexReturn, dte_date.strftime('%Y%m%d')]]
                                    , columns = range(20))
            # CONCAT
            df_pcf = dframe.fDf_Concat_wColOfDf1(df_header_1, df_header_2)
            df_pcf = dframe.fDf_Concat_wColOfDf1(df_pcf, df_compo_CO)
            # Create PCF Files
            str_COfilename =  '{}_{}.txt'.format(t_row['CO_FileName'], dte_date.strftime('%Y%m%d'))
            str_path = fl.fStr_CreateTxtFile(str_folder, str_COfilename, df_pcf, str_sep = '\t')
            l_pathAttach.append(str_path)
        except Exception as err:    
            print('  ERROR in fLpath_loop, 7. Create CO | {} || {}'.format(str_idLoop, str(err)))
            raise
        
    return l_pathAttach



#-----------------------------------------------------------------
# AMUNDI
#-----------------------------------------------------------------
def fDf_getFut_inDb(dte_futDate):
    str_req = """SELECT Column5, Column6, Column7, Column9, Column10
        FROM vwSTOXXEurope600FuturesRollIndexFile
        WHERE Column1 = '{}'""".format(dte_futDate)
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






