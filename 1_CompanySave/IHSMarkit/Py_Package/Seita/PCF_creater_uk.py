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
        str_path0 = fl.fStr_BuildPath(str_folder, l_pcfFileName[0])
        str_path1 = fl.fStr_BuildPath(str_folder, l_pcfFileName[1])
        str_path0 = fl.fStr_createExcel_1Sh(str_path0, '', df_Forex, bl_header = True)
        str_path1 = fl.fStr_createExcel_1Sh(str_path1, '', df_PCF)
        # add some style in FX output df
        fl.fStr_StyleIntoExcel(str_path0, str_styleName = 'Border_Header', l_border = ['thin', 'FF000000'])
        # END, path to return
        l_pathAttach = [str_path0, str_path1]
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except Exception as err:    return 'ERROR: 7. Create the files - {} | {}'.format(str_PCF, str(err)), []

    

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



def fDf_flt_rebalanceOnEquity(df_Equity, df_Rebal, df_compoIndex):
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
		
    # df_compoIndex
    df_compoIndex = df_compoIndex[['Ric', 'Price', 'FXRate']]
    df_compoIndex = df_compoIndex.rename(columns={'Ric': 'RicInIndex', 'Price': 'PriceInIndex', 'FXRate': 'FXRateInIndex'})
    df_Equity = df_Equity.merge(df_compoIndex, left_on='RIC Code', right_on = 'RicInIndex', how = 'left')
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
                df_AdditionsCurrency['FX Rate'] = 1 / df_AdditionsCurrency['FXRateInIndex']
            df_AdditionsCurrency = df_AdditionsCurrency[['RIC Code', 'FX Rate']].copy()
            df_Equity = df_Equity.merge(df_AdditionsCurrency, how='left')
            df_Equity['Exchange rate'] = df_Equity['Exchange rate'].fillna(df_Equity['FX Rate'])
    flt_RebalanceCash = (df_Equity['Execution Net Local'] * (1 / df_Equity['Exchange rate'])).sum()
    
    return df_Equity, flt_RebalanceCash




