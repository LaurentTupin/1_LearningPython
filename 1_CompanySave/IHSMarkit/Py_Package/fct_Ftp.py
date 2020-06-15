import os, datetime as dt, numpy as np
import ftplib
from ssl import SSLSocket
import paramiko as pmiko
import fct_Files as fl




#******************************************************************************
#******** Class Correction of FTP_TLS *****************************************
# Source: https://raw.githubusercontent.com/weewx/weewx/master/bin/weeutil/ftpupload.py
class ReusedSslSocket(SSLSocket):
    def unwrap(self):
        pass

class FTP_TLS_IgnoreHost(ftplib.FTP_TLS):
    def makepasv(self):
        _, port = super().makepasv()
        return self.host, port
    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn, server_hostname = self.host, session = self.sock.session)
            conn.__class__ = ReusedSslSocket
        return conn, size
# *****************************************************************************



#---------------------------------------------------------------
#------------- Decorator -------------
#---------------------------------------------------------------
def dec_singletonsClass(input_classe):
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
# ------------- CLASS FTP management ---------------------------
#---------------------------------------------------------------
@dec_singletonsClass
class c_FTP():
    def __init__(self, str_host, str_uid, str_pwd, bl_ssl = False, int_timeOut = -1, int_portnumber = 21):
        #print('New FTP Connection')
        self.__str_host = str_host
        self.__str_uid = str_uid
        self.__str_pwd = str_pwd        
        self.__bl_ssl = bl_ssl
        self.__int_timeOut = int_timeOut
        self.__int_portnumber = int_portnumber
        
    def __del__(self):
        self.__ftpConnexionClose()
        
    def __ftpConnexionClose(self):
        #print('Closing FTP Connection: {}'.format(self.__str_host))
        try:    
            self.o_ftpConnexion.quit()  
            self.o_ftpConnexion.close()
        except: pass

    # ========== CONNEXION ==============================
    def __ftpClassic_Connect(self):
        try:
            if self.__int_timeOut <= 0:
                ftp_connect = ftplib.FTP(self.__str_host)
            else:
                ftp_connect = ftplib.FTP(self.__str_host, timeout = self.__int_timeOut)
            ftp_connect.login(user = self.__str_uid, passwd = self.__str_pwd)
        except:
            print(' ERROR: f_ftpConect in c_FTP')
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__int_timeOut )
            raise
        self.o_ftpConnexion = ftp_connect
        
    def __ftpSSL_Connect(self):
        try:
            ftp_connect = FTP_TLS_IgnoreHost(self.__str_host)
            if self.__int_timeOut <= 0:
                ftp_connect.connect(host = self.__str_host, port = self.__int_portnumber)
            else:
                ftp_connect.connect(host = self.__str_host, port = self.__int_portnumber, timeout = self.__int_timeOut)
            ftp_connect.auth()
            #            ftp_connect.set_debuglevel(1)  
            #            ftp_connect.set_pasv(True) 
            ftp_connect.login(user =  self.__str_uid, passwd = self.__str_pwd)
            ftp_connect.prot_p()
        except:
            print(' ERROR: ftpSSL_Connect')
            print(' - ' + self.__str_host, self.__str_uid, self.__str_pwd, ' | Port: ', self.__int_portnumber)
            raise
        self.o_ftpConnexion = ftp_connect
    
    def ftp_Connect(self, str_host, str_uid, str_pwd, bl_ssl = False, int_timeOut = -1, int_portnumber = 21):
        if self.__str_host == str_host and self.__str_uid == str_uid and self.__str_pwd == str_pwd and self.__bl_ssl == bl_ssl:
            try:
                ftpConnexion = self.o_ftpConnexion
                #print(' FTP: An existing connexion already exist and will be used again | Server: {}'.format(ftpConnexion.host))
                return True
            except: pass
        else:
            self.__ftpConnexionClose()          # Even if connexion NOT exist, does not matter as it will pass on expect of the function
            self.__init__(str_host, str_uid, str_pwd, bl_ssl, int_timeOut, int_portnumber) # Init the variables
        # CONNECT
        try:
            if self.__bl_ssl:   self.__ftpSSL_Connect() 
            else:               self.__ftpClassic_Connect()
        except:
            self.__init__(str_host.replace(' ', ''), str_uid.replace(' ', ''), str_pwd.replace(' ', ''), bl_ssl, int_timeOut, int_portnumber)
            if self.__bl_ssl:   self.__ftpSSL_Connect() 
            else:               self.__ftpClassic_Connect()
            print(' WARNING: A parameter in the FTP must have a space in it, please remove it !')
            
    # ==================================================
    
    
    def ftp_changeFolder(self, l_Folder):
        # Was the past connexion already on some folder ?
        try:        l_pastSessionFolder = self.l_Folder
        except:     l_pastSessionFolder = []
        # if Past Folder List is the same than the one now: DO NOTHING
        if l_Folder == l_pastSessionFolder:     return True
        # Run the List of Folder BACKWARD to go back to root
        try:
            for str_folder in l_pastSessionFolder:
                if not str_folder == None:
                    self.o_ftpConnexion.cwd("../")
        except:
            print(' ERROR: ftp_changeFolder, FTP could not change backwards folder')
            print(' - ', l_Folder)
        # Run the List of Folder
        try:
            for str_folder in l_Folder:
                if not str_folder == None:
                    self.o_ftpConnexion.cwd(str_folder)
        except:
            print(' ERROR: ftp_changeFolder, FTP could not change folder')
            print(' - ', l_Folder)
            try:    print(' - ', str_folder)
            except: pass
        # Fin: Assign the folder to a variable to check up later
        self.l_Folder = l_Folder
        
        
    def fL_fileInFTP(self):
        try:    self.l_nameFiles = self.o_ftpConnexion.nlst()
        except:
            print(' ERROR in fL_fileInFTP')
            raise
        return self.l_nameFiles
        
    def fL_fileInFTP_wCharac(self):
        try:    self.l_nameFiles_wCharac = self.o_ftpConnexion.retrlines('LIST')
        except:
            print(' ERROR in fL_fileInFTP')
            raise
        return self.l_nameFiles_wCharac
        
    
    def ftp_DownloadFile(self, str_fileName, str_folder):
        # Create the file
        try:
            Open_file = open(os.path.join(str_folder, str_fileName), 'wb')
        except:
            print(' ERROR in ftp_DownloadFile - Creation of the file')
            print(' - ', str_folder, str_fileName)
            raise
        # Fill the file with whats in FTP
        try:
            self.o_ftpConnexion.retrbinary('RETR {}'.format(str_fileName), Open_file.write)
        except Exception as err:  
            print(' ERROR in ftp_DownloadFile - retrbinary | {}'.format(str(err)))
            print(' - ', str_folder, str_fileName)
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__bl_ssl, self.__int_timeOut, self.__int_portnumber)
            Open_file.close()
            # delete the file
            fl.del_fichier(str_folder, str_fileName)
            raise
        Open_file.close()
        
        
    def ftp_UploadFile(self, str_fileName, str_folder):
        # Create the file
        try:
            Open_file = open(os.path.join(str_folder, str_fileName), 'rb')
        except:
            print(' ERROR in ftp_UploadFile - Opening of the file')
            print(' - ', str_folder, str_fileName)
            raise
        # Fill the file with whats in FTP
        try:
            self.o_ftpConnexion.storbinary('STOR {}'.format(str_fileName), Open_file)
        except Exception as err:
            Open_file.close()
            print(' ERROR in ftp_UploadFile - storbinary | {}'.format(str(err)))
            print(' - ', str_folder, str_fileName)
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__bl_ssl, self.__int_timeOut, self.__int_portnumber)
            raise
        Open_file.close()
        
        
