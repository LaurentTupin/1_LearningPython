try:
    import os, time
    import pyodbc as db
    import pandas as pd
    import datetime as dt
    #import sqlalchemy
    import fct_Files as fl
except Exception as err:
    str_lib = str(err).replace("No module named ", "").replace("'", "")
    print(" ATTENTION,  Missing library: '{0}' \n * Please Open Anaconda prompt and type: 'pip install {0}'".format(str_lib))



#---------------------------------------------------------------
#------------- Decorator -------------
#---------------------------------------------------------------
def dec_singletonsCLass(input_classe):
    '''
    Singeltons decorators: prendre toujours que la premiere instance 
    (exemple : instance de connexion a database, on ne veut pas plusieurs instances
    , mais tjrs la premiere si elle existe)
    '''    
    d_instances = {}
    def wrap_getInstances(*l_paramInput, **d_paramInput):
        if input_classe not in d_instances:
            # Add instances as value in the dictionary where the key is the class
            d_instances[input_classe] = input_classe(*l_paramInput, **d_paramInput)
        # If an instance already exist for ones class, just use this instance
        return d_instances[input_classe]
    return wrap_getInstances



#---------------------------------------------------------------
# ------------- CLASS DB management ----------------------------
#---------------------------------------------------------------


@dec_singletonsCLass
class c_sqlDB():
    def __init__(self):
        self.__cloudPathForCsv_default = os.path.join(os.environ['USERPROFILE'], r'IHS Markit\HK PCF Services Team - General\Auto_py\file')
        self.__server_default = '10.233.6.147'
        self.df_UID = pd.read_csv(os.path.join(self.__cloudPathForCsv_default, 'DatabasePassword.csv'))
        df_UID = self.df_UID
        self.__database_default = df_UID.loc[df_UID['Server'] == self.__server_default, 'Database'].values[0]
        self.__uid_default = df_UID.loc[df_UID['Server'] == self.__server_default, 'Uid'].values[0]
        self.__pwd_default = df_UID.loc[df_UID['Server'] == self.__server_default, 'Password'].values[0]
        
        self.__server =             self.__server_default
        self.__database =           self.__database_default
        self.__uid =                self.__uid_default
        self.__pwd =                self.__pwd_default
        self.__cloudPathForCsv =    self.__cloudPathForCsv_default
        self.__bl_AlertIfEmptyReq = True
        self.__request = 'Request not defined'
    
    #=====================================================
    @property
    def server(self):
        return self.__server
    @server.setter
    def server(self, str_server):
        if str_server != '':
            # Change of server ==> Change of default Value from CSV file (possibility to override after)
            self.__server_default = str_server
            df_UID = self.df_UID
            self.__database_default =   df_UID.loc[df_UID['Server'] == self.__server_default, 'Database'].values[0]
            self.__uid_default =        df_UID.loc[df_UID['Server'] == self.__server_default, 'Uid'].values[0]
            self.__pwd_default =        df_UID.loc[df_UID['Server'] == self.__server_default, 'Password'].values[0]
        # Real Value = Default
        self.__server =             self.__server_default
        self.__database =           self.__database_default
        self.__uid =                self.__uid_default
        self.__pwd =                self.__pwd_default
    @property
    def database(self):
        return self.__database
    @database.setter
    def database(self, str_database):
        # If SolaQC, we will take FIX value, but not on the default one !!!
        if str_database == 'SolaQC':
            df_UID = self.df_UID
            self.__server =         '10.233.6.147'
            self.__database =       'SolaQC'
            self.__uid =            df_UID.loc[df_UID['Server'] == self.__server, 'Uid'].values[0]
            self.__pwd =            df_UID.loc[df_UID['Server'] == self.__server, 'Password'].values[0]
        elif str_database != '':    self.__database = str_database
        else:                       self.__database = self.__database_default
    @property
    def uid(self):
        return self.__uid
    @uid.setter
    def uid(self, str_uid):
        if str_uid != '':           self.__uid = str_uid
        elif self.__database != 'SolaQC':
            self.__uid = self.__uid_default
    @property
    def pwd(self):
        return self.__pwd
    @pwd.setter
    def pwd(self, str_pwd):
        if str_pwd != '':           self.__pwd = str_pwd
        elif self.__database != 'SolaQC':
            self.__pwd = self.__pwd_default
    @property
    def cloudPathForCsv(self):
        return self.__cloudPathForCsv
    @cloudPathForCsv.setter
    def cloudPathForCsv(self, str_cloudPathForCsv):
        if str_cloudPathForCsv != '':   self.__cloudPathForCsv = str_cloudPathForCsv
        else:                           self.__cloudPathForCsv = self.__cloudPathForCsv_default
    @property
    def request(self):
        return self.__request
    @request.setter
    def request(self, str_request):
        if str_request != '':       self.__request = str_request
        else:                       self.__request = 'Request not defined'    
    @property
    def bl_AlertIfEmptyReq(self):
        return self.__bl_AlertIfEmptyReq
    @bl_AlertIfEmptyReq.setter
    def bl_AlertIfEmptyReq(self, bl_AlertIfEmptyReq):
        self.__bl_AlertIfEmptyReq = bl_AlertIfEmptyReq
    #=====================================================
    
    def db_seeDriversAvailable(self):
        self.__drivers = db.drivers()
        return self.__drivers
    
    def db_printMessageWArg(self, str_msg):
        print('--------------------------------------')
        print(str_msg)
        print('  - ', self.__server, self.__database, self.__uid, self.__pwd)
        print('  - ', self.__request)
        print('--------------------------------------')
    
    def GetRequestFromDecompo(self, str_from, str_select, l_where, str_groupBy, str_orderBy):
        try:
            str_req = ' SELECT ' + str_select
            str_req += ' \r\n' + ' FROM ' + str_from
            if not l_where == []:
                str_req += ' \r\n' + ' WHERE '  + l_where[0]
                for str_where in l_where[1:]:
                    if not str_where == '':
                        str_req += ' \r\n' + ' AND '  + str_where
            if not str_groupBy == '':
                str_req += ' \r\n' + ' GROUP BY ' + str_groupBy
            if not str_orderBy == '':
                str_req += ' \r\n' + ' ORDER BY ' + str_orderBy
        except:
            self.db_printMessageWArg(' ERROR: GetRequestFromDecompo did not work')
            raise
        #self.__request = str_req
        self.request = str_req
        return self.request
    
    def db_sqlConnectCursor(self):
        try:
            self.cnxn = db.connect('DRIVER={SQL Server};SERVER=' + self.__server + 
                                  ';DATABASE=' + self.__database + 
                                  ';UID=' + self.__uid + 
                                  ';PWD=' + self.__pwd)
                                    #trusted_connection=YES;  for Windiws Authentification
            self.cursor = self.cnxn.cursor()
        except:
            self.db_printMessageWArg(' ERROR: db_sqlConnectCursor did not work')
            self.db_CloseConnexion()
            raise
            
    def db_Execute(self, bl_prod = True):
        try:
            if not bl_prod:
                print(self.__request)
            self.cursor.execute(self.__request)
        except:
            self.db_printMessageWArg(' ERROR: db_Execute did not work. the request is not working')
            raise
            
    def db_Commit(self):
        try:
            self.cnxn.commit()
        except:
            self.db_printMessageWArg(' ERROR: db_Commit did not work')
            raise
            
    def getDataFrame_fReq(self):
        self._pd_extract = False
        try:
            self._pd_extract = pd.read_sql(self.__request, self.cnxn)
            # Message if empty
            if self.__bl_AlertIfEmptyReq:
                if self._pd_extract.empty or self._pd_extract.dropna(how = 'all').empty:
                    self.db_printMessageWArg(' EMPTY: getDataFrame_fReq is empty: ')
        except:
            self.db_printMessageWArg(' ERROR: read_sql')
            raise
        return self._pd_extract
    
    def getDataFrame_multipleReq(self):
        self._pd_extract = False
        try:
            l_resultSet = self.cursor.fetchall()
            df_resultSet = pd.DataFrame.from_records(l_resultSet)
            while (self.cursor.nextset()): 
                l_resultSet = self.cursor.fetchall()
                df_resultSet_Suiv = pd.DataFrame.from_records(l_resultSet)
                df_resultSet = self.fDf_Concat(df_resultSet, df_resultSet_Suiv)
            # Final Result
            self._pd_extract = df_resultSet
            # Message if empty
            if self.__bl_AlertIfEmptyReq:
                if self._pd_extract.empty or self._pd_extract.dropna(how = 'all').empty:
                    self.db_printMessageWArg(' EMPTY: getDataFrame_multipleReq is empty: ')
        except:
            self.db_printMessageWArg(' ERROR: getDataFrame_multipleReq // pd.DataFrame.from_records did not work')
            raise
        return self._pd_extract
    
    @classmethod
    def fDf_Concat(cls, df1, df2):
        try:
            if len(df1.columns) >= len(df2.columns):
                df2.columns = df1.columns[:len(df2.columns)]
                df_return = pd.concat([df1, df2], ignore_index = True)
                df_return = df_return[df1.columns]
            else:
                df2.columns = list(df1.columns) + list(df2.columns[len(df1.columns):])
                df_return = pd.concat([df1, df2], ignore_index = True)
                df_return = df_return[df2.columns]
        except: df_return = False
        return df_return
    
    def db_CloseConnexion(self):
        try:    
            self.cursor.close()
            del self.cursor
        except: pass
        try:    self.cnxn.close()
        except: pass
        
    def __del__(self):
        self.db_CloseConnexion()
        #        self.db_printMessageWArg(' * Notes: Closing DB Connexion')
        
    #    # OLD Functions: ''' Insert a Wholde CSV in Table '''
    #    def db_InsertDF_inTable(self, df_toIntegrate, str_table):
    #        engine = sqlalchemy.create_engine("mssql+pyodbc://HKG-VMDEV-SQL2.hkg.asia.cib/db_Hybrid?driver=SQL+Server+Native+Client+11.0")
    #        df_toIntegrate.to_sql(str_table, engine, if_exists = 'append')
    
    

