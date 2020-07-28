import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay
import PCF_genericProcess as pp
import fct_Date as dat
import fct_dataframe as dframe
import fct_Files as fl
from datetime import datetime
import win32com.client
import pyodbc
import sys
import re
import csv
import os


#------------------------------------------------------------------------------
# London
#------------------------------------------------------------------------------
def pcf_PhillipCap(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_COMPO =  dic_df['ZIP_Compo']
        df_FX =     dic_df['ZIP_FX']
        df_NAV =    dic_df['OUT_NAV']
        df_FundDiv= dic_df['SQL_FundDiv']
        df_PAF =    dic_df['SQL_PAF']
        str_folder= dic_df['Folder']
    except Exception as err:    return 'ERROR: Dataframe - {} | {}'.format(str_PCF, str(err)), []
    
    l_pcfFileName = ['Phillip SGX FX_{}.xlsx'.format(dte_date.strftime('%Y%m%d')),
                     'Phillip SGX_{}.xls'.format(dte_date.strftime('%Y%m%d'))]
    
    # 1. Variables
    try:
        str_DivDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date,'%Y%m%d', 1, 367, bl_Backward = False)
        str_pcfDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date,'%d/%m/%Y', 1, 367, bl_Backward = False)
        df_NAV.columns = ['Date','CODE','Units','Bid_Price']
        flt_Nav = df_NAV[df_NAV['CODE'] == 'SG1DB9000009']['Bid_Price'].values[0]
        flt_share = df_NAV[df_NAV['CODE'] == 'SG1DB9000009']['Units'].values[0]
        int_CreationUnits = 50000
        if len(df_FundDiv) > 0:     
            flt_FundDiv = df_FundDiv['NetAmount'].sum()
            flt_Nav = (flt_Nav - flt_FundDiv)
        if len(df_PAF) > 0:         
            flt_PAF = df_PAF['PriceAdjustmentFactor'].sum()
            flt_Nav = flt_Nav * flt_PAF
            flt_share = flt_share / flt_PAF
    except Exception as err:    return 'ERROR: 1. Variables - {} | {}'.format(str_PCF, str(err)), []
    
    # 2. reform Holdings DF
    try:
        # just take some rows of your Compo DATAFRAME
        df_COMPO.columns = ['Company Name', 'Quantity', 'Currency', 'Unit Cost', 'Book Value', 'Price', ' Market Value',
                            'Accrued', 'Total Market', 'Total G/L', 'Col11', 'RIC', 'ISIN']
        int_endCompo = int(pd.DataFrame([i for i, x in enumerate(df_COMPO['Company Name'] == 'TOTAL ORDINARY SHARES') if x]).iloc[0])
        df_COMPO = dframe.fDf_CleanPrepareDF(df_COMPO.iloc[10:int_endCompo], l_colToDropNA = ['Quantity'], 
                                             l_colToBeFloat = ['Quantity','Price'], l_colSort = ['ISIN'])
        df_COMPO['ISIN'] = df_COMPO['ISIN'].str.upper()
        # Add new columns
        df_COMPO['Shares (Basket)'] = ((df_COMPO['Quantity'] / (flt_share / int_CreationUnits)).apply(np.trunc)).astype(int)
    except Exception as err:    return 'ERROR: 2. reform Holdings DF - {} | {}'.format(str_PCF, str(err)), []
    
    # 2.2 Check Error on Input files
    try:
        for it_comp in range(len(df_COMPO)):
            if len(df_COMPO['ISIN'].iloc[it_comp]) != 12:
                print('  ERROR: The ISIN column in the vendor file contains a non valid ISIN identifier (more than 12 char)')
                print('  * No output has been generated')
                print('  - Value that caused the error: {}'.format(str(df_COMPO['ISIN'].iloc[it_comp])))
                return str_resultFigures, []
    except Exception as err:    return 'ERROR: 2.2 Check Error on Input files - {} | {}'.format(str_PCF, str(err)), []
    
    # 3. Reform FX DF
    try:
        # just take some rows of your Compo DATAFRAME
        int_lenCol = len(df_FX.columns)
        df_FX.columns = ['1', 'Currency', 'Description', 'Close_Price', 'Exchange Rate', 'Fx_secondary', ' Date'][:int_lenCol]
        df_FX = df_FX[['Currency','Exchange Rate']].copy()
        df_FX['Currency'].replace(['SGD=', 'HKD=', 'AUD=', 'CNY=', 'THB='], ['SGD', 'HKD', 'AUD', 'CNY', 'THB'], inplace=True)
        df_FX = dframe.fDf_DropRowsIfNa_resetIndex(df_FX, ['Exchange Rate'])
        df_FX = dframe.fDf_fillColUnderCondition(df_FX, 'Exchange Rate', lambda x:1/x, 'Currency', 'AUD', True)
        df_FX.loc[len(df_FX)] = ['USD',1.0]
        df_COMPO = dframe.fDf_JoinDf(df_COMPO, df_FX, 'Currency', 'left')
    except Exception as err:    return 'ERROR: 3. reform FX DF - {} | {}'.format(str_PCF, str(err)), []
    
    # 4. Dividend & Change df_COMPO
    try:
        df_codePivot = pp.fDf_phillipCap_GetPivotCode_wDiv(df_COMPO, 'RIC', str_folder + 'raw', 
                                                           'PivotCode_uk_PhilippCap.csv', str_DivDate)
        df_COMPO = pd.merge(df_COMPO, df_codePivot, on = 'RIC', how = 'left')
        df_COMPO['AdjustedPrice'] = df_COMPO['Price'] - df_COMPO['GrossAmount']
        df_COMPO['1_col'] = ''
        df_COMPO = df_COMPO[['1_col','Company Name', 'Currency', 'AdjustedPrice', 'Shares (Basket)',
                             'ISIN', 'Sedol', 'RIC', 'Bloomberg', 'Exchange Rate', 'Quantity']].copy()
    except Exception as err:    return 'ERROR: 4. Dividend & Change df_COMPO - {} | {}'.format(str_PCF, str(err)), []
    
    # 5. Re-Made FX
    try:
        df_Forex = dframe.fDf_FilterOnCol(df_FX, 'Currency', ['AUD', 'CNY', 'HKD', 'SGD', 'THB'])
        df_Forex['Close Date'] = dte_date.strftime("%m/%d/%Y")
        df_Forex['Currency Code'] = df_Forex['Currency']
        df_Forex['From Currency'] = df_Forex['Currency']
        # Dont know how to do ...
        df_Forex = dframe.fDf_fillColUnderCondition(df_Forex, 'From Currency', 'Australian Dollar', 'Currency', 'AUD')
        df_Forex = dframe.fDf_fillColUnderCondition(df_Forex, 'From Currency', 'Chinese Renminbi', 'Currency', 'CNY')
        df_Forex = dframe.fDf_fillColUnderCondition(df_Forex, 'From Currency', 'Hong Kong Dollar', 'Currency', 'HKD')
        df_Forex = dframe.fDf_fillColUnderCondition(df_Forex, 'From Currency', 'Singapore Dollar', 'Currency', 'SGD')
        df_Forex = dframe.fDf_fillColUnderCondition(df_Forex, 'From Currency', 'Thai Baht', 'Currency', 'THB')
        df_Forex = df_Forex[['From Currency', 'Currency Code','Exchange Rate', 'Close Date']].copy()
        df_Forex.sort_values('From Currency', inplace = True)
    except Exception as err:    return 'ERROR: 5. FX out - {} | {}'.format(str_PCF, str(err)), []
    
    # 6. From Final File
    try:
        # MARKET CAP
        flt_MarketCap = (df_COMPO['AdjustedPrice'] * df_COMPO['Shares (Basket)'] * df_COMPO['Exchange Rate']).sum()
        # HEADER LEVEL OUTPUT
        df_PCFHeader = pd.DataFrame(columns = range(3))
        df_PCFHeader.loc[0] = ['', '', '']
        df_PCFHeader.loc[1] = ['', '', '']
        df_PCFHeader.loc[2] = ['', 'Phillip Capital', '']
        df_PCFHeader.loc[3] = ['', '', '']
        df_PCFHeader.loc[4] = ['', 'Indicative Creation / Redemption basket Composition for trade date', str_pcfDate]
        df_PCFHeader.loc[5] = ['', '', '']
        df_PCFHeader.loc[6] = ['', 'FUND INFORMATION', '']
        df_PCFHeader.loc[7] = ['', 'Fund Name', 'PHILLIP SGX APAC DIVIDEND LEADERS REIT ETF']
        df_PCFHeader.loc[8] = ['', 'ISIN', 'SG1DB9000009']
        df_PCFHeader.loc[9] = ['', 'BBG Ticker', 'PAREIT SP Equity']
        df_PCFHeader.loc[10] = ['', 'Reuters', 'PHIL.SI']
        df_PCFHeader.loc[11] = ['', 'Fund Currency', 'USD']
        df_PCFHeader.loc[12] = ['', 'NAV per Share', flt_Nav]
        df_PCFHeader.loc[13] = ['', 'Number of Fund Shares in Issue', flt_share]
        df_PCFHeader.loc[14] = ['', 'Total NAV of Basket', flt_Nav * int_CreationUnits]
        df_PCFHeader.loc[15] = ['', 'Estimated Cash Position of Basket', round((flt_Nav * int_CreationUnits) - (flt_MarketCap), 2)]
        df_PCFHeader.loc[16] = ['', 'Creation Redemption', int_CreationUnits]
        df_PCFHeader.loc[17] = ['', '', '']
        # ADD a title row
        df_COMPO.columns = ['', 'Company Name', 'Currency', 'Price', 'Shares (Basket)', 'ISIN', 'SEDOL', 
                            'RIC', 'Bloomberg', 'FX Rate', 'Shares (Fund)']
        # CONCAT
        df_PCF = dframe.fDf_Concat_wColOfDf1(df_PCFHeader, df_COMPO, bl_colDf2_AsARow = True)
    except Exception as err:    return 'ERROR: 6. From Final File - {} | {}'.format(str_PCF, str(err)), []
    
    # 7. Create the files
    try:
        # FX
        str_path0 = fl.fStr_BuildPath(str_folder, l_pcfFileName[0])
        str_path0 = fl.fStr_createExcel_1Sh(str_path0, '', df_Forex, bl_header = True)
        fl.fStr_StyleIntoExcel(str_path0, str_styleName = 'Border_Header', l_border = ['thin', 'FF000000'])                                                             
        # PCF 
        str_path1 = fl.fStr_BuildPath(str_folder, l_pcfFileName[1])
        str_path1 = fl.fStr_createExcel_1Sh(str_path1, '', df_PCF)
        l_pathAttach = [str_path0, str_path1]
    except Exception as err:    return 'ERROR: 7. Create the files - {} | {}'.format(str_PCF, str(err)), []

    l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]

    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________






