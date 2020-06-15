import pyodbc
import pandas as pd
import numpy as np
import math
import datetime as dt
import fct_Date as fDate
import fct_StaticInfo as fStat
import fct_HistoricData as fData

server = 'SRVCLDDFXP004\MSPARDFXP02'
db1 = 'ETF_DW'


def printAllEtfAum(fileFolder, fileName, mat_details, mat_synth):
    writer = pd.ExcelWriter(str.replace(fileFolder + '\\' + fileName, '\\\\', '\\'), datetime_format='yyyy-mm-dd')
    wb = writer.book
    wb.formats[0].font_size = 9
    mat_details.to_excel(writer, sheet_name='Details', index=False, startrow=2, startcol=0)
    mat_synth.to_excel(writer, sheet_name='Synthesis', index=False, startrow=2, startcol=0)
    ws_details = writer.sheets['Details']
    ws_synth = writer.sheets['Synthesis']

    # cell formats
    format_pct = wb.add_format({'num_format': '0.00%', 'font_size': 9})
    format_flt0 = wb.add_format({'num_format': '#,##0', 'font_size': 9})
    format_flt2 = wb.add_format({'num_format': '#,##0.00', 'font_size': 9})
    format_flt4 = wb.add_format({'num_format': '#,##0.0000', 'font_size': 9})

    ws_details.set_column('G:G', None, format_flt2)
    ws_details.set_column('I:K', None, format_flt2)
    ws_synth.set_column('F:L', None, format_flt2)

    writer.save()


def printAllEtfNav(fileFolder, fileName, mat_details, mat_synth):
    writer = pd.ExcelWriter(str.replace(fileFolder + '\\' + fileName, '\\\\', '\\'), datetime_format='yyyy-mm-dd')
    wb = writer.book
    wb.formats[0].font_size = 9
    mat_details.to_excel(writer, sheet_name='Details', index=False, startrow=2, startcol=0)
    mat_synth.to_excel(writer, sheet_name='Synthesis', index=False, startrow=2, startcol=0)
    ws_details = writer.sheets['Details']
    ws_synth = writer.sheets['Synthesis']

    # cell formats
    format_pct = wb.add_format({'num_format': '0.00%', 'font_size': 9})
    format_flt0 = wb.add_format({'num_format': '#,##0', 'font_size': 9})
    format_flt2 = wb.add_format({'num_format': '#,##0.00', 'font_size': 9})
    format_flt4 = wb.add_format({'num_format': '#,##0.0000', 'font_size': 9})

    ws_details.set_column('G:G', None, format_flt2)
    ws_details.set_column('I:I', None, format_flt2)
    ws_synth.set_column('F:G', None, format_flt4)

    writer.save()