#---------------------------------------------------------------
#----- Function to launch the Class ----------------------------
#---------------------------------------------------------------
        
# ***** EXECUTE a SP *****************
#@fl.dec_getTimePerf(5)
def db_DefineConnectCursor(str_req, str_server = '', str_database = '', str_uid = '', str_pwd = ''):
    inst_db = c_sqlDB()
    inst_db.server = str_server
    inst_db.database = str_database
    inst_db.uid = str_uid
    inst_db.pwd = str_pwd
    inst_db.request = str_req
    inst_db.db_sqlConnectCursor()
    return True

# ***** Execute a Stored Proc *****************
#@fl.dec_getTimePerf(5)
def db_EXEC(str_req, str_server = '', str_database = '', str_uid = '', str_pwd = '', bl_prod = True):
    inst_db = c_sqlDB()
    db_DefineConnectCursor(str_req, str_server, str_database, str_uid, str_pwd)
    inst_db.db_Execute(bl_prod)
    inst_db.db_Commit()
    #    print(inst_db.server, inst_db.database, inst_db.uid, inst_db.pwd,'\n')
    return True

# ***** Select to dataframe *****************
#@dec_getTimePerf(10)
def db_SelectReq(str_req, str_server = '',str_database = '', str_uid = '', str_pwd = '', bl_prod = True, bl_AlertIfEmptyReq = True):
    inst_db = c_sqlDB()
    db_DefineConnectCursor(str_req, str_server, str_database, str_uid, str_pwd)
    inst_db.bl_AlertIfEmptyReq = bl_AlertIfEmptyReq
    df_result = inst_db.getDataFrame_fReq()
    inst_db.db_Commit()
    return df_result