def ThanosCode():
    str_folderRoot = r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Auto_py' + '\\'
    
    ### Dates
    dte_inputdate = (datetime.now() - BDay(3)).date()
    print('dte_inputdate', dte_inputdate)
    inputdate = dte_inputdate.strftime("%Y%m%d")
    #    inputdate = '20200722' # Manual date bypass - 'yyyymmdd'
    rebalanceinputdate = datetime.strptime(inputdate, "%Y%m%d").strftime("%d%b%Y")    
    str_DivDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_inputdate, "%Y-%m-%d", 1, '367')
    dte_DivDate = datetime.strptime(str_DivDate, "%Y-%m-%d").date()
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
    df_compoIndex = pd.read_sql(querystring, con)
    
    ### Getting Fund Ref Data
    querystring = "select * from tblCodePivot where Isin = 'SG1T81931787' AND CurrencyCode = 'USD'"
    cur.execute(querystring)
    cur.commit()
    df_FundRefData = pd.read_sql(querystring, con)
    
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
    df_Summary = df_Summary.iloc[-30:].copy()
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
    # TO GO ON SEITA Operation on Input Sheet
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
            df_Equity, flt_RebalanceCash = fDf_flt_rebalanceOnEquity(df_Equity, df_Rebal, df_compoIndex)
    df_Equity['Exchange rate'] = df_Equity['Exchange rate'].astype(float)
    # Operation on df_Div_Data
    int_DivData_End = int(df_Div_Data.loc[df_Div_Data['Stock name'] == 'UNDERLYING'].index.values)
    df_Div_Data = df_Div_Data[0:int_DivData_End]
    #    df_Div_Data['Ex-date '] = pd.to_datetime(df_Div_Data['Ex-date ']).apply(lambda x: x.date())
    df_Div_Data = df_Div_Data[df_Div_Data['Ex-date '].astype('str') == str_DivDate]
    df_Div_Data = df_Div_Data[['Stock name', 'Net Rate']]
    # Operation on df_EstCash
    df_EstCash.columns = ['ColumnA','ColumnB','ColumnC','ColumnD','ColumnE']
    
    # VARIABLES
    #    FundIsin = 'SG1T81931787'
    #    FundCurrency = 'USD'
    FundName = 'ETF CIMB ASEAN 40' # not pulling from SOLA to keep it consistent with legacy
    CreationRedemption = 50000
    print(df_Summary)
    NAV = df_Summary.loc[df_Summary['Pricing Date'] == dte_inputdate, 'NAV \n(Per Unit)'].iloc[0]
    FundNOSH = df_Summary.loc[df_Summary['Pricing Date'] == dte_inputdate, 'Outstanding Units'].iloc[0]
    TotalFundNAV = df_Summary.loc[df_Summary['Pricing Date'] == dte_inputdate, 'Total NAV'].iloc[0]
    flt_NumberofBaskets = FundNOSH / CreationRedemption
    Liquidity = df_EstCash.loc[df_EstCash['ColumnA'] == 'liquidity as of Pricing Date', 'ColumnB'].iloc[0]
    NetInOutFlow = df_EstCash.loc[df_EstCash['ColumnD'] == 'Net In/outflow:', 'ColumnE'].iloc[0]
    # Payables = df_EstCash.loc[df_EstCash['ColumnA'] == 'Payable & Receivables for Rebalancing Trades', 'ColumnB'].fillna(0).iloc[0]
    DivDistr = df_EstCash.loc[df_EstCash['ColumnA'] == 'Dividend Distribution', 'ColumnB'].fillna(0).iloc[0]
    flt_UnequitizedCashOfFund = Liquidity + NetInOutFlow + DivDistr # + Payables
    flt_UnequitizedCash = flt_UnequitizedCashOfFund / flt_NumberofBaskets
    
    
    # Create PCF: Composition
    df_hold = df_Equity.copy()
    df_hold['1Col'] = ''
    df_hold['Shares'] = (df_hold['Today Holdings'] / flt_NumberofBaskets).astype(int)
    df_hold['FX Rate'] = (1 / df_hold['Exchange rate'])
    df_hold = df_hold[['1Col', 'Name', 'CCY', 'Today Closing Price', 'Shares', 'SEDOL', 'RIC Code', 'FX Rate']]
    df_hold.columns = ['', 'Company Name', 'Currency', 'Price', 'Shares', 'SEDOL', 'RIC', 'FX Rate']
    # Pivot: getting the Isin from Ric
    df_codePivot = pp.Asean40_GetPivotCode(df_Equity, 'RIC Code', str_folderRoot + 'file', 'PivotCode_Asean40.csv')    
    # Merge 
    df_hold = df_hold.merge(df_codePivot)
    df_hold = df_hold.merge(df_Div_Data, left_on='Company Name', right_on='Stock name', how='outer').fillna(0)
    # Cash
    flt_EquitizedCash = (((df_Equity['Today Holdings'] / flt_NumberofBaskets) - df_hold['Shares']) * df_hold['Price'] * df_hold['FX Rate']).sum()
    flt_CashFromDividends = (df_hold['Net Rate'] * df_hold['Shares'] * df_hold['FX Rate']).sum() 
    flt_Fees = 0.0065 * (dte_DivDate - dte_inputdate).days / 365 * (TotalFundNAV / flt_NumberofBaskets)
    flt_EstimatedCash = flt_UnequitizedCash + flt_EquitizedCash + flt_CashFromDividends 
    flt_EstimatedCash = flt_EstimatedCash + (flt_RebalanceCash / flt_NumberofBaskets) - flt_Fees
     # Back to Composition
    df_hold['Price'] = df_hold['Price'] - df_hold['Net Rate']
    # Diplaying a smaller number of decimal points for FX Rate
    df_hold['FX Rate'] = df_hold['FX Rate'].map('{:,.7f}'.format)  
    df_hold = df_hold[['', 'Company Name', 'Currency', 'Price', 'Shares', 'ISIN', 'SEDOL', 'RIC', 'FX Rate']]   
    
    ### Header Level Output
    df_Head = pd.DataFrame(columns=('', 'Company Name', 'Currency', 'Price', 'Shares', 'ISIN', 'SEDOL', 'RIC', 'FX Rate'))
    df_Head.loc[0] = ['', '', '', '', '', '', '', '', '']
    df_Head.loc[1] = ['', '', '', '', '', '', '', '', '']
    df_Head.loc[2] = ['', 'CIMB ETF', '', '', '', '', '', '', '']
    df_Head.loc[3] = ['', '', '', '', '', '', '', '', '']
    df_Head.loc[4] = ['', 'Indicative Creation / Redemption basket Composition for trade date', dte_DivDate.strftime("%d/%m/%Y"), '', '', '', '', '', '']
    df_Head.loc[5] = ['', '', '', '', '', '', '', '', '']
    df_Head.loc[6] = ['', 'Fund Information', '', '', '', '', '', '', '']
    df_Head.loc[7] = ['', 'Fund Name', FundName, '', '', '', '', '', '']
    df_Head.loc[8] = ['', 'ISIN',  df_FundRefData['Isin'].iloc[0], '', '', '', '', '', '']
    df_Head.loc[9] = ['', 'BBG Ticker', df_FundRefData['Bloomberg'].iloc[0].replace('Equity', '').strip(), '', '', '', '', '', '']
    df_Head.loc[10] = ['', 'Reuters', df_FundRefData['Ric'].iloc[0], '', '', '', '', '', '']
    df_Head.loc[11] = ['', 'Fund Currency', df_FundRefData['CurrencyCode'].iloc[0], '', '', '', '', '', '']
    df_Head.loc[12] = ['', 'NAV per Share', NAV, '', '', '', '', '', '']
    df_Head.loc[13] = ['', 'Number of Fund Shares in Issue', FundNOSH, '', '', '', '', '', '']
    df_Head.loc[14] = ['', 'Total NAV of Fund per Creation / Redemption Unit', TotalFundNAV / flt_NumberofBaskets, '', '', '', '', '', '']
    df_Head.loc[15] = ['', 'Total Cash Position of Fund per Creation / Redemption Unit', flt_EstimatedCash, '', '', '', '', '', '']
    df_Head.loc[16] = ['', 'Creation Redemption', CreationRedemption, '', '', '', '', '', '']
    
    # Merge Header and Compo
    df_PCF = dframe.fDf_Concat_wColOfDf1(df_Head, df_hold, True, 1)
    df_PCF_csv = df_PCF.iloc[2:, :].copy()
    #    df_Head.loc[17] = ['', '', '', '', '', '', '', '', '']
    #    df_Head.loc[18] = ['', 'Company Name', 'Currency', 'Price', 'Shares', 'ISIN', 'SEDOL', 'RIC', 'FX Rate']
    #    ### Main Output
    #    df_PCF = df_Head.append(df_hold)
    
    # Create Files
    str_path = str_pathPCF + 'PCF_{}_ASEAN40'.format(dte_DivDate.strftime("%Y%m%d"))
    fl.fStr_createExcel_1Sh(str_path + '.xls', '', df_PCF, bl_header = False)
    fl.fStr_CreateTxtFile(str_path + '.csv.tmp', '', df_PCF_csv, bl_header = False, bl_index = False, o_quoting = csv.QUOTE_NONNUMERIC)
    
    with open(str_path + '.csv.tmp', 'r') as data:
    	plaintext = data.read()
    	pattern = re.compile(r'(""){1,}')
    	plaintext = re.sub(pattern, ',', plaintext)
    	pattern = re.compile(r'(,){2,}')
    	plaintext = re.sub(pattern, ',', plaintext)
    data = open(str_path + '.csv.tmp', 'w')
    data.write(plaintext)
    
    
