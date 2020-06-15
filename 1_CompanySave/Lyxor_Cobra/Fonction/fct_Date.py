import pyodbc
import pandas as pd
import math
import datetime as dt

server = 'SRVCLDDFXP004\MSPARDFXP02'
db1 = 'ETF_DW'

def getIsinEndDate(isin):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT dte_IsinEndDate "
                   "FROM V_Ref_FundIsinPListing "
                   "WHERE str_Isin = '" + isin + "' ")
    extract = pd.DataFrame.from_records(cursor.fetchall(), columns=['DATE'])
    date_res = str(extract.head(1)['DATE'].iloc[0])
    res = date_res
    return res


def getIsinStartDate(isin):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT dte_IsinStartDate "
                   "FROM V_Ref_FundIsinPListing "
                   "WHERE str_Isin = '" + isin + "' ")
    extract = pd.DataFrame.from_records(cursor.fetchall(), columns=['DATE'])
    date_res = str(extract.head(1)['DATE'].iloc[0])
    res = date_res
    return res


def getLastNavDate(isin, date_ref, navType):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT MAX(dte_Date) "
                   "FROM Mkt_Nav "
                   "WHERE str_Isin = '" + isin + "' "
                   "    AND str_NavType = '" + navType + "' "
                   "    AND dte_Date <= '" + date_ref + "' ")
    extract = pd.DataFrame.from_records(cursor.fetchall(), columns=['DATE'])
    date_res = str(extract.head(1)['DATE'].iloc[0])
    if date_res == 'None':
        res = date_ref
    else:
        res = date_res
    return res


def getLastCommonDate(isin, date_ref, navType, idxBbg, idxType):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT MAX(N.dte_Date) "
                   "FROM Mkt_Nav N "
                   "    INNER JOIN Mkt_IndexLast I ON I.dte_Date=N.dte_Date "
                   "WHERE N.str_Isin = '" + isin + "' "
                   "    AND N.str_NavType = '" + navType + "' "
                   "    AND I.str_Bbg = '" + idxBbg + "' "
                   "    AND I.str_LastType = '" + idxType + "' "
                   "    AND N.dte_Date <= '" + date_ref + "' ")
    extract = pd.DataFrame.from_records(cursor.fetchall(), columns=['DATE'])
    date_res = str(extract.head(1)['DATE'].iloc[0])
    if date_res == 'None':
        res = date_ref
    else:
        res = date_res
    return res