# ***** Mulitple Proc to dataframe *****************
#@dec_getTimePerf(10)
def db_MultipleReq(str_req, str_server = '',str_database = '', str_uid = '', str_pwd = '', bl_prod = True, bl_AlertIfEmptyReq = True):
    inst_db = c_sqlDB()
    db_DefineConnectCursor(str_req, str_server, str_database, str_uid, str_pwd)
    inst_db.db_Execute()
    inst_db.bl_AlertIfEmptyReq = bl_AlertIfEmptyReq
    df_result = inst_db.getDataFrame_multipleReq()
    inst_db.db_Commit()
    return df_result

# ***** Building request & Select to dataframe *****************
#@dec_getTimePerf(10)
def fDf_sqlBuildSelect(str_from, str_select = '*', l_where = [], str_groupBy = '', str_orderBy = ''):
    inst_db = c_sqlDB()
    #Just to go back to default value and not stay on SOLAQC database...
    db_DefineConnectCursor('')
    inst_db.GetRequestFromDecompo(str_from, str_select, l_where, str_groupBy, str_orderBy)
    df_result = inst_db.getDataFrame_fReq()
    inst_db.db_Commit()
    return df_result

# ***** SQL Request and Save into CSV  *****************
#@dec_getTimePerf(5)
def fDf_GetRequest_or_fromCsvFile(str_req, str_fileName, int_dayToKeep, str_cloudPathForCsv = '', bl_AlertIfEmptyReq = True):
    inst_db = c_sqlDB()
    inst_db.cloudPathForCsv = str_cloudPathForCsv
    
    # ----- Get the Path -----
    str_Path = os.path.join(inst_db.cloudPathForCsv, str_fileName)
    
    # ----- Delete if the file is too old -----
    if fl.fBl_FileExist(str_Path):
        try:    fl.del_fichier_ifOldEnought(str_Path,'', int_dayToKeep)
        except: pass
    
    # ----- Try to read the file (if it exists) -----
    try:    df_return = pd.read_csv(str_Path, header = 0)
    except:
        # ----- Does not EXIST -----
        df_return = db_SelectReq(str_req, bl_AlertIfEmptyReq = bl_AlertIfEmptyReq)
        # ----- Save the request on CSV -----
        try:    df_return.to_csv(str_Path, index = False, header = True)
        except: print(' Warning in fDf_GetRequest_or_fromCsvFile: No access to {}\n - file: {}'.format(str_Path, str_fileName))
    return df_return



