import pandas as pd
import fct_DB as db
import math
    

#==============================================================================
# Read file for Dataframe
#==============================================================================
def fDf_readCsv_enhanced(str_path, bl_header, str_sep = ',', l_names = None, str_encoding = None):       
    try:
        df_data = pd.read_csv(str_path, header = bl_header, sep = str_sep, names = l_names, encoding = str_encoding)
    # -------------------------------------------------------------
    # RECURSIVE solution if second row has more columns or enoding does not recognise special Symbol like EUR
    except pd.errors.ParserError as err:
        print(' ERROR ParserError: {}'.format(str(err)[:-1]))
        str_find = 'saw '
        int_position = int(str(err).find(str_find)) + len(str_find)
        str_nbCol = str(err)[int_position:]
        print(' - Nb of columns we should have: {}'.format(str(int(str_nbCol))))
        df_data = fDf_readCsv_enhanced(str_path, bl_header, str_sep, range(int(str_nbCol)))
        print(' - Error Solved')
    except UnicodeDecodeError as err:
        print(' ERROR UnicodeDecodeError: {}'.format(err))
        with open(str_path, 'r') as f:
            str_encoding = f.encoding 
            print(' - Encoding of the file is actually: {}'.format(str_encoding))
        df_data = fDf_readCsv_enhanced(str_path, bl_header, str_sep, l_names, str_encoding)
        print(' - Error Solved')
    except Exception as err:
        print('   ERROR in fDf_readCsv_enhanced: other undetcted')
        print('   - Error: ', str(err))
        print('   - str_path', str_path)
        print('   - bl_header', bl_header)
        print('   - str_sep', str_sep)
        print('   - l_names', l_names)
        print('   - str_encoding', str_encoding)
        return None
    return df_data



#==============================================================================
# Operation on Dataframe
#==============================================================================

#SELECT df column by number of Col: df_OUT_LIGHTINV.col.str.get(0)

def fDf_CleanPrepareDF(df_in, l_colToBeFloat = [], l_colToDropNA = [], o_fillNA_by = -404, l_colSort = [], bl_ascending = True):
    df = df_in.copy()
    # Change Null to NA (if directly out of DB)
    df.fillna(value = pd.np.nan, inplace = True)
    # Make sure column is float
    if l_colToBeFloat:
        for str_colToBeFloat in l_colToBeFloat:
            df[str_colToBeFloat] = df[str_colToBeFloat].astype(float)
    # Drop NA & fill NA to avoid any issue and bug
    if l_colToDropNA:
        for str_colToDropNA in l_colToDropNA:
            df.dropna(subset = [str_colToDropNA], inplace = True)  
    # Fill NA by...
    if o_fillNA_by != -404:
         df.fillna(value = o_fillNA_by, inplace = True)
    if l_colSort:
        df.sort_values(by = l_colSort, ascending = bl_ascending, inplace = True)
    return df

def fDf_DropRowsIfNa_resetIndex(df, l_colToDropNA = []):
    if l_colToDropNA:   df.dropna(axis = 'index', subset = l_colToDropNA, inplace = True)
    else:               df.dropna(axis = 'index', inplace = True)
    df.reset_index(drop = True, inplace = True)
    return df

def dDf_fillNaColumn(df, str_colTarget, str_colValueToInputIfNA):
    df[str_colTarget] = df[str_colTarget].fillna(df[str_colValueToInputIfNA])
    return df
    
def fDf_fillColUnderCondition(df, str_colToApply, ValueToApply, str_colCondition, ValueCondition, bl_except = False):
    '''Transform un DF avec condition
    ValueToApply can be a value or a lambda function'''
    if bl_except:   df[str_colToApply] = df[str_colToApply].mask(df[str_colCondition] != ValueCondition, ValueToApply)
    else:           df[str_colToApply] = df[str_colToApply].mask(df[str_colCondition] == ValueCondition, ValueToApply)
    #df[str_colToApply] = [ValueToApply if x == ValueCondition else '-' for x in df[str_colCondition]]
    #df['Units'] = df['Units'].where(df['column'] == 'S', - df['Units'])
    return df

def fDf_FilterOnCol(df, str_colToApply, l_isIN = [], str_startWith = ''):
    if l_isIN:
        df = df[df[str_colToApply].isin(l_isIN)].copy()
        #df_Holdings = df_OUT_LIGHTINV[df_OUT_LIGHTINV['GTI'].isin(['S01','S39'])]
    elif str_startWith != '':
        df = df[df[str_colToApply].startswith(str_startWith, na = False)].copy()
        #df_Fund = df_Fund[df_Fund['colForCriteria'].str.startswith('S', na = False)].copy()
    return df