def fTup_GetLastRowCol(xl_sh, int_rowStart = 1, int_colStart = 1):
    int_row = int_rowStart
    int_col = int_colStart
    while xl_sh.Cells(int_row, int_colStart).Value != None:
        int_row += 1
    int_lastRow = int_row - 1
    
    while xl_sh.Cells(int_rowStart, int_col).Value != None:
        int_col += 1
    int_lastCol = int_col - 1
    #    print(xl_sh.Name, 'last_row', int_lastRow, 'last_col', int_lastCol)
    return int_lastRow, int_lastCol



def fDf_flt_rebalanceOnEquity(df_Equity, df_Rebal, df_compo):
    # df_Rebal
    df_Equity = df_Equity.merge(df_Rebal, left_on='RIC Code', right_on='Ric', how='outer').copy()
	# NOSH ADJUSTMENT
    df_Equity.loc[df_Equity['B/S'] == 'S', 'Today Holdings'] = df_Equity['Today Holdings'] - df_Equity['Executed Shares']
    df_Equity.loc[df_Equity['B/S'] == 'B', 'Today Holdings'] = df_Equity['Today Holdings'] + df_Equity['Executed Shares']
    df_Equity.loc[df_Equity['B/S'] == 'B', 'Execution Net Local'] = -df_Equity['Execution Net Local']
		# ADDITIONS
    df_Equity['RIC Code'] = df_Equity['RIC Code'].fillna(df_Equity['Ric'])
    df_Equity['Name'] = df_Equity['Name'].fillna(df_Equity['Company Name'])
    df_Equity['CCY'] = df_Equity['CCY'].fillna(df_Equity['Currency'])
    df_Equity['SEDOL'] = df_Equity['SEDOL'].fillna(df_Equity['Sedol'])
    df_Equity['Today Holdings'] = df_Equity['Today Holdings'].fillna(df_Equity['Executed Shares'])
		
    # df_compo
    df_compo = df_compo[['Ric', 'Price', 'FXRate']]
    df_compo = df_compo.rename(columns={'Ric': 'RicInIndex', 'Price': 'PriceInIndex', 'FXRate': 'FXRateInIndex'})
    df_Equity = df_Equity.merge(df_compo, left_on='RIC Code', right_on='RicInIndex', how='left')
    df_Equity['Today Closing Price'] = df_Equity['Today Closing Price'].fillna(df_Equity['PriceInIndex'])

	# DUE TO CONSTITUENT FXRATE DIFFERENCE BETWEEN THE INDEX AND THE PROVIDER FILE
	# IF THE CURRENCY CODE IS ALREADY IN THE COMPOSITION, FETCH THE FXRATE FROM ANOTHER ROW IN THE PCF
	# ELSE GET THE FXRATE FROM THE INDEX
    df_AdditionsCurrency = df_Equity.loc[df_Equity['Exchange rate'].isnull()].copy()
    if not df_AdditionsCurrency.empty:
        for i in df_AdditionsCurrency.index:
            if df_AdditionsCurrency['Currency'].isin(df_Equity['Currency']).any():
                df_AdditionsCurrency['FX Rate'] = df_Equity.loc[df_Equity['Currency'] == df_AdditionsCurrency['Currency'].iloc[0], 'Exchange rate'].iat[0]
            else:
                onsCurrency['FX Rate'] = 1 / df_AdditionsCurrency['FXRateInIndex']
            df_AdditionsCurrency = df_AdditionsCurrency[['RIC Code', 'FX Rate']].copy()
            df_Equity = df_Equity.merge(df_AdditionsCurrency, how='left')
            df_Equity['Exchange rate'] = df_Equity['Exchange rate'].fillna(df_Equity['FX Rate'])
    flt_RebalanceCash = (df_Equity['Execution Net Local'] * (1 / df_Equity['Exchange rate'])).sum()
    
    return df_Equity, flt_RebalanceCash