#str_fileName = 'WisdomTreePCF_COMS_20200518.xlsx'
#str_folder = r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Auto_py\HK_WisdomTree Commodity\WCOE open 20200519'
### CONNECT
##inst_ftp = ftp_prep2('ftp.wisdomtree.com', 'markiteu','eternalsunshine',[], True)
#ftp_connect = FTP_TLS_IgnoreHost('ftp.wisdomtree.com')
#ftp_connect.connect(host = 'ftp.wisdomtree.com', port = 21)
#ftp_connect.auth()
#ftp_connect.set_debuglevel(1)  
#ftp_connect.set_pasv(True) 
#ftp_connect.login(user = 'markiteu', passwd = 'eternalsunshine')
#ftp_connect.prot_p()
##UPLOAD
##Open_file = open(os.path.join(str_folder, str_fileName), 'rb')
##ftp_connect.storbinary('STOR {}'.format(str_fileName), Open_file)
##inst_ftp.o_ftpConnexion.storbinary('STOR ' + str_fileName, Open_file)
#
##DOWNLOAD
#Open_file  = open(os.path.join(str_folder, str_fileName), 'wb')
#ftp_connect.retrbinary('RETR {}'.format(str_fileName), Open_file.write)
##inst_ftp.o_ftpConnexion.retrbinary('RETR {}'.format(str_fileName), Open_file.write)
#
#Open_file.close()
#ftp_connect.quit()
#ftp_connect.close()



  
        
