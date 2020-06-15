import pandas as pd
import datetime as dt
import fct_outlook as out
import DNS_3genericProcess as pp

str_paramFile = 'DNS_Param.csv'
str_paramFile_PcfAddress = 'DNS_Param_PcfAdr.csv'



#-----------------------------------------------------------------
# Variables
#-----------------------------------------------------------------
str_paramMailFile = 'DNS_Param_Mail.csv'
str_fromm = 'Markit ETF Management'
str_message = "Hello all, \r\n \r\n" +  \
            "Please find the files for today.\r\n" +  \
            "Please send any questions or feedback to DeltaOneSupport@ihsmarkit.com \r\n" +  \
            "Regards, \r\n \r\n" +  \
            "Markit ETF Management"


#-----------------------------------------------------------------
# Download Files Functions
#-----------------------------------------------------------------
def dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, str_perimeter, bl_dfRequired = True, bl_forceDwld = False):
    # Download Files
    try:
        print('============= ' +  str_perimeter + ' =============')
        # From CSV Parameters
        try: df_Param = pd.read_csv(str_paramFile)
        except: print(' ERROR: Cannot read Seita_Param')
        df_Param.fillna(value = '', inplace = True)
        df_Param = df_Param.loc[df_Param['PCF'] == str_perimeter]
        # Get the Files into DF
        dic_df = pp.fDic_pcfAutomate_GetFiles2(df_Param, str_folderRoot, dte_date, bl_ArchiveMails, bl_dfRequired, bl_forceDwld)
        # Check
        if not dic_df: print(' ERROR: dic_df is empty or imcomplete')
        # Init
        str_resultFigures = pp.Initt(str(dte_date))
        df_Param = None
        # OUTPUT is the list of files downloaded
        l_pathAttach = dic_df['files']
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except: return ' ERROR: Download files: dwl_downloadFiles', []
    return str_resultFigures, l_pathAttach


#-----------------------------------------------------------------
# Entrance Function for downloading
#-----------------------------------------------------------------
def DownloadFiles(str_perimeter, str_folderRoot, dte_date, bl_ArchiveMails = False):
    # Param
    if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
    
    #-----------------------------------------------------------------
    # Several PCF at the same time (keep for example)
    #-----------------------------------------------------------------
    if str_perimeter == 'HK - AM':
        str_resultFigures1, l_pathFiles1 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'EXGM', False, True)
        str_resultFigures2, l_pathFiles2 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'EXC2', False, True)
        str_resultFigures3, l_pathFiles3 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'HK_Samsung', False, True)
        str_resultFigures4, l_pathFiles4 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails,  'DB_AM', False, True)     
        if not l_pathFiles1: print(' ERROR: EXGM did not run correctly')
        elif not l_pathFiles2: print(' ERROR: EXC2 did not run correctly')
        elif not l_pathFiles3: print(' ERROR: HK_Samsung did not run correctly')
        elif not l_pathFiles4: print(' ERROR: DB_AM did not run correctly')
        # ----------------------------- Merge all PCF created -----------------------------
        l_pathFiles = l_pathFiles1 + l_pathFiles2 + l_pathFiles3  + l_pathFiles4
        str_resultFigures = str_resultFigures1 + '\n\n' + str_resultFigures2 + '\n\n' + str_resultFigures3 \
                            + '\n\n' + str_resultFigures4
    else: 
        str_resultFigures, l_pathFiles = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, str_perimeter, False, True)
        if not l_pathFiles: print(' ERROR: ' + str_perimeter + ' did not run correctly')
    return str_resultFigures, l_pathFiles
#___________________________________________________________________________________________









#-----------------------------------------------------------------
# Get Path of the PCF
#-----------------------------------------------------------------
def GetPcfPath(str_perimeter, str_folderRoot, dte_date):
    # Download Files
    try:
        print('============= ' +  str_perimeter + ' =============')
        # From CSV Parameters
        try: df_Param = pd.read_csv(str_paramFile_PcfAddress)
        except: print(' ERROR: Cannot read Seita_Param')
        df_Param.fillna(value = '', inplace = True)
        df_Param = df_Param.loc[df_Param['PCF'] == str_perimeter]
        # Get the Path into a list
        l_pathPcf = []
        for i, row in enumerate(df_Param.index):
            str_folder = pp.fStr_generateFolderRaw(df_Param, row, str_folderRoot, dte_date)
            str_FileName = pp.fStr_generateFileName(df_Param, row, dte_date)
            str_Path = str_folder.replace(str_folderRoot,'') + str_FileName
            if not str_Path in l_pathPcf:
                l_pathPcf.append(str_Path)
        # Check
        if not l_pathPcf: return(' ERROR: l_pathPcf is empty'), []
    except: return ' ERROR: GetPcfPath did not work: ' + str_perimeter, []
    return '', l_pathPcf


