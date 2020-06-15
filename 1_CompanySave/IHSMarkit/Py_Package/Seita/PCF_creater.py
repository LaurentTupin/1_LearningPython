import os
import numpy as np
import pandas as pd
import datetime as dt
import shutil
import glob
import math
from pandas.tseries.offsets import BDay
import PCF_genericProcess as pp
import PCF_download as dwl
import fct_Date as dat
import fct_DB as db
import fct_dataframe as dframe
import fct_Files as fl


#-----------------------------------------------------------------
# Produce PCF - Entrance Function
#-----------------------------------------------------------------
def producePCF(str_pcf, str_folderRoot, dte_date, bl_ArchiveMails = False):
    if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
    
    # Load or Download Files
    try:                        str_resultFigures, dic_df = dwl.fDic_downloadFiles(str_folderRoot, dte_date, bl_ArchiveMails, str_pcf, True, False)
    except Exception as Err:    return 'ERROR: Download files in producePCF - {1} | {0}'.format(str(Err), str_pcf), []
    
    #-----------------------------------------------------------------
    # India - Bengalore
    #-----------------------------------------------------------------
    if str_pcf == 'BGLR Evening':
        str_resultFigures1, l_pathPcf1 = pcf_YUANTA('YUANTA', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures2, l_pathPcf2 = pcf_BglrSamsung('BGLR_Samsung', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures3, l_pathPcf3 = pcf_FUBON('FUBON', str_folderRoot, dte_date, str_resultFigures, dic_df)
        # ----------------------------- Merge all PCF created -----------------------------
        l_pathPcf = l_pathPcf1 + l_pathPcf2 + l_pathPcf3
        str_resultFigures = '{1}{0}{2}{0}{3}'.format('\n\n', str_resultFigures1, str_resultFigures2, str_resultFigures3)
    
    elif str_pcf == 'BGLR_Samsung':
        str_resultFigures, l_pathPcf = pcf_BglrSamsung(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
    
    elif str_pcf == 'YUANTA':
        str_resultFigures, l_pathPcf = pcf_YUANTA(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
    
    elif str_pcf == 'YUANTA_2019':
        str_resultFigures, l_pathPcf = pcf_YUANTA(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
    
    elif str_pcf == 'FUBON':
        str_resultFigures, l_pathPcf = pcf_FUBON(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
    
    elif str_pcf == 'CATHAY':
        str_resultFigures, l_pathPcf = pcf_CATHAY(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
    
    #-----------------------------------------------------------------
    # US
    #-----------------------------------------------------------------
    elif str_pcf == 'US_Harvest_China':
        str_resultFigures, l_pathPcf = pcf_Harvest(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
    
    #-----------------------------------------------------------------
    # HONG KONG - AM
    #-----------------------------------------------------------------
    elif str_pcf == 'HK Morning':
        str_resultFigures1, l_pathPcf1 = pcf_SAM('HK_Samsung', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures2, l_pathPcf2 = pcf_OnlyForwarding('HK_Samsung-2812', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures3, l_pathPcf3 = pcf_SAM_ICE('HK_Samsung-ICE', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures4, l_pathPcf4 = pcf_Nikko('HK_Nikko', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures5, l_pathPcf5 = pcf_NikkoSGX('HK_Nikko_SGX', str_folderRoot, dte_date, str_resultFigures, dic_df)
#        str_resultFigures4, l_pathPcf4 = pcf_Nikko63(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures6, l_pathPcf6 = pcf_Nikko63(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures7, l_pathPcf7 = pcf_OnlyForwarding('HK_ChinaAMC_Bond', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures8, l_pathPcf8 = pcf_GlobalX('HK_GlobalX', str_folderRoot, dte_date, str_resultFigures, dic_df)
        # ----------------------------- Merge all PCF created -----------------------------
        l_pathPcf = l_pathPcf1 + l_pathPcf2 + l_pathPcf3 + l_pathPcf4 + l_pathPcf6 + l_pathPcf7 + l_pathPcf8
        str_resultFigures = '{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}{7}'.format('\n\n', str_resultFigures1, str_resultFigures2, str_resultFigures3, 
                             str_resultFigures4, str_resultFigures6, str_resultFigures7, str_resultFigures8)
    
    elif str_pcf == 'HK_Samsung-ICE':
        str_resultFigures, l_pathPcf = pcf_SAM_ICE(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    elif str_pcf == 'HK_Samsung':
        # TO_DO : Merge these Process
        str_resultFigures1, l_pathPcf1 = pcf_SAM('HK_Samsung', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures2, l_pathPcf2 = pcf_OnlyForwarding('HK_Samsung-2812', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures3, l_pathPcf3 = pcf_SAM_ICE('HK_Samsung-ICE', str_folderRoot, dte_date, str_resultFigures, dic_df)
        # ----------------------------- Merge all PCF created -----------------------------    
        l_pathPcf = l_pathPcf1 + l_pathPcf2 + l_pathPcf3
        str_resultFigures = '{1}{0}{2}{0}{3}'.format('\n\n', str_resultFigures1, str_resultFigures2, str_resultFigures3)
        
    elif str_pcf == 'HK_ChinaAMC_Bond':
        str_resultFigures, l_pathPcf = pcf_OnlyForwarding(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    elif str_pcf == 'HK_GlobalX':
        str_resultFigures, l_pathPcf = pcf_GlobalX(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    elif str_pcf == 'HK_Nikko':
#        str_resultFigures, l_pathPcf = pcf_Nikko63(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures4, l_pathPcf4 = pcf_Nikko('HK_Nikko', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures5, l_pathPcf5 = pcf_NikkoSGX('HK_Nikko_SGX', str_folderRoot, dte_date, str_resultFigures, dic_df)
        # ----------------------------- Merge all PCF created -----------------------------
        l_pathPcf = l_pathPcf4 + l_pathPcf5
        str_resultFigures = '{1}{0}{2}'.format('\n\n', str_resultFigures4, str_resultFigures5)
        
    elif str_pcf == 'HK_Nikko63':
        str_resultFigures, l_pathPcf = pcf_Nikko63(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    #-----------------------------------------------------------------
    # HONG KONG - Exception Process
    #-----------------------------------------------------------------
    elif str_pcf == 'HK_Nikko63_intra':
        str_resultFigures, l_pathPcf = pcf_Nikko63_Intra(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    elif str_pcf == 'HK_Samsung-ICE':
        str_resultFigures, l_pathPcf = pcf_SAM_ICE(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    #-----------------------------------------------------------------
    # HONG KONG - Noon
    #-----------------------------------------------------------------
    elif str_pcf == 'HK_Noon':
        str_resultFigures1, l_pathPcf1 = pcf_OnlyForwarding('HK_PingAn', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures2, l_pathPcf2 = pcf_ChinaAMC('HK_ChinaAMC', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures3, l_pathPcf3 = pcf_WisdomTree('HK_WisdomTree', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures4, l_pathPcf4 = pcf_EasyFi('HK_EASY_FI', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures5, l_pathPcf5 = pcf_EasyComo('HK_EASY_COMO', str_folderRoot, dte_date, str_resultFigures, dic_df)
        str_resultFigures6, l_pathPcf6 = pcf_OnlyForwarding('HK_EASY_JBEM', str_folderRoot, dte_date, str_resultFigures, dic_df)
        # ----------------------------- Merge all PCF created -----------------------------
        l_pathPcf = l_pathPcf1 + l_pathPcf2 + l_pathPcf3 + l_pathPcf4 + l_pathPcf5 + l_pathPcf6
        str_resultFigures = '{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}'.format('\n\n', str_resultFigures1, str_resultFigures2, str_resultFigures3, 
                             str_resultFigures4, str_resultFigures5, str_resultFigures6)
        
    elif str_pcf == 'HK_PingAn':
        str_resultFigures, l_pathPcf = pcf_OnlyForwarding(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    elif str_pcf == 'HK_ChinaAMC':
        str_resultFigures, l_pathPcf = pcf_ChinaAMC(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    elif str_pcf == 'HK_WisdomTree':
        str_resultFigures, l_pathPcf = pcf_WisdomTree(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    elif str_pcf == 'HK_EASY_FI':
        str_resultFigures, l_pathPcf = pcf_EasyFi(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    elif str_pcf == 'HK_EASY_COMO':
        str_resultFigures, l_pathPcf = pcf_EasyComo(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    elif str_pcf == 'HK_EASY_JBEM':
        str_resultFigures, l_pathPcf = pcf_OnlyForwarding(str_pcf, str_folderRoot, dte_date, str_resultFigures, dic_df)
        
    #-----------------------------------------------------------------
    else: 
        str_resultFigures, l_pathPcf = "\n You really didn't choose the right PCF in PCF_CREATER: {}".format(str_pcf), []
    
    if not l_pathPcf:    print(' ERROR: {} did not run correctly'.format(str_pcf))
    return str_resultFigures, l_pathPcf


#-----------------------------------------------------------------
# Send PCF - Entrance Function
#-----------------------------------------------------------------
def sendPCF(dte_date, l_Path, str_pcf, str_MailType, bl_draft = True):
    if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
    
    if l_Path == []:    
        bl_success = pp.pcf_sendMail(dte_date, [], str_pcf, str_MailType, bl_draft)
        #return 'No PCF Selected to be sent, you need to select at least one !'
        
    elif str_pcf == 'BGLR Evening':
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'BGLR_Samsung', str_MailType, bl_draft)
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'YUANTA', str_MailType, bl_draft)
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'FUBON', str_MailType, bl_draft)
        
    elif str_pcf == 'HK Morning':
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'HK_Samsung', str_MailType, bl_draft)
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'HK_Nikko', str_MailType, bl_draft)
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'HK_Nikko63', str_MailType, bl_draft)
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'HK_ChinaAMC_Bond', str_MailType, bl_draft)
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'HK_GlobalX', str_MailType, bl_draft)
        
    elif str_pcf == 'HK_Noon':
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'HK_PingAn', str_MailType, bl_draft)
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'HK_ChinaAMC', str_MailType, bl_draft)
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'HK_WisdomTree', str_MailType, bl_draft)
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'HK_EASY_FI', str_MailType, bl_draft)
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'HK_EASY_COMO', str_MailType, bl_draft)
        bl_success = pp.pcf_sendMail(dte_date, l_Path, 'HK_EASY_JBEM', str_MailType, bl_draft)
        
    else:
        bl_success = pp.pcf_sendMail(dte_date, l_Path, str_pcf, str_MailType, bl_draft)
    # Return
    if not bl_success: return str_pcf + ' Mail did not work out !!'
    else: return True


#-----------------------------------------------------------------
# Send PCF FTP - Entrance Function
#-----------------------------------------------------------------
def sendFTP(dte_date, l_Path, str_pcf):
    if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
    
    if l_Path == []:    
        #        bl_success, l_ListFilesFTP = pcf_sendFTP(dte_date, [], str_pcf)
        return 'No PCF Selected to be sent, you need to select at least one !'
        
    elif str_pcf == 'BGLR Evening':
        bl_success1, l_ListFilesFTP1 = pp.pcf_sendFTP(dte_date, l_Path, 'BGLR_Samsung')
        bl_success2, l_ListFilesFTP2 = pp.pcf_sendFTP(dte_date, l_Path, 'YUANTA')
        bl_success3, l_ListFilesFTP3 = pp.pcf_sendFTP(dte_date, l_Path, 'FUBON')
        bl_success = bl_success1 and bl_success2 and bl_success3
        l_ListFilesFTP = l_ListFilesFTP1 + l_ListFilesFTP2 + l_ListFilesFTP3
        
    elif str_pcf == 'HK Morning':
        bl_success1, l_ListFilesFTP1 = pp.pcf_sendFTP(dte_date, l_Path, 'HK_Samsung')
        bl_success2, l_ListFilesFTP2 = pp.pcf_sendFTP(dte_date, l_Path, 'HK_Nikko')
        bl_success3, l_ListFilesFTP3 = pp.pcf_sendFTP(dte_date, l_Path, 'HK_Nikko63')
        bl_success4, l_ListFilesFTP4 = pp.pcf_sendFTP(dte_date, l_Path, 'HK_ChinaAMC_Bond')
        bl_success5, l_ListFilesFTP5 = pp.pcf_sendFTP(dte_date, l_Path, 'HK_GlobalX')
        bl_success = bl_success1 and bl_success2 and bl_success3 and bl_success4 and bl_success5
        l_ListFilesFTP = l_ListFilesFTP1 + l_ListFilesFTP2 + l_ListFilesFTP3 + l_ListFilesFTP4 + l_ListFilesFTP5
        
    elif str_pcf == 'HK_Noon':
        bl_success1, l_ListFilesFTP1 = pp.pcf_sendFTP(dte_date, l_Path, 'HK_PingAn')
        bl_success2, l_ListFilesFTP2 = pp.pcf_sendFTP(dte_date, l_Path, 'HK_ChinaAMC')
        bl_success3, l_ListFilesFTP3 = pp.pcf_sendFTP(dte_date, l_Path, 'HK_WisdomTree')
        bl_success4, l_ListFilesFTP4 = pp.pcf_sendFTP(dte_date, l_Path, 'HK_EASY_FI')
        bl_success5, l_ListFilesFTP5 = pp.pcf_sendFTP(dte_date, l_Path, 'HK_EASY_COMO')
        bl_success6, l_ListFilesFTP6 = pp.pcf_sendFTP(dte_date, l_Path, 'HK_EASY_JBEM')
        bl_success = bl_success1 and bl_success2 and bl_success3 and bl_success4 and bl_success5 and bl_success6
        l_ListFilesFTP = l_ListFilesFTP1 + l_ListFilesFTP2 + l_ListFilesFTP3 + l_ListFilesFTP4 + \
                        l_ListFilesFTP5 + l_ListFilesFTP6
        
    else:
        bl_success, l_ListFilesFTP = pp.pcf_sendFTP(dte_date, l_Path, str_pcf)
    # Return
    if not bl_success: return 'ERROR on {} : pcf_sendFTP did not work out !!!'.format(str_pcf), l_ListFilesFTP
    else: return True, l_ListFilesFTP














#====================================================================================================================
# PCF with their specificities
#====================================================================================================================
epsilon = 0.0000001
flt_SamsungNAV = 0


def pcf_OnlyForwarding(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # List the files :)
    try:        l_pathAttach = dic_df['files']
    except:     return 'ERROR: List of the files - {}'.format(str_PCF), []
    
    # END    
    l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________




#------------------------------------------------------------------------------
# Bengalore
#------------------------------------------------------------------------------

def pcf_YUANTA(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Name of the PCF
    try:        
        str_folder = dic_df['Folder']
        str_fileDest = str_folder + 'YuantaETFs_{}.xlsx'.format(dte_date.strftime('%Y%m%d'))
        l_pathInputFiles = dic_df['files']
    except:     return 'ERROR: {} - Dataframe'.format(str_PCF), []
    
    # Create Excel
    try:        pp.Act_CopySheetExcel_fomCsv(str_fileDest, l_pathInputFiles)
    except:     return 'ERROR: {} - Act_CopySheetExcel_fomCsv'.format(str_PCF), []
    
    # END
    l_pathAttach = [str_fileDest.replace(str_folderRoot, '')]
    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________




def Act_Change1stRowWithDate(str_path, dte_date):
    try:
        df_mod = pd.read_csv(str_path, header = None)  #, header = None, index_col = None
        df_mod.loc[0, 0] = 'Date'
        df_mod.loc[0, 1] = dte_date.strftime('%Y-%m-%d')
        df_mod.loc[0, 2] = ''
        df_mod.loc[0, 3] = ''
        df_mod.loc[0, 4] = ''
        df_mod.to_csv(str_path, header = False, index = False)
    except:     print('  ERROR in Act_Change1stRowWithDate:  ', str_path, dte_date)
    
    
def pcf_FUBON(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Name of the PCF
    try:        
        str_folder = dic_df['Folder']
        l_pathInputFiles = dic_df['files']
    except:     return 'ERROR: {} - Dataframe'.format(str_PCF), []
    
    # Gather file dowloaded 2 by 2
    try:
        l_pathAttach = []
        l_path_Build = list(set([path.replace('2_','') for path in l_pathInputFiles]))
        for str_path in l_path_Build:
            l_pathToMerge = [path for path in l_pathInputFiles if path.replace('2_','') == str_path]
            str_fileCsv1 = str_folder + 'raw' + '\\' + str_path.split('\\')[-1]
            str_fileDest = str_folder + str_path.split('\\')[-1]
            #Add Date to the CSV
            Act_Change1stRowWithDate(str_fileCsv1, dte_date)
            str_fileDest = str_fileDest.replace('id_', 'f_')
            str_fileDest = str_fileDest.replace('.csv', '.xlsx')
            pp.Act_CopySheetExcel_fomCsv(str_fileDest, l_pathToMerge, ['Sheet1','Sheet2'])
            l_pathAttach.append(str_fileDest)            
    except:     return 'ERROR: {} - Act_CopySheetExcel_fomCsv'.format(str_PCF), []
    
    # END
    l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________



def Act_EmptyRowsCathay(str_path, dte_date):
    try:
        df_mod = pd.read_csv(str_path, header = None)  #, header = None, index_col = None
        for i in range(6):
            df_mod.loc[0, i] = ''
            df_mod.loc[1, i] = ''
            df_mod.loc[2, i] = ''
        df_mod.to_csv(str_path, header = False, index = False)
    except:     print('  ERROR in Act_EmptyRowsCathay:  ', str_path, dte_date)


def pcf_CATHAY(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Name of the PCF
    try:        
        str_folder = dic_df['Folder']
        l_pathInputFiles = dic_df['files']
        str_fileDest = str_folder + 'Cathay_{}.xlsx'.format(dte_date.strftime('%Y%m%d'))
    except:     return 'ERROR: {} - Dataframe'.format(str_PCF), []
    
    # Change CSV
    try:
        for str_path in l_pathInputFiles:
            str_fileCsv1 = str_folder + 'raw' + '\\' + str_path.split('\\')[-1]
            Act_EmptyRowsCathay(str_fileCsv1, dte_date)
    except:     return 'ERROR: {} - Act_Change1stRowWithDate'.format(str_PCF), []
    
    # Create Excel
    #pp.Act_CopySheetExcel(str_fileDest, l_pathInputFiles)
    #pp.Act_CopySheetExcel_fomCsv(str_fileDest, l_pathInputFiles)
    try:        pp.Act_CopySheetExcel_fomCsv(str_fileDest, l_pathInputFiles)
    except:     return 'ERROR: {} - Act_CopySheetExcel_fomCsv'.format(str_PCF), []
    
    # END    
    l_pathAttach = [str_fileDest.replace(str_folderRoot, '')]
    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________



def pcf_BglrSamsung(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        SHLPXS = dic_df['ZIP_SHLP00845164_SR0490XS']
        SHLPXP = dic_df['ZIP_SHLP00845164_SR0490XP']
        SHIPXS = dic_df['ZIP_SHIP00845156_SR0490XS']
        SHIPXP = dic_df['ZIP_SHIP00845156_SR0490XP']
        SCLPXS = dic_df['ZIP_SCLP00845149_SR0490XS']
        SCLPXP = dic_df['ZIP_SCLP00845149_SR0490XP']
        SCIPXS = dic_df['ZIP_SCIP00845131_SR0490XS']
        SCIPXP = dic_df['ZIP_SCIP00845131_SR0490XP']
        #df_HolidayCal = dic_df['sql_Calendar']
        df_CodePivot = dic_df['sql_CodePivot']
        str_folder = dic_df['Folder']
        l_files = dic_df['files']
    except: return 'ERROR: Dataframe - {}'.format(str_PCF), []
    
    # First output file (just a path) (already download from the ZIP) (just to forward)
    l_pathAttach = [path for path in l_files if 'SKCO00844753_SR0490XP_' in path]
    
    # Other Param
    int_ApplicationSize = 300000
    str_outpath = str_folder.replace('Input','Output')
    # Create the folder
    try:    fl.fBl_createDir(str_outpath)
    except: return 'ERROR: Could not Create Folder: ' + str_outpath, []
    
    # Calendar Treat
    try:
        str_inputdate = dte_date.strftime("%Y%m%d")
        str_outputdate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, '%Y%m%d', 1, '240')
        str_PCFdate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, '%m/%d/%Y', 1, '240')
    except: return 'ERROR: Calendar - {}'.format(str_PCF), []
    
    # Rest
    try:
        # Making sure the order of ISINs coming from SQL doesn't affect the rest of the process
        Isin_Ordering = ['HK0000330537', 'HK0000330545', 'HK0000330552', 'HK0000330560']
        df_CodePivot['Isin'] = pd.Categorical(df_CodePivot['Isin'], categories = Isin_Ordering, ordered=True)
        df_CodePivot.sort_values('Isin', inplace=True)
        
        # Add a column
        df_CodePivot.loc[df_CodePivot['Ric'] == '7205.HK', 'ParentCompany'] = 'SHLP'
        df_CodePivot.loc[df_CodePivot['Ric'] == '7312.HK', 'ParentCompany'] = 'SHIP'
        df_CodePivot.loc[df_CodePivot['Ric'] == '7228.HK', 'ParentCompany'] = 'SCLP'
        df_CodePivot.loc[df_CodePivot['Ric'] == '7328.HK', 'ParentCompany'] = 'SCIP'
    except: return 'ERROR: Rest  - {}'.format(str_PCF), []
    
    ### ETF HEADER LEVEL - PARSED FILES
    try:
        df_HeaderLevelData = pd.DataFrame()
        df_HeaderLevel = pd.DataFrame()
        l_XPFiles = [SHLPXP, SHIPXP, SCLPXP, SCIPXP]
        for file in l_XPFiles:
            df_HeaderLevelData['ParentCompany'] = [file['PARENT COMPANY'].iloc[0]]
            df_HeaderLevelData['NAV'] = [file[' NET NAV/UNIT LESS PERFORMANCE FEE'].iloc[0]]
            df_HeaderLevelData['SharesOut'] = [file[' NO OF UNITS O/S'].iloc[0]]
            df_HeaderLevel = df_HeaderLevel.append(df_HeaderLevelData)
        df_HeaderLevel = df_HeaderLevel.reset_index(drop=True)
        df_Header = df_CodePivot.merge(df_HeaderLevel)
    except: return 'ERROR: ETF HEADER LEVEL - PARSED FILES - {}'.format(str_PCF), []
    
    ### Bring another Input file but he is here only sometimes
    try:
        try:
            # 1. Find the Path of the Zip again
            #print('------------ Find Special File - Ignore Error ------------')
            str_ZipPath = [path for path in l_files if 'HSBC_BULKREPORTS_' in path and '.zip' in path][0]
            #            str_folder = r'\\uk-pdeqtfs01\E\Data\Lucerne\Data\SOLA PCF\Auto_Py\BGLR_Samsung\Input' + '\\'
            #            str_ZipName = 'HSBC_BULKREPORTS_{}{}.zip'.format(dte_date.strftime('%d%m%Y'),'{XXXX}')
            #            str_ZipName = fl.fStr_GetMostRecentFile_InFolder(str_folder, str_ZipName)
            #            if str_ZipName == '': 
            #                print('ZIP cannot be found: ', str_ZipName, str_folder)
            #                raise
            #            else: str_ZipPath =  str_folder + str_ZipName
            
            # 2. Unzip it - Extract the right file
            str_fileName = 'HKGRFMHKSSET_ST-FM-TX-001-01_{}_1_{}.XLS'.format(str_inputdate, '{XXXXXX}')
            fl.ZipExtractFile(str_ZipPath, str_folder, str_fileName)
            # ********************* I actually Extract everything as I dont have the functionalities  
                        # of taking the last onelike below **************************
            #fl.ZipExtractFile(str_ZipPath, str_folder, '', True)
            
            # 3. Get the file in Dataframe  +   4. Use the file for corpoarte actions
            CorpAction = pd.DataFrame()
            for f in [glob.glob(str_folder+'HKGRFMHKSSET_ST-FM-TX-001-01_'+str_inputdate+'*.XLS')]:
                if len(f) == 0:
                    break
                elif len(f) > 0:
                    list_of_files = glob.glob(str_folder+'HKGRFMHKSSET_ST-FM-TX-001-01_'+str_inputdate+'*.XLS')
                    latest_file = max(list_of_files, key = os.path.getctime)
                    print('latest_file:', latest_file)
                    Corp = pd.read_excel(latest_file)
                    DateCheck = Corp[Corp.eq('Dealing Date:').any(1)].iloc[0].dropna()
                    DateCheck = dt.datetime.strptime(DateCheck[1], '%d-%m-%Y').strftime('%Y%m%d')
                    if DateCheck != str_inputdate:
                        print('\nThe corporate actions file, '+f[0][47:]+', has stale data ('+DateCheck+'), \
                              please check with the provider and rerun the process')
                        raise
                    else:
                        print('\nCorporate Action File Parsed '+latest_file[47:])
                        Identifier = Corp.iloc[Corp[Corp.eq('Dealing Summary Report').any(1)].index + 1,0]
                        NewShares = Corp.iloc[Corp[Corp.eq('Total Quantity In Issue After This Dealing:').any(1)].index]
                        NewShares = NewShares.dropna(axis=1).iloc[:,1]
                        CorpAction['Identifier'] = Identifier.str.strip().str[-4:]
                        CorpAction['New NOSH'] = NewShares.values
                        CorpAction = CorpAction.reset_index(drop=True)
                        NewNOSH = pd.merge(left = df_Header, right=CorpAction, left_on='ParentCompany', right_on='Identifier', how='left')
                        NewNOSH.loc[NewNOSH['ParentCompany'] == NewNOSH['Identifier'], 'SharesOut'] = NewNOSH['New NOSH']
                        df_Header['SharesOut'] = NewNOSH['SharesOut'].astype('int')        
        except: pass
        #print('-----------------------------------------------------')
    except: print('** SHOULD NEVER HAPPEN  *** Corporate Actions HKGRFMHKSSET_ST-FM-TX-001-01 not in the ZIP')
    
    ### CONSTITUENT LEVEL - PARSED FILES
    try:
        ConstituentLevelData = pd.DataFrame()
        Constituent = pd.DataFrame()
        XSFiles = [SHLPXS, SHIPXS, SCLPXS, SCIPXS]
        for file in XSFiles:
            ConstituentLevelData['Currency'] = [file[' CURRENCY CODE'].iloc[0]]
            ConstituentLevelData['Price'] = [file[' MARKET PRICE'].iloc[0]]
            ConstituentLevelData['Contracts/Shares'] = ''
            ConstituentLevelData['Holdings'] = file[' HOLDINGS'].iloc[0]
            ConstituentLevelData['BBG Ticker'] = file[' BLOOMBERG'].iloc[0].strip()
            ConstituentLevelData['Reuters'] = file[' REUTERS'].iloc[0].strip()
            ConstituentLevelData['ParentCompany'] = file['COMPANY CODE'].iloc[0].strip()
            querystring = "SELECT CurrentName FROM tblCodePivot WHERE Ric = " + "'" + file[' REUTERS'].iloc[0].strip() + "'"
            Futures = db.db_SelectReq(querystring)        
            if Futures.empty:
                raise ValueError("Warning: Futures contract has not been located in the database, check the futures in the "
                                 "" + file['COMPANY CODE'].iloc[0].strip() + "XS input file with the Reference Data Team.")
            ConstituentLevelData['Futures'] = Futures['CurrentName'].iloc[0]
            Constituent = Constituent.append(ConstituentLevelData)
            
        Constituent = Constituent.reset_index(drop=True)
        Final = df_Header.merge(Constituent)
        Final['Contracts/Shares'] = round(Final['Holdings'] * int_ApplicationSize / Final['SharesOut'], 4)
        Final['Cash - Futures Exposure'] = (Final['NAV'] * int_ApplicationSize) - (Final['Price'] * Final['Contracts/Shares'] * 50)
    except: return 'ERROR: CONSTITUENT LEVEL - PARSED FILES  - {}'.format(str_PCF), []
    
    # Create the PCF    
    try:
        IDC = pd.DataFrame()
        # HEADER LEVEL
        for Ticker in Final['ExchangeTicker']:
            PCFHeader = pd.DataFrame(columns=('', 'Futures', 'Currency', 'Price', 'Contracts/Shares', 'BBG Ticker', 'Reuters'))
            PCFHeader.loc[0] = ['', '', '', '', '', '', '']
            PCFHeader.loc[1] = ['', 'Samsung', '', '', '', '', '']
            PCFHeader.loc[2] = ['', '', '', '', '', '', '']
            PCFHeader.loc[3] = ['', 'Indicative Creation / Redemption basket Composition for trade date', str_PCFdate, '', '', '', '']
            PCFHeader.loc[4] = ['', '', '', '', '', '', '']
            PCFHeader.loc[5] = ['', 'FUND INFORMATION', '', 'Date', '', '', '']
            PCFHeader.loc[6] = ['', 'Fund Name', Final.loc[Final['ExchangeTicker'] == Ticker, 'CurrentName'].iloc[0], '', '', '', '']
            PCFHeader.loc[7] = ['', 'ISIN', Final.loc[Final['ExchangeTicker'] == Ticker, 'Isin'].iloc[0], '', '', '', '']
            PCFHeader.loc[8] = ['', 'BBG Ticker', Final.loc[Final['ExchangeTicker'] == Ticker, 'Bloomberg'].iloc[0], '', '', '', '']
            PCFHeader.loc[9] = ['', 'RIC', Final.loc[Final['ExchangeTicker'] == Ticker, 'Ric'].iloc[0], '', '', '', '']
            PCFHeader.loc[10] = ['', 'Fund Currency', 'HKD', '', '', '', '']
            PCFHeader.loc[11] = ['', 'Nav per Unit ', Final.loc[Final['ExchangeTicker'] == Ticker, 'NAV'].iloc[0]
                                    , dte_date.strftime("%m/%d/%Y"), '', '', '']
            PCFHeader.loc[12] = ['', 'Number of Units Outstanding', Final.loc[Final['ExchangeTicker'] == Ticker, 'SharesOut'].iloc[0], 
                                      '', '', '', '']
            PCFHeader.loc[13] = ['', 'Nav per Application Unit size (HKD)', 
                                     Final.loc[Final['ExchangeTicker'] == Ticker, 'NAV'].iloc[0] * int_ApplicationSize, '', '', '', '']
            PCFHeader.loc[14] = ['', 'Estimated Cash Amount for Application (HKD)', 
                                     Final.loc[Final['ExchangeTicker'] == Ticker, 'NAV'].iloc[0] * int_ApplicationSize, '', '', '', '']
            PCFHeader.loc[15] = ['', 'Application Size(Units/Application size)', int_ApplicationSize, '', '', '', '']
            PCFHeader.loc[16] = ['', 'Cash (HKD)', Final.loc[Final['ExchangeTicker'] == Ticker, 'NAV'].iloc[0] * int_ApplicationSize, 
                                 '', '', '', '']
            PCFHeader.loc[17] = ['', 'Cash - Futures Exposure', Final.loc[Final['ExchangeTicker'] == Ticker, 'Cash - Futures Exposure'].iloc[0], 
                                 '', '', '', '']
            PCFHeader.loc[18] = ['', '', '', '', '', '', '']
            PCFHeader.loc[19] = ['', 'Futures', 'Currency', 'Price', 'Contracts/Shares', 'BBG Ticker', 'Reuters']
            
        # CONSTITUENT LEVEL
            PCFCon = pd.DataFrame(columns=('', 'Futures', 'Currency', 'Price', 'Contracts/Shares', 'BBG Ticker', 'Reuters'))
            PCFCon['Futures'] = Final.loc[Final['ExchangeTicker'] == Ticker, 'Futures']
            PCFCon['Currency'] = Final.loc[Final['ExchangeTicker'] == Ticker, 'Currency']
            PCFCon['Price'] = Final.loc[Final['ExchangeTicker'] == Ticker, 'Price']
            PCFCon['Contracts/Shares'] = Final.loc[Final['ExchangeTicker'] == Ticker, 'Contracts/Shares']
            PCFCon['BBG Ticker'] = Final.loc[Final['ExchangeTicker'] == Ticker, 'BBG Ticker']
            PCFCon['Reuters'] = Final.loc[Final['ExchangeTicker'] == Ticker, 'Reuters']
            
        ### OUTPUT
            PCFFinal = PCFHeader.append(PCFCon)
            str_pcfPath = str_outpath + 'SAMSUNG_' + str(Ticker) + '_' + str_outputdate + '.xls'
            PCFFinal.to_excel(str_pcfPath, index=False, header=None)
            l_pathAttach.append(str_pcfPath)
            
        ### SIGNS FOR IDC SCHEMA
            if (Final.loc[Final['ExchangeTicker'] == Ticker, 'NAV'].iloc[0] * int_ApplicationSize) > 0:
                sign = '+'
            else:
                sign = '-'
            if PCFCon['Contracts/Shares'].iloc[0] > 0:
                sign2 = '+'
            else:
                sign2 = '-'
        ### IDC
            IDCData = pd.DataFrame(columns=('Code', 'Isin', 'Date', 'Date2', 'Currency', 'Exchange', 'Nav', 'Cash', 'Sign', 'CreationUnits', 'Currency2'))
            IDCData.loc[0] = [Ticker, Final.loc[Final['ExchangeTicker'] == Ticker, 'Isin'].iloc[0], str_outputdate, 1, 'HKD', 'XHKG', 
                                Final.loc[Final['ExchangeTicker'] == Ticker, 'NAV'].iloc[0],
                                Final.loc[Final['ExchangeTicker'] == Ticker, 'NAV'].iloc[0] * int_ApplicationSize, sign, int_ApplicationSize, '']
            IDCData.loc[1] = [PCFCon['BBG Ticker'].iloc[0], PCFCon['Futures'].iloc[0], 'XHKG', str_outputdate, Ticker, 
                                Final.loc[Final['ExchangeTicker'] == Ticker, 'Isin'].iloc[0],abs(PCFCon['Contracts/Shares'].iloc[0]), 
                                sign2, 50, PCFCon['Price'].iloc[0], 'HKD']
            IDC = IDC.append(IDCData)
    except: return 'ERROR: Create PCF 0 - {0} - {1}'.format(str_PCF, Ticker), []
    
    # Create PCF 2
    try:
        IDC = IDC.reset_index(drop=True)
        SchemaIDs = [15, 3, 1, 3, 15, 3, 1, 3]
        IDC.insert(0, '', SchemaIDs)
        
        str_pcfPath = str_outpath + 'DeltaOne.Samsung.' + str_inputdate + '.csv'
        IDC.to_csv(str_pcfPath, index=False, header=None)
        l_pathAttach.append(str_pcfPath)
    except: return 'ERROR: Create PCF 2 - {}'.format(str_PCF), []
    
    # END    
    l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]

    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________    






#------------------------------------------------------------------------------
# US
#------------------------------------------------------------------------------
def pcf_Harvest(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_HOLD =   dic_df['ZIP_NETRCNH']
        df_NAV =    dic_df['OUT_NAVharvest']   
        str_folder =    dic_df['Folder']
        #==============================================
        # TO REMOVE - Just for Print for your review
        print(df_NAV)
        #==============================================
    except Exception as err:    return 'ERROR: Dataframe - {} | {}'.format(str_PCF, str(err)), []
    
    # 0. define Model
    try:
        #==============================================
        # You need to do a Model of xlsx file that would be the model for all your pcf created: ModelHarvest.xlsx
        str_modelfolder = fl.fStr_BuildPath(str_folderRoot, 'US_Harvest')
        str_modelFileName = 'ModelHarvest.xlsx'
        l_pcfFileName = ['PCF Final file Name number 1' + dte_date.strftime('%Y%m%d') + '.xlsx', 
                         'PCF Final file Name number 2' + dte_date.strftime('%Y%m%d') + '.xlsx']
        #==============================================
    except Exception as err:    return 'ERROR: 0. define Model - {} | {}'.format(str_PCF, str(err)), []
    
    # 1. Variables
    try:
        flt_Nav = df_NAV[df_NAV['colForCriteria'] =='USD']['ColNav'].values[0]
        flt_aum = df_NAV[df_NAV['colForCriteria'] =='USD']['ColAUM'].values[0]
        flt_share = df_NAV[df_NAV['colForCriteria'] =='USD']['colShares'].values[0]
        int_CreationUnits = 50000
        flt_BasketNav = flt_Nav * int_CreationUnits
    except Exception as err:    return 'ERROR: 1. Variables - {} | {}'.format(str_PCF, str(err)), []
    
    # 2. reform Holdings DF
    try:
        # just take some rows (62:540) / columns (All) of your Hold DATAFRAME by position
        df_Fund = df_HOLD.iloc[62:540,:].copy()
        print(df_Fund.head(10))
        #        # just take some columns of your Hold DATAFRAME (if they have a name, for here, they should have only number: )
        #        df_Fund = df_Fund[['col_1_YouCHoose', 'col_2_YouCHoose']]
        #        # Rename the columns
        #        df_Fund.columns = ['GTI', 'Name']
        #        # Just take some rows
        #        df_Fund = df_Fund[df_Fund['colForCriteria'].str.startswith('S', na = False)].copy()
        # Put back the rows as 0,1,2,3,4,5,6...
        df_Fund.reset_index(drop = True, inplace = True)
    except Exception as err:    return 'ERROR: 2. reform Holdings DF - {} | {}'.format(str_PCF, str(err)), []
    
    # 3. Build last DF from Model
    try:
        df_Final = pd.read_excel(fl.fStr_BuildPath(str_modelfolder, str_modelFileName), header = None, index_col = None)
        df_Final.fillna(value = '', inplace = True)
        df_Final.iloc[5, 1] = str(flt_Nav)
        df_Final.iloc[6, 1] = str(flt_aum)
        df_Final.iloc[7, 1] = str(flt_share)
        df_Final.iloc[8, 1] = str(flt_BasketNav)
        # CONCAT
        df_FundFinal =  dframe.fDf_Concat_wColOfDf1(df_Final.loc[:9], df_Fund)
    except Exception as err:    return 'ERROR: 3. Build last DF from Model - {} | {}'.format(str_PCF, str(err)), []

    # 4. Create the files
    try:
        str_path0 = fl.fStr_BuildPath(str_folder, l_pcfFileName[0])
        # Copy files
        shutil.copyfile(fl.fStr_BuildPath(str_modelfolder, str_modelFileName), str_path0)
        # Fill in 
        str_path0 = fl.fStr_fillXls_celByCel(str_path0, df_FundFinal, '', 0, len(df_FundFinal) - 41, 35)
        l_pathAttach = [str_path0]
    except Exception as err:    return 'ERROR: 4. Create the files - {} | {}'.format(str_PCF, str(err)), []

    # 6. Build the return message
    try:
        str_resultFigures += '\n' + str(round(flt_Nav, 4)) + ' : Nav per Unit'
        str_resultFigures += '\n' + str(round(flt_aum, 0)) + ' : Asset Under M'
        str_resultFigures += '\n' + str(round(flt_share, 0)) + ' : Total Shares in Issue'
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except Exception as err:    return 'ERROR: END - {} | {}'.format(str_PCF, str(err)), []
    
    # Close EXCEL
    try:
        inst_xlApp = fl.c_win32_xlApp()
        inst_xlApp.QuitXlApp(bl_force = False)
    except Exception as Err:    print('  (*) ERROR: Close EXCEL - {} | {}'.format(str_PCF, str(Err)))
       
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________






#------------------------------------------------------------------------------
# HONG KONG
#------------------------------------------------------------------------------   
def pcf_Nikko63_Intra(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_intra = dic_df['OUT_Niko_Intra'] 
        #str_folder =    dic_df['Folder']
        print(' ...Try to see the document :')
        print(df_intra)
    except Exception as err:    return 'ERROR: Dataframe - {} | {}'.format(str_PCF, str(err)), [] 
    
    return str_resultFigures, [1, 2]


    
def pcf_Nikko63(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_HOLD =   dic_df['OUT_Niko_HOLD']
        df_NAV =    dic_df['OUT_Niko_NAV']   
        str_folder =    dic_df['Folder']
    except Exception as err:    return 'ERROR: Dataframe - {} | {}'.format(str_PCF, str(err)), []

    # 1. Variables
    try:
        str_modelfolder = fl.fStr_BuildPath(str_folderRoot, 'HK_Nikko')
        str_modelFileName = 'NikkoAMGlobalInternetETF.xlsx'
        str_modelFileName_SGX = 'NikkoSGX.xlsx'
        dte_navDate = df_NAV[df_NAV['Share currency'] =='USD']['NAV date'].values[0]
        if len(str(dte_navDate)) == 7:
            dte_navDate = '0' + str(dte_navDate)
        dte_navDate = dat.fDte_formatToDate(str(dte_navDate), '%d%m%Y')
        l_pcfFileName = ['Nikko AM Global Internet ETF - Basket - ' + dte_navDate.strftime('%Y%m%d') + '.xlsx', 
                         'Nikko AM Global Internet ETF - Fund - ' + dte_navDate.strftime('%Y%m%d') + '.xlsx',
                         'Nikko AM Global Internet ETF - SGX - ' + dte_navDate.strftime('%Y%m%d') + '.xlsx']
        # Rounding issue from pandas
        df_NAV['Price share CCY'] = df_NAV['Price share CCY'].apply(lambda x: round(x, 13))
        flt_Nav = df_NAV[df_NAV['Share currency'] =='USD']['Price share CCY'].values[0]
        flt_aum = df_NAV[df_NAV['Share currency'] =='USD']['TNA of the fund in fund CCY'].values[0]
        flt_aum_share = df_NAV[df_NAV['Share currency'] =='USD']['TNA of the share in fund CCY'].values[0]
        flt_share = df_NAV[df_NAV['Share currency'] =='USD']['Nb of outstanding shares'].values[0]
        int_CreationUnits = 50000
        flt_BasketNav = flt_Nav * int_CreationUnits
    except Exception as err:    return 'ERROR: 1. Variables - {} | {}'.format(str_PCF, str(err)), []
    
    # 20. reform Holdings DF
    try:
        df_HOLD = df_HOLD[['GTI code', 'Security name','External value code','Sedol codification','Security currency',
                           'Quantity','Quotation price of Security','Exchange rate', 'Evaluation price in fund ccy']]
        df_HOLD.columns = ['GTI', 'Name','Isin','Sedol','Ccy','Qty','Price','Fx', 'Fund_MktCap']
        df_HOLD = df_HOLD.fillna(value = '').copy()
        # Split between HOLDINGS and Cash
        df_Holdings =   df_HOLD[df_HOLD['Isin'] != '']
        df_Cash =       df_HOLD[df_HOLD['Isin'] == '']
        if len(df_Cash[df_Cash['GTI'].str.startswith('S', na = False)]) > 0:
            print(' WARNING in pcf_Nikko63: Cash has holdings')
            print(df_Cash[df_Cash['GTI'].str.startswith('S', na = False)])
        if len(df_Cash[df_Cash['GTI'].str.startswith('R', na = False)]) > 0:
            print(' WARNING in pcf_Nikko63: Cash has holdings')
            print(df_Cash[df_Cash['GTI'].str.startswith('R', na = False)])
        if len(df_Holdings[df_Holdings['GTI'].str.startswith('S', na = False)]) == 0:
            print(' WARNING in pcf_Nikko63: No holdings with S')
            print(df_Holdings[df_Holdings['GTI'].str.startswith('S', na = False)])
        if len(df_Holdings[df_Holdings['GTI'].str.startswith('C', na = False)]) > 0:
            print(' WARNING in pcf_Nikko63: holdings has CO')
            print(df_Holdings[df_Holdings['GTI'].str.startswith('C', na = False)])
        if len(df_Holdings[df_Holdings['GTI'] == '']) > 0:
            print(' WARNING in pcf_Nikko63: holdings has empty GTI')
            print(df_Holdings[df_Holdings['GTI'] == ''])
        df_Holdings.reset_index(drop = True, inplace = True)
    except Exception as err:    return 'ERROR: 20. reform Holdings DF - {} | {}'.format(str_PCF, str(err)), []
    # 21. Build Df on Basket
    try:
        df_Basket = df_Holdings[['Name','Isin','Sedol','Ccy','Qty','Price','Fx']].copy()
        if '63' in str_PCF:
            df_Basket['Qty_basket'] = df_Basket['Qty'] * int_CreationUnits / flt_share * (flt_aum_share / flt_aum)
        else:
            df_Basket['Qty_basket'] = df_Basket['Qty'] * int_CreationUnits / flt_share 
        df_Basket['Qty_basket'] = df_Basket['Qty_basket'].apply(lambda x: math.floor(x))
        df_Basket['Basket_MktCap'] = df_Basket['Qty_basket'] * df_Basket['Price'] / df_Basket['Fx']
        df_Basket['Weight'] = df_Basket['Basket_MktCap'] / flt_BasketNav
        # Variables Again
        flt_BasketMarketCap = df_Basket['Basket_MktCap'].sum()
        flt_BasketCash = flt_BasketNav - flt_BasketMarketCap
        flt_BasketCashWeight = flt_BasketCash / flt_BasketNav
    except Exception as err:    return 'ERROR: 21. Build Df on Basket - {} | {}'.format(str_PCF, str(err)), []
    # 22. SGX customization
    try:
        df_SGX = df_Basket.copy()
        df_SGX['Fx'] = 1 / df_SGX['Fx']
        df_SGX = dframe.fDf_InsertColumnOfIndex(df_SGX, 1, 0)
        df_SGX['Price'] = df_SGX['Price'].apply(lambda x : round(x,6))
        df_SGX = df_SGX[['ind', 'Name','Ccy','Price','Qty_basket','Isin','Sedol','Fx']]
        # Back to normal basket: Fill the last ROW ...
        df_Basket = df_Basket[['Name','Isin','Sedol','Ccy','Qty_basket','Price','Basket_MktCap','Weight']].copy()
        df_Basket.loc[len(df_Basket)] = ['CASH COMPONENT','NIL','NIL','USD',str(flt_BasketCash),'0',str(flt_BasketCash),str(flt_BasketCashWeight)]
    except Exception as err:    return 'ERROR: # 22. SGX customization - {} | {}'.format(str_PCF, str(err)), []
    # 22. Build Df on Fund
    try:
        df_Fund = df_Holdings[['Name','Isin','Sedol','Ccy','Qty','Price','Fund_MktCap']].copy()
        df_Fund['Qty'] = df_Fund['Qty'].apply(lambda x: math.floor(x))
        df_Fund['Weight'] = df_Fund['Fund_MktCap'] / flt_aum
        # Variables again
        flt_FundMarketCap = df_Holdings['Fund_MktCap'].sum()
        flt_aum2 = flt_FundMarketCap + df_Cash['Fund_MktCap'].sum()
        if abs(flt_aum2 - flt_aum) > 0.2: 
            print('  ***  Warning : AUM is not the same from source')
            print('  ***  flt_aum: ', flt_aum)
            print('  ***  flt_aum2: ', flt_aum2)
        flt_FundCash = flt_aum2 - flt_FundMarketCap
        flt_FundCashWeight = flt_FundCash / flt_aum       
        # To Fill the last ROW ...
        df_Fund.loc[len(df_Fund)] = ['CASH COMPONENT','NIL','NIL','USD', str(flt_FundCash),'0', str(round(flt_FundCash, 2)), str(flt_FundCashWeight)]
    except Exception as err:    return 'ERROR: 22. Build Df on Fund - {} | {}'.format(str_PCF, str(err)), []
    
    # 3. Build last DF from Model
    try:
        df_Final = pd.read_excel(fl.fStr_BuildPath(str_modelfolder, str_modelFileName), header = None, index_col = None)
        df_Final.fillna(value = '', inplace = True)
        df_Final.iloc[0, 1] = dte_navDate.strftime('%m/%d/%Y')
        df_Final.iloc[5, 1] = str(flt_Nav)
        df_Final.iloc[6, 1] = str(flt_aum)
        df_Final.iloc[7, 1] = str(flt_share)
        # SGX
        df_SGXfinal = pd.read_excel(fl.fStr_BuildPath(str_modelfolder, str_modelFileName_SGX), header = None, index_col = None)
        df_SGXfinal.fillna(value = '', inplace = True)
        df_SGXfinal.iloc[3, 2] = dte_navDate.strftime('%m/%d/%Y')
        df_SGXfinal.iloc[11, 2] = str(flt_Nav)
        df_SGXfinal.iloc[12, 2] = str(flt_aum)
        df_SGXfinal.iloc[13, 2] = str(flt_share)
        df_SGXfinal.iloc[14, 2] = str(int_CreationUnits)
        df_SGXfinal.iloc[15, 2] = str(flt_BasketCash)
        # CONCAT
        df_FundFinal =  dframe.fDf_Concat_wColOfDf1(df_Final.loc[:9], df_Fund)
        if '63' in str_PCF:         df_Final.iloc[6, 1] = str(flt_aum_share)                # Exception for 63
        df_BasketFinal= dframe.fDf_Concat_wColOfDf1(df_Final.loc[:9], df_Basket)
        df_SGXfinal =  dframe.fDf_Concat_wColOfDf1(df_SGXfinal.loc[:18], df_SGX)
    except Exception as err:    return 'ERROR: 3. Build last DF from Model - {} | {}'.format(str_PCF, str(err)), []

    # 4. Create the files
    try:
        str_path0 = fl.fStr_BuildPath(str_folder, l_pcfFileName[0])
        str_path1 = fl.fStr_BuildPath(str_folder, l_pcfFileName[1])
        str_path2 = fl.fStr_BuildPath(str_folder, l_pcfFileName[2])
        # Copy files
        shutil.copyfile(fl.fStr_BuildPath(str_modelfolder, str_modelFileName), str_path0)
        shutil.copyfile(fl.fStr_BuildPath(str_modelfolder, str_modelFileName), str_path1)
        shutil.copyfile(fl.fStr_BuildPath(str_modelfolder, str_modelFileName_SGX), str_path2)
        # Fill in 
        str_path0 = fl.fStr_fillXls_celByCel(str_path0, df_BasketFinal, '', 0, len(df_BasketFinal) - 41, 35)
        str_path1 = fl.fStr_fillXls_celByCel(str_path1, df_FundFinal, '', 0, len(df_FundFinal) - 41, 35)
        str_path2 = fl.fStr_fillXls_celByCel(str_path2, df_SGXfinal, '', 0, len(df_SGX) - 30, 40)
        l_pathAttach = [str_path0, str_path1, str_path2]
    except Exception as err:    return 'ERROR: 4. Create the files - {} | {}'.format(str_PCF, str(err)), []

    # 6. Build the return message
    try:
        str_resultFigures += '\n' + str(round(flt_Nav, 4)) + ' : Nav per Unit'
        str_resultFigures += '\n' + str(round(flt_aum, 0)) + ' : Asset Under M'
        str_resultFigures += '\n' + str(round(flt_share, 0)) + ' : Total Shares in Issue'
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except Exception as err:    return 'ERROR: END - {} | {}'.format(str_PCF, str(err)), []
    
    # Close EXCEL
    try:
        inst_xlApp = fl.c_win32_xlApp()
        inst_xlApp.QuitXlApp(bl_force = False)
    except Exception as Err:    print('  (*) ERROR: Close EXCEL - {} | {}'.format(str_PCF, str(Err)))
    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________
  



def pcf_EasyFi(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # List the files :)
    try:        
        str_folder = dic_df['Folder']
        str_folder = str_folder.replace('Easy Commodity - open','Easy FI - open')
        fl.fBl_createDir(str_folder)
        l_PCF = ['COELQC_', 'COSRIC_', 'COSRIC3_', 'COSRIC5_', 'PCFELQC', 'PCFSRIC', 'PCFSRIC3', 'PCFSRIC5']
        l_resultPath = ['{0}{1}{2}.txt'.format(str_folder, x, dte_date.strftime('%Y%m%d')) for x in l_PCF]
        l_requestPath = ['{0}file\\~Easy PCF geneation SQL - {1}.txt'.format(str_folderRoot, x.replace('_', '')) for x in l_PCF]
    except:     return 'ERROR: List of the filles - {}'.format(str_PCF), []
    
    # Check the integration in database
    try:
        bl_check = True
        l_reqCheck = ['Select MAX(i.AsAtDate) as DATE from vwIndexSummary i where IndexID = 222614',
                      'Select MAX(i.AsAtDate) as DATE from vwIndexSummary i where IndexID = 250715',
                      'Select MAX(i.AsAtDate) as DATE from vwIndexSummary i where ListingID = 2906716',
                      'Select MAX(i.AsAtDate) as DATE from vwIndexSummary i where ListingID = 2906732',
                      'Select MAX(i.AsAtDate) as DATE from vwETFSummary i where ETFID = 16841',
                      'Select MAX(i.AsAtDate) as DATE from vwETFSummary i where ETFID = 21250',
                      'Select MAX(i.AsAtDate) as DATE from vwETFSummary i where ETFID = 23075',
                      'Select MAX(i.AsAtDate) as DATE from vwETFSummary i where ETFID = 23076']
        for str_req in l_reqCheck:
            df_sqlResult = db.db_SelectReq(str_req)
            int_dateDiff = dat.fInt_dateDifference(dte_date, df_sqlResult['DATE'].values[0])
            if int_dateDiff > 0:
                print('The request returns a Date older than expected: {0}. \n (*) {1} \n'.format(df_sqlResult['DATE'].values[0], str_req))
                bl_check = False
        # If one Check is not OK, we will return empty list
        if not bl_check:        
            return 'The check did not pass !', []
    except:     return 'ERROR: Check the integration in database - {}'.format(str_PCF), []
    
    # Execute Request and save the result into Result Files
    try:
        for i_pcf in range(len(l_PCF)):
            str_req = fl.fStr_ReadFile_sql(l_requestPath[i_pcf])
            df_sqlResult = db.db_MultipleReq(str_req)
            df_sqlResult.fillna(value = 'NULL', inplace = True)
            fl.fStr_CreateTxtFile(l_resultPath[i_pcf], '', df_sqlResult, str_sep = '\t', bl_header = False, bl_index = False)
            # Replace the shitty 0E-14
            try:    fl.UpdateTxtFile(l_resultPath[i_pcf], '0E-14', '0.00000000000000')            
            except: pass
    except Exception as err: 
        return 'ERROR: Execute Request and save the result into Result Files - {0} | {1} | {2}'.format(str_PCF, l_PCF[i_pcf], str(err)), []
    
    l_pathAttach = [path.replace(str_folderRoot, '') for path in l_resultPath]
    
    return 'ok', l_pathAttach
#___________________________________________________________________________________________






def IsDateMatching_WT(dte_NAVDate, df_IndexValue, df_FX):
    # Index date
    dte_IndexDate = df_IndexValue.loc[df_IndexValue['Index'] == 'Date', 'BNPIC52T'].values[0]
    dte_IndexDate = dat.fDte_formatToDate(dte_IndexDate, '%d-%b-%Y')
    # FX date
    dte_fxDate = df_FX.loc[df_FX['ToCurrencyCode'] =='EUR', 'AsAtDate'].values[0]
    dte_fxDate = dat.fDte_formatToDate(dte_fxDate, '%m/%d/%Y')
    # Compare
    if dte_IndexDate != dte_NAVDate:
        print('')
        print(' ERROR: the NAV date is different from the Index date')
        print(' - The NAV Date in the Last Valuation file for the 2 funds LU1291109533 & LU1291109616 is : {}'.format(dte_NAVDate))
        print(' - The Index Date is : {}'.format(dte_IndexDate))
        print('------------------------------------------------------------')
        print(df_IndexValue.head(5))
        print('------------------------------------------------------------')
        print(df_FX.head(5))
        print('------------------------------------------------------------')
        return False
    return True



    
def pcf_EasyComo(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_MACRO_NAV = dic_df['MACRO_NAV']
        df_Composition = dic_df['OUT_COMPOSITION']
        df_IndexValue = dic_df['OUT_INDEXVALUE']        
        df_IndexValue_dm2 = dic_df['OUT_INDEXVALUE_Dm2']
        df_LastValuation = dic_df['OUT_LASTVALUATION']
        df_FX = dic_df['Como_sql_FX']
        df_FX_dm2 = dic_df['Como_sql_FX_dm2']
        str_folder = dic_df['Folder']
    except Exception as err: return 'ERROR: Dataframe - {} | {}'.format(str_PCF, str(err)), []
    
    # Get the right dataframe for Dm2
    try:
        # NAV Date
        dte_NAVDate_LU1291109533 = df_LastValuation.loc[df_LastValuation['ISIN Code'] == 'LU1291109533', 'NAV Date'].values[0]
        dte_NAVDate_LU1291109616 = df_LastValuation.loc[df_LastValuation['ISIN Code'] == 'LU1291109616', 'NAV Date'].values[0]
        dte_NAVDate_LU1291109533 = dat.fDte_formatToDate(dte_NAVDate_LU1291109533)
        dte_NAVDate_LU1291109616 = dat.fDte_formatToDate(dte_NAVDate_LU1291109616)
        if not dte_NAVDate_LU1291109533 == dte_NAVDate_LU1291109616:
            print(' ERROR: the NAV date in the Last Valuation file is different for the 2 funds : LU1291109533 & LU1291109616')
            print(' - The NAV Date for LU1291109533 is : {}, {}'.format(dte_NAVDate_LU1291109533, type(dte_NAVDate_LU1291109533)))
            print(' - The NAV Date for LU1291109616 is : {}, {}'.format(dte_NAVDate_LU1291109616, type(dte_NAVDate_LU1291109616)))
            return ' ERROR: the NAV date in the Last Valuation file is different for the 2 funds : LU1291109533 & LU1291109616', [] 
        else:
            dte_NAVDate = dte_NAVDate_LU1291109533
        # LOOP until we match the Date
        if not IsDateMatching_WT(dte_NAVDate, df_IndexValue_dm2, df_FX_dm2):
            l_listPast = ['3', '4', '5']
            for str_i in l_listPast:
                str_indexID = 'OUT_INDEXVALUE_Dm{}'.format(str_i)
                str_fxID = 'Como_sql_FX_dm{}'.format(str_i)
                df_IndexValue_dm2 = dic_df[str_indexID]
                df_FX_dm2 = dic_df[str_fxID]
                if IsDateMatching_WT(dte_NAVDate, df_IndexValue_dm2, df_FX_dm2):
                    print('We found the right date for D minus {0}: {1}'.format(str_i, dte_NAVDate))
                    break
                else:
                    # Return Error when last one is reached
                    if str_i == l_listPast[-1]:
                        return ' ERROR: the NAV date and the index date are different. Please check the files manually', []                            
    except Exception as err: return 'ERROR: Get the right dataframe for Dm2 - {} | {}'.format(str_PCF, str(err)), []
    
    # Other param
    str_Date = dte_date.strftime("%Y%m%d")
    str_dm1 = (dte_date-BDay(1)).strftime("%Y%m%d")
    l_pcfFileName = ['COGSCU_{}.txt'.format(dte_date.strftime('%Y%m%d')),
                     'COGSDE_GSCE_{}.txt'.format(dte_date.strftime('%Y%m%d')),
                     'PCFGSCU{}.txt'.format(dte_date.strftime('%Y%m%d')),
                     'PCFGSCE{}.txt'.format(dte_date.strftime('%Y%m%d'))]
    
    # Variables
    try:
        int_creationUnit_gscu = 13 * 10000
        flt_nav_gscu = df_LastValuation.loc[df_LastValuation['ISIN Code'] == 'LU1291109533', 'NAV/share'].values[0]
        flt_shareNb_gscu = df_LastValuation.loc[df_LastValuation['ISIN Code'] == 'LU1291109533', 'Share Nb'].values[0]
        #-----------------------
        # Index Value
        flt_indexValue_dm1 = float(df_IndexValue.loc[df_IndexValue['Index'] == 'Index Value', 'BNPIC52T'].values[0])
        flt_indexValue_dm2 = float(df_IndexValue_dm2.loc[df_IndexValue_dm2['Index'] == 'Index Value', 'BNPIC52T'].values[0])
        flt_indexMove = flt_indexValue_dm1 / flt_indexValue_dm2
        #-----------------------
        flt_navEstimated_gscu = flt_nav_gscu * flt_indexMove
        flt_aum_gscu = flt_navEstimated_gscu * int_creationUnit_gscu
    except: return 'ERROR: Variables gscu - {}'.format(str_PCF), []
    try:
        int_creationUnit_gsde = 3 * 10000
        flt_nav_gsde = df_LastValuation.loc[df_LastValuation['ISIN Code'] == 'LU1291109616', 'NAV/share'].values[0]
        flt_shareNb_gsde = df_LastValuation.loc[df_LastValuation['ISIN Code'] == 'LU1291109616', 'Share Nb'].values[0]
        #-----------------------
        # Fx
        flt_fx_usdeur = float(df_FX.loc[df_FX['ToCurrencyCode'] =='EUR', 'Value'].values[0])
        flt_fx_usdeur_dm2 = float(df_FX_dm2.loc[df_FX_dm2['ToCurrencyCode'] =='EUR', 'Value'].values[0])
        flt_fxMove = flt_fx_usdeur / flt_fx_usdeur_dm2
        #-----------------------
        flt_navEstimated_gsde = flt_nav_gsde * flt_indexMove * flt_fxMove
        flt_aum_gsde = flt_navEstimated_gsde * int_creationUnit_gsde
    except: return 'ERROR: Variables gsde - {}'.format(str_PCF), []
    
    # Composition
    try:
        str_colName = 'Bloomberg Code'
        df_codePivot = pp.EasyComo_GetPivotCode(df_Composition, str_colName, str_folderRoot + 'file', 'PivotCode_EasyComo.csv')
        df_Composition = pd.merge(df_Composition, df_codePivot, on = str_colName, how = 'left')
        df_Composition.reset_index(drop = True, inplace = True)
        df_Composition['1Col'] = '3'
        df_Composition['1Col_B'] = 'B'
        df_Composition['2Col_ind'] = df_Composition.index + 1
        df_Composition['3Col_fut'] = 'Future'
        df_Composition['4Col_NULL'] = 'NULL'
        df_Composition['7Col_0'] = '0'
        df_Composition['10Col'] = '-'
        df_Composition['15Col_T'] = 'T'
        df_Composition['FX_GSDE'] = df_Composition['FX'] * flt_fx_usdeur
        df_Composition['Spot_COGSDE'] = df_Composition['Spot'] * df_Composition['FX_GSDE']
        df_Composition['Weight'] = df_Composition['Relative Weight'] * 100
        # Cash Weight
        flt_cashWeight = df_Composition.loc[df_Composition['Bloomberg Code'] == '-', 'Relative Weight'].sum()
        df_Composition = df_Composition.loc[df_Composition['Bloomberg Code'] != '-'].copy()
        int_nbCompo = len(df_Composition.index)  # or df_Composition.shape[0]
    except: return 'ERROR: Composition - {}'.format(str_PCF), []
    
    # Compo - COGSCU
    try:
        d_COGSCU_comp = df_Composition.copy()
        d_COGSCU_comp['3Col_isin'] = 'LU1291109533'
        d_COGSCU_comp['11Col_CCY'] = 'USD' 
        d_COGSCU_comp['Mkt_Cap'] = flt_aum_gscu * d_COGSCU_comp['Relative Weight']
        d_COGSCU_comp['Shares'] = d_COGSCU_comp['Mkt_Cap'] / (d_COGSCU_comp['FX'] * d_COGSCU_comp['Spot'] * d_COGSCU_comp['Multiplier'])
        d_COGSCU = d_COGSCU_comp[['1Col', '2Col_ind', '3Col_isin', '4Col_NULL', 'SecurityName', 'Shares', 'Spot','Mkt_Cap', 'Weight', 
                                  '10Col', '10Col', '11Col_CCY', '4Col_NULL', '4Col_NULL', 'Ric', 'Bloomberg']]
    except Exception as err: return 'ERROR: Compo - COGSCU - {} | {}'.format(str_PCF, str(err)), []
    # Compo - COGSDE
    try:
        d_COGSDE_comp = df_Composition.copy()
        d_COGSDE_comp['3Col_isin'] = 'LU1291109616'
        d_COGSDE_comp['11Col_CCY'] = 'EUR' 
        d_COGSDE_comp['Mkt_Cap'] = flt_aum_gsde * d_COGSDE_comp['Relative Weight']
        d_COGSDE_comp['Shares'] = d_COGSDE_comp['Mkt_Cap'] / (d_COGSDE_comp['FX_GSDE'] * d_COGSDE_comp['Spot'] * d_COGSDE_comp['Multiplier'])
        d_COGSDE = d_COGSDE_comp[['1Col', '2Col_ind', '3Col_isin', '4Col_NULL', 'SecurityName', 'Shares', 'Spot_COGSDE', 'Mkt_Cap', 'Weight', 
                                  '10Col', '10Col', '11Col_CCY', '4Col_NULL', '4Col_NULL', 'Ric', 'Bloomberg']]
    except Exception as err: return 'ERROR: Compo - COGSDE - {} | {}'.format(str_PCF, str(err)), []
    
    # Compo - PCFGSCU
    try:
        d_PCFGSCU = d_COGSCU_comp[['1Col_B', '3Col_isin', '3Col_fut', 'Isin', 'Ric', 'Bloomberg', '7Col_0', 'SecurityName', 'Shares', 
                                   '10Col', '10Col','2Col_ind', 'Spot', '10Col', '15Col_T', '3Col_isin', 'Mkt_Cap', 'Weight', 
                                   '4Col_NULL', '4Col_NULL']].copy()
    except Exception as err: return 'ERROR: Compo - PCFGSCU - {} | {}'.format(str_PCF, str(err)), []
    
    # Compo - PCFGSCE
    try:
        d_PCFGSCE = d_COGSDE_comp[['1Col_B', '3Col_isin', '3Col_fut', 'Isin', 'Ric', 'Bloomberg', '7Col_0', 'SecurityName', 'Shares', 
                                   '10Col', '10Col','2Col_ind', 'Spot_COGSDE', '10Col', '15Col_T', '3Col_isin', 'Mkt_Cap', 'Weight', 
                                   '4Col_NULL', '4Col_NULL']].copy()
    except Exception as err: return 'ERROR: Compo - PCFGSCE - {} | {}'.format(str_PCF, str(err)), []
    
    # Header COGSCU
    try:
        flt_mktCap_gscu = d_COGSCU['Mkt_Cap'].sum()
        flt_cashEstimated_gscu = flt_cashWeight * flt_aum_gscu
        df_Head_gscu = pd.DataFrame(columns = range(0, 24))
        df_Head_gscu.loc[len(df_Head_gscu)] = ['1','-','LU1291109533','NULL','BNP PARIBAS EASY ENERGY & METALS ENHANCED ROLL (USD)',
                                                  '-','BNPIC52T COMM TR INDEX','NULL','-','-','P','S','-','-','-','-','-','-','-','','','','','']
        df_Head_gscu.loc[len(df_Head_gscu)] = ['2', str_Date, 'LU1291109533', str(round(int_creationUnit_gscu,0)), str(round(flt_aum_gscu, 4)),
                                                  str(round(flt_mktCap_gscu, 4)), str(round(flt_navEstimated_gscu, 9)), 
                                                  str(round(flt_cashEstimated_gscu, 4)), str(round(flt_cashWeight, 4)),'EUR', 
                                                  str(int(flt_shareNb_gscu)), str(round(flt_aum_gscu, 4)), 'NULL','NULL', '', 'NULL',
                                                  str(round(flt_navEstimated_gscu, 9)), str_Date, 
                                                  str(flt_indexValue_dm1), str_Date,'-','-','-','-']
    except Exception as err: return 'ERROR: Header COGSCU - {} | {}'.format(str_PCF, str(err)), []
    # Header COGSDE
    try:
        flt_mktCap_gsde = d_COGSDE['Mkt_Cap'].sum()
        flt_cashEstimated_gsde = flt_cashWeight * flt_aum_gsde
        df_Head_gsde = pd.DataFrame(columns = range(0, 24))
        df_Head_gsde.loc[len(df_Head_gsde)] = ['1','-','LU1291109616','NULL','BNP PARIBAS EASY ENERGY & METALS ENHANCED ROLL (EUR)',
                                                 '-','BNPIC52T COMM TR INDEX ','NULL','-','-','P','S','-','-','-','-','-','-','-','','','','','']
        df_Head_gsde.loc[len(df_Head_gsde)] = ['2', str_Date, 'LU1291109616', str(round(int_creationUnit_gsde,0)), str(round(flt_aum_gsde, 4)),
                                                  str(round(flt_mktCap_gsde, 4)), str(round(flt_navEstimated_gsde, 9)), 
                                                  str(round(flt_cashEstimated_gsde, 4)), str(round(flt_cashWeight, 4)), 'EUR', 
                                                  str(int(flt_shareNb_gsde)), str(round(flt_aum_gsde, 4)), 'NULL','NULL', '', 'NULL',
                                                  str(round(flt_navEstimated_gsde, 9)), str_Date, 
                                                  str(flt_indexValue_dm1 * flt_fx_usdeur), str_Date,'-','-','-','-']
    except Exception as err: return 'ERROR: Header COGSDE - {} | {}'.format(str_PCF, str(err)), []
    
    # Header PCFGSCU
    try:
        df_Head_PCFGSCU = pd.DataFrame(columns = range(0, 30))
        df_Head_PCFGSCU.loc[len(df_Head_PCFGSCU)] = ['H','NSCFR0IGSCU0','DV', str(int(int_nbCompo)), '1', str_Date, str_dm1, 
                            str(round(flt_navEstimated_gscu, 9)), '-', '-',str(round(flt_cashEstimated_gscu /int_creationUnit_gscu, 9)), '-',
                            str(int(flt_shareNb_gscu)), str(round(flt_aum_gscu, 4)), str(int(int_creationUnit_gscu)),'USD','USD','USD',
                            'LU1291109533','GSCU.PA','GSCU FP Equity','.BNPIC52T','IGSCU','-','-','-','-','-','-',
                            str(round(flt_indexValue_dm1, 9))]
    except Exception as err: return 'ERROR: Header PCFGSCU - {} | {}'.format(str_PCF, str(err)), []
    # Header PCFGSCE
    try:
        df_Head_PCFGSCE = pd.DataFrame(columns = range(0, 30))
        df_Head_PCFGSCE.loc[len(df_Head_PCFGSCE)] = ['H','NSCFR0IGSCE4','DV', str(int(int_nbCompo)), '1', str_Date, str_dm1, 
                            str(round(flt_navEstimated_gsde, 9)), '-', '-', str(round(flt_cashEstimated_gsde /int_creationUnit_gsde, 9)), '-',
                            str(int(flt_shareNb_gsde)), str(round(flt_aum_gsde, 4)), str(int(int_creationUnit_gsde)),'EUR','USD','EUR',
                            'LU1291109616', 'GSCE.AS', 'GSCE NA Equity','.BNPIC52T','IGSCE','-','-','-','-','-','-',
                            str(round(flt_indexValue_dm1 * flt_fx_usdeur, 9))]
    except Exception as err: return 'ERROR: Header PCFGSCE - {} | {}'.format(str_PCF, str(err)), []
    
    
    # Create Final DF
    try:
        l_pathAttach = ['{0}{1}'.format(str_folder, x) for x in l_pcfFileName]
        df_finalGSCU = dframe.fDf_Concat_wColOfDf1(df_Head_gscu, d_COGSCU)
        df_finalGSDE = dframe.fDf_Concat_wColOfDf1(df_Head_gsde, d_COGSDE)
        df_finalPCFGSCU = dframe.fDf_Concat_wColOfDf1(df_Head_PCFGSCU, d_PCFGSCU)
        df_finalPCFGSCE = dframe.fDf_Concat_wColOfDf1(df_Head_PCFGSCE, d_PCFGSCE)
        df_finalGSCU.fillna(value = '', inplace = True)
        df_finalGSDE.fillna(value = '', inplace = True)
        df_finalPCFGSCU.fillna(value = '', inplace = True)
        df_finalPCFGSCE.fillna(value = '', inplace = True)
        fl.fStr_CreateTxtFile(l_pathAttach[0], '', df_finalGSCU, str_sep = '\t')        #, str_sep = '\t', bl_header = False, bl_index = False
        fl.fStr_CreateTxtFile(l_pathAttach[1], '', df_finalGSDE, str_sep = '\t')
        fl.fStr_CreateTxtFile(l_pathAttach[2], '', df_finalPCFGSCU, str_sep = '\t')
        fl.fStr_CreateTxtFile(l_pathAttach[3], '', df_finalPCFGSCE, str_sep = '\t')
    except Exception as err: return 'ERROR: Create Final DF - {} | {}'.format(str_PCF, str(err)), []
    
    # Build the Target Nav File
    try:
        # MERGE the DF
        df_GSCUGSCE = dframe.fDf_Concat_wColOfDf1(df_Head_PCFGSCU, df_Head_PCFGSCE)
        # Create the Row to add
        df_NavToAdd = pp.fDf_EasyCom_NavToAdd(df_GSCUGSCE, dte_date, dte_NAVDate)
        # CONCAT
        df_MACRO_NAV = dframe.fDf_Concat_wColOfDf1(df_MACRO_NAV, df_NavToAdd)
        df_MACRO_NAV.fillna(value = '', inplace = True)
        # Create the Excel File wihout model
        str_pathTargetNav = fl.fStr_BuildPath(str_folder.replace('Easy Commodity - open','Target NAV'), 
                                              'NavCalcOutputs_{}.xlsx'.format(str_dm1))        
        str_pathTargetNav = fl.fStr_createExcel_SevSh(str_pathTargetNav, '', [df_MACRO_NAV], ['Output'], 
                                                      bl_header = True, d_options = {'strings_to_numbers': True})
        #str_pathTargetNav = fl.fStr_createExcel_1Sh(str_pathTargetNav, '', df_MACRO_NAV, str_SheetName = '', bl_header = True)
        # END
        l_pathAttach.append(str_pathTargetNav)
    except Exception as err: return 'ERROR: Build the Target Nav File - {} | {}'.format(str_PCF, str(err)), []
    
    # END
    try:
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except Exception as err: return 'ERROR: END - {} | {}'.format(str_PCF, str(err)), []
    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________






def pcf_WisdomTree(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_Compo = dic_df['OUT_Compo']
        df_Nav = dic_df['FTP_NAV']
        df_Fwd = dic_df['FTP_Forward']
        df_FX = dic_df['sql_FX']
        df_WCOG = dic_df['Out_WCOG']
        df_WCOA = dic_df['Out_WCOA']
        str_folder = dic_df['Folder']
    except: return 'ERROR: {} - Dataframe'.format(str_PCF), []
    
    # Other param
    l_pcfFileName = ['WisdomTreePCF_WCOM_' + dte_date.strftime('%Y%m%d') + '.xlsx', 
                     'WisdomTreePCF_WCOE_' + dte_date.strftime('%Y%m%d') + '.xlsx', 
                     'WisdomTreePCF_COMS_' + dte_date.strftime('%Y%m%d') + '.xlsx', 
                     'WisdomTreePCF_WCOA_' + dte_date.strftime('%Y%m%d') + '.xlsx', 
                     'WisdomTreePCF_WCOG_' + dte_date.strftime('%Y%m%d') + '.xlsx']
    l_etfFileName = ['WTWCOM.etf', 'WTWCOE.etf', 'WTCOMS.etf', 'WTWCOA.etf', 'WTWCOG.etf']
    
    # NAV df
    try:
        i_row_WISX004 = df_Nav.loc[df_Nav['SEDOL'] == 'WISX004'].index[0]
        i_row_WISX005 = df_Nav.loc[df_Nav['SEDOL'] == 'WISX005'].index[0]
        i_row_WISX006 = df_Nav.loc[df_Nav['SEDOL'] == 'WISX006'].index[0]
        i_sep = i_row_WISX006 - i_row_WISX005
        df_Nav_Use = df_Nav.iloc[i_row_WISX004:i_row_WISX006 + i_sep, 0:10].copy()
        df_Nav_Use.reset_index(drop = True, inplace = True)
    except: return 'ERROR: {} - NAV df'.format(str_PCF), []
    
    # Variables
    try:
        # NAV File
        str_NavDate = df_Nav_Use.iloc[0, 1]
        dte_NavDate = dat.fDte_formatToDate(str_NavDate, '%Y%m%d')
        flt_navWCOM = float(df_Nav_Use.iloc[3, 1])
        flt_navWCOE = float(df_Nav_Use.iloc[11, 1])
        flt_navCOMS = float(df_Nav_Use.iloc[19, 1])
        int_CreationUnits_WCOM = int(df_Nav_Use.iloc[1, 1])
        int_CreationUnits_WCOE = int(df_Nav_Use.iloc[9, 1])
        int_CreationUnits_COMS = int(df_Nav_Use.iloc[17, 1])
        flt_ShareOutstanding_WCOM = float(df_Nav_Use.iloc[6, 1])
        flt_ShareOutstanding_WCOE = float(df_Nav_Use.iloc[14, 1])
        flt_ShareOutstanding_COMS = float(df_Nav_Use.iloc[22, 1])
        flt_factor1_WCOM = int_CreationUnits_WCOM / flt_ShareOutstanding_WCOM
        flt_factor1_WCOE = int_CreationUnits_WCOE / flt_ShareOutstanding_WCOE
        flt_factor1_COMS = int_CreationUnits_COMS / flt_ShareOutstanding_COMS
        flt_AUM_WCOM = flt_navWCOM * flt_ShareOutstanding_WCOM
        flt_AUM_WCOE = flt_navWCOE * flt_ShareOutstanding_WCOE
        flt_AUM_COMS = flt_navCOMS * flt_ShareOutstanding_COMS
        flt_TotalNAV_WCOM = flt_navWCOM * int_CreationUnits_WCOM
        flt_TotalNAV_WCOE = flt_navWCOE * int_CreationUnits_WCOE
        flt_TotalNAV_COMS = flt_navCOMS * int_CreationUnits_COMS
        # Forward
        flt_fwdUsd_Shares_WCOM = df_Fwd.loc[df_Fwd['Class Number'] == 'WISX4', 'Notional Value'].values[0]
        flt_fwdGbp_Shares_WCOM = abs(df_Fwd.loc[df_Fwd['Class Number'] == 'WISX4', 'Contract Value'].values[0])
        flt_fwdUsd_Shares_WCOE = df_Fwd.loc[df_Fwd['Class Number'] == 'WISX5', 'Notional Value'].values[0]
        flt_fwdGbp_Shares_WCOE = abs(df_Fwd.loc[df_Fwd['Class Number'] == 'WISX5', 'Contract Value'].values[0])
        flt_fwdUsd_Shares_COMS = df_Fwd.loc[df_Fwd['Class Number'] == 'WISX6', 'Notional Value'].values[0]
        flt_fwdGbp_Shares_COMS = abs(df_Fwd.loc[df_Fwd['Class Number'] == 'WISX6', 'Contract Value'].values[0])
        # Fx
        try:    
            df_FX_GBP = df_FX.loc[df_FX['ToCurrencyCode'] == 'GBP', 'Value'].values[0]
            df_FX_EUR = df_FX.loc[df_FX['ToCurrencyCode'] == 'EUR', 'Value'].values[0]
            df_FX_CHF = df_FX.loc[df_FX['ToCurrencyCode'] == 'CHF', 'Value'].values[0]
        except: 
            print('Fx Array:')
            print(df_FX)
            return 'ERROR: {} - Fx is empty or does not have GBP / EUR / CHF in it'.format(str_PCF), []
        # Cash
        flt_csh_WCOM = (flt_fwdUsd_Shares_WCOM * flt_factor1_WCOM * df_FX_GBP) + (flt_fwdGbp_Shares_WCOM * flt_factor1_WCOM)
        flt_csh_WCOE = (flt_fwdUsd_Shares_WCOE * flt_factor1_WCOE * df_FX_EUR) + (flt_fwdGbp_Shares_WCOE * flt_factor1_WCOE)
        flt_csh_COMS = (flt_fwdUsd_Shares_COMS * flt_factor1_COMS * df_FX_CHF) + (flt_fwdGbp_Shares_COMS * flt_factor1_COMS)
    except: return 'ERROR: {} - Variables |frt'.format(str_PCF), []
    
    
    # df_Result_1Head
    try:
        df_Result_1Head_Wcom = pd.DataFrame(columns = range(0, 21))
        df_Result_1Head_Wcoe = pd.DataFrame(columns = range(0, 21))
        df_Result_1Head_Coms = pd.DataFrame(columns = range(0, 21))
        #---------------------------------------------------------------------------------------
        df_Result_1Head_Wcom.loc[len(df_Result_1Head_Wcom)] = ['RecordType', 'Name', 'SecurityType', 'Ric', 'Sedol', 'Bloomberg', 
                                 'ExchangeTicker', 'Isin', 'Cusip', 'CurrencyCode', 'MIC', 'NAV', 'Divisor', 'SharesOutstanding', 
                                 'CreationUnits', 'AUM', 'ExcludedCash', 'EscrowCash', 'TotalExpenseRatio', 'Leverage', 'AsAtDate']
        df_Result_1Head_Wcoe.loc[len(df_Result_1Head_Wcoe)] = ['RecordType', 'Name', 'SecurityType', 'Ric', 'Sedol', 'Bloomberg', 
                                 'ExchangeTicker', 'Isin', 'Cusip', 'CurrencyCode', 'MIC', 'NAV', 'Divisor', 'SharesOutstanding', 
                                 'CreationUnits', 'AUM', 'ExcludedCash', 'EscrowCash', 'TotalExpenseRatio', 'Leverage', 'AsAtDate']
        df_Result_1Head_Coms.loc[len(df_Result_1Head_Coms)] = ['RecordType', 'Name', 'SecurityType', 'Ric', 'Sedol', 'Bloomberg', 
                                 'ExchangeTicker', 'Isin', 'Cusip', 'CurrencyCode', 'MIC', 'NAV', 'Divisor', 'SharesOutstanding', 
                                 'CreationUnits', 'AUM', 'ExcludedCash', 'EscrowCash', 'TotalExpenseRatio', 'Leverage', 'AsAtDate']
        #---------------------------------------------------------------------------------------
        df_Result_1Head_Wcom.loc[len(df_Result_1Head_Wcom)] = ['H', 'WisdomTree Enhanced Commodity UCITS ETF - GBP Hedged Acc', 'ETF', 'WDWCOM.L', 'BF5JBB4', 'WCOM LN', 
                                 'WCOM', 'IE00BG88WH84', '', 'GBX', 'XLON', str(flt_navWCOM), str(int_CreationUnits_WCOM), str(flt_ShareOutstanding_WCOM), 
                                 str(int_CreationUnits_WCOM), str(flt_AUM_WCOM), '', '', '', '1', dte_NavDate.strftime('%d-%m-%Y')]
        df_Result_1Head_Wcoe.loc[len(df_Result_1Head_Wcoe)] = ['H', 'WisdomTree Enhanced Commodity UCITS ETF - EUR Hedged Acc', 'ETF', 'WCOE.MI', 'BF5JCP5', 'WCOE IM', 
                                 'WCOE', 'IE00BG88WG77', '', 'EUR', 'XMIL', str(flt_navWCOE), str(int_CreationUnits_WCOE), str(flt_ShareOutstanding_WCOE), 
                                 str(int_CreationUnits_WCOE), str(flt_AUM_WCOE), '', '', '', '1', dte_NavDate.strftime('%d-%m-%Y')]
        df_Result_1Head_Coms.loc[len(df_Result_1Head_Coms)] = ['H', 'WisdomTree Enhanced Commodity UCITS ETF - CHF Hedged Acc', 'ETF', 'COMS.S', 'BG88WL2', 'COMS SW', 
                                 'COMS', 'IE00BG88WL21', '', 'CHF', 'XSWX', str(flt_navCOMS), str(int_CreationUnits_COMS), str(flt_ShareOutstanding_COMS), 
                                 str(int_CreationUnits_COMS), str(flt_AUM_COMS), '', '', '', '1', dte_NavDate.strftime('%d-%m-%Y')]
        #---------------------------------------------------------------------------------------
        df_Result_1Head_Wcom.loc[len(df_Result_1Head_Wcom)] = ['H', 'WisdomTree Enhanced Commodity UCITS ETF - GBP Hedged Acc', 'ETF', 'WTWCOM.S', 'BJH4VS2', 'WCOM SE', 
                                 'WCOM', 'IE00BG88WH84', '', 'GBP', 'XSWX', str(flt_navWCOM), str(int_CreationUnits_WCOM), str(flt_ShareOutstanding_WCOM), 
                                 str(int_CreationUnits_WCOM), str(flt_navWCOM * flt_ShareOutstanding_WCOM), '', '', '', '1', dte_NavDate.strftime('%d-%m-%Y')]
        df_Result_1Head_Wcoe.loc[len(df_Result_1Head_Wcoe)] = ['H', 'WisdomTree Enhanced Commodity UCITS ETF - EUR Hedged Acc', 'ETF', 'WCOE.S', 'BJH4VT3', 'WCOE SE', 
                                 'WCOE', 'IE00BG88WG77', '', 'EUR', 'XSWX', str(flt_navWCOE), str(int_CreationUnits_WCOE), str(flt_ShareOutstanding_WCOE), 
                                 str(int_CreationUnits_WCOE), str(flt_navWCOE * flt_ShareOutstanding_WCOE), '', '', '', '1', dte_NavDate.strftime('%d-%m-%Y')]
        df_Result_1Head_Coms.loc[len(df_Result_1Head_Coms)] = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        #---------------------------------------------------------------------------------------
        df_Result_1Head_Wcom.loc[len(df_Result_1Head_Wcom)] = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        df_Result_1Head_Wcoe.loc[len(df_Result_1Head_Wcoe)] = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        df_Result_1Head_Coms.loc[len(df_Result_1Head_Coms)] = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    except: return 'ERROR: {} - df_Result_1Head'.format(str_PCF), []
    
    
    # df_Result_3Compo
    try:
        df_Result_3Compo_Wcom = pd.DataFrame(columns = range(0, 20))
        df_Result_3Compo_Wcoe = pd.DataFrame(columns = range(0, 20))
        df_Result_3Compo_Coms = pd.DataFrame(columns = range(0, 20))
        #---------------------------------------------------------------------------------------
        df_Result_3Compo_Wcom.loc[len(df_Result_3Compo_Wcom)] = ['RecordType', 'Name', 'SecurityType', 'Ric', 'Sedol', 'Bloomberg', 'Isin', 'Cusip', 'Other', 'CurrencyCode', 
                                  'MIC', 'Price', 'AdjustedOpenPrice', 'DividendAdjustment', 'ShareFactor', 'Creation', 'Redemption', 'Tracking', 'Excluded', 'GICS']
        df_Result_3Compo_Wcoe.loc[len(df_Result_3Compo_Wcoe)] = ['RecordType', 'Name', 'SecurityType', 'Ric', 'Sedol', 'Bloomberg', 'Isin', 'Cusip', 'Other', 'CurrencyCode', 
                                  'MIC', 'Price', 'AdjustedOpenPrice', 'DividendAdjustment', 'ShareFactor', 'Creation', 'Redemption', 'Tracking', 'Excluded', 'GICS']
        df_Result_3Compo_Coms.loc[len(df_Result_3Compo_Coms)] = ['RecordType', 'Name', 'SecurityType', 'Ric', 'Sedol', 'Bloomberg', 'Isin', 'Cusip', 'Other', 'CurrencyCode', 
                                  'MIC', 'Price', 'AdjustedOpenPrice', 'DividendAdjustment', 'ShareFactor', 'Creation', 'Redemption', 'Tracking', 'Excluded', 'GICS']
        #---------------------------------------------------------------------------------------
        df_Result_3Compo_Wcom.loc[len(df_Result_3Compo_Wcom)] = ['C', 'SHORT (USD)', '', '2784136.XD', '', '', '', '', '', 'USD', '', '1', '1', '', 
                                 str(flt_factor1_WCOM), '', '', str(flt_fwdUsd_Shares_WCOM), str(flt_fwdUsd_Shares_WCOM), '']
        df_Result_3Compo_Wcoe.loc[len(df_Result_3Compo_Wcoe)] = ['C', 'SHORT (USD)', '', '2784136.XD', '', '', '', '', '', 'USD', '', '1', '1', '', 
                                 str(flt_factor1_WCOE), '', '', str(flt_fwdUsd_Shares_WCOE), str(flt_fwdUsd_Shares_WCOE), '']
        df_Result_3Compo_Coms.loc[len(df_Result_3Compo_Coms)] = ['C', 'SHORT (USD)', '', '2784136.XD', '', '', '', '', '', 'USD', '', '1', '1', '', 
                                 str(flt_factor1_COMS), '', '', str(flt_fwdUsd_Shares_COMS), str(flt_fwdUsd_Shares_COMS), '']
        #---------------------------------------------------------------------------------------
        df_Result_3Compo_Wcom.loc[len(df_Result_3Compo_Wcom)] = ['C', 'LONG (GBP)', '', '2785900.XD', '', '', '', '', '', 'GBP', '', '1', '1', '', 
                                 str(flt_factor1_WCOM), '', '', str(flt_fwdGbp_Shares_WCOM), str(flt_fwdGbp_Shares_WCOM), '']
        df_Result_3Compo_Wcoe.loc[len(df_Result_3Compo_Wcoe)] = ['C', 'LONG (EUR)', '', '2786029.XD', '', '', '', '', '', 'EUR', '', '1', '1', '', 
                                 str(flt_factor1_WCOE), '', '', str(flt_fwdGbp_Shares_WCOE), str(flt_fwdGbp_Shares_WCOE), '']
        df_Result_3Compo_Coms.loc[len(df_Result_3Compo_Coms)] = ['C', 'LONG (CHF)', '', '2928852.XD', '', '', '', '', '', 'CHF', '', '1', '1', '', 
                                 str(flt_factor1_COMS), '', '', str(flt_fwdGbp_Shares_COMS), str(flt_fwdGbp_Shares_COMS), '']
        #---------------------------------------------------------------------------------------
        
        # Calculus Compo Generic
        df_Compo = df_Compo.loc[(df_Compo['Underlying'] != 'US_CONSTANT') & (df_Compo['Bloomberg Code'] != '-')].copy()
        df_Compo['B_Spot_x_Weight'] = df_Compo['Spot'] * df_Compo['Weight']
        flt_rolling = df_Compo['B_Spot_x_Weight'].sum()
        df_Compo['C_indexWeights'] = df_Compo['B_Spot_x_Weight'] / flt_rolling
        df_Compo['Shares'] = df_Compo['C_indexWeights'] / df_Compo['Spot']
        df_codePivot = pp.WisdomTree_GetPivotCode(df_Compo, 'Bloomberg Code', str_folderRoot + 'file', 'PivotCode_WisdomTree.csv')        
        df_Compo = pd.merge(df_Compo, df_codePivot, on = 'Bloomberg Code', how = 'left')
        df_Compo.rename(columns = {'Bloomberg Code':'Bloomberg'}, inplace = True)
        # Calculus Compo Particular
        df_Compo_Wcom = df_Compo[['Bloomberg', 'B_Spot_x_Weight', 'C_indexWeights', 'Shares', 'Spot', 'CurrentName', 'Mic', 'Ric']].copy()
        df_Compo_Wcoe = df_Compo[['Bloomberg', 'B_Spot_x_Weight', 'C_indexWeights', 'Shares', 'Spot', 'CurrentName', 'Mic', 'Ric']].copy()
        df_Compo_Coms = df_Compo[['Bloomberg', 'B_Spot_x_Weight', 'C_indexWeights', 'Shares', 'Spot', 'CurrentName', 'Mic', 'Ric']].copy()
        df_Compo_Wcom['Shares'] = df_Compo_Wcom['Shares'] * (flt_TotalNAV_WCOM - flt_csh_WCOM) / df_FX_GBP
        df_Compo_Wcoe['Shares'] = df_Compo_Wcoe['Shares'] * (flt_TotalNAV_WCOE - flt_csh_WCOE) / df_FX_EUR
        df_Compo_Coms['Shares'] = df_Compo_Coms['Shares'] * (flt_TotalNAV_COMS - flt_csh_COMS) / df_FX_CHF
        # Final
        df_Compo_Wcom['A'] = 'C'
        df_Compo_Wcom['B'] = df_Compo_Wcom['CurrentName']
        df_Compo_Wcom['C'] = 'Future'
        df_Compo_Wcom['D'] = df_Compo_Wcom['Ric']
        df_Compo_Wcom['E'] = ''
        df_Compo_Wcom['F'] = df_Compo_Wcom['Bloomberg']
        df_Compo_Wcom['G'] = ''
        df_Compo_Wcom['H'] = ''
        df_Compo_Wcom['I'] = ''
        df_Compo_Wcom['J'] = 'USD'
        df_Compo_Wcom['K'] = df_Compo_Wcom['Mic']
        df_Compo_Wcom['L'] = df_Compo_Wcom['Spot']
        df_Compo_Wcom['M'] = df_Compo_Wcom['Spot']
        df_Compo_Wcom['N'] = ''
        df_Compo_Wcom['O'] = '1'
        df_Compo_Wcom['P'] = df_Compo_Wcom['Shares']
        df_Compo_Wcom['Q'] = df_Compo_Wcom['Shares']
        df_Compo_Wcom['R'] = df_Compo_Wcom['Shares']
        df_Compo_Wcom['S'] = ''
        df_Compo_Wcom['T'] = ''
        #--------------------------------------
        df_Compo_Wcoe['A'] = 'C'
        df_Compo_Wcoe['B'] = df_Compo_Wcoe['CurrentName']
        df_Compo_Wcoe['C'] = 'Future'
        df_Compo_Wcoe['D'] = df_Compo_Wcoe['Ric']
        df_Compo_Wcoe['E'] = ''
        df_Compo_Wcoe['F'] = df_Compo_Wcoe['Bloomberg']
        df_Compo_Wcoe['G'] = ''
        df_Compo_Wcoe['H'] = ''
        df_Compo_Wcoe['I'] = ''
        df_Compo_Wcoe['J'] = 'USD'
        df_Compo_Wcoe['K'] = df_Compo_Wcoe['Mic']
        df_Compo_Wcoe['L'] = df_Compo_Wcoe['Spot']
        df_Compo_Wcoe['M'] = df_Compo_Wcoe['Spot']
        df_Compo_Wcoe['N'] = ''
        df_Compo_Wcoe['O'] = '1'
        df_Compo_Wcoe['P'] = df_Compo_Wcoe['Shares']
        df_Compo_Wcoe['Q'] = df_Compo_Wcoe['Shares']
        df_Compo_Wcoe['R'] = df_Compo_Wcoe['Shares']
        df_Compo_Wcoe['S'] = ''
        df_Compo_Wcoe['T'] = ''
        #--------------------------------------
        df_Compo_Coms['A'] = 'C'
        df_Compo_Coms['B'] = df_Compo_Coms['CurrentName']
        df_Compo_Coms['C'] = 'Future'
        df_Compo_Coms['D'] = df_Compo_Coms['Ric']
        df_Compo_Coms['E'] = ''
        df_Compo_Coms['F'] = df_Compo_Coms['Bloomberg']
        df_Compo_Coms['G'] = ''
        df_Compo_Coms['H'] = ''
        df_Compo_Coms['I'] = ''
        df_Compo_Coms['J'] = 'USD'
        df_Compo_Coms['K'] = df_Compo_Coms['Mic']
        df_Compo_Coms['L'] = df_Compo_Coms['Spot']
        df_Compo_Coms['M'] = df_Compo_Coms['Spot']
        df_Compo_Coms['N'] = ''
        df_Compo_Coms['O'] = '1'
        df_Compo_Coms['P'] = df_Compo_Coms['Shares']
        df_Compo_Coms['Q'] = df_Compo_Coms['Shares']
        df_Compo_Coms['R'] = df_Compo_Coms['Shares']
        df_Compo_Coms['S'] = ''
        df_Compo_Coms['T'] = ''
        #--------------------------------------
        df_Compo_Wcom = df_Compo_Wcom[['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']]
        df_Compo_Wcoe = df_Compo_Wcoe[['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']]
        df_Compo_Coms = df_Compo_Coms[['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']]
        # UNION
        df_Result_3Compo_Wcom = dframe.fDf_Concat_wColOfDf1(df_Result_3Compo_Wcom, df_Compo_Wcom)
        df_Result_3Compo_Wcoe = dframe.fDf_Concat_wColOfDf1(df_Result_3Compo_Wcoe, df_Compo_Wcoe)
        df_Result_3Compo_Coms = dframe.fDf_Concat_wColOfDf1(df_Result_3Compo_Coms, df_Compo_Coms)
    except Exception as err: return 'ERROR: df_Result_3Compo xxrfg - {} | {}'.format(str_PCF, str(err)), []
    
    
    # df_2Redemption
    try:
        # Count
        int_nbConsti = df_Compo['Shares'].count()
        # DF
        df_2Redemption_Wcom = pd.DataFrame(columns = range(0, 7))
        df_2Redemption_Wcoe = pd.DataFrame(columns = range(0, 7))
        df_2Redemption_Coms = pd.DataFrame(columns = range(0, 7))
        #---------------------------------------------------------------------------------------
        df_2Redemption_Wcom.loc[len(df_2Redemption_Wcom)] = ['RecordType', 'Basket', 'Cash', 'EstimatedCash', 'TotalCash', 'CalculatedNAV', 'ConstituentCount']
        df_2Redemption_Wcoe.loc[len(df_2Redemption_Wcoe)] = ['RecordType', 'Basket', 'Cash', 'EstimatedCash', 'TotalCash', 'CalculatedNAV', 'ConstituentCount']
        df_2Redemption_Coms.loc[len(df_2Redemption_Coms)] = ['RecordType', 'Basket', 'Cash', 'EstimatedCash', 'TotalCash', 'CalculatedNAV', 'ConstituentCount']
        #---------------------------------------------------------------------------------------
        df_2Redemption_Wcom.loc[len(df_2Redemption_Wcom)] = ['B', 'Creation', str(flt_csh_WCOM), str(flt_csh_WCOM), '0', str(flt_navWCOM), str(int_nbConsti)]
        df_2Redemption_Wcoe.loc[len(df_2Redemption_Wcoe)] = ['B', 'Creation', str(flt_csh_WCOE), str(flt_csh_WCOE), '0', str(flt_navWCOE), str(int_nbConsti)]
        df_2Redemption_Coms.loc[len(df_2Redemption_Coms)] = ['B', 'Creation', str(flt_csh_COMS), str(flt_csh_COMS), '0', str(flt_navCOMS), str(int_nbConsti)]
        #---------------------------------------------------------------------------------------
        df_2Redemption_Wcom.loc[len(df_2Redemption_Wcom)] = ['B', 'Redemption', str(flt_csh_WCOM), str(flt_csh_WCOM), '0', str(flt_navWCOM), str(int_nbConsti)]
        df_2Redemption_Wcoe.loc[len(df_2Redemption_Wcoe)] = ['B', 'Redemption', str(flt_csh_WCOE), str(flt_csh_WCOE), '0', str(flt_navWCOE), str(int_nbConsti)]
        df_2Redemption_Coms.loc[len(df_2Redemption_Coms)] = ['B', 'Redemption', str(flt_csh_COMS), str(flt_csh_COMS), '0', str(flt_navCOMS), str(int_nbConsti)]
        #---------------------------------------------------------------------------------------
        df_2Redemption_Wcom.loc[len(df_2Redemption_Wcom)] = ['B', 'Tracking', '0', '0', '0', str(flt_navWCOM), str(int_nbConsti + 2)]
        df_2Redemption_Wcoe.loc[len(df_2Redemption_Wcoe)] = ['B', 'Tracking', '0', '0', '0', str(flt_navWCOE), str(int_nbConsti + 2)]
        df_2Redemption_Coms.loc[len(df_2Redemption_Coms)] = ['B', 'Tracking', '0', '0', '0', str(flt_navCOMS), str(int_nbConsti + 2)]
        #---------------------------------------------------------------------------------------
        df_2Redemption_Wcom.loc[len(df_2Redemption_Wcom)] = ['', '', '', '', '', '', '']
        df_2Redemption_Wcoe.loc[len(df_2Redemption_Wcoe)] = ['', '', '', '', '', '', '']
        df_2Redemption_Coms.loc[len(df_2Redemption_Coms)] = ['', '', '', '', '', '', '']
    except: return 'ERROR: {} - df_2Redemption %xcf'.format(str_PCF), [] 
       
    
    # UNION FInale
    try:
        df_Wcom = dframe.fDf_Concat_wColOfDf1(df_Result_1Head_Wcom, df_2Redemption_Wcom)
        df_Wcoe = dframe.fDf_Concat_wColOfDf1(df_Result_1Head_Wcoe, df_2Redemption_Wcoe)
        df_Coms = dframe.fDf_Concat_wColOfDf1(df_Result_1Head_Coms, df_2Redemption_Coms)
        #---------------------------------------------------------------------------------------
        df_Wcom = dframe.fDf_Concat_wColOfDf1(df_Wcom, df_Result_3Compo_Wcom)
        df_Wcoe = dframe.fDf_Concat_wColOfDf1(df_Wcoe, df_Result_3Compo_Wcoe)
        df_Coms = dframe.fDf_Concat_wColOfDf1(df_Coms, df_Result_3Compo_Coms)
    except: return 'ERROR: {} - UNION FInale %xcf'.format(str_PCF), [] 
    
    
    # Pcf Path
    try:
        df_Wcom.fillna(value = '', inplace = True)
        df_Wcoe.fillna(value = '', inplace = True)
        df_Coms.fillna(value = '', inplace = True)
        # Create XLS wihout model
        bl_header = False
        str_path0 = fl.fStr_createExcel_SevSh(str_folder, l_pcfFileName[0], [df_Wcom], ['WDWCOM'], bl_header, {'strings_to_numbers': True})
        str_path1 = fl.fStr_createExcel_SevSh(str_folder, l_pcfFileName[1], [df_Wcoe], ['WCOE'], bl_header, {'strings_to_numbers': True})
        str_path2 = fl.fStr_createExcel_SevSh(str_folder, l_pcfFileName[2], [df_Coms], ['COMS'], bl_header, {'strings_to_numbers': True})
        str_path3 = fl.fStr_BuildPath(str_folder, l_pcfFileName[3])
        str_path4 = fl.fStr_BuildPath(str_folder, l_pcfFileName[4])
        # Format for Excel
        fl.fStr_StyleIntoExcel(str_path0, '', [1, 5, 10], '3_BlueHeader', True, 'WHITE', ['solid', 'solid', '4F81BD'])
        fl.fStr_StyleIntoExcel(str_path1, '', [1, 5, 10], '3_BlueHeader', True, 'WHITE', ['solid', 'solid', '4F81BD'])
        fl.fStr_StyleIntoExcel(str_path2, '', [1, 5, 10], '3_BlueHeader', True, 'WHITE', ['solid', 'solid', '4F81BD'])
        fl.fStr_StyleIntoExcel(str_path0, '', [1, 5, 10], 'Table_Border', False, '', [], ['thin', '4A7FB0'])
        fl.fStr_StyleIntoExcel(str_path1, '', [1, 5, 10], 'Table_Border', False, '', [], ['thin', '4A7FB0'])
        fl.fStr_StyleIntoExcel(str_path2, '', [1, 5, 10], 'Table_Border', False, '', [], ['thin', '4A7FB0'])
        # Open and Save Excel
        df_test = pd.DataFrame({'col1': ['RecordType']})
        try:    fl.fStr_fillXls_celByCel(fl.fStr_BuildPath(str_folder, l_pcfFileName[0]), df_test, 'WDWCOM')
        except: print('  - Opening Excel File is an optional process step, continue forward. Path: {}'.format(fl.fStr_BuildPath(str_folder, l_pcfFileName[0])))
        try:    fl.fStr_fillXls_celByCel(fl.fStr_BuildPath(str_folder, l_pcfFileName[1]), df_test, 'WCOE')
        except: print('  - Opening Excel File is an optional process step, continue forward. Path: {}'.format(fl.fStr_BuildPath(str_folder, l_pcfFileName[1])))
        try:    fl.fStr_fillXls_celByCel(fl.fStr_BuildPath(str_folder, l_pcfFileName[2]), df_test, 'COMS')
        except: print('  - Opening Excel File is an optional process step, continue forward. Path: {}'.format(fl.fStr_BuildPath(str_folder, l_pcfFileName[2])))
        # Path
        l_pathAttach = [str_path0, str_path1, str_path2, str_path3, str_path4]
    except: return 'ERROR: {} - Pcf Path %xcf'.format(str_PCF), [] 
    
    # ETF Path
    try:
        for etf in l_etfFileName:
            if 'WCOM' in etf:
                str_path0 = pp.fStr_CreateEtfFile(str_folder, etf, dte_date, 'DE000A2X2PA9', '0YS1', 'IE00BG88WH84', 'GBP', flt_navWCOM)
            elif 'WCOE' in etf:
                str_path1 = pp.fStr_CreateEtfFile(str_folder, etf, dte_date, 'DE000A2NC9W9', '0EXC', 'IE00BG88WG77', 'EUR', flt_navWCOE)
            elif 'COMS' in etf:
                str_path2 = pp.fStr_CreateEtfFile(str_folder, etf, dte_date, 'DE000A21VY91', '3PWC', 'IE00BG88WL21', 'CHF', flt_navCOMS)
            elif 'WCOA' in etf:
                flt_navWCOA = df_WCOA.iloc[1, 11]
                str_path3 = pp.fStr_CreateEtfFile(str_folder, etf, dte_date, 'DE000A169VT9', '3XL7', 'IE00BYMLZY74', 'USD', flt_navWCOA)
            elif 'WCOG' in etf:
                flt_navWCOG = df_WCOG.iloc[1, 11]
                str_path4 = pp.fStr_CreateEtfFile(str_folder, etf, dte_date, 'DE000A2X2N83', '0YQZ', 'IE00BZ1GHD37', 'USD', flt_navWCOG)
        # Path
        l_pathAttachETF = [str_path0, str_path1, str_path2, str_path3, str_path4]
        l_pathAttach += l_pathAttachETF
    except: return 'ERROR: {} - EF Path $try'.format(str_PCF), [] 
    
    # Build the return message
    try:
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
        str_resultFigures += '\n' + str(round(flt_navWCOM, 4)) + ' : nav of WCOM'
        str_resultFigures += '\n' + '------------------------------------------------' 
    except: return 'ERROR: {} - Build the return message'.format(str_PCF), []
    
    # Close EXCEL
    try:
        inst_xlApp = fl.c_win32_xlApp()
        inst_xlApp.QuitXlApp(bl_force = False)
    except Exception as Err: print('  (*) ERROR: Close EXCEL - {} | {}'.format(str_PCF, str(Err)))
    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________



def pcf_ChinaAMC(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_Head_2x = dic_df['FTP_HeadAMCL_2x']
        df_Hold_2x = dic_df['FTP_HoldAMCL_2x']
        df_Head_m1x = dic_df['FTP_HeadAMCV_-1x']
        df_Hold_m1x = dic_df['FTP_HoldAMCV_-1x']
        df_Head_m2x = dic_df['FTP_HeadAMCD_-2x']
        df_Hold_m2x = dic_df['FTP_HoldAMCD_-2x']
        df_TradeFile = dic_df['FTP_TradeFile']
        df_DealFile_2x = dic_df['FTP_DealFile2x']
        df_DealFile_m1x = dic_df['FTP_DealFile-1x']
        df_DealFile_m2x = dic_df['FTP_DealFile-2x']
        str_folder = dic_df['Folder']
        try:        df_CME = dic_df['Json_CME_china']
        except:     df_CME = 0
    except:     return 'ERROR: {} - Dataframe'.format(str_PCF), []
    
    # Other param
    l_pcfFileName = ['Official_PCF_CAMC Direxion L&I ETF_NQ100_2x_' + dte_date.strftime('%Y%m%d') + '.xlsx',
                     'Official_PCF_CAMC Direxion L&I ETF_NQ100_-1x_' + dte_date.strftime('%Y%m%d') + '.xlsx',
                     'Official_PCF_CAMC Direxion L&I ETF_NQ100_-2x_' + dte_date.strftime('%Y%m%d') + '.xlsx']
    str_DateNav = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, "%Y-%m-%d", -1, '240')
    dte_DateNav = pd.to_datetime(str_DateNav)
    
    # Variables
    try:
        flt_NavPerShare_2x = df_Head_2x[df_Head_2x[' COMP CODE'] =='AMCL'][' NET NAV/UNIT LESS PERFORMANCE FEE'].values[0]
        flt_NavPerShare_m1x = df_Head_m1x[df_Head_m1x[' COMP CODE'] =='AMCV'][' NET NAV/UNIT LESS PERFORMANCE FEE'].values[0]
        flt_NavPerShare_m2x = df_Head_m2x[df_Head_m2x[' COMP CODE'] =='AMCD'][' NET NAV/UNIT LESS PERFORMANCE FEE'].values[0]
        flt_totalShareIssue_2x = df_Head_2x[df_Head_2x[' COMP CODE'] =='AMCL'][' NO OF UNITS O/S'].values[0]
        flt_totalShareIssue_m1x = df_Head_m1x[df_Head_m1x[' COMP CODE'] =='AMCV'][' NO OF UNITS O/S'].values[0]
        flt_totalShareIssue_m2x = df_Head_m2x[df_Head_m2x[' COMP CODE'] =='AMCD'][' NO OF UNITS O/S'].values[0]
        int_CreationUnits = 100000
        flt_BasketNav_2x = int_CreationUnits * flt_NavPerShare_2x
        flt_BasketNav_m1x = int_CreationUnits * flt_NavPerShare_m1x
        flt_BasketNav_m2x = int_CreationUnits * flt_NavPerShare_m2x
        flt_FutPrice_2x = df_Hold_2x[df_Hold_2x[' SUB-TYPE'] == 'FT'][' MARKET PRICE'].values[0]
        #        flt_FutPrice_m1x = df_Hold_m1x[df_Hold_m1x[' SUB-TYPE'] == 'FT'][' MARKET PRICE'].values[0]
        #        flt_FutPrice_m2x = df_Hold_m2x[df_Hold_m2x[' SUB-TYPE'] == 'FT'][' MARKET PRICE'].values[0]
        # Trade File
        try:        str_FutName = df_TradeFile['Security Description'].values[0]
        except:     str_FutName = ''
        try:        str_FutCcy = df_TradeFile['Settle Curr'].values[0]
        except:     str_FutCcy = ''
        try:        str_FutTicker = df_TradeFile['Symbol'].values[0]
        except:     str_FutTicker = ''
        # CME Fut Price
        try:
            bl_rolling = False
            # Last Fut Price from CME
            flt_lastCMEFutPrice = df_CME['settle'].values[0]
            # Get the price of the NExt Future (3 months away) on CME
            flt_FutPrice_3Maway = flt_lastCMEFutPrice
            flt_FutPrice_3Maway  = df_CME.loc[df_CME['month'] == pp.fDte_dateFutures(dte_date, 3), 'settle'].values[0]
        except:     pass
        # look if it is ROLLING
        try:
            # Check the symbol of other Future if it exists
            try:        str_FutNEW_ticker = df_TradeFile[df_TradeFile['HSBC Acct'] =='AMCL']['Symbol'].values[1]
            except:     
                try:    str_FutNEW_ticker = df_TradeFile[df_TradeFile['HSBC Acct'] =='AMCV']['Symbol'].values[1]
                except:     
                    str_FutNEW_ticker = df_TradeFile[df_TradeFile['HSBC Acct'] =='AMCD']['Symbol'].values[1]
            # and test if its different from the first one
            if str_FutNEW_ticker != str_FutTicker:          bl_rolling = True
        except:     pass
        try:
            #['Buy', 'Cover'] ==> 1 else -1
            df_TradeFile['int_short'] = 1
            df_TradeFile['int_short'] = df_TradeFile['int_short'].where(df_TradeFile['Transaction Type'] == 'Buy', -1)
            df_TradeFile['int_short'] = df_TradeFile['int_short'].where(df_TradeFile['Transaction Type'] != 'Cover', 1)
            df_TradeFile['Quant'] = df_TradeFile['Quantity'] * df_TradeFile['int_short']
            try:        flt_Quant_2x = df_TradeFile[df_TradeFile['HSBC Acct'] =='AMCL']['Quant'].sum()
            except:     flt_Quant_2x = 0
            try:        flt_Quant_m1x = df_TradeFile[df_TradeFile['HSBC Acct'] =='AMCV']['Quant'].sum()
            except:     flt_Quant_m1x = 0
            try:        flt_Quant_m2x = df_TradeFile[df_TradeFile['HSBC Acct'] =='AMCD']['Quant'].sum()
            except:     flt_Quant_m2x = 0
        except:
            flt_Quant_2x = 0
            flt_Quant_m1x = 0
            flt_Quant_m2x = 0
        # Contracts Share
        int_Holdings_2x = df_Hold_2x[df_Hold_2x[' SUB-TYPE'] == 'FT'][' HOLDINGS'].values[0]
        int_Holdings_m1x = df_Hold_m1x[df_Hold_m1x[' SUB-TYPE'] == 'FT'][' HOLDINGS'].values[0]
        int_Holdings_m2x = df_Hold_m2x[df_Hold_m2x[' SUB-TYPE'] == 'FT'][' HOLDINGS'].values[0]
        flt_contractsShares_2x = flt_Quant_2x + int_Holdings_2x
        flt_contractsShares_m1x = flt_Quant_m1x + int_Holdings_m1x
        flt_contractsShares_m2x = flt_Quant_m2x + int_Holdings_m2x
        # Dealing File
        try:
            df_DealFile_2x['Units'] = df_DealFile_2x['Units'].where(df_DealFile_2x['Subscription(S)/\nRedemption(R)'] == 'S', - df_DealFile_2x['Units'])
            flt_deal_2x = df_DealFile_2x['Units'].sum()
        except:     flt_deal_2x = 0        
        try:
            df_DealFile_m1x['Units'] = df_DealFile_m1x['Units'].where(df_DealFile_m1x['Subscription(S)/\nRedemption(R)'] == 'S', - df_DealFile_m1x['Units'])
            flt_deal_m1x = df_DealFile_m1x['Units'].sum()
        except:     flt_deal_m1x = 0        
        try:
            df_DealFile_m2x['Units'] = df_DealFile_m2x['Units'].where(df_DealFile_m2x['Subscription(S)/\nRedemption(R)'] == 'S', - df_DealFile_m2x['Units'])
            flt_deal_m2x = df_DealFile_m2x['Units'].sum()
        except:     flt_deal_m2x = 0
        # Conclusion  Contracts Share
        flt_contractsShares_2x = flt_contractsShares_2x * int_CreationUnits / (flt_totalShareIssue_2x + flt_deal_2x) 
        flt_contractsShares_m1x = flt_contractsShares_m1x * int_CreationUnits / (flt_totalShareIssue_m1x + flt_deal_m1x)
        flt_contractsShares_m2x = flt_contractsShares_m2x * int_CreationUnits / (flt_totalShareIssue_m2x + flt_deal_m2x)
    except:     return 'ERROR: {} - Variables'.format(str_PCF), []
    
    # Take DF from Model
    try:
        str_modelfolder = str_folderRoot + 'HK_ChinaAMC\\'
        str_modelFileName = 'ChinaAMC_model.xlsx'
        df_Result = pd.read_excel(str_modelfolder + str_modelFileName, header = None, index_col = None)
        df_Result.fillna(value = '', inplace = True)
        df_Result.iloc[4, 2] = dte_date.strftime('%m/%d/%Y')
        df_Result.iloc[5, 2] = dte_DateNav.strftime('%m/%d/%Y')
        df_Result.iloc[16, 2] = 'N/A '
        df_Result.iloc[19, 2] = str(int_CreationUnits)
        if str_FutName != '':       df_Result.iloc[22, 1] = str(str_FutName)
        if str_FutCcy != '':        df_Result.iloc[22, 3] = str(str_FutCcy)
        if str_FutTicker != '':     df_Result.iloc[22, 8] = str(str_FutTicker)
        if str_FutTicker != '':     df_Result.iloc[22, 9] = str(str_FutTicker)
    except: return 'ERROR: {} - Take last DF from Model /-8'.format(str_PCF), []
    
    # Estimated Daily Occurred Expense, Fee and Charges
    try:
        flt_fx = df_Result.iloc[22, 4]
        int_multiplier = df_Result.iloc[22, 7]
        df_TradeFile['Fee_1'] = - df_TradeFile['Quant'] * int_multiplier
        # flt_FutPrice_2x is the same for m1x & m2x
        # ================== Faire Attention au futur si il y a plus d'une ligne par future (check from Excel) ==================
        if not bl_rolling:
            df_TradeFile['Fee_2'] = df_TradeFile['Fee_1'] * (df_TradeFile['Price'] - flt_FutPrice_2x)
            flt_FutPrice = flt_FutPrice_2x
            # CHECK
            if flt_FutPrice_2x != flt_FutPrice_3Maway:
                print('\n')
                print('  ATTENTION... The Fut Price is {}'.format(flt_FutPrice_2x))
                print('  - On CME, it is different though... The Fut Price is {}'.format(flt_FutPrice_3Maway))
                print(r'  - URL = https://www.cmegroup.com/trading/equity-index/us-index/e-mini-nasdaq-100_quotes_settlements_futures.html', '\n\n')
        else:
            #---------------------------------------------------------------------------------------------
            df_TradeFile['FutPrice'] = flt_FutPrice_3Maway
            df_TradeFile.loc[df_TradeFile['Symbol'] == str_FutNEW_ticker, 'FutPrice'] = flt_FutPrice_3Maway  #Useless but just to remind
            df_TradeFile.loc[df_TradeFile['Symbol'] == str_FutTicker, 'FutPrice'] = flt_FutPrice_2x            
            #---------------------------------------------------------------------------------------------
            df_TradeFile['Fee_2'] = df_TradeFile['Fee_1'] * (df_TradeFile['Price'] - df_TradeFile['FutPrice'])
            #-------------------------- CHECK ------------------------------------------------------------
            print('  ROOOOLLINGGG !!!!!!!')
            print('  - Old Future Price: ', flt_FutPrice_2x)
            print('  - CME 3M away Future:    ', pp.fDte_dateFutures(dte_date, 3))
            print('  - CME 3M away Fut Price: ', flt_FutPrice_3Maway)
            if flt_FutPrice_2x == flt_FutPrice_3Maway:
                print('  - ATTENTION... There is supposed to be a ROLLING today but old and new future price are equal !!!')
                print(r'  - URL = https://www.cmegroup.com/trading/equity-index/us-index/e-mini-nasdaq-100_quotes_settlements_futures.html')
            #-------------------------- New Future Charac to fill if ROLLING -----------------------------
            try:        str_FutName_NEW = df_TradeFile.loc[df_TradeFile['Symbol'] == str_FutNEW_ticker, 'Security Description'].values[0]
            except:     str_FutName_NEW = ''
            if str_FutName_NEW != '':       df_Result.iloc[22, 1] = str(str_FutName_NEW)
            if str_FutNEW_ticker != '':     df_Result.iloc[22, 8] = str(str_FutNEW_ticker)
            if str_FutNEW_ticker != '':     df_Result.iloc[22, 9] = str(str_FutNEW_ticker)
            flt_FutPrice = flt_FutPrice_3Maway
        #=======================================================================================================================
        df_TradeFile['Fee_3'] = df_TradeFile['Fee_2'] - df_TradeFile['Total Commission']
        df_TradeFile_2x = df_TradeFile[df_TradeFile['HSBC Acct'] =='AMCL'].copy()
        df_TradeFile_m1x = df_TradeFile[df_TradeFile['HSBC Acct'] =='AMCV'].copy()
        df_TradeFile_m2x = df_TradeFile[df_TradeFile['HSBC Acct'] =='AMCD'].copy()
        df_TradeFile_2x['Fee_4'] = df_TradeFile_2x['Fee_3'] * int_CreationUnits / (flt_totalShareIssue_2x + flt_deal_2x)
        df_TradeFile_m1x['Fee_4']= df_TradeFile_m1x['Fee_3']* int_CreationUnits / (flt_totalShareIssue_m1x+ flt_deal_m1x)
        df_TradeFile_m2x['Fee_4']= df_TradeFile_m2x['Fee_3']* int_CreationUnits / (flt_totalShareIssue_m2x+ flt_deal_m2x)
        flt_Trade_2x = df_TradeFile_2x['Fee_4'].sum()
        flt_Trade_m1x= df_TradeFile_m1x['Fee_4'].sum()
        flt_Trade_m2x= df_TradeFile_m2x['Fee_4'].sum()
        # Management fees per days
        int_dateDifference = (dte_date - dte_DateNav).days
        flt_magFee_2x  = - round(0.0208 * flt_BasketNav_2x  / 365, 2) * int_dateDifference
        flt_magFee_m1x = - round(0.0208 * flt_BasketNav_m1x / 365, 2) * int_dateDifference
        flt_magFee_m2x = - round(0.022  * flt_BasketNav_m2x / 365, 2) * int_dateDifference
        flt_magFee_2x  = flt_magFee_2x + flt_Trade_2x
        flt_magFee_m1x = flt_magFee_m1x+ flt_Trade_m1x
        flt_magFee_m2x = flt_magFee_m2x+ flt_Trade_m2x
    except: return 'ERROR: {} - Estimated Daily Occurred Expense, Fee and Charges'.format(str_PCF), []
        
    # Build DF from Model
    try:
        # A. Leverage x2
        df_Lev_2x = df_Result.copy()
        df_Lev_2x.iloc[8, 2] = 'ChinaAMC Direxion NASDAQ-100 Daily (2x) Leveraged Product'
        df_Lev_2x.iloc[9, 2] = 'HK0000306594'
        df_Lev_2x.iloc[10, 2] = '7261 HK'
        df_Lev_2x.iloc[11, 2] = '7261.HK'
        df_Lev_2x.iloc[13, 2] = str(flt_NavPerShare_2x)
        df_Lev_2x.iloc[14, 2] = str(flt_totalShareIssue_2x)
        df_Lev_2x.iloc[15, 2] = str(flt_BasketNav_2x)
        df_Lev_2x.iloc[18, 2] = str(flt_magFee_2x)
        df_Lev_2x.iloc[22, 5] = str(flt_FutPrice)
        df_Lev_2x.iloc[22, 6] = str(flt_contractsShares_2x)
        flt_BasketExposure_2x = flt_fx * flt_FutPrice * flt_contractsShares_2x * int_multiplier
        df_Lev_2x.iloc[22, 10] = str(flt_BasketExposure_2x)
        flt_EstimatedCash_2x = round(flt_BasketNav_2x + flt_magFee_2x - flt_BasketExposure_2x, 2)
        df_Lev_2x.iloc[17, 2] = str(flt_EstimatedCash_2x)
        # B. Short x-1
        df_Lev_m1x = df_Result.copy()
        df_Lev_m1x.iloc[8, 2] = 'ChinaAMC Direxion NASDAQ-100 Daily (-1x) Inverse Product'
        df_Lev_m1x.iloc[9, 2] = 'HK0000306602'
        df_Lev_m1x.iloc[10, 2] = '7331 HK'
        df_Lev_m1x.iloc[11, 2] = '7331.HK'
        df_Lev_m1x.iloc[13, 2] = str(flt_NavPerShare_m1x)
        df_Lev_m1x.iloc[14, 2] = str(flt_totalShareIssue_m1x)
        df_Lev_m1x.iloc[15, 2] = str(flt_BasketNav_m1x)
        df_Lev_m1x.iloc[18, 2] = str(flt_magFee_m1x)
        df_Lev_m1x.iloc[22, 5] = str(flt_FutPrice)
        df_Lev_m1x.iloc[22, 6] = str(flt_contractsShares_m1x)
        flt_BasketExposure_m1x = flt_fx * flt_FutPrice * flt_contractsShares_m1x * int_multiplier
        df_Lev_m1x.iloc[22, 10] = str(flt_BasketExposure_m1x)
        flt_EstimatedCash_m1x = round(flt_BasketNav_m1x + flt_magFee_m1x - flt_BasketExposure_m1x, 2)
        df_Lev_m1x.iloc[17, 2] = str(flt_EstimatedCash_m1x)
        # C. Short x-2
        df_Lev_m2x = df_Result.copy()
        df_Lev_m2x.iloc[8, 2] = 'ChinaAMC Direxion NASDAQ-100 Daily (-2x) Inverse Product'
        df_Lev_m2x.iloc[9, 2] = 'HK0000525649'
        df_Lev_m2x.iloc[10, 2] = '7522 HK'
        df_Lev_m2x.iloc[11, 2] = '7522.HK'
        df_Lev_m2x.iloc[13, 2] = str(flt_NavPerShare_m2x)
        df_Lev_m2x.iloc[14, 2] = str(flt_totalShareIssue_m2x)
        df_Lev_m2x.iloc[15, 2] = str(flt_BasketNav_m2x)
        df_Lev_m2x.iloc[18, 2] = str(flt_magFee_m2x)
        df_Lev_m2x.iloc[22, 5] = str(flt_FutPrice)
        df_Lev_m2x.iloc[22, 6] = str(flt_contractsShares_m2x)
        flt_BasketExposure_m2x = flt_fx * flt_FutPrice * flt_contractsShares_m2x * int_multiplier
        df_Lev_m2x.iloc[22, 10] = str(flt_BasketExposure_m2x)
        flt_EstimatedCash_m2x = round(flt_BasketNav_m2x + flt_magFee_m2x - flt_BasketExposure_m2x, 2)
        df_Lev_m2x.iloc[17, 2] = str(flt_EstimatedCash_m2x)
    except: return 'ERROR: {} - Build last DF from Model /*9'.format(str_PCF), []
    
    # Copy Model and fill it
    try:
        shutil.copyfile(str_modelfolder + str_modelFileName, str_folder + l_pcfFileName[0])
        str_path0 = fl.fStr_fillXls_celByCel(str_folder + l_pcfFileName[0], df_Lev_2x, 'Nasdaq 100 2X')
        shutil.copyfile(str_modelfolder + str_modelFileName, str_folder + l_pcfFileName[1])
        str_path1 = fl.fStr_fillXls_celByCel(str_folder + l_pcfFileName[1], df_Lev_m1x, 'NASDAQ -1')
        shutil.copyfile(str_modelfolder + str_modelFileName, str_folder + l_pcfFileName[2])
        str_path2 = fl.fStr_fillXls_celByCel(str_folder + l_pcfFileName[2], df_Lev_m2x, 'Nasdaq 100 -2X')
        # Feeder le model pour avoir le dernier RIC du Fut
        fl.fStr_fillXls_celByCel(str_modelfolder + str_modelFileName, df_Lev_2x)
        # Path
        l_pathAttach = [str_path0, str_path1, str_path2]
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except Exception as err: return 'ERROR:  Copy Modell and fill it *-/ - {0} | {1}'.format(str_PCF, str(err)), []
    
    # Build the return message
    try:
        str_resultFigures += '\n' + str(round(flt_NavPerShare_2x, 4)) + ' : Nav per Unit 2x'
        str_resultFigures += '\n' + str(round(flt_totalShareIssue_2x, 2)) + ' : Total Share Issue 2x'
        str_resultFigures += '\n' + str(round(flt_BasketNav_2x, 2)) + ' : Basket NAV 2x'
        str_resultFigures += '\n' + str(round(flt_FutPrice_2x, 2)) + ' : Fut Price'
        str_resultFigures += '\n' + '------------------------------------------------' 
    except: return 'ERROR: {} - Build the return message'.format(str_PCF), []
    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________



def fDf_GetHeader_forICE(str_pcfpath, str_sheetName, int_header, int_id = -1, str_isin = ''):
    df_PCF = pd.read_excel(str_pcfpath, sheet_name = str_sheetName, header = int_header, index_col = None)
    dte_pcfDate = df_PCF.iloc[9, 8]
    dte_pcfDate = dat.fDte_formatToDate(dte_pcfDate)
    flt_estimatedCash = df_PCF.iloc[10, 8]
    str_nav = df_PCF.iloc[3, 8]
    df_header = pd.DataFrame(columns = range(0, 13))
    df_header.loc[len(df_header)] = ['1', str(int_id), str_isin, dte_pcfDate.strftime('%Y%m%d'), '', '', 'XHKG', str(round(str_nav, 4)), 
                  str(abs(flt_estimatedCash)), ['+' if x>=0 else '-' for x in [flt_estimatedCash]][0], '', '', '']
    return df_header, dte_pcfDate
#----------------------------------------

def fDf_GetCompo_forICE(str_pcfpath, str_sheetName, int_header, dte_pcfDate, int_id = -1, str_isin = ''):
    df_compo = pd.read_excel(str_pcfpath, sheet_name = str_sheetName, header = int_header, index_col = None)
    #df_compo = df_compo[df_compo['ISIN'].str.apply(lambda x: len(x) > 1)]
    df_compo = df_compo[df_compo['ISIN'].str.len() > 1]
    df_compo['1col_2'] = '2'
    df_compo['3col_rien'] = ''
    df_compo['11col_rien'] = ''
    df_compo['5col_date'] = dte_pcfDate.strftime('%Y%m%d')
    df_compo['6col_idFund'] = str(int_id)
    df_compo['7col_isin'] = str_isin
    df_compo['PlusOuMoins'] = ['+' if x>=0 else '-' for x in df_compo['QUANTITY']]
    df_compo['QUANTITY'] = df_compo['QUANTITY'].apply(lambda x: abs(x))
    # End
    df_compo = df_compo[['1col_2', 'ISIN', '3col_rien', 'SEDOL', '5col_date', '6col_idFund', '7col_isin', 
                         'QUANTITY', 'PlusOuMoins','NAME', '11col_rien', 'CURRENCY', 'PRICE']]
    return df_compo
#----------------------------------------

def fDf_getHSI(df_in, int_stockCode = -1, str_isin = '', str_isin2 = '', in_id2 = -1, flt_fx_USDHKD = 1):
    # Start some Exception process on OIL
    if int_stockCode == 3097:
        int_CU = 250000
        flt_nav = df_in.iloc[4, 6]
        #print('flt_nav:', flt_nav, type(flt_nav))
        if type(flt_nav) == str:
            flt_nav = float(flt_nav.replace('HK$','').replace(',',''))
        flt_Cash = df_in.iloc[6, 6]
        #print('flt_Cash:', flt_Cash, type(flt_Cash))
        if type(flt_Cash) == str:
            flt_Cash = float(flt_Cash.replace('HK$','').replace(',',''))
        flt_UnitsOutstanding = df_in.iloc[7, 6]
        dte_pcfDate = df_in.iloc[10, 6]
        df_Pcf = df_in.iloc[12:,:5].copy()
    else:
        int_CU = 100000
        flt_nav = df_in.iloc[3, 6]
        flt_UnitsOutstanding = df_in.iloc[6, 6]
        dte_pcfDate = df_in.iloc[9, 6]
        df_Pcf = df_in.iloc[11:,:5].copy()
    flt_basketOutstanding = flt_UnitsOutstanding / int_CU
    dte_pcfDate = dat.fDte_formatToDate(dte_pcfDate, '%Y-%m-%d')
    df_Pcf.reset_index(drop = True, inplace = True)
    df_Pcf.rename(columns = df_Pcf.iloc[0], inplace = True)     #.drop(df_Pcf.index[0])
    df_Pcf = df_Pcf[df_Pcf['NAME'].str.len() > 1]               # Remove empty row
    
    # Build the final DF
    #print(2)
    df_Pcf['1Col'] = '3'
    # Exception process on OIL
    if int_stockCode == 3097:
        df_Pcf['TICKER'] = df_Pcf['RIC']
        df_Pcf['1Col'] = df_Pcf['1Col'].mask(df_Pcf['TICKER'] == 'RIC', '1')
    else:
        df_Pcf['1Col'] = df_Pcf['1Col'].mask(df_Pcf['TICKER'] == 'TICKER', '1')
    df_Pcf['1Col'] = df_Pcf['1Col'].mask((df_Pcf['TICKER'].str.split('.').str.len() > 1), '2')
    df_Pcf['1Col'] = df_Pcf['1Col'].mask((df_Pcf['TICKER'].str.split().str.len() > 1), '2')
    df_Pcf['2Col'] = df_Pcf['TICKER']
    df_Pcf['2Col'] = df_Pcf['2Col'].mask(df_Pcf['1Col'] == '1', str(int_stockCode))
    df_Pcf['2Col'] = df_Pcf['2Col'].mask(df_Pcf['1Col'] == '2', str_isin2)
    df_Pcf['3Col'] = df_Pcf['NAME']
    df_Pcf['3Col'] = df_Pcf['3Col'].mask(df_Pcf['1Col'] == '1', str_isin)
    df_Pcf['3Col'] = df_Pcf['3Col'].mask(df_Pcf['1Col'] == '2', '')
    df_Pcf['4Col'] = 'HKG'
    df_Pcf['4Col'] = df_Pcf['4Col'].mask(df_Pcf['1Col'] == '1', dte_pcfDate.strftime('%Y%m%d'))
    df_Pcf['4Col'] = df_Pcf['4Col'].mask(df_Pcf['1Col'] == '2', str(in_id2))
    df_Pcf['5Col'] = dte_pcfDate.strftime('%Y%m%d')
    df_Pcf['5Col'] = df_Pcf['5Col'].mask(df_Pcf['1Col'] == '1', '2')
    df_Pcf['6Col'] = str(int_stockCode)
    df_Pcf['6Col'] = df_Pcf['6Col'].mask(df_Pcf['1Col'] == '1', 'HKD')
    df_Pcf['7Col'] = str_isin
    df_Pcf['7Col'] = df_Pcf['7Col'].mask(df_Pcf['1Col'] == '1', '')
    # colonne 8
    #print(3)
    df_Pcf['QUANTITY'] = df_Pcf['QUANTITY'].mask(df_Pcf['1Col'] == '1', 0)
    df_Pcf['QUANTITY'] = df_Pcf['QUANTITY'].mask(df_Pcf['1Col'] == '2', 0)
    df_Pcf['8Col'] = df_Pcf['QUANTITY'].astype(float) * flt_basketOutstanding
    df_Pcf['8Col'] = df_Pcf['8Col'].mask(df_Pcf['1Col'] == '1', flt_nav)
    # Colonne 10 prep
    #print(4)
    df_Pcf['10Col_prep'] = 0
    df_Pcf['10Col_prep'] = df_Pcf['10Col_prep'].mask(df_Pcf['2Col'] == 'HIM0', 50)
    df_Pcf['10Col_prep'] = df_Pcf['10Col_prep'].mask(df_Pcf['2Col'] == 'HCM0', 50)
    df_Pcf['10Col_prep'] = df_Pcf['10Col_prep'].mask(df_Pcf['2Col'] == 'HUM0', 10)
    df_Pcf['10Col_prep'] = df_Pcf['10Col_prep'].mask(df_Pcf['2Col'] == 'MHCM0', 10)
    df_Pcf['10Col_prep'] = df_Pcf['10Col_prep'].mask(df_Pcf['2Col'] == 'CLZ0', 1000)    # OIL Specific
    df_Pcf['10Col_Calculus'] = df_Pcf['10Col_prep'] * df_Pcf['8Col']
    flt_sumCol10 = df_Pcf['10Col_Calculus'].sum()
    # Colonne 10
    #print(5)
    df_Pcf['10Col'] = df_Pcf['10Col_prep']
    df_Pcf['10Col'] = df_Pcf['10Col'].mask(df_Pcf['1Col'] == '1', '+')
    df_Pcf['10Col'] = df_Pcf['10Col'].mask(df_Pcf['1Col'] == '2', '')
    # Colonne 9
    #print(6)
    df_Pcf['9Col'] = '+'
    df_Pcf['9Col'] = df_Pcf['9Col'].mask(df_Pcf['1Col'] == '1', flt_nav * flt_UnitsOutstanding - flt_sumCol10)
    df_Pcf['9Col'] = df_Pcf['9Col'].mask(df_Pcf['8Col'] < 0, '-')
    # colonne 8
    df_Pcf['8Col'] = df_Pcf['8Col'].apply(lambda x : abs(x))
    # colonne rest
    #print(7)
    df_Pcf['11Col'] = df_Pcf['PRICE']
    df_Pcf['11Col'] = df_Pcf['11Col'].mask(df_Pcf['1Col'] == '1', str(flt_UnitsOutstanding))
    df_Pcf['11Col'] = df_Pcf['11Col'].mask(df_Pcf['1Col'] == '2', str(in_id2))
    df_Pcf['12Col'] = 'HKD'
    #print(8)
    df_Pcf['12Col'] = df_Pcf['12Col'].mask(df_Pcf['2Col'] == 'CLZ0', 'USD')             # OIL Specific
    df_Pcf['12Col'] = df_Pcf['12Col'].mask(df_Pcf['1Col'] == '1', '')
    df_Pcf['13Col'] = ''
    df_Pcf['13Col'] = df_Pcf['13Col'].mask(df_Pcf['1Col'] == '2', '0.0000')
    
    # Sepcific to OIL
    if len(df_Pcf[df_Pcf['1Col'] == '2']) == 0:
        if len(df_Pcf[df_Pcf['2Col'] == 'CLZ0']) > 0:
            df_Pcf['7Col'] = df_Pcf['7Col'].mask(df_Pcf['1Col'] == '1', 'XHKG')
            df_Pcf['4Col'] = df_Pcf['4Col'].mask(df_Pcf['1Col'] == '3', 'XNYM')
            df_Pcf['Price_OIL'] = df_Pcf['PRICE']
            df_Pcf['Price_OIL'] = df_Pcf['Price_OIL'].mask(df_Pcf['1Col'] == '1', 0)
            df_Pcf['10Col_Calculus'] = df_Pcf['10Col_prep'] * df_Pcf['8Col'] * df_Pcf['Price_OIL'] * flt_fx_USDHKD
            flt_sumCol10 = df_Pcf['10Col_Calculus'].sum()
            df_Pcf['9Col'] = df_Pcf['9Col'].mask(df_Pcf['1Col'] == '1', round(flt_Cash * flt_basketOutstanding + flt_sumCol10, 0))
            flt_SpecialVal = df_Pcf.loc[df_Pcf['1Col'] == '1', '9Col'].values[0]
            if flt_SpecialVal > 0:  df_Pcf.loc[df_Pcf['1Col'] == '1', '10Col'].values[0] = '-'
            else:                   df_Pcf.loc[df_Pcf['1Col'] == '1', '9Col'].values[0] = abs(flt_SpecialVal)
        else:                                       # Sepcific to other than OIL
            # Replace 1 by 15
            df_Pcf['1Col'] = df_Pcf['1Col'].mask(df_Pcf['1Col'] == '1', '15')
    # End
    df_Pcf = df_Pcf[['1Col', '2Col', '3Col', '4Col', '5Col', '6Col', '7Col', '8Col', '9Col', '10Col', '11Col', '12Col', '13Col']].copy()
    return df_Pcf
#----------------------------------------

def pcf_GlobalX(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_Nav =        dic_df['Out_Nav']
        df_Out_Fx =     dic_df['Out_Fx']
        try:    df_FTP_Oil =        dic_df['FTP_Oil']
        except: df_FTP_Oil = None
        try:    df_FTP_SPX =        dic_df['FTP_SPX']
        except: df_FTP_SPX = None
        try:   
            df_FTP_HSI_LEV =    dic_df['FTP_HSI_LEV']
            df_FTP_HSI_INV =    dic_df['FTP_HSI_INV']
            df_FTP_HSCEI_LEV =  dic_df['FTP_HSCEI_LEV']
            df_FTP_HSCEI_INV =  dic_df['FTP_HSCEI_INV']
        except: df_FTP_HSI_LEV = None
        str_folder = dic_df['Folder']
    except: return 'ERROR: Dataframe - {}'.format(str_PCF), []

    # Other param
    try:    
        l_pcfFileName = ['PCF_{}(Incl FX).xlsx'.format(dte_date.strftime('%Y%m%d')), 
                         'MiraeAsset.{}.csv'.format(dte_date.strftime('%Y%m%d'))]
    except: return 'ERROR: Other Param - {} '.format(str_PCF), []
    
    # Rename PCF
    try:
        # Copy
        str_pcfpath = [path for path in dic_df['files'] if 'ETF_PCFReport_MIRAE' in path][0]
        shutil.copyfile(str_pcfpath, str_pcfpath.replace('\\raw',''))
        # Rename
        str_oldName = str_pcfpath.split('\\')[-1]
        str_newName = l_pcfFileName[0]
        fl.Act_Rename(str_folder, str_oldName, str_newName, False)
        l_pathAttach = [str_folder + str_newName]
    except: return 'ERROR: Rename PCF - {} '.format(str_PCF), []
    
    # Build the First Rows
    try:
        df_MXCN_head,   dte_MXCN =   fDf_GetHeader_forICE(str_pcfpath, 'MXCN', None, 3040, 'HK0000151925')
        df_HSHDYI_head, dte_HSHDYI = fDf_GetHeader_forICE(str_pcfpath, 'HSHDYI', None, 3110, 'HK0000151933')
        df_CSI300_head, dte_CSI300 = fDf_GetHeader_forICE(str_pcfpath, 'CSI300', None, 83127, 'HK0000215316')
        df_SOLCCC_head, dte_SOLCCC = fDf_GetHeader_forICE(str_pcfpath, 'SOLCCC', None, 2826, 'HK0000516713')
        df_SOLCBT_head, dte_SOLCBT = fDf_GetHeader_forICE(str_pcfpath, 'SOLCBT', None, 2820, 'HK0000516697')
        df_SOLCEV_head, dte_SOLCEV = fDf_GetHeader_forICE(str_pcfpath, 'SOLCEV', None, 2845, 'HK0000562659')
        df_SOLCCB_head, dte_SOLCCB = fDf_GetHeader_forICE(str_pcfpath, 'SOLCCB', None, 2806, 'HK0000562634')
        df_SOLCCE_head, dte_SOLCCE = fDf_GetHeader_forICE(str_pcfpath, 'SOLCCE', None, 2809, 'HK0000562675')
    except Exception as err: return 'ERROR:Build the First Rows - {0} | {1} '.format(str_PCF, str(err)), []
    
    # Build the Compo
    try:
        df_MXCN =   fDf_GetCompo_forICE(str_pcfpath, 'MXCN', 12, dte_MXCN, 3040, 'HK0000151925')
        df_HSHDYI = fDf_GetCompo_forICE(str_pcfpath, 'HSHDYI', 12, dte_HSHDYI, 3110, 'HK0000151933')
        df_CSI300 = fDf_GetCompo_forICE(str_pcfpath, 'CSI300', 12, dte_CSI300, 83127, 'HK0000215316')
        # Place for shitty row
        df_SOLCCC = fDf_GetCompo_forICE(str_pcfpath, 'SOLCCC', 12, dte_SOLCCC, 2826, 'HK0000516713')
        df_SOLCBT = fDf_GetCompo_forICE(str_pcfpath, 'SOLCBT', 12, dte_SOLCBT, 2820, 'HK0000516697')
        df_SOLCEV = fDf_GetCompo_forICE(str_pcfpath, 'SOLCEV', 12, dte_SOLCEV, 2845, 'HK0000562659')
        df_SOLCCB = fDf_GetCompo_forICE(str_pcfpath, 'SOLCCB', 12, dte_SOLCCB, 2806, 'HK0000562634')
        df_SOLCCE = fDf_GetCompo_forICE(str_pcfpath, 'SOLCCE', 12, dte_SOLCCE, 2809, 'HK0000562675')        
    except Exception as err: return 'ERROR: Build the Compo - {0} | {1} '.format(str_PCF, str(err)), []
    
    # Come back to First row
    try:
        df_MXCN_head.iloc[0, 4] = len(df_MXCN.index)
        df_MXCN_head.iloc[0, 5] = 'HKD'
        df_MXCN_head.iloc[0, 10] = '200000'
        df_HSHDYI_head.iloc[0, 4] = len(df_HSHDYI.index)
        df_HSHDYI_head.iloc[0, 5] = 'HKD'
        df_HSHDYI_head.iloc[0, 10] = '200000'
        df_CSI300_head.iloc[0, 4] = len(df_CSI300.index)
        df_CSI300_head.iloc[0, 5] = 'CNY'
        df_CSI300_head.iloc[0, 10] = '500000'
        df_SOLCCC_head.iloc[0, 4] = len(df_SOLCCC.index)
        df_SOLCCC_head.iloc[0, 5] = 'CNH'
        df_SOLCCC_head.iloc[0, 10] = '50000'
        df_SOLCBT_head.iloc[0, 4] = len(df_SOLCBT.index)
        df_SOLCBT_head.iloc[0, 5] = 'CNH'
        df_SOLCBT_head.iloc[0, 10] = '50000'
        df_SOLCEV_head.iloc[0, 4] = len(df_SOLCEV.index)
        df_SOLCEV_head.iloc[0, 5] = 'CNH'
        df_SOLCEV_head.iloc[0, 10] = '50000'
        df_SOLCCB_head.iloc[0, 4] = len(df_SOLCCB.index)
        df_SOLCCB_head.iloc[0, 5] = 'CNH'
        df_SOLCCB_head.iloc[0, 10] = '50000'
        df_SOLCCE_head.iloc[0, 4] = len(df_SOLCCE.index)
        df_SOLCCE_head.iloc[0, 5] = 'CNH'
        df_SOLCCE_head.iloc[0, 10] = '50000'
    except Exception as err: return 'ERROR: Come back to First row - {0} | {1} '.format(str_PCF, str(err)), []
    
    # Shitty Row
    try:
        #df_ICE.loc[len(df_ICE)] = ['', '', '', dte_pcfDate.strftime('%Y%m%d'), '', '', '', '', '', '', '', '', '']
        flt_nav = df_Nav.loc[(df_Nav['Account code'] == 'MACS') & (df_Nav['Share Class ID'] == 'AHK'), 'Accounting NAV per Share'].values[0]
        df_shittyRow = pd.DataFrame(columns = range(13))
        df_shittyRow.loc[len(df_shittyRow)] = ['1', '3127', 'HK0000215324', dte_CSI300.strftime('%Y%m%d'), '1', 'HKD', 'XHKG',
                                                 str(round(flt_nav, 4)),'0', '+', '1', '', '']
        df_shittyRow.loc[len(df_shittyRow)] = ['2', 'HK0000215316', '215316', '', dte_CSI300.strftime('%Y%m%d'), '3127', 'HK0000215324', 
                                                 '1', '+', '', 'I:83127.IV', 'HKD', '']
    except Exception as err: return 'ERROR: Shitty Row - {0} | {1} '.format(str_PCF, str(err)), []
    
    # Adding OIL, SPX, HSI/HSCEI
    try:
        # FX
        df_Out_Fx.columns = ['FundCcy', 'Curr', 'Date', 'Fx', 'PereviousDate', 'FxDm1', '%Change']
        flt_fx_USDHKD = df_Out_Fx[df_Out_Fx['Curr'] =='USD']['Fx'].values[0]
        # SPX
        if not df_FTP_SPX is None:
            flt_nav = df_FTP_SPX.iloc[4, 6]
            df_SPX = pd.DataFrame(columns = range(13))
            df_SPX.loc[len(df_SPX)] = ['1', '7322', 'HK0000305430', dte_MXCN.strftime('%Y%m%d'), '1', 'HKD', '',str(round(flt_nav * flt_fx_USDHKD, 4)),
                                       '0', '+', '1', '', '']
            df_SPX.loc[len(df_SPX)] = ['2', 'USD00000NAV1', '', 'USDNAV1', dte_MXCN.strftime('%Y%m%d'), '7322', 'HK0000305430',str(round(flt_nav, 4)),
                                       '+', 'USD NAV', '', 'USD', '1.0000']
        # HSI / HSCEI
        if not df_FTP_HSI_LEV is None:
            df_HSI_LEV = fDf_getHSI(df_FTP_HSI_LEV, 7231, 'HK0000323144', 'HK2800008867', 6188557)
            df_HSI_INV = fDf_getHSI(df_FTP_HSI_INV, 7336, 'HK0000323169')
            df_HSCEI_LEV = fDf_getHSI(df_FTP_HSCEI_LEV, 7230, 'HK0000323169', 'HK2828013055', 6724092)
            df_HSCEI_INV = fDf_getHSI(df_FTP_HSCEI_INV, 7362, 'HK0000323151')
        # OIL
        if not df_FTP_Oil is None:
            df_Oil = fDf_getHSI(df_FTP_Oil, 3097, 'HK0000296944', '', -1, flt_fx_USDHKD)
    except Exception as err: return 'ERROR: Adding OIL, SPX, HSI/HSCEI - {0} | {1} '.format(str_PCF, str(err)), []
    
    # Merge the Dataframe
    try:
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_MXCN_head, df_MXCN)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_HSHDYI_head)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_HSHDYI)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_CSI300_head)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_CSI300)
        # Place for shitty row
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_shittyRow)
        # Rest of PCF
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_SOLCCC_head)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_SOLCCC)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_SOLCBT_head)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_SOLCBT)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_SOLCEV_head)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_SOLCEV)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_SOLCCB_head)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_SOLCCB)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_SOLCCE_head)
        df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_SOLCCE)
        if not df_FTP_SPX is None:
            df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_SPX)
        if not df_FTP_HSI_LEV is None:
            df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_HSI_LEV)
            df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_HSI_INV)
            df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_HSCEI_LEV)
            df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_HSCEI_INV)
        if not df_FTP_Oil is None:
            df_ICE = dframe.fDf_Concat_wColOfDf1(df_ICE, df_Oil)
    except Exception as err: return 'ERROR: Merge the Dataframe - {0} | {1} '.format(str_PCF, str(err)), []
    
    # Create ICE
    try:
        str_pathICE = fl.fStr_CreateTxtFile(str_folder, l_pcfFileName[1], df_ICE)
        # Create tmp file (Dont put it in the return for mail)
        shutil.copyfile(str_pathICE, str_pathICE.replace('.csv','.tmp'))
         # PCF Path for return
        l_pathAttach.append(str_pathICE)
        l_pathAttach.append(str_pathICE.replace('.csv','.tmp'))
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except Exception as err: return 'ERROR: Create ICE - {0} | {1} '.format(str_PCF, str(err)), []
    
    return 'All good', l_pathAttach
#___________________________________________________________________________________________



def pcf_Nikko(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_OUT_LIGHTINV = dic_df['OUT_Niko_HOLD']
        df_OUT_navFile_Nikko = dic_df['OUT_Niko_NAV']
        #        df_OUT_LIGHTINV = dic_df['OUT_LIGHTINV']
        #        df_OUT_navFile_Nikko = dic_df['OUT_navFile_Nikko']        
        str_folder = dic_df['Folder']
    except: return 'ERROR: {} - Dataframe'.format(str_PCF), []
    
    # Other param
    try:
        dte_navDate = df_OUT_navFile_Nikko[df_OUT_navFile_Nikko['Share currency'] =='USD']['NAV date'].values[0]
        if len(str(dte_navDate)) == 7:
            dte_navDate = '0' + str(dte_navDate)
        dte_navDate = dat.fDte_formatToDate(str(dte_navDate), '%d%m%Y')
        #str_dm1 = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, '%Y%m%d', -1, '240')
        str_modelfolder = str_folderRoot + 'HK_Nikko\\'
        str_modelFileName = 'NikkoAMGlobalInternetETF.xlsx'
        #    l_pcfFileName = ['Nikko AM Global Internet ETF - SGX - ' + dte_navDate.strftime('%Y%m%d') + '.xlsx']
        l_pcfFileName = ['Nikko AM Global Internet ETF - Basket - ' + dte_navDate.strftime('%Y%m%d') + '.xlsx', 
                         'Nikko AM Global Internet ETF - Fund - ' + dte_navDate.strftime('%Y%m%d') + '.xlsx']
    except: return 'ERROR: {} - Other Param xsw'.format(str_PCF), []
    
    # 1. Variables
    try:
        # Rounding issue form pandas
        df_OUT_navFile_Nikko['Price share CCY'] = df_OUT_navFile_Nikko['Price share CCY'].apply(lambda x: round(x, 13))
        flt_NavPerShare = df_OUT_navFile_Nikko[df_OUT_navFile_Nikko['Share currency'] =='USD']['Price share CCY'].values[0]
        flt_aum = df_OUT_navFile_Nikko[df_OUT_navFile_Nikko['Share currency'] =='USD']['TNA of the fund in fund CCY'].values[0]
        flt_totalShareIssue = df_OUT_navFile_Nikko[df_OUT_navFile_Nikko['Share currency'] =='USD']['Nb of outstanding shares'].values[0]
        #str_fundCCY = df_OUT_navFile_Nikko[df_OUT_navFile_Nikko['Share Currency'] =='USD']['Fund Currency'].values[0]
        int_CreationUnits = 50000
        flt_BasketNav = flt_NavPerShare * int_CreationUnits
    except: return 'ERROR: {} - 1. Variables'.format(str_PCF), []
    
    # 21. Build Df on Basket
    try:
        # Chaage columns Name to be more clear afterwards
        df_OUT_LIGHTINV = df_OUT_LIGHTINV[['GTI code', 'Security name','External value code','Sedol codification','Security currency',
                                           'Quantity','Quotation price of Security','Exchange rate', 'Evaluation price in fund ccy']]
        df_OUT_LIGHTINV.columns = ['GTI', 'Name','Isin','Sedol','Ccy','Qty','Price','Fx', 'Fund_MktCap']        
        # Split between HOLDINGS and Cash
        df_Holdings = df_OUT_LIGHTINV[df_OUT_LIGHTINV['GTI'].str.startswith('S', na = False)].copy()
        #df_Holdings = df_OUT_LIGHTINV[df_OUT_LIGHTINV.col.str.get(0).isin(['S'])]
        #df_Holdings = df_OUT_LIGHTINV[df_OUT_LIGHTINV['GTI'].isin(['S01','S39'])]
        df_Holdings.reset_index(drop = True, inplace = True)
        df_Cash = df_OUT_LIGHTINV[~df_OUT_LIGHTINV['GTI'].str.startswith('S', na = True)].copy()
        #df_Cash = df_OUT_LIGHTINV[df_OUT_LIGHTINV['GTI'] == 'CO']
        
        # BASKET
        df_Basket = df_Holdings[['Name','Isin','Sedol','Ccy','Qty','Price','Fx']].copy()
        df_Basket['Qty_basket'] = df_Basket['Qty'] / flt_totalShareIssue * int_CreationUnits
        df_Basket['Qty_basket'] = df_Basket['Qty_basket'].apply(lambda x: math.floor(x))
        df_Basket['Basket_MktCap'] = df_Basket['Qty_basket'] * df_Basket['Price'] / df_Basket['Fx']
        df_Basket['Weight'] = df_Basket['Basket_MktCap'] / flt_BasketNav
        df_Basket = df_Basket[['Name','Isin','Sedol','Ccy','Qty_basket','Price','Basket_MktCap','Weight']].copy()
    except: return 'ERROR: {} - 21. Build Df on Basket'.format(str_PCF), []
    # 22. Build Df on Basket
    try:
        # Variables again
        flt_BasketMarketCap = df_Basket['Basket_MktCap'].sum()
        flt_BasketCash = flt_BasketNav - flt_BasketMarketCap
        flt_BasketCashWeight = flt_BasketCash / flt_BasketNav
        # To Fill the last ROW ...
        df_Basket.loc[len(df_Basket)] = ['CASH COMPONENT','NIL','NIL','USD',str(flt_BasketCash),
                                          '0',str(flt_BasketCash),str(flt_BasketCashWeight)]
    except: return 'ERROR: 22. Build Df on Basket - {}'.format(str_PCF), []
    
    # 212. Build Df on Fund
    try:
        df_Fund = df_Holdings[['Name','Isin','Sedol','Ccy','Qty','Price','Fund_MktCap']].copy()
        df_Fund['Qty'] = df_Fund['Qty'].apply(lambda x: math.floor(x))
        df_Fund['Weight'] = df_Fund['Fund_MktCap'] / flt_aum
    except Exception as err:    return 'ERROR: 212. Build Df on Fund - {} | {}'.format(str_PCF, str(err)), []
    # 222. Build Df on Fund
    try:
        # Variables again
        flt_FundMarketCap = df_Holdings['Fund_MktCap'].sum()
        flt_aum2 = flt_FundMarketCap + df_Cash['Fund_MktCap'].sum()
        if abs(flt_aum2 - flt_aum) > 0.1: 
            print('  ***  Warning : AUM is not the same from source')
            print('  ***  flt_aum: ', flt_aum)
            print('  ***  flt_aum2: ', flt_aum2)
        flt_FundCash = flt_aum2 - flt_FundMarketCap
        flt_FundCashWeight = flt_FundCash / flt_aum       
        # To Fill the last ROW ...
        df_Fund.loc[len(df_Fund)] = ['CASH COMPONENT','NIL','NIL','USD', str(flt_FundCash),
                                    '0', str(round(flt_FundCash, 2)), str(flt_FundCashWeight)]
    except Exception as err:    return 'ERROR: 222. Build Df on Fund - {} | {}'.format(str_PCF, str(err)), []
    
    # 3. Build last DF from Model
    try:
        df_Final = pd.read_excel(str_modelfolder + str_modelFileName, header = None, index_col = None)
        df_Final.fillna(value = '', inplace = True)
        df_Final.iloc[0, 1] = dte_navDate.strftime('%m/%d/%Y')
        df_Final.iloc[5, 1] = str(flt_NavPerShare)
        df_Final.iloc[6, 1] = str(flt_aum)
        df_Final.iloc[7, 1] = str(flt_totalShareIssue)
        # A. BASKET
        df_BasketFinal = df_Final.copy()
        df_Basket.columns = df_BasketFinal.columns
        df_BasketFinal = pd.concat([df_BasketFinal.loc[:9], df_Basket], ignore_index=True)
        # B. FUND
        df_FundFinal = df_Final.copy()
        df_Fund.columns = df_FundFinal.columns
        df_FundFinal = pd.concat([df_BasketFinal.loc[:9], df_Fund], ignore_index=True)
    except: return 'ERROR: {} - 3. Build last DF from Model'.format(str_PCF), []
    
    # 4. Copy Model and fill it
    try:
        # A. BASKET
        shutil.copyfile(str_modelfolder + str_modelFileName, str_folder + l_pcfFileName[0])
        i_len = len(df_BasketFinal) - 41
        if i_len != 0:      str_path = fl.fStr_fillXls_celByCel(str_folder + l_pcfFileName[0], df_BasketFinal, '', 0, i_len, 35)
        else:               str_path = fl.fStr_fillXls_celByCel(str_folder + l_pcfFileName[0], df_BasketFinal)        
        l_path0 = [str_path]
        # B. FUND
        shutil.copyfile(str_modelfolder + str_modelFileName, str_folder + l_pcfFileName[1])
        i_len = len(df_FundFinal) - 41
        if i_len != 0:      str_path = fl.fStr_fillXls_celByCel(str_folder + l_pcfFileName[1], df_FundFinal, '', 0, i_len, 35)
        else:               str_path = fl.fStr_fillXls_celByCel(str_folder + l_pcfFileName[1], df_FundFinal)
        l_path1 = [str_path]
        # Path
        l_pathAttach = l_path0 + l_path1
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except Exception as err:    return 'ERROR: 4. Copy Modell and fill it */- - {} | {}'.format(str_PCF, str(err)), []
    
    # 6. Build the return message
    try:
        str_resultFigures += '\n' + str(round(flt_NavPerShare, 4)) + ' : Nav per Unit'
        str_resultFigures += '\n' + str(round(flt_aum, 0)) + ' : Asset Under M'
        str_resultFigures += '\n' + str(round(flt_totalShareIssue, 0)) + ' : Total Shares in Issue'
        str_resultFigures += '\n\n' + str(round(int_CreationUnits, 0)) + ' : Basket Creation Issue'
        str_resultFigures += '\n' + str(round(flt_BasketNav, 0)) + ' : Basket NAV'
        str_resultFigures += '\n' + str(round(flt_BasketMarketCap, 0)) + ' : Basket Market Cap'
        str_resultFigures += '\n' + str(round(flt_BasketCash, 0)) + ' : Basket Cash'
        str_resultFigures += '\n' + str(round(flt_BasketCashWeight*100, 0)) + '% : Basket Cash Weight'
        str_resultFigures += '\n\n' + str(round(flt_FundMarketCap, 0)) + ' : Fund Market Cap'
        str_resultFigures += '\n' + str(round(flt_FundCash, 0)) + ' : Fund Cash'
        str_resultFigures += '\n' + str(round(flt_FundCashWeight*100, 0)) + '% : Fund Cash Weight'
        str_resultFigures += '\n' + '------------------------------------------------' 
    except: return 'ERROR: {} - 6. Build the return message'.format(str_PCF), []
    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________
  
    


def pcf_NikkoSGX(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_OUT_LIGHTINV = dic_df['OUT_Niko_HOLD']
        df_OUT_navFile_Nikko = dic_df['OUT_Niko_NAV']    
        str_folder = dic_df['Folder']
    except: return 'ERROR: {} - Dataframe'.format(str_PCF), []
    
    # Other param
    try:
        dte_navDate = df_OUT_navFile_Nikko[df_OUT_navFile_Nikko['Share currency'] =='USD']['NAV date'].values[0]
        if len(str(dte_navDate)) == 7:
            dte_navDate = '0' + str(dte_navDate)
        dte_navDate = dat.fDte_formatToDate(str(dte_navDate), '%d%m%Y')
        #str_dm1 = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, '%Y%m%d', -1, '240')
        str_modelfolder = str_folderRoot + 'HK_Nikko\\'
        str_modelFileName = 'NikkoSGX.xlsx'
        l_pcfFileName = ['Nikko AM Global Internet ETF - SGX - ' + dte_navDate.strftime('%Y%m%d') + '.xlsx']
    except: return 'ERROR: {} - sgx Other Param'.format(str_PCF), []
    
    
    # 1. Variables
    try:
        df_OUT_navFile_Nikko['Price share CCY'] = df_OUT_navFile_Nikko['Price share CCY'].apply(lambda x: round(x, 13))
        flt_NavPerShare = df_OUT_navFile_Nikko[df_OUT_navFile_Nikko['Share currency'] =='USD']['Price share CCY'].values[0]
        flt_aum = df_OUT_navFile_Nikko[df_OUT_navFile_Nikko['Share currency'] =='USD']['TNA of the fund in fund CCY'].values[0]
        flt_totalShareIssue = df_OUT_navFile_Nikko[df_OUT_navFile_Nikko['Share currency'] =='USD']['Nb of outstanding shares'].values[0]
        #str_fundCCY = df_OUT_navFile_Nikko[df_OUT_navFile_Nikko['Share Currency'] =='USD']['Fund Currency'].values[0]
        int_CreationUnits = 50000
        flt_BasketNav = flt_NavPerShare * int_CreationUnits
    except: return 'ERROR: {} - 1. sgx Variables'.format(str_PCF), []
    
    # 2. Build Df for SGX
    try:
        # Chaage columns Name to be more clear afterwards
        df_OUT_LIGHTINV = df_OUT_LIGHTINV[['GTI code', 'Security name','External value code','Sedol codification','Security currency',
                                           'Quantity','Quotation price of Security','Exchange rate', 'Evaluation price in fund ccy']]
        df_OUT_LIGHTINV.columns = ['GTI', 'Name','Isin','Sedol','Ccy','Qty','Price','Fx', 'Fund_MktCap']        
        # Split between HOLDINGS and Cash
        df_Holdings = df_OUT_LIGHTINV[df_OUT_LIGHTINV['GTI'].isin(['S01','S39'])]
        #df_Cash = df_OUT_LIGHTINV[df_OUT_LIGHTINV['GTI'] == 'CO']
        
        # BASKET 
        df_Basket = df_Holdings[['Name','Isin','Sedol','Ccy','Qty','Price','Fx']].copy()
        df_Basket['Qty_basket'] = df_Basket['Qty'] / flt_totalShareIssue * int_CreationUnits
        df_Basket['Qty_basket'] = df_Basket['Qty_basket'].apply(lambda x: math.floor(x))
        df_Basket['Basket_MktCap'] = df_Basket['Qty_basket'] * df_Basket['Price'] / df_Basket['Fx']        
        
        # Variables Again
        flt_BasketMarketCap = df_Basket['Basket_MktCap'].sum()
        flt_BasketCash = flt_BasketNav - flt_BasketMarketCap
        
        # Customize for SGX
        df_Basket['Fx'] = 1/df_Basket['Fx']
        df_Basket = df_Basket[['Name','Ccy','Price','Qty_basket','Isin','Sedol','Fx']]
        df_Basket = dframe.fDf_InsertColumnOfIndex(df_Basket, 1, 0)
        # ROUNDING
        df_Basket['Price'] = df_Basket['Price'].apply(lambda x : round(x,6))
    except: return 'ERROR: {} - 2. Build Df for SGX'.format(str_PCF), []
    
    # 3. Build last DF from Model
    try:
        df_Final = pd.read_excel(str_modelfolder + str_modelFileName, header = None, index_col = None)
        df_Final.fillna(value = '', inplace = True)
        df_Final.iloc[3, 2] = dte_navDate.strftime('%m/%d/%Y')
        df_Final.iloc[11, 2] = str(flt_NavPerShare)
        df_Final.iloc[12, 2] = str(flt_aum)
        df_Final.iloc[13, 2] = str(flt_totalShareIssue)
        df_Final.iloc[14, 2] = str(int_CreationUnits)
        df_Final.iloc[15, 2] = str(flt_BasketCash)
        # A. BASKET
        df_Basket.columns = df_Final.columns  #[1:]
        df_Final = pd.concat([df_Final.loc[:18], df_Basket], ignore_index = True)
    except: return 'ERROR: {} - 3. sgx Build last DF from Model'.format(str_PCF), []
    
    # 4. sgx Copy Model and fill it
    try:
        shutil.copyfile(str_modelfolder + str_modelFileName, str_folder + l_pcfFileName[0])
        str_path = fl.fStr_fillXls_celByCel(str_folder + l_pcfFileName[0], df_Final, '', 0, len(df_Basket) - 30, 40)
        l_pathAttach = [str_path]
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except Exception as err:    return 'ERROR: 4. sgx x Copy Model and fill it - {} | {}'.format(str_PCF, str(err)), []
    
    # 6. Build the return message
    try:
        str_resultFigures += '\n' + str(round(flt_NavPerShare, 4)) + ' : Nav per Unit'
        str_resultFigures += '\n' + str(round(flt_aum, 0)) + ' : Asset Under M'
        str_resultFigures += '\n' + str(round(flt_totalShareIssue, 0)) + ' : Total Shares in Issue'
        str_resultFigures += '\n\n' + str(round(int_CreationUnits, 0)) + ' : Basket Creation Issue'
        str_resultFigures += '\n' + str(round(flt_BasketNav, 0)) + ' : Basket NAV'
        str_resultFigures += '\n' + str(round(flt_BasketMarketCap, 0)) + ' : Basket Market Cap'
        str_resultFigures += '\n' + str(round(flt_BasketCash, 0)) + ' : Basket Cash'
        str_resultFigures += '\n' + '------------------------------------------------' 
    except: return 'ERROR: {} - 6. sgx Build the return message'.format(str_PCF), []    
    
    # Close EXCEL
    try:
        inst_xlApp = fl.c_win32_xlApp()
        inst_xlApp.QuitXlApp(bl_force = False)
    except Exception as Err: print('  (*) ERROR: Close EXCEL - {} | {}'.format(str_PCF, str(Err)))
    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________
    








def pcf_SAM_ICE(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_PCF_3175 = dic_df['PCF_3175']
        df_PCF_2812 = dic_df['PCF_2812']        
        str_folder = dic_df['Folder']
    except: return 'ERROR: Dataframe - {}'.format(str_PCF), []
    
    # Other param
    l_pcfFileName = ['DeltaOne.Samsung2.' + dte_date.strftime('%Y%m%d') + '.csv']
    
    #-----------------------------------------
    # PCF_3175 - Input variables
    try:
        flt_NavPerShare = df_PCF_3175.iloc[15, 2]
        str_Isin = df_PCF_3175.iloc[6, 2]
        int_Units = df_PCF_3175.iloc[14, 2]
        flt_Nav = float(flt_NavPerShare) * float(int_Units*1.0)
                
        # Futures row 1
        str_Reuters = df_PCF_3175.iloc[20, 6]
        str_FutName = df_PCF_3175.iloc[20, 1]
        flt_Contracts = df_PCF_3175.iloc[20, 4]
        flt_Price = df_PCF_3175.iloc[20, 3]
        str_Currency = df_PCF_3175.iloc[20, 2]
        
        # Futures row 2
        bl_secondRow = False
        int_nbRow = 1
        str_Reuters_2 = df_PCF_3175.iloc[21, 6]
        if str_Reuters_2:
            try:
                bl_TryNan = np.isnan(str_Reuters_2)
                if not bl_TryNan:
                    #to go to Error in case there is no Error
                    raise            
            except:
                str_FutName_2 = df_PCF_3175.iloc[21, 1]
                flt_Contracts_2 = df_PCF_3175.iloc[21, 4]
                flt_Price_2 = df_PCF_3175.iloc[21, 3]
                bl_secondRow = True
                int_nbRow = 2
    except: 
        print('\n ERROR on the DF: \n')
        print(df_PCF_3175)
        return 'ERROR: PCF_3175 Define variables - {}'.format(str_PCF), []
    
    # PCF_3175 - Building DF
    try:
        df_ICE_3175 = pd.DataFrame(columns = range(0, 13))
        df_ICE_3175.loc[0] = ['15', '3175', str_Isin, dte_date.strftime('%Y%m%d'), str(int_nbRow), 'HKD', 'XHKG', 
                               str(round(flt_NavPerShare, 4)), str(round(flt_Nav, 3)), '+', str(int_Units), '', '']
        df_ICE_3175.loc[1] = ['3', str(str_Reuters), str(str_FutName), 'XNYM', dte_date.strftime('%Y%m%d'), '3175', str_Isin, 
                               str(flt_Contracts), '+', '1000', str(flt_Price), str_Currency, '']
        if bl_secondRow:
            df_ICE_3175.loc[2] = ['3', str(str_Reuters_2), str(str_FutName_2), 'XNYM', dte_date.strftime('%Y%m%d'), '3175', str_Isin, 
                                   str(flt_Contracts_2), '+', '1000', str(flt_Price_2), str_Currency, '']
    except: return 'ERROR: PCF_3175 Build DF - {}'.format(str_PCF), []
    
    
    #-----------------------------------------
    # PCF_2812 - Input variables
    try:
        str_Isin = df_PCF_2812.iloc[6, 2]
        flt_NavPerShare = df_PCF_2812.iloc[15, 2]
        int_Units = df_PCF_2812.iloc[14, 2]
        flt_Cash = abs(df_PCF_2812.iloc[13, 2])
        
        # Take the list in the DF... DELETE the enpty rows
        df_PCF_2812_list = df_PCF_2812.loc[21:].copy()
        df_PCF_2812_list.dropna(axis = 'index', subset = ['Unnamed: 2'], inplace = True)        
        int_nbRow = len(df_PCF_2812_list)
    except: return 'ERROR: PCF_2812 Define variables - {}'.format(str_PCF), []
    
    # PCF_2812 - Building DF 1
    try:
        df_ICE_2812 = pd.DataFrame(columns = range(0, 13))
        df_ICE_2812.loc[0] = ['1', '2812', str_Isin, dte_date.strftime('%Y%m%d'), str(int_nbRow), 'HKD', 'XHKG', 
                                   str(round(flt_NavPerShare, 4)), str(flt_Cash), '+', str(int_Units), '', '']
        
        # ======================= List DF 1 =======================
        # keep only 13 columns 
        df_PCF_2812_list = df_PCF_2812_list.iloc[:, :13]
        # Change column name and re-index to be clearer
        df_PCF_2812_list.columns = df_ICE_2812.columns
            #   df_PCF_2812_list.rename(columns = df_ICE_2812.columns, inplace = True)
        df_PCF_2812_list.reset_index(drop = True, inplace = True)        
    except: return 'ERROR: PCF_2812 Build DF 1 - {}'.format(str_PCF), []
    
    # PCF_2812 - Building DF 2 - Pivot to get Sedol
    try:
        # ======================= Code Pivot =======================
        l_Isin = df_PCF_2812_list[6].tolist()
        df_CP_US = dframe.fDf_GetvwSecL('Code_HKsamsung_US.csv', 1, 'Isin, Ric AS [R2], Sedol AS [S2]', l_Isin)
        l_bbg = df_PCF_2812_list[5].tolist()
        df_CP_China = dframe.fDf_GetvwSecL_NoCase('Code_HKsamsung_Asia.csv', 1, 'Isin, Ric, Sedol AS [S1]', l_bbg)
        df_codePivot = df_CP_US.merge(df_CP_China, on = 'Isin', how = 'left')
        df_codePivot['Sedol'] = df_codePivot['S1'].fillna(df_codePivot['S2'])
        #df_codePivot['Sedol'] = np.where(df_codePivot['S1'].isnull(), df_codePivot['S2'], df_codePivot['S1'])
        df_codePivot.fillna(value = 0, inplace = True)
        df_codePivot = df_codePivot.rename(columns = {'Isin':6})
    except: return 'ERROR: PCF_2812 Build DF - Pivot to get Sedol - {}'.format(str_PCF), []
    
    # PCF_2812 - Building DF 3
    try:
        # ======================= List DF =======================
        # Change the value of entire columns
        df_PCF_2812_list[0] = '2'
        df_PCF_2812_list[7] = ''
        df_PCF_2812_list[8] = '+'
        df_PCF_2812_list.loc[df_PCF_2812_list[4] < 0, 8] = '-'
        df_PCF_2812_list[9] = ''
        df_PCF_2812_list[10] = dte_date.strftime('%Y%m%d')
        df_PCF_2812_list[11] = '2812'
        df_PCF_2812_list[12] = str_Isin
        # Sedol        
        df_PCF_2812_list = df_PCF_2812_list.merge(df_codePivot, on = 6, how = 'left')
        df_PCF_2812_list[5] = df_PCF_2812_list['Sedol']
        df_PCF_2812_list = df_PCF_2812_list.iloc[:, :13]
        
        # Change columns order...
        l_newOrder = [0, 6, 7, 5, 10, 11, 12, 4, 8, 1, 9, 2, 3]
        df_PCF_2812_list = df_PCF_2812_list[df_PCF_2812_list.columns[l_newOrder]]
            #   df_PCF_2812_list = df_PCF_2812_list[['','','','','','','','']]
        #print(df_PCF_2812_list)
        
        # Change column name and re-index to be clearer
        df_PCF_2812_list.columns = df_ICE_2812.columns
        df_PCF_2812_list.reset_index(drop = True, inplace = True)
        # ======================================================
        
        # MERGE
        df_ICE_2812 = df_ICE_2812.append(df_PCF_2812_list)
    except: return 'ERROR: PCF_2812 Build DF 3 - {}'.format(str_PCF), []
    
    #-----------------------------------------
    # Final DF
    try:
        df_ICE = df_ICE_3175.append(df_ICE_2812)
        df_ICE.fillna(value = '', inplace = True)
        str_pathICE = fl.fStr_CreateTxtFile(str_folder, l_pcfFileName[0], df_ICE)
        shutil.copyfile(str_pathICE, str_pathICE.replace('.csv','.tmp'))
        l_pathAttach = [str_pathICE]
        l_pathAttach.append(str_pathICE.replace('.csv','.tmp'))
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except: return 'ERROR: Create Pcf - {}'.format(str_PCF), []
    
    #    # Create tmp file (Dont put it in the return for mail)
    #    try:
    #        for path in l_pathAttach:
    #            shutil.copyfile(str_folderRoot + path, str_folderRoot + path.replace('.csv','.tmp'))
    #    except: return 'ERROR: Create tmp file - {}'.format(str_PCF), []
    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________
    


def pcf_SAM(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_SKCO = dic_df['OUT_SKCO']
        df_HDX = dic_df['SFTP_ParamikoDM1']
        df_HDX_dm2 = dic_df['SFTP_ParamikoDM2']
        df_futCME = dic_df['HTML_JSON']
        df_FX = dic_df['sql_FX']
        df_Ric1 = dic_df['sql_Ric1']
        df_Ric2 = dic_df['sql_Ric2']
        str_folder = dic_df['Folder']
    except: return 'ERROR: Dataframe - {}'.format(str_PCF), []
    
    # Other param
    str_modelfolder = str_folderRoot + 'HK_Samsung\\'
    str_modelFileName = 'SAMSUNG_3175_.xlsx'
    l_pcfFileName = ['SAMSUNG_3175_' + dte_date.strftime('%Y%m%d') + '.xlsx']
    
    # Treat Dataframe to create PCF
    # 1. Variables
    try:
        flt_fx = df_FX[df_FX['ToCurrencyCode'] == 'HKD']['Value'].values[0]
        flt_contractSize = 1000
        flt_mgtFees = 0.996
        
        dte_SKCO = df_SKCO.loc[df_SKCO['PARENT COMPANY'] == 'SKCO', ' VALUATION DATE'].values[0]
        dte_SKCO = pd.to_datetime(dte_SKCO.astype(str))
        str_DateNav = dat.fDat_GetCorrectOffsetDate_Calendar(dte_SKCO, "%m/%d/%Y", 1, '240')
        dte_DateNav = pd.to_datetime(str_DateNav)
        str_hdx = df_HDX.loc[df_HDX['Index Name'] == 'S&P GSCI Crude Oil', 'Date'].values[0]
        dte_hdx = pd.to_datetime(str_hdx)
        dte_DateNav = (max(dte_hdx, dte_DateNav))
        
        flt_NavPerShare = df_SKCO.loc[df_SKCO['PARENT COMPANY'] == 'SKCO', ' NAV/UNIT BEFORE LESS PERFORM FEE'].values[0]
        flt_nbUnitsOutstanding = df_SKCO.loc[df_SKCO['PARENT COMPANY'] == 'SKCO', ' NO OF UNITS O/S'].values[0]
        flt_Units = 250000
        flt_Nav = flt_NavPerShare * flt_Units
        
        flt_ER = df_HDX.loc[df_HDX['Index Code'] == 'SPGSCL', 'ER'].values[0]
        flt_ER_dm2 = df_HDX_dm2.loc[df_HDX['Index Code'] == 'SPGSCL', 'ER'].values[0]
        flt_estimatedNAV = flt_NavPerShare * flt_ER / flt_ER_dm2
        #        global flt_SamsungNAV 
        #        flt_SamsungNAV = flt_estimatedNAV
        
        # RollIn // RollOut
        flt_rollIn, flt_rollOut = pp.f2Flt_rollover(dte_date)
        # Month + 1
        str_fut1 = 'Light Sweet Crude ' + pp.fDte_dateFutures(dte_date, 1)
        try:        str_ric1 = df_Ric1['Ric'].values[0]
        except:     str_ric1 = ''
        try:        flt_price1 = df_futCME.loc[df_futCME['month'] == pp.fDte_dateFutures(dte_date, 1), 'settle'].values[0]
        except:     flt_price1 = 0
        if not  flt_rollIn == 0:
            flt_price1 = float(flt_price1)
            flt_contracts = flt_estimatedNAV * flt_Units * flt_mgtFees / flt_fx / flt_contractSize / flt_price1 * flt_rollIn
            flt_contracts = pp.fFlt_roundDown(flt_contracts, 2)
        else:       flt_contracts = 0
        
        # Month + 2   
        str_ric2 = df_Ric2['Ric'].values[0]
        flt_price2 = df_futCME.loc[df_futCME['month'] == pp.fDte_dateFutures(dte_date, 2), 'settle'].values[0]
        flt_price2 = float(flt_price2)
        str_fut2 = 'Light Sweet Crude ' + pp.fDte_dateFutures(dte_date, 2)
        flt_contracts2 = flt_estimatedNAV * flt_Units * flt_mgtFees / flt_fx / flt_contractSize / flt_price2 * flt_rollOut
        flt_contracts2 = pp.fFlt_roundDown(flt_contracts2, 2)        
        flt_cashHKD = round((flt_estimatedNAV * flt_Units) - flt_fx * 1000 * (flt_price2 * flt_contracts2 +
                      flt_price1 * flt_contracts), 0)
    except: return 'ERROR: 1. Variables - {}'.format(str_PCF), []
    # 2. Change the model file before to copy it
    try:
        shutil.copyfile(str_modelfolder + str_modelFileName, str_folder + l_pcfFileName[0])
        df_result = pd.read_excel(str_folder + l_pcfFileName[0], header = None, index_col = None)
    except: return 'ERROR: 2. Cannot take the model in df - {}'.format(str_PCF), [] 
    # 3. Update the Array
    try:
        df_result.fillna(value = '', inplace = True)
        df_result.loc[3] = ['','Indicative Creation / Redemption basket Composition for trade date', dte_date.strftime('%m/%d/%Y'),'','','','']
        df_result.loc[11] = ['','Nav per Unit ', str(round(flt_NavPerShare, 4)), dte_SKCO.strftime('%m/%d/%Y'),'','','']
        df_result.loc[12] = ['','Number of Units Outstanding', str(flt_nbUnitsOutstanding),'','','','']
        df_result.loc[13] = ['','Nav per Application Unit size (HKD)', str(round(flt_Nav, 0)),'','','','']
        df_result.loc[14] = ['','Estimated Cash Amount for Application (HKD)', str(round(flt_Nav, 0)),'','','','']
        df_result.loc[15] = ['','Application Size(Units/Application size)', str(flt_Units),'','','','']
        df_result.loc[16] = ['','Estimated NAV** (Reference purpose only)', str(flt_estimatedNAV), dte_DateNav.strftime('%m/%d/%Y'),'','','']
        df_result.loc[17] = ['','Cash (HKD)', str(flt_cashHKD),'','','','']
        df_result.loc[21] = ['1', str_fut2, 'USD', flt_price2, round(flt_contracts2,2), str_ric2, str_ric2]
        df_result.loc[22] = ['2', str_fut1, 'USD', flt_price1, round(flt_contracts,2), str_ric1, str_ric1]
    except: return 'ERROR: 3. Update the Array - {}'.format(str_PCF), [] 
    # 5.Create Pcf as a txt file and xls file with some important point to show caculation
    try:
        # Delete the Row of Futures if Contracts = 0
        if flt_rollIn == 0:
            print(' RollIn = 0')
            df_result.drop(df_result.index[range(22, 23)], inplace = True)
            df_result.reset_index(drop = True, inplace = True)
            str_pathAttach = fl.fStr_fillXls_celByCel(str_folder + l_pcfFileName[0], df_result,'',0, -1, 22)
            l_pathAttach = [str_pathAttach]
            #l_pathAttach = pp.fL_fillExcel_RetunPath(str_folder, l_pcfFileName, df_result, False, True, -1, 22)
        elif flt_rollOut == 0:
            print(' RollOut = 0')
            # Delete 1ere row donc on met '1' sur la deuxieme ligne
            df_result.loc[22] = ['1', str_fut1, 'USD', flt_price1, round(flt_contracts,2), str_ric1, str_ric1]
            df_result.drop(df_result.index[range(21, 22)], inplace = True)
            df_result.reset_index(drop = True, inplace = True)
            str_pathAttach = fl.fStr_fillXls_celByCel(str_folder + l_pcfFileName[0], df_result,'',0, -1, 21)
            l_pathAttach = [str_pathAttach]
            #l_pathAttach = pp.fL_fillExcel_RetunPath(str_folder, l_pcfFileName, df_result, False, True, -1, 21)
        else:
            str_pathAttach = fl.fStr_fillXls_celByCel(str_folder + l_pcfFileName[0], df_result)
            l_pathAttach = [str_pathAttach]
        if not l_pathAttach: return 'ERROR: SAMSUNG - Could not create the PCF', []
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except: return 'ERROR: 5.Create Pcf - {}'.format(str_PCF), [] 
    # 6. Build the return message
    try:
        str_resultFigures += '\n' + str(round(flt_NavPerShare, 4)) + '         Nav per Unit'
        str_resultFigures += '\n' + str(flt_nbUnitsOutstanding) + '   Number of Units Outstanding'
        str_resultFigures += '\n' + str(round(flt_Nav, 0)) + '     Nav per Application Unit size (HKD)'
        str_resultFigures += '\n' + str(flt_Units) + '          Application Size(Units/Application size)'
        str_resultFigures += '\n' + str(round(flt_estimatedNAV,4)) + '         Estimated NAV** (Reference purpose only)'
        str_resultFigures += '\n' + str(flt_cashHKD) + '         Cash (HKD)'
        str_resultFigures += '\n' + '------------------------------------------------' 
    except: return 'ERROR: 6. Build the return message - {}'.format(str_PCF), [] 
        
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________






#------------------------------------------------------------------------------
# SINAGPORE
#------------------------------------------------------------------------------
def pcf_Amundi(str_folderRoot, dte_date, str_resultFigures, dic_df):
    l_pathAttach = dic_df['files']
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________


def pcf_AmundiBeta(str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Name of the PCF
    l_pcfFileName = ['PCFMKTN.' + dte_date.strftime('%Y%m%d')  + '.txt']
    
    # 0. Dataframe
    try:
        df_NAVFILE = dic_df['FOLDER_NAVFILE']
        str_folder = dic_df['Folder'] 
    except: return 'ERROR: AMUNDI_BETA - 0. Dataframe', []
    
    # Get SQL
    try:
        str_futuresDate_dm1 = (dte_date-BDay(1)).strftime("%d.%m.%Y")
        df_futures = pp.fDf_getFut_inDb(str_futuresDate_dm1)
        #HOLCAL = mReq.fDf_GetHoliday()
        ISEXMETN = pp.fDf_GetPosition('.ISEXMETN')
        ISEXFER = pp.fDf_GetPosition('.ISEXFER')
        SXXPFEER = pp.fDf_GetPosition('.SXXPFEER')
        ISEXFERCON = pp.fDf_GetComposition('.ISEXFER', dte_date.strftime("%Y-%m-%d"))
        BETA = pp.fDf_GetBeta(2725604)
        CREATIONUNIT = pp.fDf_GetCreationUnit('720273')
        FEES_SPREAD = pp.fDf_GetFeesSpread('720273')
    except: return 'ERROR: AMUNDI_BETA - SQL request', []
    
    #Treat Dataframe to create PCF
    # 1. Variables
    try:
        int_weekDay = dte_date.weekday()
        dte_lastFriday = dat.fDte_formatToDate(dat.fDte_lastFriday(dte_date), '%Y-%m-%d')
        str_dteYesterday = (dte_date-BDay(1)).strftime("%Y-%m-%d")
        RollOverWeek = pp.fBl_RollOverWeek(dte_date)
        futuresvalue = df_futures['Column5'].iloc[0]
        futuresvalue2 = df_futures['Column6'].iloc[0]
        Future1Percentage = float(df_futures['Column7'].iloc[0])
        FuturesCode = df_futures['Column9'].iloc[0]
        FuturesCode2 = df_futures['Column10'].iloc[0]
        # Get the code
        FutureCode, futmonth, futyear, Future1Percentage = pp.fFl_getFutCode(int_weekDay, False, FuturesCode, FuturesCode2, 
                                                                             Future1Percentage, futuresvalue2)
        FutureCode2,futmonth2,futyear2,Future1Percentage = pp.fFl_getFutCode(int_weekDay, RollOverWeek, FuturesCode, FuturesCode2, 
                                                                             Future1Percentage, futuresvalue2)
        futuresvalue, futuresvalue2 = pp.fFl_getFutValue(futuresvalue, futuresvalue2, RollOverWeek, int_weekDay, FutureCode2, 
                                                         str_dteYesterday, Future1Percentage)
        CU = int(CREATIONUNIT['Value'].iloc[0])
        SwapSpread = round(FEES_SPREAD['DailySwapRate'].iloc[0] * 10000 * 365)
        ManagementFees = round(FEES_SPREAD['AnnualManagementFeeRate'].iloc[0] * 10000)
        AUM = df_NAVFILE.loc[df_NAVFILE['ISIN'] == 'FR0013284304', 'AUM'].iloc[0]
        SharesOutstanding = df_NAVFILE.loc[df_NAVFILE['ISIN'] == 'FR0013284304', 'Nombre de Parts'].iloc[0]
        NAV = AUM / SharesOutstanding
        NAVCU = NAV * CU
        FridayBenchPerformance = (ISEXMETN.loc[ISEXMETN['AsAtDate'] == str(dte_lastFriday), 'Value'].iloc[0] /
        							  ISEXMETN.loc[ISEXMETN['AsAtDate'] == str(dte_lastFriday), 'Value'].iloc[0]) - 1        
        FridayiMTMLong = NAVCU * (1 + FridayBenchPerformance)
        Fridaybeta = BETA.loc[BETA['AsAtDate'] == str(dte_lastFriday), 'Value'].iloc[0]
        FridayiMTMShort = FridayiMTMLong * Fridaybeta
        
        if int_weekDay == 0:
            iMTMShort = FridayiMTMShort
            fees = NAVCU * (1 + FridayBenchPerformance) * ((SwapSpread + ManagementFees) / 10000) / 365
            iNAVCU = FridayiMTMLong - fees
            iNAV = iNAVCU / CU
            EstCash = -fees
        else:	# REST OF THE WEEK
            LongPerformance = (ISEXFER.loc[ISEXFER['AsAtDate'] == str_dteYesterday, 'Value'].iloc[0] /
                                           ISEXFER.loc[ISEXFER['AsAtDate'] == str(dte_lastFriday), 'Value'].iloc[0]) - 1    
            TodayBenchPerformancce = (ISEXMETN.loc[ISEXMETN['AsAtDate'] == str_dteYesterday, 'Value'].iloc[0] /
                                                   ISEXMETN.loc[ISEXMETN['AsAtDate'] == str(dte_lastFriday), 'Value'].iloc[0]) - 1
            ShortPerformance = (SXXPFEER.loc[SXXPFEER['AsAtDate'] == str_dteYesterday, 'Value'].iloc[0] /
                                             SXXPFEER.loc[SXXPFEER['AsAtDate'] == str(dte_lastFriday), 'Value'].iloc[0]) - 1
            iMTMLong = FridayiMTMLong * (1 + LongPerformance)
            fees = NAVCU * (1 + TodayBenchPerformancce) * ((SwapSpread + ManagementFees) / 10000) / 365
            iMTMShort = FridayiMTMShort * (1 + ShortPerformance)
            iNAVCU = iMTMLong - fees - (iMTMShort - FridayiMTMShort)
            iNAV = iNAVCU / CU
            EstCash = -fees - (iMTMShort - FridayiMTMShort)
    except: return 'ERROR: AMUNDI_BETA - 1. Variables', []
    # 2. Df
    try:
        PCFFuture = pd.DataFrame(columns=range(0, 30))
        PCFIndex = pd.DataFrame(columns=range(0, 30))
        PCFFuture.loc[0] = ['B', 'FR0013284304', 'Future', '-', '-', FutureCode, '', 'Future Stoxx 600 ' + futmonth + " " + futyear, 
                     - iMTMShort * Future1Percentage / futuresvalue / 50, '-', '-', 1, futuresvalue, 1, 'T', 'FR0013284304', 
                     '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        if (RollOverWeek and int_weekDay > 0):
            PCFFuture.loc[1] = ['B', 'FR0013284304', 'Future', '-', '-',FutureCode2, '', 'Future Stoxx 600 ' + futmonth2 + " " + futyear2, 
                         - iMTMShort * (1- Future1Percentage) / futuresvalue2 / 50, '-', '-', 2, futuresvalue2, 1, 'T','FR0013284304',
                         '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    except: return 'ERROR: AMUNDI_BETA - 2. Df -- A', []
    try:
        PCFIndex[3] = ISEXFERCON['Isin']
        PCFIndex[0] = 'B'
        PCFIndex[1] = 'FR0013284304'
        PCFIndex[2] = 'Equity'
        PCFIndex[4] = ISEXFERCON['Ric']
        PCFIndex[5] = ISEXFERCON['Bloomberg']
        PCFIndex[6] = ''
        PCFIndex[7] = ISEXFERCON['SecurityName'].str[:30]
        PCFIndex[8] = (iMTMLong * ISEXFERCON['PctWeight'] / ISEXFERCON['Price'] / ISEXFERCON['FXRate'] / 1).astype(str).str[:11]
        PCFIndex[9] = '-'
        PCFIndex[10] = '-'
        PCFIndex[11] = PCFIndex.index + 2
        PCFIndex[12] = ISEXFERCON['Price']
        PCFIndex[13] = ISEXFERCON['FXRate']
        PCFIndex[14] = 'T'
        PCFIndex[15] = 'FR0013284304'
    except: return 'ERROR: AMUNDI_BETA - 2. Df -- B', []
    # 3. Add rows of title
    try:
        # MERGE Future & Equity
        PCFCon = PCFFuture.append(PCFIndex)
        # HEADER LEVEL
        PCFHeader = pd.DataFrame(columns=range(0, 30))
        PCFHeader.loc[0] = ['H', 'NSCFR0IMKTN4', 'DV', "%.0f" % PCFCon[0].count(), '1', dte_date.strftime('%Y%m%d'), 
                          (dte_date-BDay(1)).strftime("%Y%m%d"), round(iNAV, 4), '-', '-',round(EstCash / CU, 14), 
                          '-',"%.0f" % SharesOutstanding, round(SharesOutstanding * iNAV, 2), "%.0f" % CU, 'EUR','EUR', 
                          'EUR', 'FR0013284304', 'MKTN.PA', 'MKTN FP','.ISEXMETN', 'IMKTN', '-', '-', '-', '-', '-', '-', 
                          ISEXMETN.loc[ISEXMETN['AsAtDate'] == str(str_dteYesterday), 'Value'].iloc[0]]
    except: return 'ERROR: AMUNDI_BETA - 3. Add rows of title', []
    # 4. FINAL OUTPUT
    try:
        PCFFinal = PCFHeader.append(PCFCon)
    except: return 'ERROR: AMUNDI_BETA - 4. FINAL OUTPUT', []
    # 5.Create Pcf as a txt file and xls file with some important point to show caculation
    try:
        print(l_pcfFileName)
        l_pathAttach = pp.fL_CreateTxtFile_RetunPath(str_folder, l_pcfFileName, PCFFinal)
        if not l_pathAttach: return 'ERROR: Could not create the PCF AMUNDI_BETA', []
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except: return 'ERROR: AMUNDI_BETA - 5.Create Pcf', []
    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________












#====================================================================================================
# DEPRECATED
#====================================================================================================