#if __name__ == '__main__':
#    ThanosCode()




def pcf_CimbFtseAsean40(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        # Special Treatment on Passwrod Excel: we do all sheet at once (dico of dico of dataframe) (fl.fDf_readExcelWithPassword)
        df_Summary =    dic_df['FOL_Hold']['Summary']
        df_Equity =     dic_df['FOL_Hold']['Equity']
        df_Div_Data =   dic_df['FOL_Hold']['Div']
        df_EstCash =    dic_df['FOL_Hold']['Est Cash']  
        df_FundRefData= dic_df['SQL_FundRefData']
        try:        df_Rebal = dic_df['FOL_Rebal']
        except:     df_Rebal = None
        try:        df_compoIndex = dic_df['SQL_comp']
        except:     df_compoIndex = None
        str_folder= dic_df['Folder']
    except Exception as err:    return 'ERROR: Dataframe - {} | {}'.format(str_PCF, str(err)), []
    
    # PCF Date
    try:
        dte_date = dte_date.date()
        str_DivDate = dat.fDat_GetCorrectOffsetDate_Calendar(dte_date, "%Y-%m-%d", 1, '367')
        dte_DivDate = datetime.strptime(str_DivDate, "%Y-%m-%d").date()
    except Exception as err:    return 'ERROR: PCF Date - {} | {}'.format(str_PCF, str(err)), []
    
    l_pcfFileName = ['PCF_{}_ASEAN40.xls'.format(dte_DivDate.strftime('%Y%m%d')),
                     'PCF_{}_ASEAN40.csv.tmp'.format(dte_DivDate.strftime('%Y%m%d'))]
   
    # Operation on Input df
    try:
        # Operation on df_Summary
        df_Summary['Pricing Date'] = df_Summary['Pricing Date'].apply(lambda x:x.date())
        df_Summary = df_Summary[df_Summary['Pricing Date'] == dte_date]
        # Operation on df_Equity
        df_Equity = df_Equity[df_Equity['Today Holdings'] != 0].reset_index()
        flt_RebalanceCash = 0
        if not df_Rebal is None:
            if df_Rebal['Acct'].iloc[0] != 'FTSE':
                print('''The value under the "Acct" column in the rebalance file is not #FTSE#,                  
                      make sure you have the correct file and run the script again.''')
            else:
                df_Equity, flt_RebalanceCash = fDf_flt_rebalanceOnEquity(df_Equity, df_Rebal, df_compoIndex)
        df_Equity['Exchange rate'] = df_Equity['Exchange rate'].astype(float)
        # Operation on df_Div_Data
        int_DivData_End = int(df_Div_Data.loc[df_Div_Data['Stock name'] == 'UNDERLYING'].index.values)
        df_Div_Data = df_Div_Data[0:int_DivData_End]
        #    df_Div_Data['Ex-date '] = pd.to_datetime(df_Div_Data['Ex-date ']).apply(lambda x: x.date())
        df_Div_Data = df_Div_Data[df_Div_Data['Ex-date '].astype('str') == str_DivDate]
        df_Div_Data = df_Div_Data[['Stock name', 'Net Rate']]
        # Operation on df_EstCash
        df_EstCash.columns = ['ColumnA','ColumnB','ColumnC','ColumnD','ColumnE']
    except Exception as err:    return 'ERROR: Operation on Input df - {} | {}'.format(str_PCF, str(err)), []   
    
    # 1. Variables
    try:
        FundName = 'ETF CIMB ASEAN 40' # not pulling from SOLA to keep it consistent with legacy
        CreationRedemption = 50000
        NAV =           df_Summary['NAV \n(Per Unit)'].iloc[0]
        FundNOSH =      df_Summary['Outstanding Units'].iloc[0]
        TotalFundNAV =  df_Summary['Total NAV'].iloc[0]
        flt_NumberofBaskets = FundNOSH / CreationRedemption
        Liquidity =     df_EstCash.loc[df_EstCash['ColumnA'] == 'liquidity as of Pricing Date', 'ColumnB'].iloc[0]
        NetInOutFlow =  df_EstCash.loc[df_EstCash['ColumnD'] == 'Net In/outflow:', 'ColumnE'].iloc[0]
        # Payables = df_EstCash.loc[df_EstCash['ColumnA'] == 'Payable & Receivables for Rebalancing Trades', 'ColumnB'].fillna(0).iloc[0]
        DivDistr =      df_EstCash.loc[df_EstCash['ColumnA'] == 'Dividend Distribution', 'ColumnB'].fillna(0).iloc[0]
        flt_UnequitizedCashOfFund = Liquidity + NetInOutFlow + DivDistr # + Payables
        flt_UnequitizedCash = flt_UnequitizedCashOfFund / flt_NumberofBaskets
    except Exception as err:    return 'ERROR: 1. Variables - {} | {}'.format(str_PCF, str(err)), []
    
    # 2. reform Holdings DF
    try:
        df_hold = df_Equity.copy()
        df_hold['1Col'] = ''
        df_hold['Shares'] = (df_hold['Today Holdings'] / flt_NumberofBaskets).astype(int)
        df_hold['FX Rate'] = (1 / df_hold['Exchange rate'])
        df_hold = df_hold[['1Col', 'Name', 'CCY', 'Today Closing Price', 'Shares', 'SEDOL', 'RIC Code', 'FX Rate']]
        df_hold.columns = ['', 'Company Name', 'Currency', 'Price', 'Shares', 'SEDOL', 'RIC', 'FX Rate']
        # Pivot: getting the Isin from Ric
        df_codePivot = pp.Asean40_GetPivotCode(df_Equity, 'RIC Code', str_folderRoot + 'file', 'PivotCode_Asean40.csv')    
        # Merge 
        df_hold = df_hold.merge(df_codePivot)
        df_hold = df_hold.merge(df_Div_Data, left_on='Company Name', right_on='Stock name', how='outer').fillna(0)
        # Cash
        flt_EquitizedCash = (((df_Equity['Today Holdings'] / flt_NumberofBaskets) - df_hold['Shares']) * df_hold['Price'] * df_hold['FX Rate']).sum()
        flt_CashFromDividends = (df_hold['Net Rate'] * df_hold['Shares'] * df_hold['FX Rate']).sum() 
        flt_Fees = 0.0065 * (dte_DivDate - dte_date).days / 365 * (TotalFundNAV / flt_NumberofBaskets)
        flt_EstimatedCash = flt_UnequitizedCash + flt_EquitizedCash + flt_CashFromDividends 
        flt_EstimatedCash = flt_EstimatedCash + (flt_RebalanceCash / flt_NumberofBaskets) - flt_Fees
         # Back to Composition
        df_hold['Price'] = df_hold['Price'] - df_hold['Net Rate']
        # Diplaying a smaller number of decimal points for FX Rate
        df_hold['FX Rate'] = df_hold['FX Rate'].map('{:,.7f}'.format)  
        df_hold = df_hold[['', 'Company Name', 'Currency', 'Price', 'Shares', 'ISIN', 'SEDOL', 'RIC', 'FX Rate']]
    except Exception as err:    return 'ERROR: 2. reform Holdings DF - {} | {}'.format(str_PCF, str(err)), []
    
    # 3. Header Level Output
    try:
        df_Head = pd.DataFrame(columns=('', 'Company Name', 'Currency', 'Price', 'Shares', 'ISIN', 'SEDOL', 'RIC', 'FX Rate'))
        df_Head.loc[0] = ['', '', '', '', '', '', '', '', '']
        df_Head.loc[1] = ['', '', '', '', '', '', '', '', '']
        df_Head.loc[2] = ['', 'CIMB ETF', '', '', '', '', '', '', '']
        df_Head.loc[3] = ['', '', '', '', '', '', '', '', '']
        df_Head.loc[4] = ['', 'Indicative Creation / Redemption basket Composition for trade date', dte_DivDate.strftime("%d/%m/%Y"), '', '', '', '', '', '']
        df_Head.loc[5] = ['', '', '', '', '', '', '', '', '']
        df_Head.loc[6] = ['', 'Fund Information', '', '', '', '', '', '', '']
        df_Head.loc[7] = ['', 'Fund Name', FundName, '', '', '', '', '', '']
        df_Head.loc[8] = ['', 'ISIN',  df_FundRefData['Isin'].iloc[0], '', '', '', '', '', '']
        df_Head.loc[9] = ['', 'BBG Ticker', df_FundRefData['Bloomberg'].iloc[0].replace('Equity', '').strip(), '', '', '', '', '', '']
        df_Head.loc[10] = ['', 'Reuters', df_FundRefData['Ric'].iloc[0], '', '', '', '', '', '']
        df_Head.loc[11] = ['', 'Fund Currency', df_FundRefData['CurrencyCode'].iloc[0], '', '', '', '', '', '']
        df_Head.loc[12] = ['', 'NAV per Share', NAV, '', '', '', '', '', '']
        df_Head.loc[13] = ['', 'Number of Fund Shares in Issue', FundNOSH, '', '', '', '', '', '']
        df_Head.loc[14] = ['', 'Total NAV of Fund per Creation / Redemption Unit', TotalFundNAV / flt_NumberofBaskets, '', '', '', '', '', '']
        df_Head.loc[15] = ['', 'Total Cash Position of Fund per Creation / Redemption Unit', flt_EstimatedCash, '', '', '', '', '', '']
        df_Head.loc[16] = ['', 'Creation Redemption', CreationRedemption, '', '', '', '', '', '']
    except Exception as err:    return 'ERROR: 3. Header Level Output - {} | {}'.format(str_PCF, str(err)), []
    
    # 7. Create the files
    try:
        # Merge Header and Compo
        df_PCF = dframe.fDf_Concat_wColOfDf1(df_Head, df_hold, True, 1)
        df_PCF_csv = df_PCF.iloc[2:, :].copy()
        # Create Files
        str_path_xls = fl.fStr_BuildPath(str_folder, l_pcfFileName[0])
        str_path_tmp = fl.fStr_BuildPath(str_folder, l_pcfFileName[1])
        fl.fStr_createExcel_1Sh(str_path_xls, '', df_PCF, bl_header = False)
        fl.fStr_CreateTxtFile(str_path_tmp, '', df_PCF_csv, bl_header = False, bl_index = False, o_quoting = csv.QUOTE_NONNUMERIC)
        # Change slighlty the csv - tmp
        with open(str_path_tmp, 'r') as data:
        	plaintext = data.read()
        	pattern = re.compile(r'(""){1,}')
        	plaintext = re.sub(pattern, ',', plaintext)
        	pattern = re.compile(r'(,){2,}')
        	plaintext = re.sub(pattern, ',', plaintext)
        data = open(str_path_tmp, 'w')
        data.write(plaintext)
        # Final Path to retrun
        l_pathAttach = [str_path_xls, str_path_tmp]
        l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    except Exception as err:    return 'ERROR: 7. Create the files - {} | {}'.format(str_PCF, str(err)), []
    
    #    # Create the folder liste
    #    str_path0 = fl.fStr_BuildPath(str_folder, l_pcfFileName[0])
    #    str_path1 = fl.fStr_BuildPath(str_folder, l_pcfFileName[1])
    #    str_path2 = str_path1.replace('.csv','.csv.tmp')
    #    l_pathAttach = [str_path0, str_path2]
    #    l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]

    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________