def fDf_InsertColumnOfIndex(df, int_StartNumber = 1, int_PositionOf_ColumnIndex = 0, l_colSort = [], bl_ascending = True):
    # Sort before to do anything else
    if l_colSort:
        df.sort_values(by = l_colSort, ascending = bl_ascending, inplace = True)
    # Keep the inital columns name in a list / Keep the index as well
    l_col = df.columns.tolist()
    l_index = df.index
    # Add a column of index
    df.reset_index(drop = True, inplace = True)
    df['ind'] = df.index + int_StartNumber
    df.index = l_index
    # re-Order the columns the the index column is not at the end
    if int_PositionOf_ColumnIndex == 0:
        df = df[['ind'] + l_col]
    else:
        df = df[l_col[:int_PositionOf_ColumnIndex] + ['ind'] + l_col[int_PositionOf_ColumnIndex:]]
    return df


def fDf_InsertRows(df, int_nbRows, int_rows):
    df_return = df
    for i in range(0, int_nbRows):
        df_line = pd.DataFrame([[''] * len(df_return.columns)], columns =  df_return.columns, index = [int_rows - 0.5])
        #df_return = pd.concat([df_return.ix[:int_rows], df_line, df_return.ix[int_rows + 1:]]).reset_index(drop=True)
        df_return = df_return.append(df_line, ignore_index = False)
        df_return = df_return.sort_index().reset_index(drop = True) 
    return df_return


def fDf_Concat_wColOfDf1(df1, df2, bl_colDf2_AsARow = False, int_emptyRow = 0):
    # Intro: Prepare the DF
    if bl_colDf2_AsARow or int_emptyRow > 0:
        df_inBetween = pd.DataFrame(columns = df2.columns)
        for i in range(int_emptyRow):
            df_inBetween.loc[len(df_inBetween)] = [''] * len(df2.columns)
        if bl_colDf2_AsARow:
            df_inBetween.loc[len(df_inBetween)] = df2.columns
        df2 = pd.concat([df_inBetween, df2], ignore_index = True, sort = False)
    # CONCAT
    if len(df1.columns) >= len(df2.columns):
        df2.columns = df1.columns[:len(df2.columns)]
        df_return = pd.concat([df1, df2], ignore_index = True, sort = False)
        df_return = df_return[df1.columns]
    else:
        df2.columns = list(df1.columns) + list(df2.columns[len(df1.columns):])
        df_return = pd.concat([df1, df2], ignore_index = True, sort = False)
        df_return = df_return[df2.columns]
    return df_return






def fDf_JoinDf(df_left, df_right, str_columnON, str_how = 'inner'):
    # how{‘left’, ‘right’, ‘outer’, ‘inner’}, default ‘inner’
    #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html
    
    # Verification
    if not str_columnON in df_left.columns :
        print(' ERROR  in fDf_JoinDf: Column {0} is not in left dataframe: {1}'.format(str_columnON, list(df_left.columns)))
        print(df_left.head(5), '\n\n')
        return df_left
    elif not str_columnON in df_right.columns:
        print(' ERROR  in fDf_JoinDf: Column {0} is not in left dataframe: {1}'.format(str_columnON, list(df_right.columns)))
        print(df_right.head(5), '\n\n')
        return df_left
    # JOIN 
    try:                        
        df = pd.merge(df_left, df_right, on = str_columnON, how = str_how)
        #df_Holds_MACI = df_Holds_MACI.join(df_Out_Fx[['Curr', 'Fx']].set_index('Curr'), on = 'Curr')
    except Exception as err:    
        print(' ERROR  in fDf_JoinDf: {}'.format(str(err)))
        return df_left
    return df


def fDf_imposerStr_0apVirgule(df, str_colName, int_0apVirgule = 2):
    try:
        df_result = df.copy()
        df_result[str_colName] = pd.to_numeric(df_result[str_colName])
        df_result[str_colName] = df_result[str_colName].astype(str) + '0' * int_0apVirgule
        df_temp = df_result[str_colName].str.split('.', n = 1, expand = True)
        if int_0apVirgule == 0: 
            df_result[str_colName] = df_temp[0] 
        else:
            df_temp[1] = df_temp[1].str.slice(0, int_0apVirgule)
            df_result[str_colName] = df_temp[0] + '.' + df_temp[1]
    except:
        print(' ERROR: fDf_imposerStr_0apVirgule did not work - it will pass without raising')
        print('  str_colName', str_colName, 'int_0apVirgule', int_0apVirgule)
        return df
    return df_result


