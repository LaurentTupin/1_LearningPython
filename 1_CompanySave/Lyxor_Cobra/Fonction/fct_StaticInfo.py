import pyodbc
import pandas as pd
import numpy as np
import math
import datetime as dt

server = 'SRVCLDDFXP004\MSPARDFXP02'
db1 = 'ETF_DW'


def getIsinName(isin):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP 1 str_IsinLongName "
                   "FROM V_Ref_FundIsinPListing "
                   "WHERE str_Isin = '" + isin + "' ")
    extract = pd.DataFrame.from_records(cursor.fetchall(), columns=['NAME'])
    name = str(extract.head(1)['NAME'].iloc[0])

    return name

def getIndexTracked(isin, date_ref):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT ISNULL(V.str_IndexCode, R.str_IdxMain) "
                   "FROM V_Ref_FundIsinPListing R "
	               "    LEFT JOIN Rad_Ref_FundValidity V ON V.str_Isin=R.str_Isin AND '" + date_ref + "' BETWEEN V.dte_StartDate AND V.dte_StopDate "
                   "WHERE R.str_Isin = '" + isin + "' ")
    extract = pd.DataFrame.from_records(cursor.fetchall(), columns=['INDEX'])
    res = str(extract.head(1)['INDEX'].iloc[0])
    return res

def getIsinNavCcy(isin):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP 1 str_NavCcy "
                   "FROM V_Ref_FundIsinPListing "
                   "WHERE str_Isin = '" + isin + "' ")
    extract = pd.DataFrame.from_records(cursor.fetchall(), columns=['NAV CCY'])

    if extract.empty:
        res = 'EUR'
    else:
        nav_ccy = str(extract.head(1)['NAV CCY'].iloc[0])
        res = nav_ccy
    return res


def getIndexCcy(bbg):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP 1 str_Currency "
                   "FROM Ref_Index "
                   "WHERE str_bbg = '" + bbg + "' ")
    extract = pd.DataFrame.from_records(cursor.fetchall(), columns=['CCY'])

    if extract.empty:
        res = 'EUR'
    else:
        nav_ccy = str(extract.head(1)['CCY'].iloc[0])
        res = nav_ccy
    return res


def getEtfBenchmark(isin, date_from, date_to):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT str_IndexCode, dte_StartDate, dte_StopDate "
                   "FROM Rad_Ref_FundValidity "
                   "WHERE str_Isin='" + isin + "' "
                   "    AND '" + date_from + "' <= dte_StopDate "
                   "    AND '" + date_to + "' >= dte_StartDate ")
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=['INDEX', 'FROM', 'TO'])

    if df.empty:
        cursor.execute("SELECT str_IdxMain, '1990-01-01', '2100-12-31' "
                   "FROM V_Ref_EtfIsinPListing "
                   "WHERE str_Isin='" + isin + "' ")
        df = pd.DataFrame.from_records(cursor.fetchall(), columns=['INDEX', 'FROM', 'TO'])

    df['FROM'] = [dt.datetime.strptime(x, "%Y-%m-%d") for x in df['FROM']]
    df['TO'] = [dt.datetime.strptime(x, "%Y-%m-%d") for x in df['TO']]
    return df


def getIsinFromFile(filePath):
    extract = pd.read_csv(filePath, header=0)
    return extract


def getDataFromIsin(isin, field):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP 1 " + field + " "
                   "FROM V_Ref_FundIsinPListing "
                   "WHERE str_Isin = '" + isin + "' ")
    extract = pd.DataFrame.from_records(cursor.fetchall(), columns=['DATA'])

    if isinstance(extract.head(1)['DATA'].iloc[0], str) or isinstance(extract.head(1)['DATA'].iloc[0], unicode):
        resData = str(extract.head(1)['DATA'].iloc[0].encode("ascii", 'xmlcharrefreplace'))
    else:
        resData = str(extract.head(1)['DATA'].iloc[0])

    return resData



#############################
## Return More than 1 value
#############################

def getAllEtf(date_ref_from, date_ref_to, issuer):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT R.str_Isin "
                   "FROM V_Ref_FundIsinPListing R "
                   "    INNER JOIN V_Ref_FundPIsinPListingEurope RM ON RM.str_Id=R.str_Id "
                   "WHERE 1=1 "
                   "    AND R.str_Issuer IN ('" + issuer + "') "
                   # "    AND R.str_Issuer IN ('LYXOR', 'ISHARES', 'DB X') "
                   # "    AND R.str_Isin NOT IN ('FR0011376565', 'FR0011376573', 'DE000A14PKQ9', 'FR0010239111', 'FR0010413518') "
                   # "    AND R.str_Isin IN ('FR0010717074') "
                   # "    AND R.str_Isin IN ('LU1407891602', 'LU1407887162', 'LU1407888996') "
                   # "    AND R.str_AssetClassLvl1='Commodities' "
                   # "    AND R.str_ShareClassType IN ('ETF', 'OLD', 'FOF') "
                   # "    AND R.str_ListingType NOT IN ('OTC') "
                   "    AND R.str_FundRegion IN ('Europe') "
                   "    AND (('" + date_ref_from + "' >= R.dte_IsinStartDate AND '" + date_ref_to + "' < R.dte_IsinEndDate) "
                   "        OR (R.str_Issuer='LYXOR' AND (R.str_IsinName LIKE '% TH' OR R.str_IsinName LIKE '% TH ') AND '" + date_ref_to + "' >= R.dte_IsinStartDate AND  '" + date_ref_to + "' < R.dte_IsinEndDate )) "
                   )
    return pd.DataFrame.from_records(cursor.fetchall(), columns=['ISIN'])


def getLyxorEtf(date_from, date_to):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT str_Isin "
                   "FROM V_Ref_FundIsinPListing "
                   "WHERE str_Issuer='LYXOR' "
                   "    AND str_FundType IN ('ETF', 'OLD') "
                   # "    AND str_Isin NOT IN ('LU1435356495') "
                   "    AND '" + date_to + "' >= dte_IsinStartDate "
                   "    AND '" + date_from + "' < dte_IsinEndDate ")
    return pd.DataFrame.from_records(cursor.fetchall(), columns=['ISIN'])


def getListEtf(isin_list):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT str_Isin "
                   "FROM V_Ref_FundIsinPListing "
                   "WHERE str_Issuer='LYXOR' "
                   "    AND str_Isin IN (" + isin_list + ") ")
    return pd.DataFrame.from_records(cursor.fetchall(), columns=['ISIN'])


def getAllIndex(date_ref_from, date_ref_to):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT I.str_Bbg FROM Ref_Index I "
                   "	INNER JOIN (SELECT str_Bbg, MIN(dte_date) min_date, MAX(dte_date) max_date "
                   "    	FROM Mkt_IndexLast WHERE str_LastType = 'BLOOMBERG' "
                   "        AND dte_Date BETWEEN '" + date_ref_from + "' AND '" + date_ref_to + "'"
                   "GROUP BY str_Bbg)L ON L.str_bbg = I.str_Bbg "
                   "WHERE bt_GetMktData = 1 "
                   "    AND min_date <= '" + date_ref_from + "' AND max_date >= '" + date_ref_to + "'"
                   )
    return pd.DataFrame.from_records(cursor.fetchall(), columns=['INDEX'])