# ------------- SFTP ----------------------------------------
@dec_singletonsClass
class c_SFTP():
    def __init__(self, str_host, str_uid, str_pwd, int_timeOut = -1, int_portnumber = 22):
        #print('New SFTP Connection')
        self.__str_host = str_host
        self.__str_uid = str_uid
        self.__str_pwd = str_pwd        
        self.__int_timeOut = int_timeOut
        self.__int_portnumber = int_portnumber
        
    def __del__(self):
        self.__sftpConnexionClose()
        
    def __sftpConnexionClose(self):
        print('Closing SFTP Connection: {}'.format(self.__str_host))
        try:    self.o_sftpOpen.close()
        except: pass
        try:    self.o_sftpConnexion.close()
        except: pass
    
    # ========== CONNEXION ==============================
    def sftp_Connect(self, str_host, str_uid, str_pwd, int_timeOut = -1, int_portnumber = 22):
        if self.__str_host == str_host and self.__str_uid == str_uid and self.__str_pwd == str_pwd:
            try:
                sftpConnexion = self.o_sftpConnexion
                #print(' SFTP: An existing connexion already exists and will be used again | Server: {}'.format(sftpConnexion.host))
                return True
            except: pass
        else:
            self.__sftpConnexionClose()          # Even if connexion NOT exist, does not matter as it will pass on expect of the function
            self.__init__(str_host, str_uid, str_pwd, int_timeOut, int_portnumber) # Init the variables
        # CONNECT
        try:
            ssh_Client = pmiko.SSHClient()
            ssh_Client.set_missing_host_key_policy(pmiko.AutoAddPolicy())
            ssh_Client.load_system_host_keys()
            if int_portnumber == -1:    ssh_Client.connect(str_host, username = str_uid, password = str_pwd)
            else:                       ssh_Client.connect(str_host, username = str_uid, password = str_pwd, port = int_portnumber)
        except:
            print(' ERROR in sftp_Connect (PARAMIKO)')
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd)
            raise
        self.o_sftpConnexion = ssh_Client
        
    def sftp_open(self):
        try:
            sftp_open = self.o_sftpConnexion.open_sftp()
        except:
            print(' ERROR in sftp_open - Open SFTP')
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd)
            raise
        self.o_sftpOpen = sftp_open
    # ==================================================
    
        
    def sftp_changeFolder(self, l_Folder):
        # Was the past connexion already on some folder ?
        try:        l_pastSessionFolder = self.l_Folder
        except:     l_pastSessionFolder = []
        # if Past Folder List is the same than the one now: DO NOTHING
        if l_Folder == l_pastSessionFolder:     return True
        # Run the List of Folder BACKWARD to go back to root
        try:
            for str_folder in l_pastSessionFolder:
                if not str_folder == None:
                    self.o_sftpOpen.chdir("../")
        except:
            print(' ERROR: sftp_changeFolder, SFTP could not change backwards folder')
            print(' - ', l_Folder)
        # Run the List of Folder
        try:
            for str_folder in l_Folder:
                if not str_folder == None:
                    self.o_sftpOpen.chdir(str_folder)
        except:
            print(' ERROR: sftp_changeFolder, SFTP could not change folder')
            print(' - ', l_Folder)
            try:    print('  - ', str_folder)
            except: pass
        # Fin: Assign the folder to a variable to check up later
        self.l_Folder = l_Folder
        
    
    def sftp_DownloadFile(self, str_fileName, str_folder):
        try:
            self.o_sftpOpen.get(str_fileName, os.path.join(str_folder, str_fileName))
        except Exception as err:
            print(' ERROR in sftp_DownloadFile - get : {}'.format(str(err)))
            print(' - ', str_fileName)
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__int_timeOut, self.__int_portnumber)
            # delete the file
            fl.del_fichier(str_folder, str_fileName)
            #self.__sftpConnexionClose()
            raise
        return True
        
    def sftp_UploadFile(self, str_fileName, str_folder):
        try:
            self.o_sftpOpen.put(os.path.join(str_folder, str_fileName), str_fileName)
        except Exception as err:
            print(' ERROR in sftp_UploadFile - put : {}'.format(str(err)))
            print(' - ',  str_fileName)
            print(' - ', self.__str_host, self.__str_uid, self.__str_pwd, self.__int_timeOut, self.__int_portnumber)
            #self.__sftpConnexionClose()
            raise
        return True

    def fL_fileInSFTP(self):
        try:    self.l_nameFiles = self.o_sftpOpen.listdir()
        except:
            print(' ERROR in fL_fileInSFTP')
            raise
        return self.l_nameFiles
        
    def fL_fileInSFTP_wCharac(self):
        try:    
            l_Files = self.o_sftpOpen.listdir_attr()
            l_Files = [file for file in l_Files if '.' in file.filename]
            self.l_nameFiles_wCharac = l_Files
        except:
            print(' ERROR in fL_fileInSFTP_wCharac')
            raise
        return self.l_nameFiles_wCharac
    
    

    
