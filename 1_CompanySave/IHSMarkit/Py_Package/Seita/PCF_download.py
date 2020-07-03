import pandas as pd
import datetime as dt
import PCF_genericProcess as pp


#-----------------------------------------------------------------
# Download Files Functions (Entrance from PCF Creation)
#-----------------------------------------------------------------
def fDic_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, str_pcf, bl_dfRequired = True, bl_forceDwld = False):
    # Download Files
    try:
        print('============= ' +  str_pcf + ' =============')
        # From CSV Parameters
        try: df_Param = pd.read_csv('Seita_Param.csv')
        except: print(' ERROR: Cannot read Seita_Param')
        df_Param.fillna(value = '', inplace = True)
        df_Param = df_Param.loc[df_Param['PCF'] == str_pcf]
        # Get the Files into DF
        dic_df = pp.fDic_pcfAutomate_GetFiles2(df_Param, str_folderRoot, dte_date, bl_ArchiveMails, bl_dfRequired, bl_forceDwld)
            # False: do not df into dico
            # True: Force download
        if not dic_df:      print('  ... (--) ERROR: dic_df is empty or imcomplete')
        else:               print('  ... * Download Files successful !', '\n')
        str_resultFigures = pp.Initt(str(dte_date))
        df_Param = None
    except: 
        print(' ERROR: Download files: fDic_downloadFiles')
        print('  str_folderRoot: ', str_folderRoot)
        print('  Other Param in fct fDic_downloadFiles: ', dte_date, bl_ArchiveMails, str_pcf, bl_dfRequired, bl_forceDwld)
        raise
    return str_resultFigures, dic_df


#-----------------------------------------------------------------
# Function for downloading. Goal of this function : Return the Path of the downloaded file
#-----------------------------------------------------------------
def dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, str_pcf, bl_dfRequired = True, bl_forceDwld = False):
    # Download Files
    try:
        str_resultFigures, dic_df = fDic_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, str_pcf, bl_dfRequired, bl_forceDwld)
        # OUTPUT is the list of files downloaded
        l_pathFiles = dic_df['files']
        l_pathFiles = [path.replace(str_folderRoot, '') for path in l_pathFiles]
    except: return ' ERROR in dwl_downloadFiles: Download files', []
    return str_resultFigures, l_pathFiles


#-----------------------------------------------------------------
# Entrance Function for downloading
#-----------------------------------------------------------------
def DownloadFiles(str_pcf, str_folderRoot, dte_date, bl_ArchiveMails = False):
    # Param
    if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')        
    #-----------------------------------------------------------------
    # Bengalore Multi PCF
    #-----------------------------------------------------------------
    if str_pcf == 'BGLR Evening':
        str_resultFigures1, l_pathFiles1 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'BGLR_Samsung', False, True)
        str_resultFigures2, l_pathFiles2 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'YUANTA', False, True)
        # ----------------------------- Merge all PCF created -----------------------------
        l_pathFiles = l_pathFiles1 + l_pathFiles2 
        str_resultFigures = str_resultFigures1 + '\n\n' + str_resultFigures2    
    #-----------------------------------------------------------------
    # HONG KONG Multi PCF
    #-----------------------------------------------------------------
    elif str_pcf == 'HK Morning':
        str_resultFigures1, l_pathFiles1 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'HK_Samsung', False, True)
        str_resultFigures2, l_pathFiles2 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'HK_Samsung-2812', False, True)
        str_resultFigures3, l_pathFiles3 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'HK_Samsung-ICE', False, True)
        str_resultFigures4, l_pathFiles4 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'HK_Nikko', False, True)
        str_resultFigures5, l_pathFiles5 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'HK_Nikko_SGX', False, True)
        str_resultFigures6, l_pathFiles6 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails,  'HK_GlobalX', False, True)
        # ----------------------------- Merge all PCF created -----------------------------
        l_pathFiles = l_pathFiles1 + l_pathFiles2 + l_pathFiles3 + l_pathFiles4 + l_pathFiles5 + l_pathFiles6
        str_resultFigures = str_resultFigures1 + '\n\n' + str_resultFigures2 + '\n\n' + str_resultFigures3 \
                            + '\n\n' + str_resultFigures4 + '\n\n' + str_resultFigures5 + '\n\n' + str_resultFigures6
    #-----------------------------------------------------------------
    # HONG KONG Noon
    #-----------------------------------------------------------------
    elif str_pcf == 'HK_Noon':
        str_resultFigures1, l_pathFiles1 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'HK_PingAn', False, True)
        str_resultFigures2, l_pathFiles2 = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, 'HK_ChinaAMC', False, True)
        # ----------------------------- Merge all PCF created -----------------------------
        l_pathFiles = l_pathFiles1 + l_pathFiles2 #+ l_pathFiles3 + l_pathFiles4 + l_pathFiles5 + l_pathFiles6
        str_resultFigures = str_resultFigures1 + '\n\n' + str_resultFigures2 #+ '\n\n' + str_resultFigures3
    #-----------------------------------------------------------------
    # 1 PCF
    #-----------------------------------------------------------------
    else:
        str_resultFigures, l_pathFiles = dwl_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, str_pcf, False, True)
    
    if not l_pathFiles:     print(' ERROR in DownloadFiles: PCF did not Work correctly: {}'.format(str_pcf))
    return str_resultFigures, l_pathFiles