def printAnalysis(fileFolder, fileName, isin, date_from, date_to, refccy, mat, etf_perf, idx_perf, etf_yield, etf_td, etf_te, etf_te_f2stdev, idx_vol):
    writer = pd.ExcelWriter(str.replace(fileFolder + '\\' + fileName, '\\\\', '\\'),
                            engine='xlsxwriter')

    wb = writer.book
    wb.formats[0].font_size = 9

    mat.to_excel(writer, sheet_name=isin, index=False, startrow=2, startcol=0)
    ws = writer.sheets[isin]

    # cell formats
    format_pct = wb.add_format({'num_format': '0.00%', 'font_size': 9})
    format_flt0 = wb.add_format({'num_format': '#,##0', 'font_size': 9})
    format_flt2 = wb.add_format({'num_format': '#,##0.00', 'font_size': 9})
    format_flt4 = wb.add_format({'num_format': '#,##0.0000', 'font_size': 9})

    ws.set_column('B:B', None, format_flt2)
    ws.set_column('C:C', None, format_flt4)
    ws.set_column('D:D', None, format_flt2)
    ws.set_column('E:E', None, format_flt4)
    ws.set_column('G:G', None, format_flt4)
    ws.set_column('H:H', None, format_flt2)
    ws.set_column('I:I', None, format_pct)
    ws.set_column('J:J', None, format_flt2)
    ws.set_column('K:K', None, format_flt4)
    ws.set_column('L:P', None, format_pct)
    ws.set_column('Q:Q', None, format_flt0)
    ws.set_column('R:R', None, format_pct)

    ws.write(0, 0, 'ISIN')
    ws.write(1, 0, isin)
    ws.write(0, 1, 'REF CCY')
    ws.write(1, 1, refccy)
    ws.write(0, 2, 'FROM')
    ws.write(1, 2, date_from)
    ws.write(0, 3, 'TO')
    ws.write(1, 3, date_to)
    ws.write(0, 4, 'YIELD')
    if not np.isnan(etf_yield):
        ws.write(1, 4, etf_yield, format_pct)
    ws.write(0, 5, 'ETF PERF')
    if not np.isnan(etf_perf):
        ws.write(1, 5, etf_perf, format_pct)
    ws.write(0, 6, 'IDX PERF')
    if not np.isnan(idx_perf):
        ws.write(1, 6, idx_perf, format_pct)
    ws.write(0, 7, 'ETF TD')
    if not np.isnan(etf_td):
        ws.write(1, 7, etf_td, format_pct)
    ws.write(0, 8, 'IDX VOL')
    if not np.isnan(idx_vol):
        ws.write(1, 8, idx_vol, format_pct)
    ws.write(0, 9, 'ETF TE')
    if not np.isnan(etf_te):
        ws.write(1, 9, etf_te, format_pct)
    ws.write(0, 10, 'ETF TE FILTERED 2 STDEV')
    if not np.isnan(etf_te_f2stdev):
        ws.write(1, 10, etf_te_f2stdev, format_pct)

    writer.save()


def printPerfAnalysis(fileFolder, fileName, isin, date_from, date_to, refccy, mat):
    writer = pd.ExcelWriter(str.replace(fileFolder + '\\' + fileName, '\\\\', '\\'),
                            engine='xlsxwriter')
    wb = writer.book
    wb.formats[0].font_size = 9

    submat = mat[['DATE', 'CUMUL ETF PERF', 'CUMUL IDX PERF']].copy()
    submat['CUMUL ETF PERF'] = 100 * (1 + submat['CUMUL ETF PERF'])
    submat['CUMUL IDX PERF'] = 100 * (1 + submat['CUMUL IDX PERF'])
    submat.rename(columns={'CUMUL ETF PERF': 'ETF PERF', 'CUMUL IDX PERF': 'IDX PERF'}, inplace=True)
    submat.to_excel(writer, sheet_name=isin, index=False, startrow=2, startcol=0)
    ws = writer.sheets[isin]

    ws.write(0, 0, 'ISIN')
    ws.write(1, 0, isin)
    ws.write(0, 1, 'REF CCY')
    ws.write(1, 1, refccy)
    ws.write(0, 2, 'FROM')
    ws.write(1, 2, date_from)
    ws.write(0, 3, 'TO')
    ws.write(1, 3, date_to)

    # Create a chart object.
    chart = wb.add_chart({'type': 'line'})
    chart.set_size({'width': 768, 'height': 480})

    chart.add_series({
        'name': 'ETF',
        'categories':  '=' + isin + '!A4:A' + str(len(submat.index)+3),
        'values':  '=' + isin + '!B4:B' + str(len(submat.index)+3)
    })
    chart.add_series({
        'name': 'Benchmark',
        'categories':  '=' + isin + '!A4:A' + str(len(submat.index)+3),
        'values':  '=' + isin + '!C4:C' + str(len(submat.index)+3)
    })

    chart.set_title({'name': '2015 Performance', 'name_font': {'size': 12}})
    chart.set_x_axis({'position_axis': 'on_tick'})
    chart.set_y_axis({'major_gridlines': {'visible': True}})
    chart.set_legend({'position': 'bottom'})

    # Insert the chart into the worksheet.
    ws.insert_chart('E3', chart)

    writer.save()




