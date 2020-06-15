import sys
sys.path.append('../')
import fct_DB as db
import fct_Files as fl

str_server = '10.233.6.147'
str_database = 'SolaQC'
str_dbUID = 'ltupin'
str_dbPwd = db.fStr_Encrypt_GetPass('Tz5Ay92@')


def fStr_Message(str_in):
    print(str_in)
    return '\n' + str_in


def fStr_SaveExcelLog(str_logFolder, str_fileName = 'log.txt'):
    str_message = ''
    try:
        str_listSP = fl.fStr_readFile(False, str_logFolder, str_fileName)
        l_StorProc = str_listSP.split('\n')
        for str_StorProc in l_StorProc:
            if not str_StorProc == '':
                str_message +=                  fStr_Message('-----------------------------------------------')
                try:
                    db.db_EXEC(str_StorProc, str_server, str_database, str_dbUID, str_dbPwd)
                    str_message +=              fStr_Message(str_StorProc)
                    str_listSP = str_listSP.replace(str_StorProc, '')
                except:         str_message +=  fStr_Message('Failed Request:  ' + str_StorProc)
            else:   str_listSP = str_listSP.replace('\n', '')
        # Vider le fichier
        str_message +=                      fStr_Message('______________________________________________')
        str_message +=                      fStr_Message('Delete the file and create an empty one')
        fl.del_fichier(str_logFolder, str_fileName)
        fl.act_createFile(False, str_logFolder, str_fileName, str_listSP)
    except:                 raise
    
    return str_message
