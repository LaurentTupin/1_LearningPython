import pyodbc
import pandas as pd
import numpy as np
import math
import datetime as dt
import fct_Date as fDate
import fct_StaticInfo as fStat
import fct_HistoricData as fData
import fct_ExcelSave as fXls

server = 'SRVCLDDFXP004\MSPARDFXP02'
db1 = 'ETF_DW'


def addUpdateAnalysisInDb(all_etf, periodType):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()

    for i, d_param in all_etf.iterrows():
        perfQuery = ("EXEC Mkt_Perf_AddUpdate '" + d_param['FROM'] + "' "
					", '" + d_param['TO'] + "' "
					", '" + periodType + "' "
					", '" + d_param['PERIOD FROM'] + "' "
					", '" + d_param['PERIOD TO'] + "' "
					", '" + d_param['ISIN'] + "' " +
					(", NULL" if d_param['LAST BENCH'] == '' else ", '" + d_param['LAST BENCH'] + "' ") +
					", 'REAL' "
					", '" + d_param['CCY'] + "' " +
					(", NULL" if np.isnan(d_param['ETF PERF']) else ", " + str(d_param['ETF PERF']) + " ") +
					(", NULL" if np.isnan(d_param['IDX PERF']) else ", " + str(d_param['IDX PERF']) + " ") +
					(", NULL" if np.isnan(d_param['ETF TD']) else ", " + str(d_param['ETF TD']) + " ") +
					(", NULL" if np.isnan(d_param['ETF TE']) else ", " + str(d_param['ETF TE']) + " ") +
					(", NULL" if np.isnan(d_param['ETF TE FILTERED 2STDEV']) else ", " + str(d_param['ETF TE FILTERED 2STDEV']) + " ") +
					(", NULL" if np.isnan(d_param['ETF YIELD']) else ", " + str(d_param['ETF YIELD']) + " ") +
					(", NULL" if np.isnan(d_param['ETF VOL']) else ", " + str(d_param['ETF VOL']) + " ") +
					(", NULL" if np.isnan(d_param['IDX VOL']) else ", " + str(d_param['IDX VOL']) + " ") +
					(", NULL" if np.isnan(d_param['NB ETF POINT']) else ", " + str(d_param['NB ETF POINT']) + " ") +
					(", NULL" if np.isnan(d_param['NB IDX POINT']) else ", " + str(d_param['NB IDX POINT']) + " ") +
					(", NULL" if np.isnan(d_param['AVG SPREAD']) else ", " + str(d_param['AVG SPREAD']) + " ") +
					(", NULL" if np.isnan(d_param['ADV']) else ", " + str(d_param['ADV']) + " "))
        print perfQuery
        cursor.execute(perfQuery)
        cursor.commit()


def addUpdateAnalysisInDb_Index(all_index, periodType):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()

    for i, d_param in all_index.iterrows():
        perfQuery = ("EXEC Mkt_PerfIndex_AddUpdate '" + d_param['FROM'] + "', '" +
                     d_param['TO'] + "', '" +
                     periodType + "', '" +
                     d_param['PERIOD FROM'] + "', '" +
                     d_param['PERIOD TO'] + "', '" +
                     d_param['INDEX'] + "', '" +
                     d_param['CCY'] + "' " +
                     (", NULL" if np.isnan(d_param['IDX PERF']) else ", " + str(d_param['IDX PERF']) + " ") +
                     (", NULL" if np.isnan(d_param['IDX VOL']) else ", " + str(d_param['IDX VOL']) + " ") +
                     (", NULL" if np.isnan(d_param['NB IDX POINT']) else ", " + str(d_param['NB IDX POINT']) + " "))
        print perfQuery
        cursor.execute(perfQuery)
        cursor.commit()