#---------------------------------------------------------------
# ------ CONTINUITY: Function to launch Class ------------------
#---------------------------------------------------------------
def ftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, bl_ssl = False, int_timeout = -1):
    inst_ftp = c_FTP(str_host, str_uid, str_pwd, bl_ssl, int_timeout)
    inst_ftp.ftp_Connect(str_host, str_uid, str_pwd, bl_ssl, int_timeout)   # Carry out check if nay of this vraiables changed
    inst_ftp.ftp_changeFolder(l_ftpFolder)
    return inst_ftp
    
def ftp_listFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, bl_ssl = False):
    inst_ftp = ftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, bl_ssl, int_timeout)
    l_nameFiles = inst_ftp.fL_fileInFTP()
    return l_nameFiles
    
#ftp_listFolder('ftpnew.wisdomtree.com', 'UCITSPCF', 'ucitsaps', ['ForwardContracts'],-1,True)
#l_files = ftp_listFolder('ftp.msci.com', 'hehurqmw ', 'cd8s=2dPV$EX+T', [''])
#print(l_files)

def ftp_printListFile_wCharac(str_host, str_uid, str_pwd,l_ftpFolder, int_timeout = -1, bl_ssl = False):
    inst_ftp = ftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, bl_ssl, int_timeout)
    l_nameFiles = inst_ftp.fL_fileInFTP_wCharac()
    return l_nameFiles
    
def fBl_ftpDownFileBinary(str_host, str_uid, str_pwd,l_ftpFolder, str_fileName, str_folder, int_timeout = -1, bl_ssl = False):
    inst_ftp = ftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, bl_ssl, int_timeout)
    inst_ftp.ftp_DownloadFile(str_fileName, str_folder)
    return True

#fBl_ftpDownFileBinary('ftp.msci.com', 'hehurqmw', 'cd8s=2dPV$EX+T', ['download'], '20200610_20200610d_10740_.zip', 
#                      r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Auto_py\US_Harvest\H_20200610\raw')
    
def fBl_ftpUpFile_Bi(str_host, str_uid, str_pwd,l_ftpFolder, str_fileName, str_folder, int_timeout = -1, bl_ssl = False):
    inst_ftp = ftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, bl_ssl, int_timeout)
    inst_ftp.ftp_UploadFile(str_fileName, str_folder)
    return True
    


# ------------- SFTP ----------------------------------------
def sftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1):
    inst_sftp = c_SFTP(str_host, str_uid, str_pwd, int_timeout)
    inst_sftp.sftp_Connect(str_host, str_uid, str_pwd, int_timeout)   # Carry out check if nay of this vraiables changed
    inst_sftp.sftp_open()
    inst_sftp.sftp_changeFolder(l_ftpFolder)
    return inst_sftp

def ssh_downFile(str_host, str_uid, str_pwd, l_ftpFolder, str_fileName, str_folder, int_timeout = -1):
    inst_sftp = sftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout)
    inst_sftp.sftp_DownloadFile(str_fileName, str_folder)
    return True
    
def ssh_upFile(str_host, str_uid, str_pwd, l_ftpFolder, str_fileName, str_folder, int_timeout = -1):   
    inst_sftp = sftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout)
    inst_sftp.sftp_UploadFile(str_fileName, str_folder)
    return True

def ssh_listFilesInFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1):
    inst_sftp = sftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout)
    l_nameFiles = inst_sftp.fL_fileInSFTP()
    return l_nameFiles

def ssh_listFilesInFolder_wCharac(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1 ):
    inst_sftp = sftp_prep(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout)
    l_nameFiles = inst_sftp.fL_fileInSFTP_wCharac()
    return l_nameFiles

# print(ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, ['DeutscheBank', 'Bond']))
def ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1 ):
    l_Files = ssh_listFilesInFolder_wCharac(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout)
    try:
        l_dteModified = [file.st_mtime for file in l_Files]
        argMax_LastDate = np.argmax(l_dteModified)
    except:
        print(' ERROR in ssh_getLastFile_inFolder')
        print(' - ', str_host, str_uid, str_pwd, l_ftpFolder, int_timeout)
        raise
    return l_Files[argMax_LastDate]

def ssh_getLastFile_inFolder_name(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1 ):
    file = ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout)
    return file.filename
    
def ssh_getLastFile_inFolder_date(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1 ):
    file = ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout)
    return dt.datetime.fromtimestamp(file.st_mtime)

def ssh_getLastFile_inFolder_size(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1 ):
    file = ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout)
    return file.st_size