def printAllEtf(fileFolder, fileName, datas):
    writer = pd.ExcelWriter(str.replace(fileFolder + '\\' + fileName, '\\\\', '\\'),
                            engine='xlsxwriter',
                            datetime_format='yyyy-mm-dd',
                            date_format='yyyy-mm-dd')
    wb = writer.book
    wb.formats[0].font_size = 9
    datas.to_excel(writer, sheet_name='ETF', index=False, startrow=2, startcol=0)
    ws = writer.sheets['ETF']

    # cell formats
    format_pct = wb.add_format({'num_format': '0.00%', 'font_size': 9})
    format_flt0 = wb.add_format({'num_format': '#,##0', 'font_size': 9})
    format_flt2 = wb.add_format({'num_format': '#,##0.00', 'font_size': 9})
    format_flt4 = wb.add_format({'num_format': '#,##0.0000', 'font_size': 9})

    ws.set_column('I:P', None, format_pct)
    ws.set_column('Q:Q', None, format_flt4)
    ws.set_column('R:R', None, format_flt2)
    ws.set_column('S:S', None, format_pct)
    ws.set_column('T:T', None, format_flt0)
    ws.set_column('U:U', None, format_pct)

    writer.save()


def getAnalysisSynthesis(isin, date_from, date_to, refccy, navType, divType, idxType, volumeType, spreadType, generateFile, fileFolder=''):
    date_PeriodFrom = ''
    date_PeriodTo = ''
    etf_perf = np.NaN
    idx_perf = np.NaN
    etf_yield = np.NaN
    etf_td = np.NaN
    etf_te = np.NaN
    etf_te_f2stdev = np.NaN
    idx_vol = np.NaN
    etf_adv = np.NaN
    etf_avg_spread = np.NaN
    etf_last_nav = np.NaN
    etf_div = np.NaN
    etf_vol = np.NaN
    nb_etf_point = np.NaN
    nb_idx_point = np.NaN

    isinName = fStat.getDataFromIsin(isin, 'str_IsinLongName')
    mat = fData.getAnalysisMatrix(isin, date_from, date_to, refccy, navType, divType, idxType, volumeType, spreadType)

    #test si vide, sortir du module
    try:
        etf_yield = float(pd.DataFrame(1 + (mat['DIV'] * mat['DIV FX'])
            /(mat['ETF'] * mat['ETF FX'])).prod(axis=0) - 1)
    except AttributeError:
        print "Fail on Nav History on Isin: " + isin + " on Date from " + date_from + " to " + date_to
        return
    except TypeError:
        print "Fail on Nav History on Isin: " + isin + " on Date from " + date_from + " to " + date_to
        return

    date_PeriodFrom = str(mat.head(1)['DATE'].iloc[0])
    date_PeriodTo = str(mat.tail(1)['DATE'].iloc[0])
    print 'PERIOD : ' + str(date_PeriodFrom) + ' to ' + str(date_PeriodTo)
    print 'ISIN : ' + str(isin)
    etf_last_bench = mat.tail(1)['INDEX'].iloc[0]
    print 'ETF LAST BENCH : ' + str(etf_last_bench)
    print 'ETF YIELD : ' + str(etf_yield)
    etf_perf = float(mat.tail(1)['YIELD FACTOR']) * float(mat.tail(1)['ETF'] * mat.tail(1)['ETF FX']) / float(mat.head(1)['ETF'] * mat.head(1)['ETF FX']) - 1
    print 'ETF PERF : ' + str(etf_perf)
    idx_perf = float(pd.DataFrame(1 + mat['INDEX RETURN']).prod(axis=0) - 1)
    print 'IDX PERF : ' + str(idx_perf)
    etf_td = etf_perf - idx_perf
    print 'ETF TD : ' + str(etf_td)

    matte = mat[mat['INDEX CLOSE'].notnull()].copy()
    matte['ETF RETURN'] = matte['ETF ADJ'] / matte['ETF ADJ'].shift(1) - 1
    matte['INDEX CHANGE'] = (matte['INDEX'] != matte['INDEX'].shift(1))
    matte['INDEX RETURN'] = matte['INDEX RETURN'].where(matte['INDEX CHANGE'], (matte['INDEX CLOSE'] * matte['INDEX FX']) / (matte['INDEX CLOSE'].shift(1) * matte['INDEX FX'].shift(1)) - 1)
    matte['TD'] = matte['ETF RETURN'] - matte['INDEX RETURN']

    etf_te = matte['TD'].std(ddof=1) * math.sqrt(252)
    print 'ETF TE : ' + str(etf_te)
    # local_avg = mat['TD'].mean()
    # local_stdev = mat['TD'].std(ddof=1)
    # etf_te_f2stdev = mat[(mat['TD'] >= local_avg - 2 * local_stdev) & (mat['TD'] <= local_avg + 2 * local_stdev)]['TD'].std(ddof=1) * math.sqrt(252)
    local_avg = matte['TD'].mean()
    local_stdev = matte['TD'].std(ddof=1)
    etf_te_f2stdev = matte[(matte['TD'] >= local_avg - 2 * local_stdev) & (matte['TD'] <= local_avg + 2 * local_stdev)]['TD'].std(ddof=1) * math.sqrt(252)
    print 'ETF TE FILTER 2 STDEV : ' + str(etf_te_f2stdev)
    etf_vol = mat['ETF RETURN'].std(ddof=1) * math.sqrt(252)
    print 'ETF VOL : ' + str(etf_vol)
    idx_vol = mat['INDEX RETURN'].std(ddof=1) * math.sqrt(252)
    print 'IDX VOL : ' + str(idx_vol)
    etf_adv = mat['VOLUME EUR'].mean()
    print 'ETF ADV EUR : ' + str(etf_adv)
    etf_avg_spread = mat['SPREAD'].mean()
    print 'ETF AVG SPREAD : ' + str(etf_avg_spread)
    etf_last_nav = mat.tail(1)['ETF'].iloc[0]
    print 'ETF LAST NAV : ' + str(etf_last_nav)
    etf_div = float(pd.DataFrame((mat['DIV'] * mat['DIV FX'])).sum())
    print 'ETF DIV : ' + str(etf_div)
    nb_etf_point = mat['ETF'].count()
    print 'ETF NB POINT : ' + str(nb_etf_point)
    nb_idx_point = mat['INDEX CLOSE'].count()
    print 'IDX NB POINT : ' + str(nb_idx_point)

    if generateFile.lower() == 'true':
        isinName = isinName.replace(' ', '_')
        isinName = isinName.replace('/', '_')
        isinName = isinName.replace('$', 'USD')
        isinName = isinName.replace('\xc2', 'GBP')
        printAnalysis(fileFolder, str(isinName) + '_' + str(isin) + '_' + str(date_from) + '_' + str(date_to) + '.xlsx', isin, date_from, date_to, refccy, mat, etf_perf, idx_perf, etf_yield, etf_td, etf_te, etf_te_f2stdev, idx_vol)


    etf_ter = fStat.getDataFromIsin(isin, 'flt_Ter')
    # return [isinName, isin, refccy, date_from, date_to, date_PeriodFrom, date_PeriodTo,
    #         etf_last_bench, etf_yield, etf_perf, idx_perf, etf_td, etf_te, etf_te_f2stdev,
    #         idx_vol, etf_last_nav, etf_div, float(etf_ter)/100, etf_adv, etf_avg_spread]
    return {isin: {'isinName': isinName, 'isin': isin, 'refCcy': refccy,
                   'dateFrom': date_from, 'dateTo': date_to, 'periodFrom': date_PeriodFrom, 'periodTo': date_PeriodTo,
                   'etfLastBench': etf_last_bench, 'etfYield': etf_yield, 'etfPerf': etf_perf,
                   'idxPerf': idx_perf, 'etfTd': etf_td, 'etfTe': etf_te, 'etfTeF2StDev': etf_te_f2stdev,
                   'etfVol': etf_vol, 'idxVol': idx_vol, 'etfLastNav': etf_last_nav, 'etfDiv': etf_div, 'etfTer': float(etf_ter)/100,
                   'etfAdv': etf_adv, 'etfAvgSpread': etf_avg_spread, 'nbEtfPoint': nb_etf_point, 'nbIdxPoint': nb_idx_point}}
    # Quarter Perf
    # return [isinName, isin, date_PeriodFrom, date_PeriodTo, float(idx_perf), float(etf_perf), float(etf_last_nav), float(etf_div), float(etf_adv), float(etf_ter)/100, float(etf_avg_spread), float(etf_te), (1+float(etf_perf))**4 - (1+float(idx_perf))**4]