##########################################################
####### Log ###########################
##########################################################
def Log_Python(d_param = {}):
    try:
        # Check the Folder exist for the user
        str_PathCloud = os.path.join(os.environ['USERPROFILE'], r'IHS Markit\HK PCF Services Team - General\Auto_py\file') 
        if not fl.fBl_FolderExist(str_PathCloud):
            print('WARNING: the following folder is not accessible from your machine: \n {}'.format(str_PathCloud))
            print(' (*) Please Contact HK Team to have access to the folder and all the features of the App')
            return -1
        elif not fl.fBl_FileExist(os.path.join(str_PathCloud, 'DatabasePassword.csv')):
            print('WARNING: you have access to the following folder but your cloud is not synch with the rest \n {}'.format(str_PathCloud))
            print(' (*) Please Contact HK Team to import the file to manage Database')
            return -1
        # PARAM
        d_param['str_uid'] = os.getlogin()
        l_uid2 = d_param['str_uid'].replace('.',' ').split(' ')
        d_param['str_uid2'] = ' '.join([mot[:1].upper() + mot[1:] for mot in l_uid2])
        d_param['dte_Date'] = dt.datetime.now().date().strftime('%Y-%m-%d')
        if not 'str_action' in d_param:     
            print('WARNING Log_Python, you did not define Action in the dico: \n{}'.format(d_param))
            d_param['str_action'] = ''
        if not 'bl_error' in d_param:           d_param['bl_error'] = 0
        if not 'str_Program' in d_param:        d_param['str_Program'] = ''
        if not 'str_path' in d_param:           d_param['str_path'] = os.path.dirname(os.path.abspath(__file__))
        if not 'str_comment' in d_param:        d_param['str_comment'] = ''
        # Query
        str_query = """EXEC sp_log_add '{0}', 'Python', '{1}', {2}, '{3}', '{4}', '{5}', '{6}','{7}'
                    """.format(d_param['str_uid'], d_param['str_action'], d_param['bl_error'], d_param['str_Program'], 
                    d_param['str_path'], d_param['str_uid2'], d_param['dte_Date'], d_param['str_comment'])
        db_EXEC(str_query, '', 'SolaQC')
    except Exception as err:        print('Log_Python did not work, please contact HK Team (LAURENT TUPIN)\n{}'.format(str(err)))
        


##########################################################
####### Encrypt ###########################
##########################################################
def fStr_Encrypt_GetPass(str_input):
    str_output = str_input
    str_output = str_output.replace('9','3')
    str_output = str_output.replace('y','r')
    str_output = str_output.replace('@','!')
    str_output = str_output.replace('T','M')
    str_output = str_output.replace('5','2')
    str_output = str_output.replace('z','v')
    str_output = str_output.replace('A','nx')
    return str_output