#-----------------------------------------------------------------


##HK_EASY
#l_file = ssh_listFilesInFolder('upload.data.euronext.com', 'IHSMarkit', 'Pj35TANS2', [])
#print(l_file)

##WisdomTree
#l_file = ftp_listFolder('ftp.wisdomtree.com', 'markiteu', 'eternalsunshine', [], -1, True)
#print(l_file)





##################################################################
### Course ###
##################################################################
#
# 1. ftp_connect.retrlines('LIST')
# ==> drwxr-xr--   dds grp            0 Feb 23  2002 data
#    TYPE
#    .d
#       d = dossier
#       - = fichier
#    Droit du proprietaire
#    .rwx
#       r = read
#       w = write (add and delete)
#       x = execute (pour un fichier)
#    Droit du groupe propriétaire
#    .r-x
#    Droit des autres
#    .r--





###################################################################
#### S-Ftp ###
###################################################################
##To use pysftp, you need to install it via your pip.
##   Open Anaconda CMD
##   pip install pysftp
#import pysftp as sftp
#import time as t
#
#def sftp_connect(str_host, str_uid, str_pwd, int_portnumber = 22):
#    sftp_con = None
#    for i in range(10):
#        try:
#            sftp_con = sftp.Connection(host = str_host, username = str_uid, password = str_pwd)
#            break
#        except:
#            print("Could not authenticate... Will re-attempt")
#            t.sleep(5)
#    if not sftp_con: return False
#    return sftp_con
#
#def sftp_changeFolder(sftp_con, *t_Folder):
#    for str_folder in t_Folder:
#        sftp_con.cwd(str_folder)
#    return sftp_con
#
#def sftp_downloadFile(sftp_con, str_localPath, str_ftpPath): 
#    #str_ftpPath = '/var/www/html/pcf1.txt'
#    sftp_con.get(str_ftpPath)
#
#def sftp_uploadFile(sftp_con, str_localPath, str_ftpPath):
#    sftp_con.put(str_localPath, str_ftpPath)
#
##To use 
##mySFtp = m_ftp.sftp_connect(str_server, str_uid, str_pwd, int_portnumber)
##data = mySFtp.listdir()  #mySFtp.listdir_attr()
##print(data)
##mySFtp.close()
##-----------------------------------------------------------------



###################################################################
#### Copy Files from FTP ###
###################################################################
#from fs.copy import copy_fs
#def fs_copyFileFtp(str_host, str_uid, str_pwd, str_ftpFolder = '', str_localFolder = 'osfs://C:/temp/'):
#    try:
#        ftp_url = 'ftp://' + str_uid + ":" + str_pwd + "@" + str_host + str_ftpFolder     # "/ThinkCapital/"
#        copy_fs(ftp_url, str_localFolder)                                                   # 'osfs://C:/temp/test/'
#    except Exception as ex:
#        print("FAILS : fs_copyFileFtp")     
#    
##To use
##m_ftp.fs_copyFileFtp(str_server, str_uid, str_pwd, '', 'osfs://C:/temp/test/')
##-----------------------------------------------------------------
    
    
#    import http.client
#
#    html = http.client.HTTPConnection(str_host, port= str(81))
#    html.request("GET", '/command=AB&time=' + str(F1))
#    r1 = html.getresponse()
#    
#    out = r1.read()
#    f = open('Files/' + IP + '-' + str(F1) + '.xml', 'wb')
#    f.write(out)
#    f.close()
    










###################################################################
#### OLD FUNCTION before CLASS ###
###################################################################  




