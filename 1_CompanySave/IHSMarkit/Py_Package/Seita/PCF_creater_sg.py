import pandas as pd
import PCF_genericProcess as pp
import fct_Date as dat
import fct_DB as db
import fct_dataframe as dframe
import fct_Files as fl

#------------------------------------------------------------------------------
# Singapore
#------------------------------------------------------------------------------
def pcf_sgEasyMsci(str_PCF, str_folderRoot, dte_date, str_resultFigures, dic_df):
    # Dataframe
    try:
        df_1NavIndic =  dic_df['fol_1Nav_Indicative']
        df_2Val_Dmc =   dic_df['out_2Val_Dmc']
        df_FX =         dic_df['sql_FX']
        str_folder =    dic_df['Folder']
        l_pathAttach = []
        l_pathAttach_1 = []
        l_pathAttach_2 = []
        l_pathAttach_3 = []
        l_pathAttach_4 = []
    except Exception as err:    return 'ERROR: Dataframe - {} | {}'.format(str_PCF, str(err)), []
    
    # 0. Define the perimeter + Input 3 : Get Composition
    try:
        df_lConfig = pd.read_csv(fl.fStr_BuildPath(str_folderRoot, r'file\SgEasy_listPerimeter.csv'))
        # DATE NAV
        dte_navDate = df_1NavIndic[df_1NavIndic['Fund Code'] == 'LU1753045332']['Index Date'].values[0]
        dte_navDate = dat.fDte_formatToDate(str(dte_navDate), '%d/%m/%Y')
        str_req = """exec spExcelGetComposition @Code = '<RIC>',@AsAtDate = '<DATE>', @RequestedSecurityType = 'Index',@DateType = 'Open'"""
        d_CompoDf = pp.fDdf_loopOnRic_SqlReq_SaveCsv(df_lConfig, str_req, dte_date, str_folder, '_comp')
        # SecurityName
        df_SecurityName = pd.read_csv(fl.fStr_BuildPath(str_folderRoot, r'file\SgEasy_SecurityName.csv'))
    except Exception as err:    return 'ERROR: 1. Input 3 : Get Composition - {} | {}'.format(str_PCF, str(err)), []
    
    str_req_CA = """SET NOCOUNT ON;
                    IF OBJECT_ID ('tempdb..#Listing') IS NOT NULL DROP TABLE #Listing
                    DECLARE @Filter NVARCHAR(255)
                    DECLARE @FamilyID BIGINT
                    DECLARE @RIC NVARCHAR(50) = '<RIC>'
                    SELECT @Filter = MIN(Filter) FROM vwIndexSummary WHERE Ric = @RIC
                    SELECT @FamilyID = MIN(FamilyID) FROM vwIndexSummary WHERE Ric = @RIC
                    SELECT @FamilyID = MIN(RefFamilyID) FROM tblFamily WHERE FamilyID = @FamilyID
                    SELECT ListingID into #Listing FROM  tblConstituent c WHERE FamilyID = @FamilyID and FilterValue like @Filter 
                    and CURRENT_TIMESTAMP BETWEEN StartDate AND EndDate
                    SELECT s.Isin, s.Ric, ca.* 
                    FROM tblDistribution ca   
                    	JOIN vwSecurityListing s on ca.ListingID = s.ListingID
                    	JOIN #Listing l ON l.ListingID = s.ListingID
                    WHERE CorporateActionSetID = 1 AND CorporateActionTypeID = 1 AND ca.XdDate = '<DATE>'
                    ORDER BY Ric asc, ca.XdDate desc
                    IF OBJECT_ID ('tempdb..#Listing') IS NOT NULL DROP TABLE #Listing"""
                    
    # 1. DividendReinvestOptions = 1
    if not [x for x in ['_2','_3','_4'] if x in str_PCF]:
        try:
            df_lConfig_1 = df_lConfig.loc[df_lConfig['DividendReinvestOptions'] == 'FundRMethod 1']
            df_EPRAtax_perMic = pd.read_csv(fl.fStr_BuildPath(str_folderRoot, r'file\SgEasy_EPRA_Tax.csv'))
            # Create Files for Output
            d_param = {'DivMethod':1,               'dte_date': dte_date,           'dte_navDate': dte_navDate,     'str_folder': str_folder,
                       'df_lConfig': df_lConfig_1,  'df_1NavIndic': df_1NavIndic,   'df_2Val_Dmc': df_2Val_Dmc,     'df_FX':df_FX,     
                       'd_CompoDf': d_CompoDf,      'd_CorpActDf': df_EPRAtax_perMic,'df_SecurityName':df_SecurityName}
            l_pathAttach_1 = pp.fLpath_loopOnRic_CreateFile(d_param)
        except Exception as err:    return 'ERROR: 1. DividendReinvestOptions = 1 - {} | {}'.format(str_PCF, str(err)), []
        
    # 2. DividendReinvestOptions = 2
    if not [x for x in ['_1','_3','_4'] if x in str_PCF]:
        try:
            df_lConfig_2 = df_lConfig.loc[df_lConfig['DividendReinvestOptions'] == 'FundRMethod 2']
            # Input 4 : Corporate Actions
            d_CorpActDf = pp.fDdf_loopOnRic_SqlReq_SaveCsv(df_lConfig_2, str_req_CA, dte_navDate, str_folder, '_CA')
            # Create Files for Output
            d_param = {'DivMethod':2,               'dte_date': dte_date,           'dte_navDate': dte_navDate,     'str_folder': str_folder,
                       'df_lConfig': df_lConfig_2,  'df_1NavIndic': df_1NavIndic,   'df_2Val_Dmc': df_2Val_Dmc,     'df_FX':df_FX,     
                       'd_CompoDf': d_CompoDf,      'd_CorpActDf': d_CorpActDf,     'df_SecurityName':df_SecurityName}
            l_pathAttach_2 = pp.fLpath_loopOnRic_CreateFile(d_param)
        except Exception as err:    return 'ERROR: 2. DividendReinvestOptions = 2 - {} | {}'.format(str_PCF, str(err)), []
    
    # 3. DividendReinvestOptions = 3
    if not [x for x in ['_1','_2','_4'] if x in str_PCF]:
        try:
            df_lConfig_3 = df_lConfig.loc[df_lConfig['DividendReinvestOptions'] == 'FundRMethod 3']
            # Create Files for Output
            d_param = {'DivMethod':3,               'dte_date': dte_date,           'dte_navDate': dte_navDate,     'str_folder': str_folder,
                       'df_lConfig': df_lConfig_3,  'df_1NavIndic': df_1NavIndic,   'df_2Val_Dmc': df_2Val_Dmc,     'df_FX':df_FX,     
                       'd_CompoDf': d_CompoDf,      'd_CorpActDf': None,            'df_SecurityName':df_SecurityName}
            l_pathAttach_3 = pp.fLpath_loopOnRic_CreateFile(d_param)
        except Exception as err:    return 'ERROR: 3. DividendReinvestOptions = 3 - {} | {}'.format(str_PCF, str(err)), []
    
    # 4. DividendReinvestOptions = 4
    if not [x for x in ['_1','_2','_3'] if x in str_PCF]:
        try:
            df_lConfig_4 = df_lConfig.loc[df_lConfig['DividendReinvestOptions'] == 'FundRMethod 4']
            # Input 4 : Corporate Actions
            d_CorpActDf = pp.fDdf_loopOnRic_SqlReq_SaveCsv(df_lConfig_4, str_req_CA, dte_navDate, str_folder, '_CA')
            # Create Files for Output
            d_param = {'DivMethod':4,               'dte_date': dte_date,           'dte_navDate': dte_navDate,     'str_folder': str_folder,
                       'df_lConfig': df_lConfig_4,  'df_1NavIndic': df_1NavIndic,   'df_2Val_Dmc': df_2Val_Dmc,     'df_FX':df_FX,     
                       'd_CompoDf': d_CompoDf,      'd_CorpActDf': d_CorpActDf,     'df_SecurityName':df_SecurityName}
            l_pathAttach_4 = pp.fLpath_loopOnRic_CreateFile(d_param)
        except Exception as err:    return 'ERROR: 4. DividendReinvestOptions = 4 - {} | {}'.format(str_PCF, str(err)), []
    
    l_pathAttach = l_pathAttach_1 + l_pathAttach_2 + l_pathAttach_3 + l_pathAttach_4
    l_pathAttach = [path.replace(str_folderRoot, '') for path in l_pathAttach]
    
    # 5. Parallel Run: Order by ISIN the Manual Py
    if not [x for x in ['_1','_2','_3','_4'] if x in str_PCF]:
        try:
            pp.Act_OrderByIsin_Easy(df_lConfig, str_folder, dte_date)
        except Exception as err:    return 'ERROR: 4. DividendReinvestOptions = 4 - {} | {}'.format(str_PCF, str(err)), []
    
    return str_resultFigures, l_pathAttach
