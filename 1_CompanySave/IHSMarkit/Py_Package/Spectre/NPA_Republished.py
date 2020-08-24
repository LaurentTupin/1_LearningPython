import time
import sys, os
sys.path.append('../')
import fct_DB as db
import fct_Files as fl



str_thisFilePath = os.path.abspath(__file__)
str_thisFilefolder = os.path.dirname(str_thisFilePath)


def fStr_Message(str_in):
    print(str_in)
    return '\n' + str_in


def fstr_RePublished(str_SqlPath, str_assetType, i_limitMinutes = 30):
    str_message = ''
    tm_startLoop = time.time()
    # 1. Get the request on the file
    str_req = fl.fStr_ReadFile_sql(os.path.join(str_thisFilefolder, str_SqlPath))
    # 2. Loop until request is empty
    while True:
        tm_start = time.time()
        df_return = db.db_SelectReq(str_req, '', '', '', '', True, False)
        tm_end = time.time()
        # 3. Message to communicate & Getting Out of the loop
        str_message += fStr_Message('------------------------------------------------')
        str_message += fStr_Message('Time of the request:   ' + str(int(tm_end - tm_start)) + ' secondes')
        # 4. Sortir de la boucle
        if len(df_return) == 0:
            str_message += fStr_Message('Empty dataframe:   ' + str_assetType)
            break
        else:
            str_message += fStr_Message('Number of rows updated:   ' + str(len(df_return)) + '  ' + str_assetType)
        if int(time.time() - tm_startLoop) > i_limitMinutes * 60:
            str_message += fStr_Message('***********************************************')
            str_message += fStr_Message('Time whole process:   ' + i_limitMinutes + ' Minutes')
            break
    str_message += fStr_Message('______________________________________________')
    return str_message


#str_sqlFileName = r'Re-Published ETF_Update Table.txt'
#str_return = fstr_RePublished(str_sqlFileName, 'ETF', 2*60)