def ThanosCode():
    
    ### Paths OUTPUT
    str_pathPCF = 'E:/Data/Lucerne/Data/SOLA PCF/UK_Cimb_FTSE_Asean40/Output/'
    str_pathPCF = r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Auto_py\UK_CIMB\Asean40_{}'.format(inputdate) + '\\'
    #    str_pathPCF = r'\\PRDFIL001WI\DeltaOneShare\PCFDistribution\Auto_py\UK_CIMB\Asean40_{}'.format(inputdate) + '\\'
    
    ### Connecting to SOLA DB
    con = pyodbc.connect('DRIVER={SQL Server};SERVER=10.233.6.147;DATABASE=SolaDBServer;UID=pcfReporting; PWD=pcfR3p0rt1n9')
    cur = con.cursor()
    
    # PULLING PRICE AND FX FROM THE INDEX
    querystring = "exec spExcelGetComposition '.FTASEAN40', '{}', 'Index', 'Tracking', 'Open'".format(str_DivDate)
    cur.execute(querystring)
    cur.commit()
    df_compo = pd.read_sql(querystring, con)
    
    ### Dates
    dte_inputdate = (datetime.now() - BDay(3)).date()
    print('dte_inputdate', dte_inputdate)
    inputdate = dte_inputdate.strftime("%Y%m%d")
    #    inputdate = '20200722' # Manual date bypass - 'yyyymmdd'
    rebalanceinputdate = datetime.strptime(inputdate, "%Y%m%d").strftime("%d%b%Y")    
    str_DivDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_inputdate, "%Y-%m-%d", 1, '367')