def round_down(n, decimals = 0):
    multiplier = 10 ** decimals
    Result = math.floor(n * multiplier) / multiplier
    return Result


def fDf_GetFirst_onGroupBy(df_in, str_colPivot, str_colMeasure, bl_sort = True, l_ColSort = [], bl_ascending = False):
    df = fDf_CleanPrepareDF(df_in, [str_colMeasure], [str_colPivot], 0)
    # Get First on a Group By - 1 : Sort the value
    if l_ColSort:
        df.sort_values(by = l_ColSort, ascending = bl_ascending, inplace = True)
    elif bl_sort:
        df.sort_values(by = [str_colPivot, str_colMeasure], ascending = False, inplace = True)
    
    df_group = df.groupby(str_colPivot)                     # Group and have the colPivot as Index
    df = df_group.first()                                   # Keep only the first of the Column Pivot
    df[str_colPivot] = df.index                             # Put again the Column Pivot that disapear into index
    df.reset_index(drop = True, inplace = True)             # reset_index
    df = df[[df.columns[-1]] + list(df.columns[:-1])] 
    return df
    


#==============================================================================
# Function not used, (Just to keep code I replaced)
#==============================================================================
def fDf_GetFirst_SumOnSecondCol(df_in, str_colPivot, str_colToSum_keepOnlyMax, str_colMeasure):
    df = fDf_CleanPrepareDF(df_in, [str_colMeasure], [str_colPivot, str_colToSum_keepOnlyMax], 0)
    
    # Group BY - keep only one row per Column Pivot 2 
    df_group = df.groupby(str_colToSum_keepOnlyMax).agg({str_colMeasure: 'sum'})
    df_group.rename(columns = {str_colMeasure : str_colMeasure + '_Sum'}, inplace = True)
    df_group[str_colToSum_keepOnlyMax] = df_group.index         # Put again the Column Pivot that disapear into index
    df_group.reset_index(drop = True, inplace = True)           # reset_index
    df = df.merge(df_group, on = str_colToSum_keepOnlyMax)      # MERGE to put the SUM on the original df
    
    # Group BY - keep only one row per Column Pivot
    df = fDf_GetFirst_onGroupBy(df, str_colPivot, str_colMeasure + '_Sum')
    
    return df

#df_codePivot = dframe.fDf_GetPivotCode('PivotCode_HKsamsung.csv', 1, 'Isin, Sedol, LotSize', l_Isin)
#df_codePivot = dframe.df_codePivot(df_codePivot, 'Isin', 'Sedol', 'LotSize')

#df = pd.DataFrame([["A","X",15],        ["A","X",13],       ["A","Y",25],
#                ["B","R",9],            ["B","S",15],       ["B",'T',8]],
#                columns=["Isin","Sedol","LotSize"])
#print(df)
#print(fDf_GetFirst_IsinSedol(df, "Isin", 'Sedol', "LotSize"))


#==============================================================================
# Get some DF from SQL
#==============================================================================
def fDf_GetPivotCode(str_fileName, int_dayToKeep, str_listColumns = 'Isin, Sedol, Bloomberg, Ric, ExchangeTicker, CurrentName ', 
                     l_Isin = [], l_Bloomberg = [], l_Sedol = []):
    try:
        str_sqlReq_start = 'SELECT {} FROM tblCodePivot '.format(str_listColumns)
        # Depends of Input we have
        if l_Isin:
            str_sqlReq = str_sqlReq_start + '\n' + " WHERE IsActive = 1 \n AND Isin IN ('" + "', '".join(l_Isin) + "') "
            str_sqlReq = str_sqlReq + '\n' + 'ORDER BY Isin'
        elif l_Bloomberg:
            str_sqlReq = str_sqlReq_start + '\n' + " WHERE Bloomberg IN ('" + "', '".join(l_Bloomberg) + "') "
            str_sqlReq = str_sqlReq + '\n' + 'ORDER BY Bloomberg'
        elif l_Sedol:
            str_sqlReq = str_sqlReq_start + '\n' + " WHERE Sedol IN ('" + "', '".join(l_Sedol) + "') "
            str_sqlReq = str_sqlReq + '\n' + 'ORDER BY Sedol'
        #print(str_sqlReq)
        # Get the DF
        df_PivotCode = db.fDf_GetRequest_or_fromCsvFile(str_sqlReq, str_fileName, int_dayToKeep)
    except: 
        print(' ERROR in fDf_GetPivotCode')
        print(' - Parameters: ', str_fileName, int_dayToKeep)
        print(' - l_Isin: ', l_Isin[:5])
        print(' - l_Bloomberg: ', l_Bloomberg[:5])
        print(' - l_Sedol: ', l_Sedol[:5])
        #print(' - str_sqlReq: ', str_sqlReq)
    return df_PivotCode