####################################################################
##### FTP without SSL ###
####################################################################  
#def f_ftpConect(str_host, str_uid, str_pwd, int_timeout = -1):
#    try:
#        if int_timeout == -1 or int_timeout == 0:
#            ftp_connect = ftplib.FTP(str_host)
#        else:
#            ftp_connect = ftplib.FTP(str_host, timeout = int_timeout)
#        ftp_connect.login(user=str_uid, passwd=str_pwd)
#    except:
#        print(' ERROR: f_ftpConect')
#        print(' - ' + str_host, str_uid, str_pwd, int_timeout )
#        raise
#    return ftp_connect
#
#
#def ftp_changeFolder(ftp_connect, l_Folder):
#    try:
#        for str_folder in l_Folder:
#            if not str_folder == None:
#                ftp_connect.cwd(str_folder)
#    except:
#        print(' ERROR: FTP could not change folder')
#        print(' -  ' + l_Folder)
#        raise
#    return ftp_connect
#
#
#### FTP with SSL ###
#def ftp_connectTLS(str_host, str_uid, str_pwd, int_timeout = -1, int_portnumber = 21):
#    try:
#        ftps_connect = ftplib.FTP_TLS(str_host)
#        #ftps_connect.debug(3)
#        if int_timeout == -1 or int_timeout == 0:
#            ftps_connect.connect(host=str_host, port=int_portnumber)
#        else:
#            ftps_connect.connect(host=str_host, port=int_portnumber, timeout=int_timeout)
#        ftps_connect.auth()
#        ftps_connect.login(user=str_uid, passwd=str_pwd)
#        ftps_connect.prot_p()
#    except:
#        print(' ERROR: ftp_connectTLS')
#        print(' - ' + str_host, str_uid, str_pwd, ' | Timeout: ', int_timeout, ' | Port: ', int_portnumber)
#        raise
#    return ftps_connect
#    
#
#def ftp_listFolder(str_host, str_uid, str_pwd, l_ftpFolder, int_timeout = -1, bl_ssl = False):
#    try:
#        if bl_ssl:      my_ftp = ftp_connectTLS(str_host, str_uid, str_pwd, int_timeout)
#        else:           my_ftp = f_ftpConect(str_host, str_uid, str_pwd, int_timeout)
#    except:
#        print(' ERROR in ftp_listFolder - Connect FTP')
#        print(' - ' + str_host, str_uid, str_pwd, l_ftpFolder)
#        raise
#    try:
#        if not my_ftp: return False
#        my_ftp = ftp_changeFolder(my_ftp, l_ftpFolder)
#        l_nameFiles = my_ftp.nlst()
#        my_ftp.close()
#    except:
#        print(' ERROR in ftp_listFolder')
#        print(' -  ' + str_host, str_uid, str_pwd, l_ftpFolder, int_timeout)
#        if my_ftp: my_ftp.close()
#        raise
#    return l_nameFiles
#
#
#def ftp_printListFile_wCharac(str_host, str_uid, str_pwd,l_ftpFolder, int_timeout = -1, bl_ssl = False):
#    try:
#        if bl_ssl:      my_ftp = ftp_connectTLS(str_host, str_uid, str_pwd, int_timeout)
#        else:           my_ftp = f_ftpConect(str_host, str_uid, str_pwd, int_timeout)
#    except:
#        print(' ERROR in ftp_printListFile_wCharac - Connect FTP')
#        print(' - ' + str_host, str_uid, str_pwd, l_ftpFolder)
#        raise
#    try:
#        if not my_ftp: return False
#        my_ftp = ftp_changeFolder(my_ftp, l_ftpFolder)
#        l_nameFiles = my_ftp.retrlines('LIST')
#        my_ftp.close()
#    except:
#        print(' ERROR in ftp_printListFile_wCharac')
#        print(' -  ' + str_host, str_uid, str_pwd, l_ftpFolder)
#        my_ftp.close()
#        raise
#    return l_nameFiles
#    
#
#def fBl_ftpDownFileBinary(str_host, str_uid, str_pwd,l_ftpFolder, str_fileName, str_filePathDest, int_timeout = -1, bl_ssl = False):
#    try:
#        if bl_ssl:      my_ftp = ftp_connectTLS(str_host, str_uid, str_pwd, int_timeout)
#        else:           my_ftp = f_ftpConect(str_host, str_uid, str_pwd, int_timeout)
#    except:
#        print(' ERROR in fBl_ftpDownFileBinary - Connect FTP')
#        print(' - ' + str_host, str_uid, str_pwd,l_ftpFolder, str_fileName)
#        raise
#    if not my_ftp: 
#        print(' EMPTY: fBl_ftpDownFileBinary can not Connect with FTP')
#        print(' - ' + str_host, str_uid, str_pwd,l_ftpFolder, str_fileName)
#        return False
#    try:
#        my_ftp = ftp_changeFolder(my_ftp, l_ftpFolder)
#    except:
#        print(' ERROR in fBl_ftpDownFileBinary - Opening Folders')
#        print(' - ' + str_host, str_uid, str_pwd,l_ftpFolder, str_fileName)
#        raise
#    #my_ftp.retrlines('LIST')
#    try:
#        Open_file = open(str_filePathDest + str_fileName, 'wb')
#    except:
#        print(' ERROR in fBl_ftpDownFileBinary - Open_file')
#        print(' - ' + str_host, str_uid, str_pwd,l_ftpFolder, str_fileName)
#        raise
#    try:
#        my_ftp.retrbinary('RETR ' + str_fileName, Open_file.write)
#    except:
#        print(' ERROR in fBl_ftpDownFileBinary - DOWNLOAD')
#        print(' - ' + str_host, str_uid, str_pwd,l_ftpFolder, str_fileName)
#        Open_file.close()
#        # delete the file
#        fl.del_fichier(str_filePathDest, str_fileName)
#        raise
#    Open_file.close()
#    my_ftp.close
#    return True
#    
#
#def fBl_ftpUpFile_Bi(str_host, str_uid, str_pwd,l_ftpFolder, str_fileName, str_filePathDest, int_timeout = -1, bl_ssl = False):
#    try:
#        if bl_ssl:      my_ftp = ftp_connectTLS(str_host, str_uid, str_pwd, int_timeout)
#        else:           my_ftp = f_ftpConect(str_host, str_uid, str_pwd, int_timeout)
#    except:
#        print(' ERROR in fBl_ftpUpFile_Bi - Connect FTP')
#        print(' - ' + str_host, str_uid, str_pwd,l_ftpFolder, str_fileName)
#        raise
#    if not my_ftp: 
#        print(' EMPTY: fBl_ftpUpFile_Bi can not Connect with FTP')
#        print(' - ' + str_host, str_uid, str_pwd,l_ftpFolder, str_fileName)
#        return False
#    try:
#        my_ftp = ftp_changeFolder(my_ftp, l_ftpFolder)
#    except:
#        print(' ERROR in fBl_ftpUpFile_Bi - Opening Folders')
#        print(' - ' + str_host, str_uid, str_pwd,l_ftpFolder, str_fileName)
#        raise
#    #my_ftp.retrlines('LIST')
#    try:
#        Open_file = open(str_filePathDest + str_fileName, 'rb')
#    except:
#        print(' ERROR in fBl_ftpUpFile_Bi - Open_file')
#        print(' - ' + str_host, str_uid, str_pwd,l_ftpFolder, str_fileName)
#        raise
#    try:
#        my_ftp.storbinary('STOR ' + str_fileName, Open_file)    #Open_file.write)
#    except:
#        print(' ERROR in fBl_ftpUpFile_Bi - UPLOAD')
#        print(' - ' + str_host, str_uid, str_pwd,l_ftpFolder, str_fileName)
#        Open_file.close()
#        raise
#    Open_file.close()
#    my_ftp.close
#    return True