#    DivDate = (datetime.strptime(inputdate, "%Y%m%d")+BDay(1)).strftime("%Y-%m-%d")
#    ### Checking for Holidays
#    querystring = "select * from tblHoliday where CalendarID = 367"
#    cur.execute(querystring)
#    cur.commit()
#    HolidayCalendar = pd.read_sql(querystring, con)
#    
#    if DivDate in HolidayCalendar['HolidayDate'].values:
#    	print('There is a Singapore bank holiday for tomorrow,', DivDate)
#    	DivDate = HolidayCalendar.loc[HolidayCalendar['HolidayDate'] == DivDate, 'NextBusDate'].iloc[0]
#        #	PCFdate = datetime.strptime(DivDate, "%Y-%m-%d").strftime("%d/%m/%Y")
#    else:
#    	print('No Bank Holidays.')
    
    # INPUT
    inpath = 'E:/Data/Lucerne/Data/SOLA PCF/UK_Cimb_FTSE_Asean40/Input/'
    #--------------------------------------------------------------------------
    # SGFABasketFile
    #--------------------------------------------------------------------------
    str_pathInput = os.path.abspath(inpath + 'SGFABasketFile' + inputdate + '.xlsx')
    ### Parse Files
    xlApp = win32com.client.Dispatch("Excel.Application")
    xlApp.DisplayAlerts = False
    xlApp.Visible = True
    xlwb = xlApp.Workbooks.Open(str_pathInput, False, True, None, Password = 'ca300')
    # Summary    
    xl_sh = xlwb.Sheets('Summary')
    int_lastRow, int_lastCol = fTup_GetLastRowCol(xl_sh, 2000, 1)
    rg_content = xl_sh.Range(xl_sh.Cells(7, 1), xl_sh.Cells(int_lastRow, 31)).Value
    df_Summary = pd.DataFrame(list(rg_content))
    df_Summary = dframe.fDf_Make1stRow_columns(df_Summary)
    # Equity
    xl_sh = xlwb.Sheets('Equity')
    int_lastRow, int_lastCol = fTup_GetLastRowCol(xl_sh, 9, 1)
    rg_content = xl_sh.Range(xl_sh.Cells(9, 1), xl_sh.Cells(int_lastRow, int_lastCol)).Value
    df_Equity = pd.DataFrame(list(rg_content))
    df_Equity = dframe.fDf_Make1stRow_columns(df_Equity)
    # Div
    xl_sh = xlwb.Sheets('Div')
    int_lastRow, int_lastCol = fTup_GetLastRowCol(xl_sh, 5, 1)
    rg_content = xl_sh.Range(xl_sh.Cells(5, 1), xl_sh.Cells(int_lastRow, int_lastCol)).Value
    df_Div_Data = pd.DataFrame(list(rg_content))
    df_Div_Data = dframe.fDf_Make1stRow_columns(df_Div_Data)
    # Est Cash
    xl_sh = xlwb.Sheets('Est Cash')
    rg_content = xl_sh.Range(xl_sh.Cells(1, 1), xl_sh.Cells(40, 5)).Value
    df_EstCash = pd.DataFrame(list(rg_content))
    df_EstCash = dframe.fDf_Make1stRow_columns(df_EstCash)
    
    #--------------------------------------------------------------------------
    # optional input file: CIMB Principle Execution
    #--------------------------------------------------------------------------
    str_pathOptionalInput = inpath+'CIMB Principle Execution ' + rebalanceinputdate + '_Asia Pacific.xlsx'
    if os.path.isfile(str_pathOptionalInput):
    	df_Rebal = pd.read_excel(str_pathOptionalInput, skiprows=8)
    else:        df_Rebal = None
    
    #--------------------------------------------------------------------------
    # Operation on Input Sheet
    #--------------------------------------------------------------------------
    # Operation on df_Summary
    df_Summary['Pricing Date'] = df_Summary['Pricing Date'].apply(lambda x:x.date())
    
    # Operation on df_Equity
    df_Equity = df_Equity[df_Equity['Today Holdings'] != 0].reset_index()
    flt_RebalanceCash = 0
    if not df_Rebal is None:
        if df_Rebal['Acct'].iloc[0] != 'FTSE':
            print('''The value under the "Acct" column in the rebalance file is not #FTSE#,                  
                  make sure you have the correct file and run the script again.''')
        else:
            df_Equity, flt_RebalanceCash = fDf_flt_rebalanceOnEquity(df_Equity, df_Rebal, df_compo)
    
    # Operation on df_Div_Data
    int_DivData_End = int(df_Div_Data.loc[df_Div_Data['Stock name'] == 'UNDERLYING'].index.values)
    df_Div_Data = df_Div_Data[0:int_DivData_End]
    #    df_Div_Data['Ex-date '] = pd.to_datetime(df_Div_Data['Ex-date ']).apply(lambda x: x.date())
    
    # Operation on df_EstCash
    df_EstCash.columns = ['ColumnA','ColumnB','ColumnC','ColumnD','ColumnE']
    
    # VARIABLES
    CreationRedemption = 50000
    FundIsin = 'SG1T81931787'
    FundCurrency = 'USD'
    FundName = 'ETF CIMB ASEAN 40' # not pulling from SOLA to keep it consistent with legacy
    NAV = df_Summary.loc[df_Summary['Pricing Date'] == dte_inputdate, 'NAV \n(Per Unit)'].iloc[0]
    FundNOSH = df_Summary.loc[df_Summary['Pricing Date'] == dte_inputdate, 'Outstanding Units'].iloc[0]
    TotalFundNAV = df_Summary.loc[df_Summary['Pricing Date'] == dte_inputdate, 'Total NAV'].iloc[0]
    NumberofBaskets = FundNOSH / CreationRedemption
    Liquidity = df_EstCash.loc[df_EstCash['ColumnA'] == 'liquidity as of Pricing Date', 'ColumnB'].iloc[0]
    NetInOutFlow = df_EstCash.loc[df_EstCash['ColumnD'] == 'Net In/outflow:', 'ColumnE'].iloc[0]
    # Payables = df_EstCash.loc[df_EstCash['ColumnA'] == 'Payable & Receivables for Rebalancing Trades', 'ColumnB'].fillna(0).iloc[0]
    DivDistr = df_EstCash.loc[df_EstCash['ColumnA'] == 'Dividend Distribution', 'ColumnB'].fillna(0).iloc[0]
    UnequitizedCashOfFund = Liquidity + NetInOutFlow + DivDistr # + Payables
    UnequitizedCash = UnequitizedCashOfFund / NumberofBaskets
    
    
    
    
    
    
    
    
    # Pivot: getting the Isin from Ric
    
    
    
    
    ### Getting Constituent Isins from SOLA DB on the back of Ric codes provided in the file
    SQLRIC = []
    Rics = pd.DataFrame()
    for row in df_Equity['RIC Code']:
    	row = str(row)
    	SQLRIC.append(row)
    SQLRIC = str(SQLRIC).replace("[", "(").replace("]", ")")
    
    ### Getting ISINs on the back of the RICs from the source file
    querystring = "select Ric as RIC, Isin as ISIN from tblCodePivot where Ric in " + SQLRIC + " and IsActive = 1"
    cur.execute(querystring)
    cur.commit()
    ISINS = pd.read_sql(querystring, con)
    
    
    
    
    
    ### Constituent Level Output
    PCFCon = pd.DataFrame(columns=('', 'Company Name', 'Currency', 'Price', 'Shares', 'SEDOL', 'RIC', 'FX Rate'))
    PCFCon[''] = ''
    PCFCon['Company Name'] = df_Equity['Name']
    PCFCon['Currency'] = df_Equity['CCY']
    PCFCon['Price'] = df_Equity['Today Closing Price']
    PCFCon['Shares'] = (df_Equity['Today Holdings'] / NumberofBaskets).astype(int)
    PCFCon['SEDOL'] = df_Equity['SEDOL']
    PCFCon['RIC'] = df_Equity['RIC Code']
    
    df_Equity['Exchange rate'] = df_Equity['Exchange rate'].astype(float)
    PCFCon['FX Rate'] = (1 / df_Equity['Exchange rate'])
    # MErge 
    PCFCon = PCFCon.merge(ISINS)
    
    
    ### Getting Dividend Net Rate from the source file where ex-date matches str_DivDate
    if (df_Div_Data['Ex-date '].astype(str) == str_DivDate).any():
    	Dividends = df_Div_Data[df_Div_Data['Ex-date '].astype('str') == str_DivDate]
    	Dividends = Dividends[['Stock name', 'Net Rate']]
    	PCFCon = PCFCon.merge(Dividends, left_on='Company Name', right_on='Stock name', how='outer').fillna(0)
        EquitizedCash = (((df_Equity['Today Holdings'] / NumberofBaskets) - PCFCon['Shares']) * PCFCon['Price'] * PCFCon['FX Rate']).sum()
    	
        CashFromDividends = (PCFCon['Net Rate'] * PCFCon['Shares'] * PCFCon['FX Rate']).sum()
    	PCFCon['Price'] = PCFCon['Price'] - PCFCon['Net Rate']
    else:
    	CashFromDividends = 0
    	EquitizedCash = (((df_Equity['Today Holdings'] / NumberofBaskets) - PCFCon['Shares']) * PCFCon['Price'] * PCFCon['FX Rate']).sum()
    
    
    
    
    
    PCFCon = PCFCon[['', 'Company Name', 'Currency', 'Price', 'Shares', 'ISIN', 'SEDOL', 'RIC', 'FX Rate']]
    
    ### Estimated Cash
    Fees = ((datetime.strptime(str_DivDate, "%Y-%m-%d") - datetime.strptime(inputdate, "%Y%m%d")).days/365*0.0065*(TotalFundNAV / NumberofBaskets))
    EstimatedCash = UnequitizedCash + EquitizedCash + CashFromDividends + (flt_RebalanceCash / NumberofBaskets) - Fees
    
    # Diplaying a smaller number of decimal points for FX Rate
    PCFCon['FX Rate'] = PCFCon['FX Rate'].map('{:,.7f}'.format)
    
    
    
    
    ### Getting Fund Ref Data
    querystring = "select * from tblCodePivot where Isin = '" + FundIsin + "'AND CurrencyCode = '" + FundCurrency + "'"
    cur.execute(querystring)
    cur.commit()
    FundRefData = pd.read_sql(querystring, con)
    
    ### Header Level Output
    PCFHeader = pd.DataFrame(columns=('', 'Company Name', 'Currency', 'Price', 'Shares', 'ISIN', 'SEDOL', 'RIC', 'FX Rate'))
    PCFHeader.loc[0] = ['', '', '', '', '', '', '', '', '']
    PCFHeader.loc[1] = ['', '', '', '', '', '', '', '', '']
    PCFHeader.loc[2] = ['', 'CIMB ETF', '', '', '', '', '', '', '']
    PCFHeader.loc[3] = ['', '', '', '', '', '', '', '', '']
    PCFHeader.loc[4] = ['', 'Indicative Creation / Redemption basket Composition for trade date', datetime.strptime(str_DivDate, "%Y-%m-%d").strftime("%d/%m/%Y"), '', '', '', '', '', '']
    PCFHeader.loc[5] = ['', '', '', '', '', '', '', '', '']
    PCFHeader.loc[6] = ['', 'Fund Information', '', '', '', '', '', '', '']
    PCFHeader.loc[7] = ['', 'Fund Name', FundName, '', '', '', '', '', '']
    PCFHeader.loc[8] = ['', 'ISIN', FundIsin, '', '', '', '', '', '']
    PCFHeader.loc[9] = ['', 'BBG Ticker', FundRefData['Bloomberg'].iloc[0].replace('Equity', '').strip(), '', '', '', '', '', '']
    PCFHeader.loc[10] = ['', 'Reuters', FundRefData['Ric'].iloc[0], '', '', '', '', '', '']
    PCFHeader.loc[11] = ['', 'Fund Currency', FundCurrency, '', '', '', '', '', '']
    PCFHeader.loc[12] = ['', 'NAV per Share', NAV, '', '', '', '', '', '']
    PCFHeader.loc[13] = ['', 'Number of Fund Shares in Issue', FundNOSH, '', '', '', '', '', '']
    PCFHeader.loc[14] = ['', 'Total NAV of Fund per Creation / Redemption Unit', TotalFundNAV / NumberofBaskets, '', '', '', '', '', '']
    PCFHeader.loc[15] = ['', 'Total Cash Position of Fund per Creation / Redemption Unit', EstimatedCash, '', '', '', '', '', '']
    PCFHeader.loc[16] = ['', 'Creation Redemption', CreationRedemption, '', '', '', '', '', '']
    PCFHeader.loc[17] = ['', '', '', '', '', '', '', '', '']
    PCFHeader.loc[18] = ['', 'Company Name', 'Currency', 'Price', 'Shares', 'ISIN', 'SEDOL', 'RIC', 'FX Rate']
    
    ### Main Output
    PCFFinal = PCFHeader.append(PCFCon)
    PCFFinal.to_excel(str_pathPCF + 'PCF_' + datetime.strptime(str_DivDate, "%Y-%m-%d").strftime("%Y%m%d") + '_ASEAN40.xls', index=False, header=None)
    
    ### CSV.TMP Outputs
    PCFTMP = PCFFinal.iloc[2:, :]
    PCFTMP.to_csv(str_pathPCF + 'PCF_' + datetime.strptime(str_DivDate, "%Y-%m-%d").strftime("%Y%m%d") + '_ASEAN40.csv.tmp', index=False, header=None, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    with open(str_pathPCF + 'PCF_' + datetime.strptime(str_DivDate, "%Y-%m-%d").strftime("%Y%m%d") + '_ASEAN40.csv.tmp', 'r') as data:
    	plaintext = data.read()
    	pattern = re.compile(r'(""){1,}')
    	plaintext = re.sub(pattern, ',', plaintext)
    	pattern = re.compile(r'(,){2,}')
    	plaintext = re.sub(pattern, ',', plaintext)
    data = open(str_pathPCF + 'PCF_' + datetime.strptime(str_DivDate, "%Y-%m-%d").strftime("%Y%m%d") + '_ASEAN40.csv.tmp', 'w')
    data.write(plaintext)
    
    # To switch on when it goes live E:\DMA\Prod\BMO\BMO_TMP

#ThanosCode()





def pcf_CimbFtseAsean40(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        # Special Treatment on Passwrod Excel: we do all sheet at once (dico of dico of dataframe) (fl.fDf_readExcelWithPassword)
        df_Summary =    dic_df['FOL_Hold']['Summary']
        df_Equity =     dic_df['FOL_Hold']['Equity']
        df_Div_Data =   dic_df['FOL_Hold']['Div']
        df_EstCash =    dic_df['FOL_Hold']['Est Cash']  
        try:        df_Rebal = dic_df['FOL_Rebal']
        except:     df_Rebal = None
        try:        df_compo = dic_df['SQL_comp']
        except:     df_compo = None
        str_folder= dic_df['Folder']
    except Exception as err:    return 'ERROR: Dataframe - {} | {}'.format(str_PCF, str(err)), []
    
    # PCF Date
    try:
        str_DivDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_inputdate, "%Y-%m-%d", 1, '367')
        dte_DivDate = datetime.strptime(str_DivDate, "%Y-%m-%d")        
    except Exception as err:    return 'ERROR: PCF Date - {} | {}'.format(str_PCF, str(err)), []
    
    l_pcfFileName = ['PCF_{}_ASEAN40.xls'.format(dte_DivDate.strftime('%Y%m%d')),
                     'PCF_{}_ASEAN40.csv'.format(dte_DivDate.strftime('%Y%m%d'))]
   
    # Rebalancing file
    try:
        df_Equity = df_Equity[df_Equity['Today Holdings'] != 0].reset_index()
        if not df_Rebal is None:
            pass
            
    except Exception as err:    return 'ERROR: Rebalancing file- {} | {}'.format(str_PCF, str(err)), []   
    
    
    
    
#    # 1. Variables
#    try:
#        str_DivDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date,'%Y%m%d', 1, 367, bl_Backward = False)
#        str_pcfDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date,'%d/%m/%Y', 1, 367, bl_Backward = False)
#        df_NAV.columns = ['Date','CODE','Units','Bid_Price']
#        flt_Nav = df_NAV[df_NAV['CODE'] == 'SG1DB9000009']['Bid_Price'].values[0]
#        flt_share = df_NAV[df_NAV['CODE'] == 'SG1DB9000009']['Units'].values[0]
#        int_CreationUnits = 50000
#        if len(df_FundDiv) > 0:     
#            flt_FundDiv = df_FundDiv['NetAmount'].sum()
#            flt_Nav = (flt_Nav - flt_FundDiv)
#        if len(df_PAF) > 0:         
#            flt_PAF = df_PAF['PriceAdjustmentFactor'].sum()
#            flt_Nav = flt_Nav * flt_PAF
#            flt_share = flt_share / flt_PAF
#    except Exception as err:    return 'ERROR: 1. Variables - {} | {}'.format(str_PCF, str(err)), []
#    
#    # 2. reform Holdings DF
#    try:
#        # just take some rows of your Compo DATAFRAME
#        df_COMPO.columns = ['Company Name', 'Quantity', 'Currency', 'Unit Cost', 'Book Value', 'Price', ' Market Value',
#                            'Accrued', 'Total Market', 'Total G/L', 'Col11', 'RIC', 'ISIN']
#        int_endCompo = int(pd.DataFrame([i for i, x in enumerate(df_COMPO['Company Name'] == 'TOTAL ORDINARY SHARES') if x]).iloc[0])
#        df_COMPO = dframe.fDf_CleanPrepareDF(df_COMPO.iloc[10:int_endCompo], l_colToDropNA = ['Quantity'], 
#                                             l_colToBeFloat = ['Quantity','Price'], l_colSort = ['ISIN'])
#        df_COMPO['ISIN'] = df_COMPO['ISIN'].str.upper()
#        # Add new columns
#        df_COMPO['Shares (Basket)'] = ((df_COMPO['Quantity'] / (flt_share / int_CreationUnits)).apply(np.trunc)).astype(int)
#    except Exception as err:    return 'ERROR: 2. reform Holdings DF - {} | {}'.format(str_PCF, str(err)), []
#    
#    # 2.2 Check Error on Input files
#    try:
#        for it_comp in range(len(df_COMPO)):
#            if len(df_COMPO['ISIN'].iloc[it_comp]) != 12:
#                print('  ERROR: The ISIN column in the vendor file contains a non valid ISIN identifier (more than 12 char)')
#                print('  * No output has been generated')
#                print('  - Value that caused the error: {}'.format(str(df_COMPO['ISIN'].iloc[it_comp])))
#                return str_resultFigures, []
#    except Exception as err:    return 'ERROR: 2.2 Check Error on Input files - {} | {}'.format(str_PCF, str(err)), []
#    
#    # 3. Reform FX DF
#    try:
#        # just take some rows of your Compo DATAFRAME
#        int_lenCol = len(df_FX.columns)
#        df_FX.columns = ['1', 'Currency', 'Description', 'Close_Price', 'Exchange Rate', 'Fx_secondary', ' Date'][:int_lenCol]
#        df_FX = df_FX[['Currency','Exchange Rate']].copy()
#        df_FX['Currency'].replace(['SGD=', 'HKD=', 'AUD=', 'CNY=', 'THB='], ['SGD', 'HKD', 'AUD', 'CNY', 'THB'], inplace=True)
#        df_FX = dframe.fDf_DropRowsIfNa_resetIndex(df_FX, ['Exchange Rate'])
#        df_FX = dframe.fDf_fillColUnderCondition(df_FX, 'Exchange Rate', lambda x:1/x, 'Currency', 'AUD', True)
#        df_FX.loc[len(df_FX)] = ['USD',1.0]
#        df_COMPO = dframe.fDf_JoinDf(df_COMPO, df_FX, 'Currency', 'left')
#    except Exception as err:    return 'ERROR: 3. reform FX DF - {} | {}'.format(str_PCF, str(err)), []
#    
#    # 4. Dividend & Change df_COMPO
#    try:
#        df_codePivot = pp.fDf_phillipCap_GetPivotCode_wDiv(df_COMPO, 'RIC', str_folder + 'raw', 
#                                                           'PivotCode_uk_PhilippCap.csv', str_DivDate)
#        df_COMPO = pd.merge(df_COMPO, df_codePivot, on = 'RIC', how = 'left')
#        df_COMPO['AdjustedPrice'] = df_COMPO['Price'] - df_COMPO['GrossAmount']
#        df_COMPO['1_col'] = ''
#        df_COMPO = df_COMPO[['1_col','Company Name', 'Currency', 'AdjustedPrice', 'Shares (Basket)',
#                             'ISIN', 'Sedol', 'RIC', 'Bloomberg', 'Exchange Rate', 'Quantity']].copy()
#    except Exception as err:    return 'ERROR: 4. Dividend & Change df_COMPO - {} | {}'.format(str_PCF, str(err)), []
#    
#    # 5. Re-Made FX
#    try:
#        df_Forex = dframe.fDf_FilterOnCol(df_FX, 'Currency', ['AUD', 'CNY', 'HKD', 'SGD', 'THB'])
#        df_Forex['Close Date'] = dte_date.strftime("%m/%d/%Y")
#        df_Forex['Currency Code'] = df_Forex['Currency']
#        df_Forex['From Currency'] = df_Forex['Currency']
#        # Dont know how to do ...
#        df_Forex = dframe.fDf_fillColUnderCondition(df_Forex, 'From Currency', 'Australian Dollar', 'Currency', 'AUD')
#        df_Forex = dframe.fDf_fillColUnderCondition(df_Forex, 'From Currency', 'Chinese Renminbi', 'Currency', 'CNY')
#        df_Forex = dframe.fDf_fillColUnderCondition(df_Forex, 'From Currency', 'Hong Kong Dollar', 'Currency', 'HKD')
#        df_Forex = dframe.fDf_fillColUnderCondition(df_Forex, 'From Currency', 'Singapore Dollar', 'Currency', 'SGD')
#        df_Forex = dframe.fDf_fillColUnderCondition(df_Forex, 'From Currency', 'Thai Baht', 'Currency', 'THB')
#        df_Forex = df_Forex[['From Currency', 'Currency Code','Exchange Rate', 'Close Date']].copy()
#        df_Forex.sort_values('From Currency', inplace = True)
#    except Exception as err:    return 'ERROR: 5. FX out - {} | {}'.format(str_PCF, str(err)), []
#    
#    # 6. From Final File
#    try:
#        # MARKET CAP
#        flt_MarketCap = (df_COMPO['AdjustedPrice'] * df_COMPO['Shares (Basket)'] * df_COMPO['Exchange Rate']).sum()
#        # HEADER LEVEL OUTPUT
#        df_PCFHeader = pd.DataFrame(columns = range(3))
#        df_PCFHeader.loc[0] = ['', '', '']
#        df_PCFHeader.loc[1] = ['', '', '']
#        df_PCFHeader.loc[2] = ['', 'Phillip Capital', '']
#        df_PCFHeader.loc[3] = ['', '', '']
#        df_PCFHeader.loc[4] = ['', 'Indicative Creation / Redemption basket Composition for trade date', str_pcfDate]
#        df_PCFHeader.loc[5] = ['', '', '']
#        df_PCFHeader.loc[6] = ['', 'FUND INFORMATION', '']
#        df_PCFHeader.loc[7] = ['', 'Fund Name', 'PHILLIP SGX APAC DIVIDEND LEADERS REIT ETF']
#        df_PCFHeader.loc[8] = ['', 'ISIN', 'SG1DB9000009']
#        df_PCFHeader.loc[9] = ['', 'BBG Ticker', 'PAREIT SP Equity']
#        df_PCFHeader.loc[10] = ['', 'Reuters', 'PHIL.SI']
#        df_PCFHeader.loc[11] = ['', 'Fund Currency', 'USD']
#        df_PCFHeader.loc[12] = ['', 'NAV per Share', flt_Nav]
#        df_PCFHeader.loc[13] = ['', 'Number of Fund Shares in Issue', flt_share]
#        df_PCFHeader.loc[14] = ['', 'Total NAV of Basket', flt_Nav * int_CreationUnits]
#        df_PCFHeader.loc[15] = ['', 'Estimated Cash Position of Basket', round((flt_Nav * int_CreationUnits) - (flt_MarketCap), 2)]
#        df_PCFHeader.loc[16] = ['', 'Creation Redemption', int_CreationUnits]
#        df_PCFHeader.loc[17] = ['', '', '']
#        # ADD a title row
#        df_COMPO.columns = ['', 'Company Name', 'Currency', 'Price', 'Shares (Basket)', 'ISIN', 'SEDOL', 
#                            'RIC', 'Bloomberg', 'FX Rate', 'Shares (Fund)']
#        # CONCAT
#        df_PCF = dframe.fDf_Concat_wColOfDf1(df_PCFHeader, df_COMPO, bl_colDf2_AsARow = True)
#    except Exception as err:    return 'ERROR: 6. From Final File - {} | {}'.format(str_PCF, str(err)), []
#    
#    # 7. Create the files
#    try:
#        # FX
#        str_path0 = fl.fStr_BuildPath(str_folder, l_pcfFileName[0])
#        str_path0 = fl.fStr_createExcel_1Sh(str_path0, '', df_Forex, bl_header = True)
#        fl.fStr_StyleIntoExcel(str_path0, str_styleName = 'Border_Header', l_border = ['thin', 'FF000000'])                                                             
#        # PCF 
#        str_path1 = fl.fStr_BuildPath(str_folder, l_pcfFileName[1])
#        str_path1 = fl.fStr_createExcel_1Sh(str_path1, '', df_PCF)
#        l_pathAttach = [str_path0, str_path1]
#    except Exception as err:    return 'ERROR: 7. Create the files - {} | {}'.format(str_PCF, str(err)), []

    # Create the folder liste
    str_path0 = fl.fStr_BuildPath(str_folder, l_pcfFileName[0])
    str_path1 = fl.fStr_BuildPath(str_folder, l_pcfFileName[1])
    str_path2 = str_path1.replace('.csv','.csv.tmp')
    l_pathAttach = [str_path0, str_path2]
    l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    

    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________

