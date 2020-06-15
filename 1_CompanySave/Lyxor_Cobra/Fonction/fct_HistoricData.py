import pyodbc
import pandas as pd
import numpy as np
import math
import datetime as dt
import fct_Date as fDate
import fct_StaticInfo as fStat

server = 'SRVCLDDFXP004\MSPARDFXP02'
db1 = 'ETF_DW'


def getEtfHisto(isin, date_from, date_to, refCcy, navType, divType):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT N.dte_Date, N.flt_NavValue, (FXN.flt_FxToWm/(CASE WHEN N.str_NavCcy COLLATE Latin1_General_CS_AS='GBp' THEN 100 ELSE 1 END)) / (FXNR.flt_FxToWm/(CASE WHEN FXNR.str_Currency COLLATE Latin1_General_CS_AS='GBp' THEN 100 ELSE 1 END)), "
                   "SUM(ISNULL(D.flt_DivAmount, 0)) flt_DivAmount, AVG(ISNULL((FXD.flt_FxToWm/(CASE WHEN D.str_Currency COLLATE Latin1_General_CS_AS='GBp' THEN 100 ELSE 1 END)) / (FXDR.flt_FxToWm/(CASE WHEN FXDR.str_Currency COLLATE Latin1_General_CS_AS='GBp' THEN 100 ELSE 1 END)), 0)), "
                   "ISNULL(V.str_IndexCode, R.str_IdxMain) "
                   "FROM V_Ref_FundIsinPListing R "
                   "    INNER JOIN Mkt_Nav N ON N.str_Isin=R.str_Isin "
                   "    INNER JOIN Mkt_FX FXN ON FXN.dte_Date=N.dte_Date AND FXN.str_Currency=N.str_NavCcy "
                   "    INNER JOIN Mkt_FX FXNR ON FXNR.dte_Date=N.dte_Date AND FXNR.str_Currency='" + refCcy + "' "
                   "    LEFT JOIN Mkt_Div D ON D.str_Isin=N.str_Isin AND D.dte_ExDate=N.dte_Date AND D.str_DivType='" + divType + "' "
                   "    LEFT JOIN Mkt_FX FXD ON FXD.dte_Date=D.dte_ExDate AND FXD.str_Currency=D.str_Currency "
                   "    LEFT JOIN Mkt_FX FXDR ON FXDR.dte_Date=D.dte_ExDate AND FXDR.str_Currency='" + refCcy + "' "
                   "    LEFT JOIN Rad_Ref_FundValidity V ON V.str_Isin=N.str_Isin AND N.dte_Date >= V.dte_StartDate AND N.dte_Date < V.dte_StopDate "
                   "WHERE N.str_NavType='" + navType + "' "
                   "    AND N.str_Isin='" + isin + "' "
                   "    AND N.dte_Date BETWEEN '" + date_from + "' AND '" + date_to + "' "
                   "GROUP BY N.dte_Date, N.flt_NavValue, (FXN.flt_FxToWm/(CASE WHEN N.str_NavCcy COLLATE Latin1_General_CS_AS='GBp' THEN 100 ELSE 1 END)) / (FXNR.flt_FxToWm/(CASE WHEN FXNR.str_Currency COLLATE Latin1_General_CS_AS='GBp' THEN 100 ELSE 1 END)), ISNULL(V.str_IndexCode, R.str_IdxMain) "
                   "ORDER BY N.dte_Date ")

    df = pd.DataFrame.from_records(cursor.fetchall(), columns=['DATE', 'ETF', 'ETF FX', 'DIV', 'DIV FX', 'INDEX'])
    df['ETF'] = [float(x) for x in df['ETF']]
    df['ETF FX'] = [float(x) for x in df['ETF FX']]
    df['DIV'] = [float(x) for x in df['DIV']]
    df['DIV FX'] = [float(x) for x in df['DIV FX']]
    df.index = [dt.datetime.strptime(x, "%Y-%m-%d") for x in df['DATE']]
    return df