def getAnalysisSynthesisIndex(indexBloom, date_from, date_to, refccy, idxType, generateFile, fileFolder=''):
    # -------------------- getAnalysisIndex --------------------
    print 'INDEX : ' + str(indexBloom)
    print 'DATE : ' + str(date_from) + ' to ' + str(date_to)
    mat = pd.DataFrame()
    mat = fData.getIdxHisto(indexBloom, date_from, date_to, refccy, idxType)
    #Trier et mettre en date
    mat = mat.sort(['DATE'], ascending=[1])
    mat.index = [dt.datetime.strptime(x, "%Y-%m-%d") for x in mat['DATE']]
    #Metre d'autres colonne et recopier uniquement celle non null
    mat['INDEX CLOSE'] = np.nan
    mat['INDEX CLOSE'] = mat['INDEX CLOSE'].where(mat['INDEX CLOSE'].notnull(), mat['IDX CLOSE'])
    #Elimine les 0
    mat = mat[mat['INDEX CLOSE'] != 0].copy()
    mat['INDEX FX'] = np.nan
    mat['INDEX FX'] = mat['INDEX FX'].where(mat['INDEX FX'].notnull(), mat['IDX FX'])
    mat['IDX RETURN'] = (mat['IDX CLOSE'] * mat['IDX FX']) / (mat['IDX CLOSE'].shift(1) * mat['IDX FX'].shift(1)) - 1
    mat['INDEX RETURN'] = np.nan
    mat['INDEX RETURN'] = mat['INDEX RETURN'].where(mat['INDEX RETURN'].notnull(), mat['IDX RETURN'])

    #supprimer les colonnes initiales
    mat.drop(['IDX CLOSE', 'IDX FX', 'IDX RETURN'], inplace=True, axis=1)

    #CUMUL IDX PERF ( juste pour le fichier excel
    mat['CUMUL IDX PERF'] = pd.DataFrame(1 + mat['INDEX RETURN']).cumprod() - 1
    # Mettre a 0 les perf initiale
    mat.loc[mat.index[0], 'INDEX RETURN'] = 0
    mat.loc[mat.index[0], 'CUMUL IDX PERF'] = 0

    # -------------------- getAnalysisIndex --------------------

    date_PeriodFrom = str(mat.head(1)['DATE'].iloc[0])
    date_PeriodTo = str(mat.tail(1)['DATE'].iloc[0])
    print 'PERIOD : ' + str(date_PeriodFrom) + ' to ' + str(date_PeriodTo)

    #idx_perf : test si vide, sortir du module
    idx_perf = np.NaN
    try:
        idx_perf = float(pd.DataFrame(1 + mat['INDEX RETURN']).prod(axis=0) - 1)
    except AttributeError:
        print "Fail on index: " + indexBloom + " on Date from " + date_from + " to " + date_to
        return
    except TypeError:
        print "Fail on index: " + indexBloom + " on Date from " + date_from + " to " + date_to
        return
    print 'INDEX RETURN : ' + str(idx_perf)

    #idx_vol
    idx_vol = np.NaN
    idx_vol = mat['INDEX RETURN'].std(ddof=1) * math.sqrt(252)
    print 'IDX VOL : ' + str(idx_vol)

    #nb_idx_point
    nb_idx_point = np.NaN
    nb_idx_point = mat['INDEX CLOSE'].count()
    print 'IDX NB POINT : ' + str(nb_idx_point)

    if generateFile.lower() == 'true':
        printAnalysis(fileFolder, str(indexBloom) + '_' + str(date_from) + '_' + str(date_to) + '.xlsx',
                      indexBloom, date_from, date_to, refccy, mat, 0, idx_perf, 0, 0, 0, 0, idx_vol)

    return {indexBloom: {'indexBloom': indexBloom, 'refCcy': refccy, 'dateFrom': date_from, 'dateTo': date_to,
                         'periodFrom': date_PeriodFrom, 'periodTo': date_PeriodTo, 'idxPerf': idx_perf,
                         'idxVol': idx_vol, 'nbIdxPoint': nb_idx_point}}
