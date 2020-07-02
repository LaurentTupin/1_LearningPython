import sys
#import numpy as np
import pandas as pd
import datetime as dt
from pandas.tseries.offsets import BDay
from dateutil.relativedelta import relativedelta
sys.path.append('../')
import fct_DB as db

##Example of Date // how to convert
#str_today_default = dt.datetime.now().date().strftime('%Y-%m-%d')
#dte_today_default = dt.datetime.strptime(str_today_default, '%Y-%m-%d')
#
#print(dte_today_default, type(dte_today_default))
#dte_today_default = fDte_AddDay(dte_today_default, - 8)
#print(dte_today_default, type(dte_today_default))






##########################################################
### Today ###
def fDte_Today():
    return dt.date.today()


#dte_d = fDte_Today()
#print(dte_d)
#str_month = dte_d.strftime('%d%b%Y')
#print(str_month)



##########################################################
### Time Test ###

# function that compares the given time against opening and closing
def fBl_TimeIsBetween(tm_start, tm_end, tm_toTest):
    if tm_start <= tm_end:  bl_result = tm_start <= tm_toTest <= tm_end
    else:                   bl_result = tm_start <= tm_toTest or tm_toTest <= tm_end
    return bl_result





##########################################################
### Date Calculation ###

def fDte_AddMonth(dte_date, int_Month = 1):
    try:
        if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
        dte_AddMonth = dte_date + relativedelta(months = int_Month)
    except: 
        print(' ERROR in fDte_AddMonth')
        print(' - dte_date: ', dte_date, int_Month, type(dte_date))
        raise
    return dte_AddMonth


def fDte_AddDay(dte_date, int_Day = 1):
    try:
        if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
        dte_AddDay = dte_date + dt.timedelta(days = int_Day)
    except: 
        print(' ERROR in fDte_AddDay')
        print(' - ', dte_date, int_Day, type(dte_date))
        raise
    return dte_AddDay 


def fInt_dateDifference(dte_bigger, dte_lower):
    try:
        dte_bigger = fDte_formatToDate(dte_bigger)
        dte_lower = fDte_formatToDate(dte_lower)
        int_dateDifference = (dte_bigger - dte_lower).days
    except: 
        print(' ERROR in fInt_dateDifference')
        print(' - dte_date: ', dte_bigger, dte_lower)
        print(' - type(dte_date):  ', type(dte_bigger) , type(dte_lower))
        raise
    return int_dateDifference


def fDat_GetCorrectOffsetDate_Calendar(dte_date, str_pyFormat, int_offset, str_CalendarID = '', bl_Backward = True):
    try:
        if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
        int_offset = int(int_offset)
        if str_CalendarID == ' ':       str_CalendarID = ''
        
        # ============= If no Calendar OR no Offset:      Find the Date (simple Offset on Business Day) =============
        if not (str_CalendarID and int_offset != 0):
            dte_OffsetDate = dte_date + BDay(int(int_offset))
        
        # ============= Check if Date exist in Calendar =============
        else:
            # Get the DataFrame
            str_sqlReq = """SELECT * FROM SolaDBServer..tblHoliday WHERE CalendarID = {}
                            AND HolidayDate BETWEEN DATEADD(yy, DATEDIFF(yy, 0, GETDATE()), 0) 
                            AND DATEADD (dd, -1, DATEADD(yy, DATEDIFF(yy, 0, GETDATE()) +1, 0))""".format(str(str_CalendarID))
            str_fileName_Calendar = 'sql_Calendar_{}.csv'.format(str(str_CalendarID))
            int_dayToKeep = 4
            df_Calendar = db.fDf_GetRequest_or_fromCsvFile(str_sqlReq, str_fileName_Calendar, int_dayToKeep)
            
            # Define if we need to go backward or forward in case Date is Holiday
            if int_offset > 0:     
                bl_Backward = False
                str_ChangeDate = 'NextBusDate'
                i_offset_start = 1
            else:
                str_ChangeDate = 'PrevBusDate'
                i_offset_start = -1
                
            # loop on all day until the final Offset defined
            for i_offset in range(i_offset_start, int_offset + i_offset_start, i_offset_start):
                dte_OffsetDate = dte_date + BDay(i_offset)
                str_sqlDate = dte_OffsetDate.strftime('%Y-%m-%d')
                if str_sqlDate in df_Calendar['HolidayDate'].values:
                    str_OffsetDate = df_Calendar.loc[df_Calendar['HolidayDate'] == str_sqlDate, str_ChangeDate].iloc[0]
                    dte_OffsetDate = dt.datetime.strptime(str_OffsetDate, '%Y-%m-%d')
                    dte_date = dte_OffsetDate - BDay(i_offset)
        # Finally: format
        str_OffsetDate = dte_OffsetDate.strftime(str_pyFormat)
    except: 
        print(' ERROR in fDat_GetCorrectOffsetDate_Calendar')
        print(' - Parameters: ', dte_date, str_pyFormat, int_offset, str_CalendarID, bl_Backward)
        print(' - type(dte_date):  ', type(dte_date))
        raise
    return str_OffsetDate