###################################################################
#### Paramiko ###
###################################################################
## http://docs.paramiko.org/en/2.4/api/sftp.html
## https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter16/sftp_get.py
## https://www.youtube.com/results?search_query=python+ssh
## https://www.youtube.com/watch?v=2Vn4yzvUtPY
##To use paramiko, you need to install it via your pip.
##   Open Anaconda Prompt
##   pip install paramiko
#
#
#def ssh_connect(str_host, str_uid, str_pwd, int_portnumber = -1):
#    try:
#        ssh_Client = pmiko.SSHClient()
#        ssh_Client.set_missing_host_key_policy(pmiko.AutoAddPolicy())
#        ssh_Client.load_system_host_keys()
#        if int_portnumber == -1:    ssh_Client.connect(str_host, username = str_uid, password = str_pwd)
#        else:                       ssh_Client.connect(str_host, username = str_uid, password = str_pwd, port = int_portnumber)
#    except:
#        print(' ERROR in ssh_connect (PARAMIKO)')
#        print(' - ' + str_host, str_uid, str_pwd)
#        raise
#    return ssh_Client
#
#
## DOWNLOAD
#def ssh_downFile(str_host, str_uid, str_pwd, l_sshFolder, str_fileName, str_filePathDest, int_timeout = -1):
#    try:
#        ssh_Client = ssh_connect(str_host, str_uid, str_pwd, int_timeout)
#        sftp_open = ssh_Client.open_sftp()
#    except:
#        print(' ERROR in ssh_downFile - Open SFTP')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, str_fileName)
#        raise
#    try:
#        for folder in l_sshFolder:
#            sftp_open.chdir(folder)  
#    except:
#        print(' ERROR in ssh_downFile - Opening Folders')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, str_fileName)
#        ssh_Client.close()
#        raise
#    try:
#        sftp_open.get(str_fileName, os.path.join(str_filePathDest, str_fileName))
#    except:
#        print(' ERROR in ssh_downFile - Paramiko could not download the file')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, str_fileName)
#        ssh_Client.close()
#        # delete the file
#        fl.del_fichier(str_filePathDest, str_fileName)
#        raise
#    ssh_Client.close()
#    return True
#
#
## UPLOAD
#def ssh_upFile(str_host, str_uid, str_pwd, l_sshFolder, str_fileName, str_filePathDest, int_timeout = -1):
#    try:
#        ssh_Client = ssh_connect(str_host, str_uid, str_pwd, int_timeout)
#        sftp_open = ssh_Client.open_sftp()
#    except:
#        print(' ERROR in ssh_upFile - Open SFTP')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, str_fileName)
#        raise
#    try:
#        for folder in l_sshFolder:
#            sftp_open.chdir(folder)  
#    except:
#        print(' ERROR in ssh_upFile - Opening Folders')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, str_fileName)
#        ssh_Client.close()
#        raise
#    try:
#        sftp_open.put(os.path.join(str_filePathDest, str_fileName), str_fileName)
#    except:
#        print(' ERROR in ssh_upFile - Paramiko could not upload the file')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, str_fileName)
#        ssh_Client.close()
#        raise
#    ssh_Client.close()
#    return True
#
#
##a = ssh_listFilesInFolder(str_host, str_uid, str_pwd, ['DeutscheBank', 'Bond'])
#def ssh_listFilesInFolder(str_host, str_uid, str_pwd, l_sshFolder, int_portnumber = -1 ):
#    try:
#        ssh_Client = ssh_connect(str_host, str_uid, str_pwd, int_portnumber)
#        sftp = ssh_Client.open_sftp()
#        for folder in l_sshFolder:
#            sftp.chdir(folder)
#        l_nameFiles = sftp.listdir()
#        ssh_Client.close()
#    except:
#        print(' ERROR in ssh_listFilesInFolder')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        raise
#    return l_nameFiles
#    
#
## print(ssh_listFilesInFolder_wCharac(str_host, str_uid, str_pwd, ['DeutscheBank', 'Bond']))
#def ssh_listFilesInFolder_wCharac(str_host, str_uid, str_pwd, l_sshFolder, int_portnumber = -1 ):
#    try:
#        ssh_Client = ssh_connect(str_host, str_uid, str_pwd, int_portnumber)
#        sftp = ssh_Client.open_sftp()
#    except:
#        print(' ERROR in ssh_listFilesInFolder_wCharac - Open SFTP')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        raise
#    try:
#        for folder in l_sshFolder:
#            sftp.chdir(folder)
#    except:
#        print(' ERROR in ssh_listFilesInFolder_wCharac - Opening Folders')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        raise
#    try:
#        l_Files = sftp.listdir_attr()
#        l_Files = [file for file in l_Files if '.' in file.filename]
#        #l_characFiles = [(file.filename, file.st_size, dt.datetime.fromtimestamp(file.st_mtime)) for file in l_Files]
#    except:
#        print(" ERROR in ssh_listFilesInFolder_wCharac - Get attrib of files 'listdir_attr'")
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        raise
#    try: ssh_Client.close()
#    except:
#        print(" ERROR in ssh_listFilesInFolder_wCharac - Close connexion")
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        raise
#    return l_Files
#
#
## print(ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, ['DeutscheBank', 'Bond']))
#def ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_sshFolder, int_portnumber = -1 ):
#    try:
#        l_Files = ssh_listFilesInFolder_wCharac(str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#    except:
#        print(' ERROR in ssh_getLastFile_inFolder')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        raise
#    if l_Files == []:
#        print(' EMPTY in ssh_getLastFile_inFolder')
#        print('  ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        return False
#    try:
#        l_dteModified = [file.st_mtime for file in l_Files]
#        argMax_LastDate = np.argmax(l_dteModified)
#    except:
#        print(' ERROR in ssh_getLastFile_inFolder to get l_dteModified')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        raise
#    return l_Files[argMax_LastDate]
#    
#
#def ssh_getLastFile_inFolder_name(str_host, str_uid, str_pwd, l_sshFolder, int_portnumber = -1 ):
#    try:
#        file = ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#    except:
#        print(' ERROR in ssh_getLastFile_inFolder_name')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        raise
#    if not file:
#        print(' EMPTY in ssh_getLastFile_inFolder_name')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        return False
#    return file.filename
#    
#
#def ssh_getLastFile_inFolder_date(str_host, str_uid, str_pwd, l_sshFolder, int_portnumber = -1 ):
#    try:
#        file = ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#    except:
#        print(' ERROR in ssh_getLastFile_inFolder_date')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        raise
#    if not file:
#        print(' EMPTY in ssh_getLastFile_inFolder_date')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        return False
#    return dt.datetime.fromtimestamp(file.st_mtime)
#    
#
#def ssh_getLastFile_inFolder_size(str_host, str_uid, str_pwd, l_sshFolder, int_portnumber = -1 ):
#    try:
#        file = ssh_getLastFile_inFolder(str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#    except:
#        print(' ERROR in ssh_getLastFile_inFolder_size')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        raise
#    if not file:
#        print(' EMPTY in ssh_getLastFile_inFolder_size')
#        print(' - ' + str_host, str_uid, str_pwd, l_sshFolder, int_portnumber)
#        return False
#    return file.st_size