def getIdxHisto(bloomberg, date_from, date_to, refccy, idxType):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()

    cursor.execute("SELECT L.dte_Date, I.str_Bbg, L.flt_LastValue, (FXI.flt_FxToWm/(CASE WHEN I.str_Currency COLLATE Latin1_General_CS_AS='GBp' THEN 100 ELSE 1 END)) / (FXR.flt_FxToWm/(CASE WHEN FXR.str_Currency COLLATE Latin1_General_CS_AS='GBp' THEN 100 ELSE 1 END)) "
                   "FROM Mkt_IndexLast L "
                   "    INNER JOIN Ref_Index I ON I.str_Bbg=L.str_Bbg "
                   "    INNER JOIN Mkt_FX FXI ON FXI.dte_Date=L.dte_Date AND FXI.str_Currency=(CASE WHEN I.str_Currency = '' Then 'EUR' else I.str_Currency END) "
                   "    INNER JOIN Mkt_FX FXR ON FXR.dte_Date=L.dte_Date AND FXR.str_Currency='" + refccy + "' "
                   "WHERE L.str_LastType='" + idxType + "' "
                   "    AND L.str_Bbg='" + bloomberg + "' "
                   "    AND L.dte_Date BETWEEN '" + date_from + "' AND '" + date_to + "' "
                   "ORDER BY L.dte_Date")

    df = pd.DataFrame.from_records(cursor.fetchall(), columns=['DATE', 'INDEX', 'IDX CLOSE', 'IDX FX'])
    df['IDX CLOSE'] = [float(x) for x in df['IDX CLOSE']]
    df['IDX FX'] = [float(x) for x in df['IDX FX']]
    df.index = [dt.datetime.strptime(x, "%Y-%m-%d") for x in df['DATE']]
    return df


def getEtfHistoAumNav(isin, date_from, date_to, navType, shOutType):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT N.dte_Date, R.str_Isin, R.str_IsinLongName, N.flt_NavValue, N.str_NavCcy, E.flt_EqyShOut*1000000, E.flt_EqyShOut*1000000*N.flt_NavValue flt_AumCcy, "
                    "   (FXN.flt_FxToWm/(CASE WHEN N.str_NavCcy COLLATE Latin1_General_CS_AS='GBp' THEN 100 ELSE 1 END)) flt_FxWm, "
                    "   E.flt_EqyShOut*1000000*N.flt_NavValue*(FXN.flt_FxToWm/(CASE WHEN N.str_NavCcy COLLATE Latin1_General_CS_AS='GBp' THEN 100 ELSE 1 END)) flt_AumEur, "
                    "   ISNULL((CASE WHEN A.flt_SeedSharesTo<0 THEN 0 ELSE A.flt_SeedSharesTo END)*1000000*N.flt_NavValue, 0) flt_SeedCcy, ISNULL((CASE WHEN A.flt_SeedSharesTo<0 THEN 0 ELSE A.flt_SeedSharesTo END)*1000000*N.flt_NavValue*(FXN.flt_FxToWm/(CASE WHEN N.str_NavCcy COLLATE Latin1_General_CS_AS='GBp' THEN 100 ELSE 1 END)), 0) flt_SeedEur, "
                    "   ISNULL(T.flt_Ter, R.flt_Ter) flt_Ter, R.str_IdxProvider "
                    "FROM V_Ref_FundIsinPListing R "
                    "    INNER JOIN Mkt_Nav N ON N.str_Isin=R.str_Isin AND N.str_NavType='" + navType + "' "
                    "    INNER JOIN Mkt_EqyShOut E ON E.dte_Date=N.dte_Date AND E.str_Isin=N.str_Isin AND E.str_EqyShOutType='" + shOutType + "' "
                    "    INNER JOIN Mkt_FX FXN ON FXN.dte_Date=N.dte_Date AND FXN.str_Currency=N.str_NavCcy "
                    "    LEFT JOIN Ref_TerChange T ON T.str_Isin=R.str_Isin AND N.dte_Date>=T.dte_StartDate AND N.dte_Date<T.dte_EndDate "
                    "    LEFT JOIN Cpt_AumSplit A ON A.str_Isin=R.str_Isin AND A.dte_To=N.dte_Date AND A.str_Period='DAY' "
                    "WHERE R.str_Isin='" + isin + "' "
                    "    AND N.dte_Date BETWEEN '" + date_from + "' AND '" + date_to + "' "
                    "ORDER BY N.dte_Date ")
    # "    LEFT JOIN (SELECT dte_Date, str_Isin, SUM(flt_SeedMEur)*1000000 flt_SeedEur FROM V_Mkt_LyxorSeed GROUP BY dte_Date, str_Isin) S ON S.str_Isin=R.str_Isin AND S.dte_Date=N.dte_Date "

    df = pd.DataFrame.from_records(cursor.fetchall(), columns=['DATE', 'ISIN', 'NAME', 'NAV', 'CCY', 'SH OUT', 'AUM (CCY)', 'FX WM', 'AUM (EUR)', 'SEED (CCY)', 'SEED (EUR)', 'TER', 'IDX PROVIDER'])
    df['NAV'] = [float(x) for x in df['NAV']]
    df['SH OUT'] = [float(x) for x in df['SH OUT']]
    df['AUM (CCY)'] = [float(x) for x in df['AUM (CCY)']]
    df['FX WM'] = [float(x) for x in df['FX WM']]
    df['AUM (EUR)'] = [float(x) for x in df['AUM (EUR)']]
    df['SEED (CCY)'] = [float(x) for x in df['SEED (CCY)']]
    df['SEED (EUR)'] = [float(x) for x in df['SEED (EUR)']]
    df['TER'] = [float(x) for x in df['TER']]
    df.index = [dt.datetime.strptime(x, "%Y-%m-%d") for x in df['DATE']]
    return df