def getAllAnalysisByIssuer(date_from, date_to, issuer, refCcy, generateFile):
    all_isin = fStat.getAllEtf(date_from, date_to, issuer)
    all_etf = pd.DataFrame(columns=['NAME', 'ISIN', 'CCY', 'FROM', 'TO', 'PERIOD FROM', 'PERIOD TO', 'LAST BENCH', 'ETF YIELD', 'ETF PERF', 'IDX PERF', 'ETF TD', 'ETF TE', 'ETF TE FILTERED 2STDEV', 'ETF VOL', 'IDX VOL', 'LAST NAV', 'DIV', 'TER', 'ADV', 'AVG SPREAD', 'NB ETF POINT', 'NB IDX POINT'])
    for i, etf_isin in all_isin['ISIN'].iteritems():
        if refCcy == 'CCY':
            navCcy = fStat.getIsinNavCcy(etf_isin)
        else:
            navCcy = refCcy

        print etf_isin
        if issuer == 'LYXOR':
            etf_analysis = fXls.getAnalysisSynthesis(etf_isin, date_from, date_to, navCcy, 'OFFICIAL', 'OFFICIAL', 'BLOOMBERG', 'BLOOMBERG', 'HID_1ST_LIM', generateFile, 'F:\LYXOR-ETF-BIU\PERSONAL\BouLy\BIU_Check\Analysis\\')
        else:
            etf_analysis = fXls.getAnalysisSynthesis(etf_isin, date_from, date_to, navCcy, 'BLOOMBERG', 'BLOOMBERG', 'BLOOMBERG', 'BLOOMBERG', 'HID_1ST_LIM', generateFile, 'F:\LYXOR-ETF-BIU\PERSONAL\BouLy\BIU_Check\Analysis\\')

        # all_etf.loc[len(all_etf)+1] = etf_analysis
        # all_etf = all_etf.append(pd.DataFrame.from_dict(etf_analysis, 'index'), ignore_index=True)

        #Test si la ligne est vide
        if etf_analysis:
            all_etf.loc[len(all_etf)+1] = [etf_analysis[etf_isin]['isinName'], etf_analysis[etf_isin]['isin'], etf_analysis[etf_isin]['refCcy'],
                                       etf_analysis[etf_isin]['dateFrom'], etf_analysis[etf_isin]['dateTo'], etf_analysis[etf_isin]['periodFrom'], etf_analysis[etf_isin]['periodTo'],
                                       etf_analysis[etf_isin]['etfLastBench'], etf_analysis[etf_isin]['etfYield'], etf_analysis[etf_isin]['etfPerf'], etf_analysis[etf_isin]['idxPerf'],
                                       etf_analysis[etf_isin]['etfTd'], etf_analysis[etf_isin]['etfTe'], etf_analysis[etf_isin]['etfTeF2StDev'],
                                       etf_analysis[etf_isin]['etfVol'], etf_analysis[etf_isin]['idxVol'], etf_analysis[etf_isin]['etfLastNav'], etf_analysis[etf_isin]['etfDiv'], etf_analysis[etf_isin]['etfTer'],
                                       etf_analysis[etf_isin]['etfAdv'], etf_analysis[etf_isin]['etfAvgSpread'], etf_analysis[etf_isin]['nbEtfPoint'], etf_analysis[etf_isin]['nbIdxPoint']]


    print all_etf
    #Si tous les ETF sont vide
    if all_etf.empty:
        return

    if int(date_to[:4]) - int(date_from[:4]) == 1 and int(date_from[5:7]) == 12 and int(date_to[5:7]) != 12:
        periodType = 'YTD_' + refCcy
    elif int(date_to[:4]) - int(date_from[:4]) == 0 and int(date_from[5:7]) != int(date_to[5:7]):
        periodType = str(int(date_to[5:7]) - int(date_from[5:7])) + 'M_' + refCcy
    elif (int(date_to[:4]) - int(date_from[:4])) == 1 and (int(date_to[5:7]) != int(date_from[5:7])):
        periodType = str(int(date_to[5:7]) + 12 - int(date_from[5:7])) + 'M_' + refCcy
    elif int(date_to[:4]) - int(date_from[:4]) >= 1 and int(date_from[5:7]) == int(date_to[5:7]):
        periodType = str(int(date_to[:4]) - int(date_from[:4])) + 'Y_' + refCcy
    else:
        periodType = 'XXX_' + refCcy

    addUpdateAnalysisInDb(all_etf, periodType)

    # Creer un fichier recap si on met True
    if generateFile.lower() == 'true':
        fXls.printAllEtf('F:\LYXOR-ETF-BIU\PERSONAL\BouLy\BIU_Check\\', 'ETF_Analysis_' + str(date_from) + '_' + str(date_to) + '_' + issuer + '_' + refCcy + '.xlsx', all_etf)

    # Month also YTD
    if int(date_to[:4]) - int(date_from[:4]) == 1 and int(date_from[5:7]) == 12 and (int(date_to[5:7]) == 1 or int(date_to[5:7]) == 3 or int(date_to[5:7]) == 6):
        periodType = str(int(date_to[5:7])) + 'M_' + refCcy
        addUpdateAnalysisInDb(all_etf, periodType)
    # YTD also 1Y
    if int(date_to[:4]) - int(date_from[:4]) == 1 and int(date_from[5:7]) == 12 and int(date_to[5:7]) == 12:
        periodType = 'YTD_' + refCcy
        addUpdateAnalysisInDb(all_etf, periodType)