#___________________________________________________________________________________________




#------------------------------------------------------------------------------
# Function for SG Easy Msci
#------------------------------------------------------------------------------
def Act_OrderByIsin_Easy(df_lConfig, str_folder, dte_date):
    str_folder = str_folder.replace('Auto_py', 'Manual_py')
    # Loop on parameters
    for i_row, t_row in df_lConfig.iterrows():
        df_pcf = None
        df_compo = None
        df_header = None
        try:
            str_pcfFilename =  '{}{}.txt'.format(t_row['Pcf_FileName'], dte_date.strftime('%Y%m%d'))
            df_pcf = dframe.fDf_readCsv_enhanced(fl.fStr_BuildPath(str_folder, str_pcfFilename), bl_header = None, str_sep='\t', str_encoding = 'cp1252')
            df_header = df_pcf.iloc[0:1].copy()
            df_compo = df_pcf.iloc[1:].copy()
            l_col = list(range(50)[:len(df_compo.columns)])
            df_compo.columns = [str(x) for x in l_col]
            df_compo.rename(columns = {'3':'Isin'}, inplace = True)
            df_compo.sort_values(by = ['Isin'], ascending = True, inplace = True)
            # index
            l_col = df_compo.columns
            df_compo = dframe.fDf_InsertColumnOfIndex(df_compo)
            df_compo['11'] = df_compo['ind']
            df_compo = df_compo[l_col]
            # Concat
            df_pcf = dframe.fDf_Concat_wColOfDf1(df_header, df_compo)
            fl.fStr_CreateTxtFile(str_folder, str_pcfFilename, df_pcf, str_sep = '\t')
        except Exception as err:
            print(' ERROR on Act_OrderByIsin_Easy - PCF | {}'.format(str(err)))
            print(' - str_pcfFilename', str_pcfFilename)
        try:
            str_COfilename =  '{}_{}.txt'.format(t_row['CO_FileName'], dte_date.strftime('%Y%m%d'))
            df_CO = dframe.fDf_readCsv_enhanced(fl.fStr_BuildPath(str_folder, str_COfilename), bl_header = None, str_sep='\t', str_encoding = 'cp1252')
            df_header = df_CO.iloc[:2].copy()
            df_compo = df_CO.iloc[2:].copy()
            l_col = list(range(50)[:len(df_compo.columns)]) 
            df_compo.columns = [str(x) for x in l_col]
            df_compo.rename(columns = {'3':'Isin'}, inplace = True)
            df_compo.sort_values(by = ['Isin'], ascending = True, inplace = True)
            # index
            l_col = df_compo.columns
            df_compo = dframe.fDf_InsertColumnOfIndex(df_compo)
            df_compo['1'] = df_compo['ind']
            df_compo = df_compo[l_col]
            # Concat
            df_CO = dframe.fDf_Concat_wColOfDf1(df_header, df_compo)
            fl.fStr_CreateTxtFile(str_folder, str_COfilename, df_CO, str_sep = '\t')
        except Exception as err:
            print(' ERROR on Act_OrderByIsin_Easy - CO | {}'.format(str(err)))
            print(' - str_COfilename', str_COfilename)
    return True

    