def getAumMatrixByIsin(isin, date_from, date_to, navType, shOutType):
    period_from = fDate.getLastNavDate(isin, date_from, navType)
    str_date_isin_end = fDate.getIsinEndDate(isin)
    date_period_from = dt.datetime.strptime(period_from, "%Y-%m-%d")
    date_period_to = dt.datetime.strptime(min(str_date_isin_end, date_to), "%Y-%m-%d")


    mat = getEtfHistoAumNav(isin, period_from, date_to, navType, shOutType)
    mat['DATE'] = [dt.datetime.strptime(x, "%Y-%m-%d") for x in mat['DATE']]
    mat['NB DAYS'] = mat['DATE'].shift(-1) - mat['DATE']
    mat['NB DAYS'] = mat['NB DAYS'].where(mat['NB DAYS'].notnull(), (date_period_to - mat['DATE']) + dt.timedelta(days=1))
    if date_from != period_from:
        print isin, date_from, period_from
        mat.loc[mat.index[0], 'NB DAYS'] = mat.loc[mat.index[1], 'DATE'] - dt.datetime.strptime(date_from, "%Y-%m-%d")

    mat['NB DAYS'] = [x.days for x in mat['NB DAYS']]

    return mat

def getAumSynthByIsin(mat, date_from, date_to):
    dt_date_from = dt.datetime.strptime(date_from, "%Y-%m-%d")
    dt_date_to = dt.datetime.strptime(date_to, "%Y-%m-%d")
    period_nb_days = float((dt_date_to - dt_date_from).days + 1)
    mat_synth = pd.DataFrame()
    mat_synth.loc[0, 'NAME'] = mat.head(1)['NAME'].iloc[0]
    mat_synth.loc[0, 'ISIN'] = mat.head(1)['ISIN'].iloc[0]
    mat_synth.loc[0, 'CCY'] = mat.head(1)['CCY'].iloc[0]
    mat_synth.loc[0, 'NB BD'] = len(mat[(mat['DATE'] >= dt_date_from) & (mat['DATE'] <= dt_date_to)].index)
    mat_synth.loc[0, 'NB CD'] = mat['NB DAYS'].sum()
    mat_synth.loc[0, 'FACTOR'] = mat['NB DAYS'].sum() / period_nb_days
    mat_synth.loc[0, 'BD AVG AUM (CCY)'] = mat[(mat['DATE'] >= dt_date_from) & (mat['DATE'] <= dt_date_to)]['AUM (CCY)'].mean()
    mat_synth.loc[0, 'BD AVG AUM (EUR)'] = mat[(mat['DATE'] >= dt_date_from) & (mat['DATE'] <= dt_date_to)]['AUM (EUR)'].mean()
    mat_synth.loc[0, 'CD AVG AUM (CCY)'] = (mat['AUM (CCY)'] * mat['NB DAYS']).sum() / mat['NB DAYS'].sum()
    mat_synth.loc[0, 'CD AVG AUM (EUR)'] = (mat['AUM (EUR)'] * mat['NB DAYS']).sum() / mat['NB DAYS'].sum()
    mat_synth.loc[0, 'BD AVG SEED (CCY)'] = mat[(mat['DATE'] >= dt_date_from) & (mat['DATE'] <= dt_date_to)]['SEED (CCY)'].mean()
    mat_synth.loc[0, 'BD AVG SEED (EUR)'] = mat[(mat['DATE'] >= dt_date_from) & (mat['DATE'] <= dt_date_to)]['SEED (EUR)'].mean()
    mat_synth.loc[0, 'CD AVG SEED (CCY)'] = (mat['SEED (CCY)'] * mat['NB DAYS']).sum() / mat['NB DAYS'].sum()
    mat_synth.loc[0, 'CD AVG SEED (EUR)'] = (mat['SEED (EUR)'] * mat['NB DAYS']).sum() / mat['NB DAYS'].sum()
    mat_synth.loc[0, 'TER FROM'] = mat.head(1)['TER'].iloc[0]
    mat_synth.loc[0, 'TER TO'] = mat.tail(1)['TER'].iloc[0]
    mat_synth.loc[0, 'IDX PROVIDER'] = mat.head(1)['IDX PROVIDER'].iloc[0]

    return mat_synth