def getAllAnalysisByIsin(date_from, date_to, refCcy, etf_isin, generateFile):
    all_etf = pd.DataFrame(columns=['NAME', 'ISIN', 'CCY', 'FROM', 'TO', 'PERIOD FROM', 'PERIOD TO', 'LAST BENCH', 'ETF YIELD', 'ETF PERF', 'IDX PERF', 'ETF TD', 'ETF TE', 'ETF TE FILTERED 2STDEV', 'ETF VOL', 'IDX VOL', 'LAST NAV', 'DIV', 'TER', 'ADV', 'AVG SPREAD', 'NB ETF POINT', 'NB IDX POINT'])

    issuer = fStat.getDataFromIsin(etf_isin, 'str_Issuer')
    print etf_isin + ' : ' + issuer

    if refCcy == 'CCY':
        navCcy = fStat.getIsinNavCcy(etf_isin)
    else:
        navCcy = refCcy

    if issuer == 'LYXOR':
        etf_analysis = fXls.getAnalysisSynthesis(etf_isin, date_from, date_to, navCcy, 'OFFICIAL', 'OFFICIAL', 'BLOOMBERG', 'BLOOMBERG', 'HID_1ST_LIM', generateFile, 'F:\LYXOR-ETF-BIU\PERSONAL\BouLy\BIU_Check\Analysis\\')
    else:
        etf_analysis = fXls.getAnalysisSynthesis(etf_isin, date_from, date_to, navCcy, 'BLOOMBERG', 'BLOOMBERG', 'BLOOMBERG', 'BLOOMBERG', 'HID_1ST_LIM', generateFile, 'F:\LYXOR-ETF-BIU\PERSONAL\BouLy\BIU_Check\Analysis\\')

    #Test si la ligne est vide
    if etf_analysis:
        all_etf.loc[len(all_etf)+1] = [etf_analysis[etf_isin]['isinName'], etf_analysis[etf_isin]['isin'], etf_analysis[etf_isin]['refCcy'],
                               etf_analysis[etf_isin]['dateFrom'], etf_analysis[etf_isin]['dateTo'], etf_analysis[etf_isin]['periodFrom'], etf_analysis[etf_isin]['periodTo'],
                               etf_analysis[etf_isin]['etfLastBench'], etf_analysis[etf_isin]['etfYield'], etf_analysis[etf_isin]['etfPerf'], etf_analysis[etf_isin]['idxPerf'],
                               etf_analysis[etf_isin]['etfTd'], etf_analysis[etf_isin]['etfTe'], etf_analysis[etf_isin]['etfTeF2StDev'],
                               etf_analysis[etf_isin]['etfVol'], etf_analysis[etf_isin]['idxVol'], etf_analysis[etf_isin]['etfLastNav'], etf_analysis[etf_isin]['etfDiv'], etf_analysis[etf_isin]['etfTer'],
                               etf_analysis[etf_isin]['etfAdv'], etf_analysis[etf_isin]['etfAvgSpread'], etf_analysis[etf_isin]['nbEtfPoint'], etf_analysis[etf_isin]['nbIdxPoint']]

    print all_etf
    #Si tous les ETF sont vide
    if all_etf.empty:
        return

    print all_etf

    if int(date_to[:4]) - int(date_from[:4]) == 1 and int(date_from[5:7]) == 12 and int(date_to[5:7]) != 12:
        periodType = 'YTD_' + refCcy
    elif int(date_to[:4]) - int(date_from[:4]) == 0 and int(date_from[5:7]) != int(date_to[5:7]):
        periodType = str(int(date_to[5:7]) - int(date_from[5:7])) + 'M_' + refCcy
    elif (int(date_to[:4]) - int(date_from[:4])) == 1 and (int(date_to[5:7]) != int(date_from[5:7])):
        periodType = str(int(date_to[5:7]) + 12 - int(date_from[5:7])) + 'M_' + refCcy
    elif int(date_to[:4]) - int(date_from[:4]) >= 1 and int(date_from[5:7]) == int(date_to[5:7]):
        periodType = str(int(date_to[:4]) - int(date_from[:4])) + 'Y_' + refCcy
    else:
        periodType = 'XXX_' + refCcy

    addUpdateAnalysisInDb(all_etf, periodType)

    # Creer un fichier recap si on met True
    if generateFile.lower() == 'true':
        fXls.printAllEtf('F:\LYXOR-ETF-BIU\PERSONAL\BouLy\BIU_Check\\', 'ETF_Analysis_' + str(date_from) + '_' + str(date_to) + '_' + issuer + '_' + refCcy + '.xlsx', all_etf)

    # Month also YTD
    if int(date_to[:4]) - int(date_from[:4]) == 1 and int(date_from[5:7]) == 12 and (int(date_to[5:7]) == 1 or int(date_to[5:7]) == 3 or int(date_to[5:7]) == 6):
        periodType = str(int(date_to[5:7])) + 'M_' + refCcy
        addUpdateAnalysisInDb(all_etf, periodType)
    # YTD also 1Y
    if int(date_to[:4]) - int(date_from[:4]) == 1 and int(date_from[5:7]) == 12 and int(date_to[5:7]) == 12:
        periodType = 'YTD_' + refCcy
        addUpdateAnalysisInDb(all_etf, periodType)