##########################################################
### Date specific in the month ###
def fDte_1OM(dte_date):
    dte_1OM = fDte_EOM(dte_date)
    dte_1OM = dte_1OM + BDay(1)
    return dte_1OM

def fDte_EOM(dte_date, int_month = -1, bl_businessDay = True):
    try:
        if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
        # Add month
        if int_month != -1 : dte_date = fDte_AddMonth(dte_date, int_month + 1)
        # Loop        
        for i_day in range(1, dte_date.day + 1):
            if bl_businessDay: dte_EOM = dte_date-BDay(i_day)
            else: dte_EOM = fDte_AddDay(dte_date, - i_day)
            if not dte_EOM.month == dte_date.month:
                return dte_EOM
    except:
        print(' ERROR in fDte_EOM')
        print(' - dte_date: ', dte_date)
        raise

def fBl_dteFirstDayMonth(dte_date):
    try:
        if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
        if (dte_date-BDay(1)).month == dte_date.month: return False
    except:
        print(' ERROR in fBl_dteFirstDayMonth')
        print(' - dte_date: ', dte_date)
        raise
    return True

def fBl_dteLastDayMonth(dte_date):
    try:
        if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
        if (dte_date + BDay(1)).month == dte_date.month: return False
    except:
        print(' ERROR in fBl_dteFirstDayMonth')
        print(' - dte_date: ', dte_date)
        raise
    return True

def is_second_friday(dte_date):
    try:
        bl_is_second_friday = dte_date.weekday() == 4 and 8 <= dte_date.day <= 14
    except:
        print(' ERROR in is_second_friday')
        print(' - dte_date: ', dte_date)
        raise
    return bl_is_second_friday

def fDte_lastFriday(dte_date):
    int_weekDay = dte_date.weekday()
    dte_last_friday = (dte_date - dt.timedelta(days = int_weekDay) + dt.timedelta(days = 4, weeks = -1))
    return dte_last_friday

def fDte_lastThursday(dte_date):
    int_weekDay = dte_date.weekday()
    dte_lastThursday = (dte_date - dt.timedelta(days = int_weekDay) + dt.timedelta(days = 3, weeks = -1))
    return dte_lastThursday

def fInt_workingDay(dte_date, str_CalendarID = '404'):
    try:
        if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
        for i_day in range(1, dte_date.day + 1):
            dte_dateOffset = fDat_GetCorrectOffsetDate_Calendar(dte_date, '%Y-%m-%d', -i_day, str_CalendarID)
            dte_dateOffset = dt.datetime.strptime(dte_dateOffset, '%Y-%m-%d')
            if not dte_dateOffset.month == dte_date.month:
                return i_day
    except:
        print(' ERROR in fInt_workingDay')
        print(' - dte_date: ', dte_date)
        raise

def fDte_formatToDate(dte_date, str_dateFormat = '%Y-%m-%d', bl_stopLoop = False):
    try:
        if type(dte_date) == str:
            dte_date = dt.datetime.strptime(dte_date, str_dateFormat)
        elif 'numpy' in str(type(dte_date)) and 'datetime' in str(type(dte_date)):
            dte_date = pd.to_datetime(str(dte_date)).replace(tzinfo = None)
        #elif type(dte_date).__module__ == np.__name__:
            #np.datetime64(dte_date).astype(datetime)
        
        # FINAL
        if type(dte_date) == dt.date:           dte_formatToDate = dte_date
        elif isinstance(dte_date, dt.date):     dte_formatToDate = dte_date
        else:                                   dte_formatToDate = dte_date.date()
    except Exception as err:
        if not bl_stopLoop:
            try:    return fDte_formatToDate(dte_date, '%Y-%m-%d', True)
            except: 
                print(' - dte_date: ', dte_date, str_dateFormat, type(dte_date), 'bl_stopLoop: ', bl_stopLoop)
                raise
        print(' ERROR in fDte_formatToDate')
        print(' - Error: ', err)
        print(' - dte_date: ', dte_date, str_dateFormat, type(dte_date), 'bl_stopLoop: ', bl_stopLoop)
        raise
    return dte_formatToDate

def fDte_formatMoisAnnee(dte_date):
    try:
        if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
        dte_formatMoisAnnee = dte_date.date().strftime('%b %Y').upper()
    except: 
        print(' ERROR in fDte_formatMoisAnnee')
        print(' - dte_date: ', dte_date, type(dte_date))
        raise
    return dte_formatMoisAnnee

def fDte_formatMoisAn(dte_date):
    try:
        if type(dte_date) == str: dte_date = dt.datetime.strptime(dte_date, '%Y-%m-%d')
        dte_formatMoisAn = dte_date.date().strftime('%b %y').upper()
    except: 
        print(' ERROR in fDte_formatMoisAn')
        print(' - dte_date: ', dte_date, type(dte_date))
        raise
    return dte_formatMoisAn

##########################################################