def getNavSynthByIsin(mat, date_from, date_to):
    dt_date_from = dt.datetime.strptime(date_from, "%Y-%m-%d")
    dt_date_to = dt.datetime.strptime(date_to, "%Y-%m-%d")
    period_nb_days = float((dt_date_to - dt_date_from).days + 1)
    mat_synth = pd.DataFrame()
    mat_synth.loc[0, 'NAME'] = mat.head(1)['NAME'].iloc[0]
    mat_synth.loc[0, 'ISIN'] = mat.head(1)['ISIN'].iloc[0]
    mat_synth.loc[0, 'CCY'] = mat.head(1)['CCY'].iloc[0]
    mat_synth.loc[0, 'NB BD'] = len(mat[(mat['DATE'] >= dt_date_from) & (mat['DATE'] <= dt_date_to)].index)
    mat_synth.loc[0, 'NB CD'] = mat['NB DAYS'].sum()
    mat_synth.loc[0, 'BD AVG NAV'] = mat[(mat['DATE'] >= dt_date_from) & (mat['DATE'] <= dt_date_to)]['NAV'].mean()
    mat_synth.loc[0, 'CD AVG NAV'] = (mat['NAV'] * mat['NB DAYS']).sum() / mat['NB DAYS'].sum()

    return mat_synth