def getAllAnalysisByIndex(date_from, date_to, refCcy, generateFile):
    # --------------------------
    all_indexTracked = fStat.getAllIndex(date_from, date_to)
    all_index = pd.DataFrame(columns=['INDEX', 'CCY', 'FROM', 'TO', 'PERIOD FROM', 'PERIOD TO', 'IDX PERF', 'IDX VOL', 'NB IDX POINT'])

    # --------------------------
    for i, index_bbg in all_indexTracked['INDEX'].iteritems():
        #*****
        if refCcy == 'CCY':
            IndexCcy = fStat.getIndexCcy(index_bbg)
        else:
            IndexCcy = refCcy
        #*****
        index_analysis = fXls.getAnalysisSynthesisIndex(index_bbg, date_from, date_to, IndexCcy, 'BLOOMBERG', generateFile,
                                                        'F:\LYXOR-ETF-BIU\PERSONAL\BouLy\BIU_Check\Analysis\\')

        #Test si la ligne est vide
        if index_analysis:
            all_index.loc[len(all_index)+1] = [index_analysis[index_bbg]['indexBloom'], index_analysis[index_bbg]['refCcy'],
                                               index_analysis[index_bbg]['dateFrom'], index_analysis[index_bbg]['dateTo'],
                                               index_analysis[index_bbg]['periodFrom'], index_analysis[index_bbg]['periodTo'],
                                               index_analysis[index_bbg]['idxPerf'], index_analysis[index_bbg]['idxVol'],
                                               index_analysis[index_bbg]['nbIdxPoint']]
    # --------------------------

    #Si tous les ETF sont vide
    if all_index.empty:
        return 'No Index : empty'
    else:
        print all_index

    # Traitement Date
    # Mois
    if int(date_to[:4]) - int(date_from[:4]) == 0 and int(date_from[5:7]) != int(date_to[5:7]):
        periodType = str(int(date_to[5:7]) - int(date_from[5:7])) + 'M_' + refCcy
    #Mois
    elif (int(date_to[:4]) - int(date_from[:4])) == 1 and (int(date_to[5:7]) != int(date_from[5:7])):
        periodType = str(int(date_to[5:7]) + 12 - int(date_from[5:7])) + 'M_' + refCcy
    #Annee
    elif int(date_to[:4]) - int(date_from[:4]) >= 1 and int(date_from[5:7]) == int(date_to[5:7]):
        periodType = str(int(date_to[:4]) - int(date_from[:4])) + 'Y_' + refCcy
    #YTD
    elif int(date_to[:4]) - int(date_from[:4]) == 1 and int(date_from[5:7]) == 12 and int(date_to[5:7]) != 12:
        periodType = 'YTD_' + refCcy
    else:
        periodType = 'XXX_' + refCcy

    addUpdateAnalysisInDb_Index(all_index, periodType)

    # YTD inclus in YEAR or MONTH
    if int(date_to[:4]) - int(date_from[:4]) == 1 and int(date_from[5:7]) == 12:
        periodType = 'YTD_' + refCcy
        addUpdateAnalysisInDb_Index(all_index, periodType)

    # Creer un fichier recap si on met True
    if generateFile.lower() == 'true':
        fXls.printAllEtf('F:\LYXOR-ETF-BIU\PERSONAL\BouLy\BIU_Check\\', 'index_analysis_' + str(date_from) + '_' + str(date_to) + '_' + refCcy + '.xlsx', all_index)



