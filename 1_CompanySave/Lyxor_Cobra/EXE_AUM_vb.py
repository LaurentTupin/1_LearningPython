
import pyodbc
import pandas as pd
import numpy as np
import math
import datetime as dt
import sys
sys.path.append("C:\Users\laurent.tupin\Documents\0. Personal\Apprendre les Programmes\Python\Lyxor - Cobra\Fonction\\")
import fct_Date as fDate
import fct_StaticInfo as fStat
import fct_HistoricData as fData
import fct_ExcelSave as fXls


server = 'SRVCLDDFXP004\MSPARDFXP02'
db1 = 'ETF_DW'
fileFolder = 'C:\Users\laurent.tupin\Documents\0. Personal\Apprendre les Programmes\Python\Lyxor - Cobra\\'
navType = 'OFFICIAL'
shOutType = 'OFFICIAL'
divType = 'OFFICIAL'
str_etf = "'All_Lyxor'"

date_from = ''
date_to = ''


# server = 'SRVCLDDFXP004\MSPARDFXP02'
# db1 = 'ETF_DW'
# navType = 'OFFICIAL'
# shOutType = 'OFFICIAL'
# divType = 'OFFICIAL'
# date_from = '11/30/2016'
# date_to = '12/30/2016'
# fileFolder = 'F:\LYXOR-ETF-BIU\REPORTS\LYXOR\ETF_Python\\'


#Traitement Date
date_from = date_from[6:] + '-' + date_from[:2] + '-' + date_from[3:5]
date_to = date_to[6:] + '-' + date_to[:2] + '-' + date_to[3:5]

#Liste Isin
if 'all' in str_etf.lower():
    if 'lyxor' in str_etf.lower():
        all_isin = fStat.getLyxorEtf(date_from, date_to)
else:
    all_isin = fStat.getListEtf(str_etf)

all_etf_details = pd.DataFrame()
all_etf_synth = pd.DataFrame()
for i, etf_isin in all_isin['ISIN'].iteritems():
    str_date_isin_end = fDate.getIsinEndDate(etf_isin)
    str_date_isin_start = fDate.getIsinStartDate(etf_isin)
    if date_from < str_date_isin_end and date_to > str_date_isin_start:
        etf_details = fData.getAumMatrixByIsin(etf_isin, date_from, date_to, navType, shOutType)
        etf_synth = fData.getAumSynthByIsin(etf_details, date_from, date_to)
        print etf_synth
        all_etf_details = all_etf_details.append(etf_details)
        all_etf_synth = all_etf_synth.append(etf_synth)

fXls.printAllEtfAum(fileFolder, 'ETF_AUM_' + str(date_to) + '.xlsx', all_etf_details, all_etf_synth)