def getAnalysisMatrix(isin, date_from, date_to, refccy, navType, divType, idxType, volumeType, spreadType):

    # date_from = getLastNavDate(isin, date_from, navType)
    idxBbg = fStat.getIndexTracked(isin, date_from)
    date_from = fDate.getLastCommonDate(isin, date_from, navType, idxBbg, idxType)
    mat = pd.DataFrame()

    pricesEtf = getEtfHisto(isin, date_from, date_to, refccy, navType, divType)

    if not pricesEtf.empty:
        pricesEtf['YIELD FACTOR'] = pd.DataFrame(1 + (pricesEtf['DIV'] * pricesEtf['DIV FX'])
                                                   / (pricesEtf['ETF'] * pricesEtf['ETF FX'])).cumprod()
        pricesEtf['ETF ADJ'] = (pricesEtf['ETF'] * pricesEtf['ETF FX']) * pricesEtf['YIELD FACTOR']
        pricesEtf['ETF RETURN'] = pricesEtf['ETF ADJ'] / pricesEtf['ETF ADJ'].shift(1) - 1

        mat = pricesEtf
        mat['INDEX CLOSE'] = np.nan
        mat['INDEX FX'] = np.nan
        mat['INDEX RETURN'] = np.nan

        idxbbg = fStat.getEtfBenchmark(isin, date_from, date_to)

        for i, idx in idxbbg.iterrows():
            pricesIdx = getIdxHisto(str(idx['INDEX']), date_from, date_to, refccy, idxType)
            pricesIdx = pd.merge(mat[['DATE']], pricesIdx, how='inner', on=['DATE'])

            pricesIdx['IDX RETURN'] = (pricesIdx['IDX CLOSE'] * pricesIdx['IDX FX']) / (pricesIdx['IDX CLOSE'].shift(1) * pricesIdx['IDX FX'].shift(1)) - 1

            # if idxbbg.shape[0] == 1:
            #     mat['INDEX'] = str(idx['INDEX'])

            mat = pd.merge(mat, pricesIdx, how='left', on=['DATE', 'INDEX'])
            mat = mat.sort(['DATE'], ascending=[1])
            mat['INDEX CLOSE'] = mat['INDEX CLOSE'].where(mat['INDEX CLOSE'].notnull(), mat['IDX CLOSE'])
            mat['INDEX FX'] = mat['INDEX FX'].where(mat['INDEX FX'].notnull(), mat['IDX FX'])
            mat['INDEX RETURN'] = mat['INDEX RETURN'].where(mat['INDEX RETURN'].notnull(), mat['IDX RETURN'])
            mat.drop(['IDX CLOSE', 'IDX FX', 'IDX RETURN'], inplace=True, axis=1)

        mat['TD'] = mat['ETF RETURN'] - mat['INDEX RETURN']
        # mat['CUMUL ETF PERF'] = mat['CUMUL ETF PERF'].fillna(method='pad')
        mat.loc[mat.index[0], 'CUMUL ETF PERF'] = 0
        mat['CUMUL IDX PERF'] = pd.DataFrame(1 + mat['INDEX RETURN']).cumprod() - 1
        mat.loc[mat.index[0], 'CUMUL IDX PERF'] = 0
        mat['CUMUL TD'] = mat['CUMUL ETF PERF'] - mat['CUMUL IDX PERF']

        volumeEtf = getVolumeHisto(isin, date_from, date_to, refccy, volumeType)
        spreadEtf = getSpreadHisto(isin, date_from, date_to, spreadType, volumeType)
        mat = pd.merge(mat, volumeEtf[['DATE', 'VOLUME EUR']], how='left', on=['DATE'])
        mat = pd.merge(mat, spreadEtf[['DATE', 'SPREAD']], how='left', on=['DATE'])

        mat.index = [dt.datetime.strptime(x, "%Y-%m-%d") for x in mat['DATE']]

        return mat


def getVolumeHisto(isin, date_from, date_to, refccy, volumeType):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT V.dte_Date, V.str_Isin, V.flt_VolumeEur, V.flt_VolumeEur/FX.flt_FxToWm flt_VolumeCcy "
                   "FROM V_Mkt_VolumeByIsin V "
                   "    INNER JOIN Mkt_FX FX ON FX.dte_Date=V.dte_Date AND FX.str_Currency='" + refccy + "' "
                   "WHERE V.str_Type='" + volumeType + "' AND V.str_Isin='" + isin + "' AND V.dte_Date BETWEEN '" + date_from + "' AND '" + date_to + "' "
                   "ORDER BY V.dte_Date")
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=['DATE', 'ISIN', 'VOLUME EUR', 'VOLUME CCY'])
    df['VOLUME EUR'] = [float(x) for x in df['VOLUME EUR']]
    df['VOLUME CCY'] = [float(x) for x in df['VOLUME CCY']]
    df.index = [dt.datetime.strptime(x, "%Y-%m-%d") for x in df['DATE']]
    return df

def getSpreadHisto(isin, date_from, date_to, spreadType, volumeType):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db1)
    cursor = cnxn.cursor()
    cursor.execute("SELECT S.dte_Date, S.str_Isin, S.flt_VWS "
                   "FROM V_Mkt_SpreadByIsin S "
                   "WHERE S.str_SpreadType='" + spreadType + "' AND S.str_VolumeType='" + volumeType + "' AND S.str_Isin='" + isin + "' AND S.dte_Date BETWEEN '" + date_from + "' AND '" + date_to + "' "
                   "ORDER BY S.dte_Date")
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=['DATE', 'ISIN', 'SPREAD'])
    df['SPREAD'] = [float(x) for x in df['SPREAD']]
    df.index = [dt.datetime.strptime(x, "%Y-%m-%d") for x in df['DATE']]
    return df