def fDf_GetvwSecL(str_fileName, int_dayToKeep, str_listColumns = 'Isin, Sedol, Bloomberg, Ric, ExchangeTicker, CurrentName ', 
                     l_Isin = [], l_Bloomberg = [], l_Sedol = []):
    try:
        str_sqlReq_start = 'SELECT {} FROM vwSecurityListing  '.format(str_listColumns)
        # Depends of Input we have
        if l_Isin:
            str_sqlReq = str_sqlReq_start + '\n' + " WHERE IsPrimaryListing = 1  \n AND Isin IN ('" + "', '".join(l_Isin) + "') "
            str_sqlReq = str_sqlReq + '\n' + 'ORDER BY Isin'
        elif l_Bloomberg:
            str_sqlReq = str_sqlReq_start + '\n' + " WHERE Bloomberg IN ('" + "', '".join(l_Bloomberg) + "') "
            str_sqlReq = str_sqlReq + '\n' + 'ORDER BY Bloomberg'
        elif l_Sedol:
            str_sqlReq = str_sqlReq_start + '\n' + " WHERE Sedol IN ('" + "', '".join(l_Sedol) + "') "
            str_sqlReq = str_sqlReq + '\n' + 'ORDER BY Sedol'
        # Get the DF
        df_PivotCode = db.fDf_GetRequest_or_fromCsvFile(str_sqlReq, str_fileName, int_dayToKeep)
    except: 
        print(' ERROR in fDf_GetvwSecL')
        print(' - Parameters: ', str_fileName, int_dayToKeep)
        print(' - l_Isin: ', l_Isin[:5])
        print(' - l_Bloomberg: ', l_Bloomberg[:5])
        print(' - l_Sedol: ', l_Sedol[:5])
    return df_PivotCode


def fDf_GetvwSecL_NoCase(str_fileName,int_dayToKeep, str_listColumns = 'Isin, Sedol, Bloomberg, Ric', l_Bloomberg = []):
    try:
        str_sqlReq_start = 'SELECT {} FROM vwSecurityListing '.format(str_listColumns)
        # Depends of Input we have
        if l_Bloomberg:
            str_sqlReq = str_sqlReq_start + '\n' + " WHERE UPPER(Bloomberg) IN (UPPER('" + "'), UPPER('".join(l_Bloomberg) + "')) "
            str_sqlReq = str_sqlReq + '\n' + 'ORDER BY Bloomberg'
        #print(str_sqlReq)
        # Get the DF
        df_PivotCode = db.fDf_GetRequest_or_fromCsvFile(str_sqlReq, str_fileName, int_dayToKeep)
    except: 
        print(' ERROR in fDf_GetCode_NoCase')
        print(' - Parameters: ', str_fileName, int_dayToKeep)
        print(' - l_Bloomberg: ', l_Bloomberg[:5])
    return df_PivotCode
    





#import numpy as np
#
#ar = np.array([[1.15, 2.50, 3.30, 4.00], [2.7, 10, 5.4, 7], [5.3, 9, 1.5, 15]])
#df = pd.DataFrame(ar, index = [1, 2, 3], columns = ['A', 'B', 'C', 'D'])
#
#print(df)
##print(df.dtypes)
#
#df = fDf_imposerStr_0apVirgule(df, 'D', 2)
#print(df)
#
##
##df['D'] = df['D'].astype(str) + '0'*3
##print(df)
##df2 = df['D'].str.split('.', n = 1, expand = True)
##
##df2[1] = df2[1].str.slice(0, 2)
##
##df['D'] = df2[0] + '.' + df2[1]
##
##print(df)