def RetrievePcfPath(str_perimeter, str_folderRoot, dte_date):
    # Param
    if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
    
    #-----------------------------------------------------------------
    # Several PCF at the same time (keep for example)
    #-----------------------------------------------------------------
    if str_perimeter == 'HK - AM':
        print(3)
        str_resultFigures1, l_pathPcf1 = GetPcfPath('EXGM', str_folderRoot, dte_date)
        str_resultFigures2, l_pathPcf2 = GetPcfPath('EXC2', str_folderRoot, dte_date)
        str_resultFigures3, l_pathPcf3 = GetPcfPath('HK_Samsung', str_folderRoot, dte_date)
        if not l_pathPcf1: print(' ERROR: EXGM did not run correctly')
        elif not l_pathPcf2: print(' ERROR: EXC2 did not run correctly')
        elif not l_pathPcf3: print(' ERROR: HK_Samsung did not run correctly')
        # ----------------------------- Merge all PCF created -----------------------------
        l_pathPcf = l_pathPcf1 + l_pathPcf2 + l_pathPcf3
        str_resultFigures = str_resultFigures1 + '\n\n' + str_resultFigures2 + '\n\n' + str_resultFigures3
    else:
        str_resultFigures, l_pathPcf = GetPcfPath(str_perimeter, str_folderRoot, dte_date)
    return str_resultFigures, l_pathPcf
#___________________________________________________________________________________________








#-----------------------------------------------------------------
# Send mails
#-----------------------------------------------------------------
def sendPCF(dte_date, l_pathAttach, str_perimeter, bl_displayMail = True):
    if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
    if l_pathAttach == []: return 'Please Select a Path'
    
    if not l_pathAttach: 
        print('No PCF Selected')
        raise
        
    bl_success = pcf_sendMail(dte_date, l_pathAttach, str_perimeter, bl_displayMail)
    if not bl_success: 
        print(str_perimeter + ' did not work out')
        raise
    else: return True    
    #    # Choose the PCF
    #    l_Path = [str_path for str_path in l_pathAttach if str_perimeter.lower() in str_path.lower()]
    #    # Create Mail
    #    if l_Path: bl_success = pcf_sendMail(dte_date, l_Path, str_perimeter, bl_displayMail)
    #    # Return
    #    if not l_Path: 
    #        print('No PCF Selected')
    #        raise
    #    elif l_Path and not bl_success: 
    #        print(str_perimeter + ' did not work out')
    #        raise
    #    else: return True
    

def pcf_sendMail(dte_date, l_pathAttach, str_perimeter, bl_displayMail):
    # From CSV Parameters
    try: df_Param = pd.read_csv(str_paramMailFile)
    except: 
        print(' ERROR: Cannot read ' + str_paramMailFile)
        raise
    try:
        df_Param = df_Param.loc[df_Param['PCF'] == str_perimeter]
        if df_Param.empty:
            str_subject = ''
            str_to = ''
            str_cc = ''
            str_bcc = ''
        else:
            df_Param.fillna('', inplace = True)
            # Subject
            str_DateFormat = df_Param.loc[df_Param['Type'] == 'Subject', 'str_DateFormat'].values[0]
            str_subject = df_Param.loc[df_Param['Type'] == 'Subject', 'str_Value'].values[0]
            if not str_DateFormat == '' and not str_subject == '': 
                str_subject = str_subject.replace('<DateFormat>', dte_date.strftime(str_DateFormat))
            # Destinataire
            df_To = df_Param.loc[df_Param['Type'] == 'To']
            df_Cc = df_Param.loc[df_Param['Type'] == 'Cc']
            df_Bcc = df_Param.loc[df_Param['Type'] == 'Bcc']
            str_to = '; '.join(df_To['str_Value'])
            str_cc = '; '.join(df_Cc['str_Value'])
            str_bcc = '; '.join(df_Bcc['str_Value'])
    except: 
        print(' ERROR: pcf_sendMail - find info in ' + str_paramMailFile)
        print(' str_perimeter: ', str_perimeter, ' | dte_date: ', dte_date, ' | bl_displayMail: ', bl_displayMail)
        print(l_pathAttach)
        raise
    # Send PCF by Mail
    try:
        bl_success = out.fBl_SendMail_outlook(bl_displayMail, str_fromm, str_to, str_cc, str_bcc, str_subject, l_pathAttach, str_message)
    except: 
        print(' ERROR: pcf_sendMail')
        print(' str_perimeter: ', str_perimeter, ' | dte_date: ', dte_date, ' | bl_displayMail: ', bl_displayMail)
        print(' str_subject: ', str_subject)
        print(' l_pathAttach: ', l_pathAttach)
        raise
    return bl_success
#___________________________________________________________________________________________