def fDdf_loopOnRic_SqlReq_SaveCsv(df_lConfig, str_req, dte_date, str_folder, str_filenameExtension = ''):
    inst_db = db.c_sqlDB()
    inst_db.server = 'D1PRDSOLADB.infocloud.local'
    str_cloudPathForCsv = inst_db.cloudPathForCsv
    #inst_db.cloudPathForCsv = str_folder + r'\raw'
    d_Df = {}
    for i_row, t_row in df_lConfig.iterrows():
        str_IndexRic = t_row['IndexRic']
        if not str_IndexRic in d_Df:        #Avoid Double
            str_fileName =  '{}{}.csv'.format(t_row['Pcf_FileName'].replace('PCF',''), str_filenameExtension)
            str_req_loop = str_req.replace('<RIC>', str_IndexRic).replace('<DATE>', dte_date.strftime('%Y%m%d'))
            df_sqlResult = db.fDf_GetRequest_or_fromCsvFile(str_req_loop, str_fileName, 30, r'{}raw'.format(str_folder), bl_EmptyMessage = False)
            # Save into dictionary
            d_Df[str_IndexRic] = df_sqlResult
        else:   pass
    inst_db.cloudPathForCsv = str_cloudPathForCsv
    return d_Df


def fLpath_loopOnRic_CreateFile(d_param):
    try:
        int_DivMethod = d_param['DivMethod']
        df_lConfig =    d_param['df_lConfig']
        df_1NavIndic =  d_param['df_1NavIndic']
        df_2Val_Dmc =   d_param['df_2Val_Dmc']
        df_FX =         d_param['df_FX']
        df_SecurityName=d_param['df_SecurityName']
        d_CompoDf =     d_param['d_CompoDf'] 
        dte_date =      d_param['dte_date']
        dte_navDate =   d_param['dte_navDate']
        str_folder =    d_param['str_folder']
        l_pathAttach = []
    except Exception as err:    
        print('  ERROR in fLpath_loop, 0. Grab the db | {}'.format(str(err)))
        raise
        
    # Loop on parameters
    for i_row, t_row in df_lConfig.iterrows():
        try:
            # GET INPUT
            str_IndexRic =  t_row['IndexRic']
            str_ric =       t_row['ETF_RIC']
            str_isin =      t_row['Isin']
            int_divisor =   t_row['Divisor']
            flt_divFactor = t_row['divFactor']
            str_idLoop =    t_row['TrackerMnemoCode']
            str_etfCcy =    t_row['ETF CCY']
            str_indexCcy =  t_row['Underlying index CCY']
            
            # NAV Df
            if len(df_1NavIndic[df_1NavIndic['Fund Code'] == str_isin]) == 0:
                print(" WARNING: the ETF (Isin = {} , Name = {} ) is not in the 1.NavIndic File: 'NavCalcOutputs_'".format(str_isin, t_row['Pcf_FileName']))
                continue
            elif len(df_2Val_Dmc[df_2Val_Dmc['ISIN Code'] == str_isin]) == 0:
                print(" WARNING: the ETF (Isin = {} , Name = {} ) is not in the 2.Val_Dmc File: 'Last-Valuation-MARKIT-'".format(str_isin, t_row['Pcf_FileName']))
                continue
            flt_nav = df_1NavIndic[df_1NavIndic['Fund Code'] == str_isin]['Calculated Target Nav'].values[0]
            flt_nav_G2 = dframe.round_Correction(flt_nav, 4) 
            flt_TotalNav = flt_nav * int_divisor
            flt_shareNb = df_2Val_Dmc[df_2Val_Dmc['ISIN Code'] == str_isin]['Share Nb'].values[0]
            flt_indexReturn = df_1NavIndic[df_1NavIndic['Fund Code'] == str_isin]['Index Return Converted'].values[0]
            # COMPO Dataframe from dico
            df_compo =  d_CompoDf[str_IndexRic].copy()
        except Exception as err:    
            print('  ERROR in fLpath_loop, 1. Compo | {} || {}'.format(str_idLoop, str(err)))
            raise
        
        try:
            # Hedged with FX
            flt_fx_UsdToEtf = df_FX.loc[df_FX['ToCurrencyCode'] == str_etfCcy, 'Value'].values[0]
            if str_etfCcy == str_indexCcy:      flt_fx_IndexToEtf = 1
            elif str_indexCcy == 'USD':         flt_fx_IndexToEtf = flt_fx_UsdToEtf
            else:
                flt_fx_UsdToIndex = df_FX.loc[df_FX['ToCurrencyCode'] == str_indexCcy, 'Value'].values[0]
                flt_fx_IndexToEtf = flt_fx_UsdToEtf / flt_fx_UsdToIndex
            df_compo['FXRate_toEtf'] = df_compo['FXRate'] * flt_fx_IndexToEtf
            df_compo['UnadjustedPrice_fxH'] = df_compo['UnadjustedPrice'] * df_compo['FXRate_toEtf']
            # SecurityName
            df_compo = dframe.fDf_JoinDf(df_compo, df_SecurityName, 'Isin', str_how = 'left')
            df_compo['Security_Name'].fillna(df_compo['SecurityName'], inplace = True)
            #df_compo['Country_code'] = df_compo['Isin'].apply(lambda str_isin : str_isin[:2])
            df_compo['Country_code'] = df_compo['DomicileCountryCode']
            # Calculate WEIGHT + UNIT (or SHARES)
            df_compo['Weight'] = df_compo['IndexQuantity'] * df_compo['UnadjustedPrice_fxH']
            flt_MaketCap = df_compo['Weight'].sum()
            df_compo['Weight'] = df_compo['Weight'] / flt_MaketCap
            df_compo['UNIT'] = flt_TotalNav * df_compo['Weight'] / (df_compo['UnadjustedPrice_fxH'])
        except Exception as err:    
            print('  ERROR in fLpath_loop, 2. Weight | {} || {}'.format(str_idLoop, str(err)))
            raise        
        #----------------------------------------------------------------------
        # Particularity according to Div Method
        #----------------------------------------------------------------------
        try:
            if int_DivMethod == 1:
                df_EPRAtax_perMic = d_param['d_CorpActDf'].copy()
                df_compo =  dframe.fDf_JoinDf(df_compo, df_EPRAtax_perMic, 'MIC', str_how = 'left')
                df_compo.fillna({'Tax_rate' : 0}, inplace = True)
                df_compo['div_NetAmount'] = df_compo['DivAmount'] * (1-df_compo['Tax_rate'])
                df_compo['NetAmount_fxH'] = df_compo['div_NetAmount'] * df_compo['FXRate_toEtf']
                df_compo['AdjustedPrice_fxH'] = df_compo['UnadjustedPrice_fxH'] - df_compo['NetAmount_fxH']
                # Calculate WEIGHT + UNIT (or SHARES)
                df_compo['Weight'] = df_compo['IndexQuantity'] * df_compo['AdjustedPrice_fxH']
                flt_MaketCap = df_compo['Weight'].sum()
                df_compo['Weight'] = df_compo['Weight'] / flt_MaketCap
                df_compo['UNIT'] = flt_TotalNav * df_compo['Weight'] / df_compo['AdjustedPrice_fxH']
                # Get the cash
                flt_cash = 0
            elif int_DivMethod == 2 or int_DivMethod == 4:
                df_CA = d_param['d_CorpActDf'][str_IndexRic][['Isin','GrossAmount','NetAmount', 'CurrencyCode']].copy()
                df_CA.columns = ['Isin','div_GrossAmount','div_NetAmount','div_ccy']
                # Convert DIVIDEND to EUR
                df_FX_div = df_FX[['ToCurrencyCode','Value']].copy()
                df_FX_div.columns = ['div_ccy','FXRate_toDiv']
                df_FX_div['FXRate_DivToUsd'] = 1/df_FX_div['FXRate_toDiv']
                df_FX_div['FXRate_DivToEtf'] = df_FX_div['FXRate_DivToUsd'] * flt_fx_UsdToEtf
                df_CA = dframe.fDf_JoinDf(df_CA, df_FX_div, 'div_ccy')
                df_CA['div_GrossAmount_fxH'] =  df_CA['div_GrossAmount'] * df_CA['FXRate_DivToEtf']
                df_CA['div_NetAmount_fxH'] =    df_CA['div_NetAmount'] * df_CA['FXRate_DivToEtf']
                df_CA = df_CA[['Isin','div_GrossAmount_fxH','div_NetAmount_fxH']].copy()
                # Put Dividenc into Compo
                df_compo = dframe.fDf_JoinDf(df_compo, df_CA, 'Isin', str_how = 'left')
                df_compo.fillna({'div_NetAmount_fxH' : 0}, inplace = True)
                
                # Only for DIV Methode 2 
                if int_DivMethod == 2:
                    df_compo['AdjustedPrice_fxH'] = df_compo['UnadjustedPrice_fxH'] - df_compo['div_NetAmount_fxH']
                    # Get the cash
                    df_compo['CASH']  = df_compo['UNIT'] * df_compo['div_NetAmount_fxH']
                    flt_cash = df_compo['CASH'].sum() / int_divisor
                    t_row['flt_cash'] = flt_cash
                elif int_DivMethod == 4:
                    # PCF:
                    df_compo['AdjustedPrice_fxH'] = df_compo['UnadjustedPrice_fxH']
                    flt_cash = 0
                    # CO: Find the NAV other then indicative NAV (G2: only for StoxxCalc = True)
                    df_compo.fillna({'div_GrossAmount_fxH' : 0}, inplace = True)
                    df_compo['div_fxH'] = df_compo['div_NetAmount_fxH']
                    df_compo = dframe.fDf_fillColUnderCondition(df_compo, 'div_fxH', df_compo['div_GrossAmount_fxH'], 'Country_code', 'FR')
                    df_compo['div_Ratio'] = df_compo['div_fxH'] * df_compo['Weight'] / df_compo['UnadjustedPrice_fxH']
                    flt_div_Ratio = df_compo['div_Ratio'].sum()
                    flt_nav_G2 = flt_nav * (1 + flt_div_Ratio) * (1 + flt_divFactor)
                    # Calculate UNIT specific for CO on Method 4:
                    flt_CO_TotalNav = (flt_nav_G2 - flt_nav) * int_divisor
                    df_compo['Additional_Shares'] = flt_CO_TotalNav * df_compo['Weight'] / df_compo['AdjustedPrice_fxH']
                    df_compo['Additional_Shares_r'] = df_compo['Additional_Shares'].apply(lambda x:dframe.round_Correction(x, 0))
                    df_compo['CO_UNIT'] = df_compo['UNIT'] + df_compo['Additional_Shares_r']
            elif int_DivMethod == 3:
                df_compo['AdjustedPrice_fxH'] = df_compo['UnadjustedPrice'] * df_compo['FXRate_toEtf']
                flt_cash = 0
        except Exception as err:    
            print('  ERROR in fLpath_loop, 3. Particularity of Div Calculus | {} || {}'.format(str_idLoop, str(err)))
            raise        
        #-------------------
        # PCF - COMPO
        #-------------------
        try:
            df_compo['1col'] = 'B'
            df_compo['2_EtfIsin'] = t_row['Isin']
            df_compo['3col'] = 'Equity'
            df_compo['6col'] = '-'
            df_compo = dframe.fDf_InsertColumnOfIndex(df_compo, l_colSort = ['Isin'])
            df_compo['15col'] = 'T'
            df_compo['PRICE_r'] = df_compo['AdjustedPrice_fxH'].apply(lambda x:dframe.round_Correction(x, 4))
            df_compo['FXRate_toEtf_r'] = df_compo['FXRate_toEtf'].apply(lambda x:dframe.round_Correction(x, 4))
            df_compo['UNIT_r'] = df_compo['UNIT'].apply(lambda x:dframe.round_Correction(x, 4))
                
            # Get Number of rows in Composition
            int_nbCompo = len(df_compo)
            t_row['int_nbCompo'] = int_nbCompo
            # FINAL COMPO
            df_compo_pcf = df_compo[['1col','2_EtfIsin','3col','Isin','Ric','6col','MIC','Security_Name', 'UNIT_r','6col','6col',
                                     'ind','PRICE_r','FXRate_toEtf_r','15col','2_EtfIsin']].copy()
        except Exception as err:    
            print('  ERROR in fLpath_loop, 4. PCF COMPO | {} || {}'.format(str_idLoop, str(err)))
            raise        
        #-------------------
        # PCF - Header
        #-------------------
        try:
            if flt_cash == 0:   flt_cash = int(flt_cash)
            
            df_header = pd.DataFrame([['H', t_row['ISINiNAV'], t_row['EuronextCategory'], int(int_nbCompo), '1',
                                      dte_date.strftime('%Y%m%d'), dte_navDate.strftime('%Y%m%d'), dframe.round_Correction(flt_nav, 4),
                                      '-','-', dframe.round_Correction(flt_cash, 13),'-', int(flt_shareNb), 
                                      dframe.round_Correction(flt_nav * int_divisor, 4),
                                      str(int_divisor), str_etfCcy, str_etfCcy, str_etfCcy,
                                      str_isin, str_ric, t_row['ETF BBG Code'],t_row['UnderlyingIndexRIC'],
                                      t_row['Indicative NAV ID'],'-','-','-','-','-','-',flt_indexReturn]]
                                    , columns = range(30))
            # CONCAT
            df_pcf = dframe.fDf_Concat_wColOfDf1(df_header, df_compo_pcf)
            # Create PCF Files
            str_pcfFilename =  '{}{}.txt'.format(t_row['Pcf_FileName'], dte_date.strftime('%Y%m%d'))
            str_path = fl.fStr_CreateTxtFile(str_folder, str_pcfFilename, df_pcf, str_sep = '\t')
            l_pathAttach.append(str_path)
        except Exception as err:    
            print('  ERROR in fLpath_loop, 5. Create PCF | {} || {}'.format(str_idLoop, str(err)))
            raise
        
        #-------------------
        # CO - COMPO
        #-------------------
        try:
            df_compo['1col'] = '3'
            if int_DivMethod == 4:      df_compo['SHARES'] = df_compo['CO_UNIT'].apply(lambda x:dframe.round_Correction(x, 0))
            else:                       df_compo['SHARES'] = df_compo['UNIT'].apply(lambda x:dframe.round_Correction(x, 0))
            df_compo['MCap'] = df_compo['SHARES'] * df_compo['PRICE_r']
            df_compo['Weight_100'] = df_compo['Weight'] * 100
            df_compo['Weight_100'] = df_compo['Weight_100'].apply(lambda x:dframe.round_Correction(x, 9))
            # FINAL COMPO
            df_compo_CO = df_compo[['1col','ind','2_EtfIsin','Isin','Security_Name','SHARES','PRICE_r','MCap',
                                    'Weight_100','Country_code','6col']].copy()
        except Exception as err:    
            print('  ERROR in fLpath_loop, 6. CO COMPO | {} || {}'.format(str_idLoop, str(err)))
            raise
        #-------------------
        # CO - Header
        #-------------------
        try:
            df_compo['CASH'] = (df_compo['UNIT_r'] - df_compo['SHARES']) * df_compo['PRICE_r']
            flt_cash = df_compo['CASH'].sum()
            df_header_1 = pd.DataFrame([['1','-', str_isin, str_idLoop, t_row['ETF Name'], '-', t_row['UnderlyingName'],
                                         t_row['ISINiNAV'], '-', t_row['iNAVName'], t_row['ManagementStyle'], t_row['Category'], t_row['Region'], 
                                         '-', t_row['InvestableUniverse'], '-', str_isin, '-', '-','']]
                                    , columns = range(20))
            df_header_2 = pd.DataFrame([['2', dte_date.strftime('%Y%m%d'), str_isin, str(int_divisor), int_divisor*dframe.round_Correction(flt_nav, 4),
                                         dframe.round_Correction(int_divisor * flt_nav - flt_cash, 2), 
                                         dframe.round_Correction(flt_nav_G2, 8), 
                                         flt_cash, 100*flt_cash / (int_divisor*flt_nav), str_etfCcy, int(flt_shareNb), 
                                         dframe.round_Correction(flt_shareNb * flt_nav, 2), '-', '-', '-', t_row['ManagementFee'],
                                         dframe.round_Correction(flt_nav, 4), dte_navDate.strftime('%Y%m%d'), flt_indexReturn, dte_date.strftime('%Y%m%d')]]
                                    , columns = range(20))
            # CONCAT
            df_pcf = dframe.fDf_Concat_wColOfDf1(df_header_1, df_header_2)
            df_pcf = dframe.fDf_Concat_wColOfDf1(df_pcf, df_compo_CO)
            # Create PCF Files
            str_COfilename =  '{}_{}.txt'.format(t_row['CO_FileName'], dte_date.strftime('%Y%m%d'))
            str_path = fl.fStr_CreateTxtFile(str_folder, str_COfilename, df_pcf, str_sep = '\t')
            l_pathAttach.append(str_path)
        except Exception as err:    
            print('  ERROR in fLpath_loop, 7. Create CO | {} || {}'.format(str_idLoop, str(err)))
            raise
        
    return l_pathAttach