def getAllAnalysisByIndex_Ticker(date_from, date_to, refCcy, index_bbg, generateFile):
    all_index = pd.DataFrame(columns=['INDEX', 'CCY', 'FROM', 'TO', 'PERIOD FROM', 'PERIOD TO', 'IDX PERF', 'IDX VOL', 'NB IDX POINT'])

    if refCcy == 'CCY':
        IndexCcy = fStat.getIndexCcy(index_bbg)
    else:
        IndexCcy = refCcy
    #*****
    index_analysis = fXls.getAnalysisSynthesisIndex(index_bbg, date_from, date_to, IndexCcy, 'BLOOMBERG', generateFile,
                                                    'F:\LYXOR-ETF-BIU\PERSONAL\BouLy\BIU_Check\Analysis\\')

    #Test si la ligne est vide
    if index_analysis:
        all_index.loc[len(all_index)+1] = [index_analysis[index_bbg]['indexBloom'], index_analysis[index_bbg]['refCcy'],
                                           index_analysis[index_bbg]['dateFrom'], index_analysis[index_bbg]['dateTo'],
                                           index_analysis[index_bbg]['periodFrom'], index_analysis[index_bbg]['periodTo'],
                                           index_analysis[index_bbg]['idxPerf'], index_analysis[index_bbg]['idxVol'],
                                           index_analysis[index_bbg]['nbIdxPoint']]
    # --------------------------

    #Si tous les ETF sont vide
    if all_index.empty:
        return 'No Index : empty'
    else:
        print all_index

    # Traitement Date
    # Mois
    if int(date_to[:4]) - int(date_from[:4]) == 0 and int(date_from[5:7]) != int(date_to[5:7]):
        periodType = str(int(date_to[5:7]) - int(date_from[5:7])) + 'M_' + refCcy
    #Mois
    elif (int(date_to[:4]) - int(date_from[:4])) == 1 and (int(date_to[5:7]) != int(date_from[5:7])):
        periodType = str(int(date_to[5:7]) + 12 - int(date_from[5:7])) + 'M_' + refCcy
    #Annee
    elif int(date_to[:4]) - int(date_from[:4]) >= 1 and int(date_from[5:7]) == int(date_to[5:7]):
        periodType = str(int(date_to[:4]) - int(date_from[:4])) + 'Y_' + refCcy
    #YTD
    elif int(date_to[:4]) - int(date_from[:4]) == 1 and int(date_from[5:7]) == 12 and int(date_to[5:7]) != 12:
        periodType = 'YTD_' + refCcy
    else:
        periodType = 'XXX_' + refCcy

    addUpdateAnalysisInDb_Index(all_index, periodType)

    # YTD inclus in YEAR or MONTH
    if int(date_to[:4]) - int(date_from[:4]) == 1 and int(date_from[5:7]) == 12:
        periodType = 'YTD_' + refCcy
        addUpdateAnalysisInDb_Index(all_index, periodType)

    # Creer un fichier recap si on met True
    if generateFile.lower() == 'true':
        fXls.printAllEtf('F:\LYXOR-ETF-BIU\PERSONAL\BouLy\BIU_Check\\', 'index_analysis_' + str(date_from) + '_' + str(date_to) + '_' + refCcy + '.xlsx', all_index)