#___________________________________________________________________________________________




#------------------------------------------------------------------------------
# Create a Security File Name (disc btw db and SG data)
# - If data source is settles, no need for it anymorw
# - Change str_folder which is the source (SG manual PCF files)
#------------------------------------------------------------------------------
def act_CreateSecurityNameFile():
    str_folder = r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Manual_py\SG_Easy\Easy MSCI 20200706'
    str_folder_Final = r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Manual_py\SG_Easy'
    l_files = fl.fList_FileInDir(str_folder)
    df_pcf_Final = None
    
    for file in l_files:
        df_pcf = dframe.fDf_readCsv_enhanced(fl.fStr_BuildPath(str_folder, file), bl_header = None, str_sep='\t', str_encoding = 'cp1252')
        l_col = list(range(50)[:len(df_pcf.columns)])
        df_pcf.columns = [str(x) for x in l_col]
        df_pcf = df_pcf[['3','4','7']]
        if df_pcf_Final is None:
            df_pcf_Final = df_pcf.copy()
        else:
            df_pcf_Final = dframe.fDf_Concat_wColOfDf1(df_pcf_Final, df_pcf)
        
    fl.fStr_CreateTxtFile(str_folder_Final, 'SgEasy_SecurityName.txt', df_pcf_Final)
    
# MANUAL Launcher
#act_CreateSecurityNameFile()
    