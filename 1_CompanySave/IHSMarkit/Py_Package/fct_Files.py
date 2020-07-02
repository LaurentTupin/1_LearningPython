import os
import pandas as pd
import datetime as dt
import shutil
from zipfile import ZipFile
import glob
import openpyxl
import win32com.client as win32
import xlsxwriter
#from openpyxl.styles import NamedStyle, Font, PatternFill, colors, Border, Side # , Alignment, Color
import openpyxl.styles as styl
import psutil
import time


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
# ------------- CLASS Excel Management (XLS, XLSX) -------------
#---------------------------------------------------------------
@dec_singletonsClass
class c_win32_xlApp():
    def __init__(self):
        #print('   *** Init class Excel Manager...')
        self.__wkIsOpen = False
        self.d_wkOpen = {}
        self.fBl_ExcelIsOpen()
    
    #=====================================================
    @property
    def visible(self):
        return self.__visible
    @visible.setter
    def visible(self, bl_visible):
        self.__visible = bl_visible
    @property
    def wb_path(self):
        return self.__wb_path
    @wb_path.setter
    def wb_path(self, str_path):
        self.__wb_path = str_path
    #=====================================================
    
    def fBl_ExcelIsOpen(self):
        try:
            self.xlApp = win32.GetActiveObject("Excel.Application")
            self.__blXlWasOpen = True
        except:
            self.__blXlWasOpen = False
        
    def FindXlApp(self, bl_visible = True, bl_gencache_EnsureDispatch = False):
        '''Get running Excel instance if possible, else return new instance.'''
        self.__visible = bl_visible
        self.__gencache_EnsureDispatch = bl_gencache_EnsureDispatch
        try:
             #print("Running Excel instance found, returning object")
            xlApp = self.xlApp
        except:
            #print("No running Excel instances, returning new instance")
            try:            
                if self.__gencache_EnsureDispatch:
                    xlApp = win32.gencache.EnsureDispatch('Excel.Application')
                else:
                    xlApp = win32.Dispatch('Excel.Application')
                    #xlApp = win32.DispatchEx('Excel.Application')
                    #xlApp = win32.dynamic.Dispatch('Excel.Application')
            except AttributeError as err_att:
                print('  ERROR in FindXlApp: {}'.format(str(err_att)))
                if "no attribute 'CLSIDToClassMap'" in str(err_att):
                    self.del_Gen_py_folder('FindXlApp')
                    return self.xlApp
        xlApp.Visible = self.__visible
        self.xlApp = xlApp
        return self.xlApp
		
    def WaitFile(self, int_sec = 1, str_msg = ' (*-*) Wait for file to load (in c_win32_xlApp)...', otherARG = ''):
        if otherARG != '': print('otherARG', otherARG, type(otherARG))
        print(str_msg)
        time.sleep(int_sec)
        
    def del_Gen_py_folder(self, str_function):
        #=====================================================
        # Documentation on the subject:
        # https://gist.github.com/rdapaz/63590adb94a46039ca4a10994dff9dbe
        # https://stackoverflow.com/questions/47608506/issue-in-using-win32com-to-access-excel-file/47612742
        #=====================================================
        str_DirPath = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Temp\gen_py')
        print('   (***) delete folder : {}'.format(str_DirPath))
        if fBl_FolderExist(str_DirPath):
            # Delete the folder
            shutil.rmtree(str_DirPath, ignore_errors = True)
        # Re- Launch Process
        if str_function == 'FindXlApp':
            # Define again the App
            xlApp = win32.Dispatch('Excel.Application')
            self.xlApp = xlApp
            return self.xlApp
        
    def OpenWorkbook(self, str_path = ''):
        if str_path != '':
            self.wb_path = str_path            
        xlWb = self.xlApp.Workbooks.Open(self.wb_path)
        self.xl_lastWk = xlWb
        # Dico - {path : obj_workbook}
        self.d_wkOpen[self.wb_path] = xlWb
        self.__wkIsOpen = True
        return self.xl_lastWk
    
    def SelectWorksheet(self):
        xlWs = self.xl_lastWsh
        # Authorize 10 try to add worksheet
        for i_try in range(1, 11):
            try:
                xlWs.Select
                return True
            except:		self.WaitFile(1, ' (**) Error on SelectWorksheet (in c_win32_xlApp), try number {}'.format(str(i_try)))
        return False
				
    def AddWorksheet(self, str_sheetName = ''):
        xlWb = self.xl_lastWk
        # Authorize 10 try to add worksheet
        for i_try in range(1, 11):
            try:
                if str_sheetName == '':		xlWs = xlWb.add_worksheet()
                else:						xlWs = xlWb.add_worksheet(str_sheetName)
                break
            except:		self.WaitFile(1, ' (**) Error on AddWorksheet (in c_win32_xlApp), try number {}'.format(str(i_try)))
        self.xl_lastWsh = xlWs
        #--------------------------------------------------
        # Shitty stuff because sheet name is not recognised
        try:        self.str_lastSheetName = self.xl_lastWsh.Name
        except Exception as Err:
            print('  ERROR in  AddWorksheet(c_win32_xlApp): {}'.format(str(Err)))
            print('  - str_sheetName: ', str_sheetName)
            self.str_lastSheetName = str_sheetName
        #--------------------------------------------------
        self.SelectWorksheet()
        return self.xl_lastWsh
	
    def RenameSheet(self, str_sheetName = ''):
        if str_sheetName != '':
            try:	self.xl_lastWsh.Name = str_sheetName  	        #xlWs.title
            except:	self.WaitFile(1, ' (**) Warning on DefineWorksheet: Could not rename Sheet into : {}'.format(str_sheetName))
		
    def DefineWorksheet(self, str_sheetName = '', int_sheetNumber = -1, str_sheetNameToADD = ''):
        xlWb = self.xl_lastWk
		# Sheets(str_sheetName)
		# Worksheets(str_sheetName)
		# ActiveSheet
		
        if str_sheetName != '':				# Name is defined
            try:	xlWs = xlWb.Sheets(str_sheetName)
            except:							# After an error, all should have been defined in the call, so RETURN to get out
                self.WaitFile(1, ' (**) Warning on DefineWorksheet: Could not find Sheet Name : {}'.format(str_sheetName))
                self.DefineWorksheet('', int_sheetNumber, str_sheetNameToADD = str_sheetName)
                return self.xl_lastWsh
            self.xl_lastWsh = xlWs
        else:
            if int_sheetNumber > 0:         # Number is defined
                try:	xlWs = xlWb.Sheets(int_sheetNumber)
                except:						# After an error, all should have been defined in the call to add worksheet, so RETURN to get out
                    self.WaitFile(1, ' (**) Warning on DefineWorksheet: Could not find Sheet Number : {}'.format(str(int_sheetNumber)))
                    self.DefineWorksheet('', -1, str_sheetNameToADD)
                    return self.xl_lastWsh
                self.xl_lastWsh = xlWs
                # Rename the Sheet if possible (if its a recall with str_sheetName defined in str_sheetNameToADD)
                self.RenameSheet(str_sheetNameToADD)
            else:
                # ADD worksheet
                self.AddWorksheet(str_sheetNameToADD)
                return self.xl_lastWsh 		# All defined in Add worksheet, we can get out
        # End
        #--------------------------------------------------
        # Shitty stuff because sheet Name is not recognised
        try:    self.str_lastSheetName = self.xl_lastWsh.Name
        except Exception as Err:
            print('  ERROR in  DefineWorksheet(c_win32_xlApp): {}'.format(str(Err)))
            print('  - ', str_sheetName, int_sheetNumber, str_sheetNameToADD)
            self.str_lastSheetName = str_sheetName
        #--------------------------------------------------
        self.SelectWorksheet()
        return self.xl_lastWsh
    
    def SaveAs(self, str_newPath, int_fileFormat = -1):
        if self.__wkIsOpen:
            # Define FileFormat
            str_lower = str_newPath.lower()
            if int_fileFormat == -1:
                if '.xlsx' in str_lower:        self.__fileFormat = 51
                elif '.xlsb' in str_lower:      self.__fileFormat = 50
                elif '.xlsm' in str_lower:      self.__fileFormat = 52
                elif '.xls' == str_lower[-4:]:  self.__fileFormat = 56
                else:                           self.__fileFormat = -1
            else:                               self.__fileFormat = int_fileFormat
            # Save As
            self.__displayAlert = self.xlApp.DisplayAlerts
            self.xlApp.DisplayAlerts = False
            try:
                if self.__fileFormat == -1:		self.xl_lastWk.SaveAs(str_newPath)
                else:							self.xl_lastWk.SaveAs(str_newPath, FileFormat = self.__fileFormat)
            except Exception as err:
                print('  Error in SaveAs (Files): {}'.format(str(err)))
                raise
            finally:
                self.xlApp.DisplayAlerts = self.__displayAlert
        else:   print('  ERROR in SaveAs (c_win32_xlApp) | a WB need to be open before to bes Saved AS')
	
    def CloseWorkbook(self, bl_saveBeforeClose = True):
        self.__saveBeforeClose = bl_saveBeforeClose
        if self.__wkIsOpen:
            self.xl_lastWk.Close(SaveChanges = self.__saveBeforeClose)
		
    def CheckAnyWkIsOpen(self):
        try:
            if self.__gencache_EnsureDispatch:		xlApp2 = win32.gencache.EnsureDispatch('Excel.Application')
            else:									xlApp2 = self.xlApp
            l_wkOpen = [wk.Name for wk in xlApp2.Workbooks]
            #            d_wkOpen = {path: wk for path, wk in self.d_wkOpen.items() if wk.Name in l_wkOpen}
            #            self.d_wkOpen = d_wkOpen
            
            d_wkOpenCopy = self.d_wkOpen.copy()
            for path, wk in d_wkOpenCopy.items():
                try:
                    wk_Name = wk.Name
                    if not wk_Name in l_wkOpen:
                        del self.d_wkOpen[path]
                except: del self.d_wkOpen[path]
            # Conclude if any wk is open
            if self.d_wkOpen:   self.__wkIsOpen = True
            else:               self.__wkIsOpen = False
        except Exception as err:
            print('  INFORMATION: CheckAnyWkIsOpen (Files): {}'.format(str(err)))
            self.__wkIsOpen = False
            self.__killExcelProcess= True
        return self.__wkIsOpen
    
    def Kill_Excel(self):
        try:
            if self.__killExcelProcess:
                for proc in psutil.process_iter():
                    if any(procstr in proc.name() for procstr in ['Excel', 'EXCEL', 'excel']):
                        proc.kill()
            #-----------------------------------------------------------------------
            elif False:     # With win32com
                o_WbemScripting = win32.Dispatch("WbemScripting.SWbemLocator")
                o_cimv2 = o_WbemScripting.ConnectServer(".", "root\cimv2")
                o_excelProcess = o_cimv2.ExecQuery("Select Caption from Win32_Process where Caption LIKE 'EXCEL%'")
                for excel in o_excelProcess:
                    try:    excel.terminate()
                    except: pass
            elif False:     # Other things picked up on Internet
                if hasattr(self, 'xlBook'):
                    print(' WARNING in Kill_Excel (Files): remaining xlBook.....')
                    del self.xl_lastWk
                import gc
                gc.collect()
            #-----------------------------------------------------------------------
            else:
                self.xlApp.Application.Quit()
                del (self.xlApp)
            #----- Delete Object to restart by Init for the Next Instance -----
            self.__del__()
        except Exception as err:
            print('  Error in Kill_Excel (Files): {}'.format(str(err)))
            raise
        
    def QuitXlApp(self, bl_force = False, bl_killExcelProcess = False):
        self.__killExcelProcess = bl_killExcelProcess
        if bl_force:
            if self.__wkIsOpen:
                try:    self.CloseWorkbook()
                except: pass
            self.Kill_Excel()
        else:
            if self.__blXlWasOpen:
                print('  (*) Warning QuitXlApp(c_win32_xlApp): Not closing EXCEL, a previous workbook might be still Open')
            else:
                self.CheckAnyWkIsOpen()
                if self.__wkIsOpen:
                    print('  (*) Warning QuitXlApp(c_win32_xlApp): Not closing EXCEL, a workbook is still Open')
                else:       
                    self.Kill_Excel()
                    
    def __del__(self):
        #        print('     *** fin Instance')
        pass



#------------------------------------------------------------------------------
# List Files in folder
#------------------------------------------------------------------------------
def fStr_BuildPath(str_folder, str_FileName):
    if str_FileName == '':      str_path = str_folder
    elif str_folder == '':      str_path = str_FileName
    else:                       str_path = os.path.join(str_folder, str_FileName)
    return str_path

def fStr_BuildFolder_wRoot(str_folderPart, str_folderRoot):
    if str_folderPart[:2] == '\\\\':    return str_folderPart
    elif str_folderPart[:2] == 'C:':    return str_folderPart
    elif str_folderPart[:2] == 'E:':    return str_folderPart
    else:                               
        return str_folderRoot + str_folderPart
    
def fBl_FileExist(str_path):
    if os.path.isfile(str_path):    return True
    else:                           return False

def fBl_FolderExist(str_path):
    if os.path.exists(str_path):    return True
    else:                           return False
    
def fList_FileInDir(str_path):
    try:        l_fic = os.listdir(str_path)
    except:
        print(' ERROR in fList_FileInDir')
        print(' - ', str_path)
        raise
    return l_fic

def fList_FileInDir_Txt(str_path):
    try:
        l_fic = os.listdir(str_path)
        l_fic = [fic for fic in l_fic if '.txt' in fic]
    except:
        print(' ERROR in fList_FileInDir_Txt')
        print(' - ', str_path)
        raise
    return l_fic

def fList_FileInDir_Csv(str_path):
    try:
        l_fic = os.listdir(str_path)
        l_fic = [fic for fic in l_fic if '.csv' in fic]
    except:
        print(' ERROR in fList_FileInDir_Csv')
        print(' - ', str_path)
        raise
    return l_fic

def fList_FileInDir_Py(str_path):
    try:
        l_fic = os.listdir(str_path)
        l_fic = [fic for fic in l_fic if '.py' in fic]
    except:
        print(' ERROR in fList_FileInDir_Py')
        print(' - ', str_path)
        raise
    return l_fic

def UpdateTxtFile(str_path, str_old, str_new = ''):
    with open(str_path, 'r') as file :
        str_text = file.read()
    # Replace the target string
    str_text = str_text.replace(str_old, str_new)
    # Write the file out again
    with open(str_path, 'w') as file:
        file.write(str_text)



#------------------------------------------------------------------------------
# Transform Names
#------------------------------------------------------------------------------
def fStr_TransformFilName_fromXXX_forGlobFunction(str_fileName_withX, bl_exactNumberX):
    # Check if its a normal Name without {X}:
    if '{X' not in str_fileName_withX and 'X}' not in str_fileName_withX:
        return str_fileName_withX
    
    # Count the Number of Series of {XX} 
    int_nbXX = str_fileName_withX.count('{X')
    int_nbXX2 = str_fileName_withX.count('X}')
    if int_nbXX != int_nbXX2: 
        print('   ERROR, check the sting str_fileName_withX in fStr_TransformFilName_fromXXX: ', str_fileName_withX)
        return str_fileName_withX
    
    # Count the number of X in each Series of {XX}
    str_fileName = str_fileName_withX
    nb = 1
    while nb in range(1, int_nbXX + 1):
        nb += 1
        for i in range(1,20):
            str_XXX = '{' + i * 'X' + '}'
            if str_fileName.count(str_XXX) > 0:
                nb = nb + str_fileName.count(str_XXX) - 1     # just in case there is several time the same XXX, we dont want to pass again on this loop
                break                
        #==================================================
        # Exact Number ???????????????????????????????
        if bl_exactNumberX:
            int_lenXX = len(str_XXX) - 2
            str_fileName = str_fileName.replace(str_XXX, int_lenXX * '?')
        # Flex Number ?
        else:
            str_fileName = str_fileName.replace(str_XXX, '*')
        #==================================================
    return str_fileName



#Return a list of File in a folder
def fL_GetFileListInFolder(str_folder, str_fileName_withX, bl_searchOnlyIfPossible = False, bl_exactNumberX = True):    
    if str_folder[-1] != '\\': str_folder += '\\'
    
    try:
        # Transform fiel name to be understood from 'glob.glob'
        str_fileName = fStr_TransformFilName_fromXXX_forGlobFunction(str_fileName_withX, bl_exactNumberX)
        # if no change, just return default
        if str_fileName == str_fileName_withX:
            return [str_folder + str_fileName_withX]
        
        # Using Glob: Code part from Thanos
        for file in [glob.glob(str_folder + str_fileName)]:
            if len(file) > 0:
                L_files = glob.glob(str_folder + str_fileName)
                #++++++++++++++++++++++++++++++++++++++++++++++++++++
                return L_files
                #++++++++++++++++++++++++++++++++++++++++++++++++++++
            # Do not raise an issue if its a search, just return File with XX
            elif bl_searchOnlyIfPossible:                   
                #print(' Return the file with the X (Search only): ', str_fileName_withX)
                return [str_folder + str_fileName_withX]
            else:
                if bl_exactNumberX:
                    print(' EMPTY fL_GetFileListInFolder... We will now search with more flex')
                    l_filesFlex = fL_GetFileListInFolder(str_folder, str_fileName_withX, False, False)
                    return l_filesFlex
                else:                
                    print(' EMPTY: file not found in fL_GetFileListInFolder')
                    print(' - Maybe check the Date (file exist but not the right date, or the number of X exceed 15 ???? ')
                    raise
    except:
        print('   ERROR in fL_GetFileListInFolder')
        print('   - str_folder: ', str_folder)
        print('   - str_fileName_withX: ', str_fileName_withX)
        raise
    return 0 #never used
        

def fStr_GetMostRecentFile_InFolder(str_folder, str_fileName_withX, bl_searchOnlyIfPossible = False, bl_exactNumberX = True):
    if str_folder[-1] != '\\': str_folder += '\\'
    # Get the lisyt of matching files
    try:
        L_FileInFolder = fL_GetFileListInFolder(str_folder, str_fileName_withX, bl_searchOnlyIfPossible, bl_exactNumberX)
    except: raise
    # Return the most recent file
    try:
        #str_latest_file = max(L_FileInFolder, key = os.path.getmtime)       # Time of Update
        str_latest_file = max(L_FileInFolder, key = os.path.getctime)       # Time of Creation
        str_fileName = str_latest_file.replace(str_folder, '')
    except:
        if bl_searchOnlyIfPossible: return str_fileName_withX
        print('  ERROR fStr_GetMostRecentFile_InFolder, Sort by Date')
        print('  - str_folder: ',str_folder)
        print('  - str_fileName_withX: ',str_fileName_withX)
        raise
    return str_fileName

## TEST
#print(fStr_GetMostRecentFile_InFolder(r'C:\Users\laurent.tupin\Documents\5_Python', 'test_2152_5412.txt'))
#print(fStr_GetMostRecentFile_InFolder(r'C:\Users\laurent.tupin\Documents\5_Python', 'test_{XXXX}_5412.txt'))
#print(fStr_GetMostRecentFile_InFolder(r'C:\Users\laurent.tupin\Documents\5_Python', 'test_{XXXX}_{XX}12.txt'))


def fL_GetFileList_withinModel(L_FileName, str_fileName_withX):
    try:
        # Check if its a normal Name without {X}:
        if '{X' not in str_fileName_withX and 'X}' not in str_fileName_withX:
            L_FileName = [fil for fil in L_FileName if str_fileName_withX.lower() in fil.lower()]
            return L_FileName
			
        # Count the Number of Series of {XX} 
        int_nbXX = str_fileName_withX.count('{X')
        int_nbXX2 = str_fileName_withX.count('X}')
        if int_nbXX != int_nbXX2: 
            print('   ERROR, check the string str_fileName_withX in fL_GetFileList_withinModel: ', str_fileName_withX)
            return L_FileName
		
        # Count the number of X in each Series of {XX}
        str_fileName = str_fileName_withX
        for nb in range(1, int_nbXX + 1):
            for i in range(1,15):
                str_XXX = '{' + i * 'X' + '}'
                if str_fileName.count(str_XXX) == 1: break
            str_fileName = str_fileName.replace(str_XXX, '?')
			
        l_fileName_part = str_fileName.split('?')
        l_files = L_FileName
        for name_part in l_fileName_part:
            l_files = [fil for fil in l_files if name_part.lower() in fil.lower()]
    except:
        print('   ERROR in fL_GetFileList_withinModel')
        print('   - str_fileName_withX: ', str_fileName_withX)
        print('   - L_FileName: ', L_FileName)
        raise
    return l_files


#def fStr_FindPath_byReplacingX(str_folder, str_fileName_withX, l_fileInput = [], bl_searchOnlyIfPossible = False):
#    try:
#        # 1. List file in Folder
#        if l_fileInput: l_files = l_fileInput
#        else:           l_files = fList_FileInDir(str_folder)
#        
#        # 2. Understand the Name of the file
#        for i in range(1,15):
#            str_XXX = '{' + i * 'X' + '}'
#            if str_fileName_withX.count(str_XXX) == 1:
#                break
#            #elif str_fileName_withX.count(str_XXX) > 1:
#            #    print(' ERROR: fStr_FindPath_byReplacingX is not yet made to support Two {XXXX} string, you need to require an Upgrade of the function')
#        
#        #----------------------------------------------------------------------
#        # If it is a Normal File without XXX: Just return the input name
#        if str_fileName_withX.count(str_XXX) == 0: return str_fileName_withX
#        #----------------------------------------------------------------------
#        
#        # Treat the filename
#        str_prefix = str_fileName_withX.split(str_XXX)[0]
#        str_suffix = str_fileName_withX.split(str_XXX)[1]
#        # Loop on files in folder to get the name
#        l_files = [file for file in l_files if str_prefix in file and str_suffix in file]
#        # RETURN
#        if len(l_files) == 1:
#            return l_files[0]        
#        elif len(l_files) == 0:
#            #------------------------------------------------------------------
#            # If search only for the name of the already downloadedm dont retrun an error, but the original name
#            if bl_searchOnlyIfPossible: return str_fileName_withX
#            
#            print(' EMPTY: file not found in fStr_FindPath_byReplacingX')
#            print(' Maybe check the Date (file exist but not the right date, or the number of X exceed 15 ???? ')
#            raise
#        elif len(l_files) > 1:
#            for file in l_files:
#                fileName = file.replace(str_prefix, '').replace(str_suffix, '')
#                if len(fileName) == len(str_XXX) - 2:
#                    return file
#    except:
#        print('   ERROR in fStr_FindPath_byReplacingX')
#        print('   str_folder: ', str_folder)
#        print('   str_fileName_withX: ', str_fileName_withX)
#        raise






#------------------------------------------------------------------------------
# Files Date
#------------------------------------------------------------------------------ 
def fDte_GetModificationDate(str_pathFile):
    try:
        if fBl_FileExist(str_pathFile):
            dte_modif = os.path.getmtime(str_pathFile)
            dte_modif = dt.datetime.fromtimestamp(dte_modif)
            return dte_modif
        else:
            print('  fDte_GetModificationDate: File does not exist: ')
            print('  - str_pathFile: ', str_pathFile)
            return -1
    except:
        print(' ERROR in fDte_GetModificationDate')
        print(' - ', str_pathFile)
        raise
    return True



#------------------------------------------------------------------------------
# DELETE
#------------------------------------------------------------------------------ 
def del_allTxtFileInFolder_ifOldEnought(str_folder, int_dayHisto = 60):
    try:
        dte_delete = dt.datetime.now() - dt.timedelta(int_dayHisto)
        l_fic = fList_FileInDir_Txt(str_folder)
        for fic in l_fic:
            str_path = os.path.join(str_folder, fic)
            if fDte_GetModificationDate(str_path) < dte_delete and fDte_GetModificationDate(str_path) != -1:
                os.remove(str_path)
    except:
        print(' ERROR in del_fic')
        print(' - ', str_folder, int_dayHisto)
        raise
    return 0


def del_fic(str_path, int_dayHisto):
    print('     DEPRECATED function: del_fic')
    a = del_allTxtFileInFolder_ifOldEnought(str_path, int_dayHisto)
    return a


def del_fichier(str_folder, str_fileName):
    try:
        str_path = os.path.join(str_folder, str_fileName)
        if str_fileName == '': str_path = str_folder
        os.remove(str_path)
    except:
        print(' ERROR in del_fichier')
        print(' - ', str_folder, str_fileName)
        raise
    return 0


def del_fichier_ifOldEnought(str_folder, str_fileName, int_dayHisto = 5):
    try:
        str_path = os.path.join(str_folder, str_fileName)
        if str_fileName == '': 
            str_path = str_folder
            str_folder = '\\'.join(str_folder.split('\\')[:-1])
        # if folder does not exist : sortir de la fonction sans delete rien (et en ayant creer le dossier)
        if fBl_createDir(str_folder):
            print(' Information: Folder was not existing (in del_fichier_ifOldEnought): ', str_folder)
            return 0
        dte_delete = dt.datetime.now() - dt.timedelta(int_dayHisto)
        dte_ModificationDate = fDte_GetModificationDate(str_path)
        if dte_ModificationDate == -1:
            # File not exisiting
            pass
        elif dte_ModificationDate < dte_delete:
            os.remove(str_path)
        else: pass
    except:
        print(' ERROR in del_fichier_ifOldEnought')
        print(' - Parameters:', str_folder, str_fileName, int_dayHisto)
        raise
    return 0
    

#-----------------------------------------------------------------
# READ
#-----------------------------------------------------------------
def fStr_ReadFile_sql(str_filePath):
    # Open and read the file as a single buffer
    file = open(str_filePath, 'r')
    str_Content = file.read()
    file.close()
    return str_Content


def fStr_readFile(bl_folderRelative, str_folder, str_fileName = 'test.txt'):
    dir_current = os.getcwd()
    try:
        # Define folder
        if bl_folderRelative:
            str_folder = os.getcwd().replace(str_folder,'') + str_folder
        # Check folder exist
        if not os.path.exists(str_folder): 
            print(' ERROR: fStr_readFile - Folder does not exist')
            print(' - ', str_folder)
            print(' - ', str_fileName)
            print(' - Folder Relative = ', bl_folderRelative)
            raise
        # Change Dir
        os.chdir(str_folder)
    except: 
        print(" ERROR: fStr_readFile")
        print(' - ', str_folder, str_fileName)
        print(' - Folder Relative = ', bl_folderRelative)
        raise
    # Read File
    try:            f = open(str_fileName,"r")
    except: 
        try:        os.chdir(dir_current)
        except:     print(" ERROR: fStr_readFile - os.chdir(dir_current) did not work -- f = open(str_fileName")
        print(' ERROR: fStr_readFile')
        print(' - Could not Open the file')
        print(' - str_folder', str_folder)
        print(' - str_fileName', str_fileName)
        print(' - Folder Relative = ', bl_folderRelative)
        raise
    try:
        str_return = f.read()
        f.close()
    except:
        try:        f.close()
        except:     print(" ERROR: fStr_readFile - f.close()")
        try:        os.chdir(dir_current)
        except:     print(" ERROR: fStr_readFile - os.chdir(dir_current) did not work -- str_return = f.read()")
        print(" ERROR: fStr_readFile")
        print(" - Could not Read the file")
        print(' - str_folder', str_folder)
        print(' - str_fileName', str_fileName)
        print(' - Folder Relative = ', bl_folderRelative)
        raise
    try:            os.chdir(dir_current)
    except: 
        print(" ERROR: fStr_readFile - os.chdir(dir_current) did not work")
        raise     
    return str_return
    


#-----------------------------------------------------------------
# CREATE
#-----------------------------------------------------------------
def fBl_createDir(str_folder):
    try:
        if not os.path.exists(str_folder):
            try: 
                os.makedirs(str_folder)
                return True
            except:
                print(' ERROR: fBl_createDir - Program could NOT create the Dir')
                print(' - ', str_folder)
                raise
        else: 
            return False      # Folder already exist
    except:
        print(' ERROR: fBl_createDir - Path cannot be tested on its existence ??')
        print(' - ', str_folder)
        raise 
    return False
    

def act_createFile(bl_folderRelative, str_folder, str_fileName = 'test.txt', str_text = ''):
    dir_current = os.getcwd()
    try:
        # Define folder
        if bl_folderRelative:
            str_folder = os.getcwd().replace(str_folder,'') + str_folder
        # Create folder
        fBl_createDir(str_folder)
        # Change Dir
        os.chdir(str_folder)
    except: 
        print(" ERROR: act_createFile - Create Dir")
        print(' - str_folder', str_folder)
        print(' - str_fileName', str_fileName)
        raise
    # Create File
    try:            f = open(str_fileName,"w+")
    except: 
        try:        os.chdir(dir_current)
        except:     print(" ERROR: act_createFile - os.chdir(dir_current) did not work -- f = open(str_fileName, ")
        print(" ERROR: act_createFile - Could not create the file")
        print(' - str_folder', str_folder)
        print(' - str_fileName', str_fileName)
        raise
    try: 
        f.write(str_text)
        f.close()
    except:
        try:        f.close()
        except:     print(" ERROR: act_createFile - f.close()")
        try:        os.chdir(dir_current)
        except:     print(" ERROR: act_createFile - os.chdir(dir_current) did not work -- f.write(str_text)")
        print(" ERROR: act_createFile - Could not write in the file")
        print(' - str_folder', str_folder)
        print(' - str_fileName', str_fileName)
        print(' - str_text', str_text)        
        raise
    try:            os.chdir(dir_current)
    except:
        print(" ERROR: act_createFile - os.chdir(dir_current) did not work")
        raise        
    return 0


def fStr_CreateTxtFile(str_folder, str_FileName, df_data, str_sep = '', bl_header = False, bl_index = False):
    try:
        if str_FileName == '':      str_path = str_folder
        else:                       str_path = os.path.join(str_folder, str_FileName)
        if str_sep == '':           str_sep = ','
        # TO CSV
        df_data.to_csv(str_path, sep = str_sep, header = bl_header, index = bl_index)
    except:
        print('  ERROR in fl.fStr_CreateTxtFile: Could not create the file: ')
        print('  - str_folder :', str_folder, 'str_FileName :', str_FileName)
        return False
    return str_path


def fStr_createExcel_1Sh(str_folder, str_FileName, df_Data, str_SheetName = '', bl_header = False):
    try:
        # Define Path
        str_path = fStr_BuildPath(str_folder, str_FileName)
        # Create the File
        if str_SheetName != '':     df_Data.to_excel(str_path, header = bl_header, index = False, sheet_name = str_SheetName)
        else:                       df_Data.to_excel(str_path, header = bl_header, index = False)
    except:
        print('  ERROR: fStr_createExcel_1Sh did not work ')
        print('  - str_path: ', str_path)
        print('  - str_SheetName: ', str_SheetName)
        return False
    return str_path


#options={'strings_to_numbers': True}
    
def fStr_createExcel_SevSh(str_folder, str_FileName, l_dfData, l_SheetName = [], bl_header = False, d_options = {}):
    try:
        # Define Path
        str_path = fStr_BuildPath(str_folder, str_FileName)
        # Create the File
        with pd.ExcelWriter(str_path, engine = 'xlsxwriter', options = d_options) as xl_writer:
            # Dataframe
            for i in range(len(l_dfData)):
                df_data = l_dfData[i]
                #Sheet Name
                try:        str_SheetName = l_SheetName[i]
                except:     str_SheetName = 'Sheet{}'.format(str(i + 1))
                # fill in
                df_data.to_excel(xl_writer, header = bl_header, index = False, sheet_name = str_SheetName)
            xl_writer.save()
    except:
        try:        xl_writer.save()
        except:     print('Could not Save the file')
        print('  ERROR: fl.fStr_createExcel_SevSh did not work ')
        print('  - ', str_folder, str_FileName)
        print('  - l_SheetName: ', l_SheetName)
        return False
    return str_path


def fStr_createExcel_SevSh_celByCel(str_folder, str_FileName, l_dfData, l_SheetName = [], bl_header = False):
    try:
        # Define Path
        if str_FileName == '':      str_path = str_folder
        else:                       str_path = os.path.join(str_folder, str_FileName)
        # Create the file (xlsxwriter cannot modify files)
        xlWb = xlsxwriter.Workbook(str_path)
        # Dataframe
        for i in range(len(l_dfData)):
            df_data = l_dfData[i]
            try:        str_SheetName = l_SheetName[i]
            except:     str_SheetName = ''
            #Sheet Name
            if str_SheetName != '':     xlWs = xlWb.add_worksheet(str_SheetName)             
            else:                       xlWs = xlWb.add_worksheet()   
            # fill in
            for i, row in enumerate(df_data.index):
                for j, col in enumerate(df_data.columns):
                    xlWs.write(i, j, str(df_data.iat[i, j]))
                    #xlWs.Cells(i+1, j+1).Value = str(df_data.iat[i, j])
        xlWb.close()
    except:
        try:        xlWb.close()
        except:     print('Could not close the file')
        print('  ERROR: fl.fStr_createExcel_SevSh_celByCel did not work ')
        print('  - ', str_folder, str_FileName)
        print('  - l_SheetName: ', l_SheetName)
        return False
    return str_path


# INSERT SHEET: 1 file out - 1 Dataframe - 1 Sheet 
def fStr_fillExcel_InsertNewSheet(str_folder, str_FileName, df_data, str_SheetName = '', bl_header = False):
    try:
        if str_FileName == '':  str_path = str_folder
        else:                   str_path = os.path.join(str_folder, str_FileName)
        # Define Book
        xl_book = openpyxl.load_workbook(filename = str_path)
        # OTHER Rows of code: 
        #   ws1 = xl_book.worksheets[ste_sheetName] 
        #   xl_book_2 = openpyxl.load_workbook(filename = str_path2)
        #   ws2 = xl_book_2.create_sheet(ws1.title)
        #   for row in ws1:
        #       for cell in row:
        #           ws2[cell.coordinate].value = cell.value
        #   xl_book_2.save(str_path2)
        # OTHER Rows of code: 
        #   xl_writer = pd.ExcelWriter(str_path, engine = 'openpyxl')
        
        with pd.ExcelWriter(str_path, engine = 'openpyxl') as xl_writer:
            xl_writer.book = xl_book
            xl_writer.sheets = dict((ws.title, ws) for ws in xl_book.worksheets)
            # Manege Sheet Name
            if str_SheetName == '':     str_SheetName = 'Sh1'
            if str_SheetName in list(xl_writer.sheets):
                print(" The sheet '{}' alrdeay exist".format(str_SheetName))
                while str_SheetName in list(xl_writer.sheets):
                    str_SheetName = str_SheetName[1:] + str_SheetName[0] + 'x'
                print(" We replace the sheet name: '{}'  but you need to improve the management of name".format(str_SheetName))
            # Add the Sheet
            df_data.to_excel(xl_writer, header = bl_header, index = False, sheet_name = str_SheetName)
            #SAVE
            xl_writer.save()
    except:
        print('  ERROR in fl.fStr_fillExcel_InsertNewSheet: Could not fill the file')
        print('  - str_path', str_path)
        print('  - str_SheetName', str_SheetName)
        return False
    return str_path


# 1 file out - n Dataframe - n Sheet
def fStr_fillXls_celByCel_plsSheets(str_folder,str_FileName,l_dfData,l_SheetName=[],l_nbRows=[],l_rowsWhere=[]):
    try:
        if str_FileName == '':      str_path = str_folder
        else:                       str_path = os.path.join(str_folder, str_FileName)        
        
        # Open the file (win32)
        inst_xlApp = c_win32_xlApp()
        inst_xlApp.FindXlApp(bl_visible = False)
        inst_xlApp.OpenWorkbook(str_path)
        #        xlApp = win32.Dispatch('Excel.Application')
        #        xlApp.Visible = False 
        #        xlWb = xlApp.Workbooks.Open(str_path)
		
        # Dataframe
        for i in range(len(l_dfData)):
            df_data = l_dfData[i]
            try:        str_SheetName = l_SheetName[i]
            except:     str_SheetName = ''
            
            #Sheet
            bl_SheetNameIsNew = (inst_xlApp.xl_lastWk.Sheets(i + 1).Name not in l_SheetName)
            if bl_SheetNameIsNew:   inst_xlApp.DefineWorksheet(str_SheetName, i + 1)
            else:                   inst_xlApp.DefineWorksheet(str_SheetName)
            
            # ------ Insert or delete ROWS ------
            int_nbRows = 0
            int_rowsWhere = 1
            if l_nbRows:
                try:        int_nbRows = l_nbRows[i]
                except:     int_nbRows = 0
                try:        int_rowsWhere = l_rowsWhere[i]
                except:     int_rowsWhere = 1
            # FILL THE SHEET
            fStr_fillXls_celByCel(str_path, df_data, str_SheetName, inst_xlApp.xl_lastWsh, int_nbRows, int_rowsWhere)
        
        # Visible and close Excel at the end
        inst_xlApp.Visible = True
        inst_xlApp.CloseWorkbook(True)
        inst_xlApp.QuitXlApp(bl_force = False)
    except:
        try: 		inst_xlApp.Visible = True
        except: 	print('  ERROR in fStr_fillXls_celByCel_plsSheets: xlApp visible did not work')
        try: 		inst_xlApp.CloseWorkbook(True)
        except: 	print('  ERROR in fStr_fillXls_celByCel_plsSheets: Excel workbook could not be closed')
        try: 		inst_xlApp.QuitXlApp(bl_force = False)
        except: 	print('  ERROR: Excel could not be closed')
        print('  ERROR in fStr_fillXls_celByCel_plsSheets: Could not create the PCF: ' + str_path)
        return False
    return str_path



# 1 file out - 1 Dataframe - 1 Sheet
def fStr_fillXls_celByCel(str_path, df_data, str_SheetName = '', xlWs = 0, int_nbRows = 0, int_rowsWhere = 1):
    try:
        # If Sheet is nothing, we must define it
        if xlWs == 0:
            bl_CloseExcel = True
            inst_xlApp = c_win32_xlApp()
            inst_xlApp.FindXlApp(bl_visible = False)
            inst_xlApp.OpenWorkbook(str_path)
            xlWs = inst_xlApp.DefineWorksheet(str_SheetName, 1)
            if not xlWs:        print('  (--) ERROR in fStr_fillXls_celByCel: really could not find the sheet')
        else:   bl_CloseExcel = False
             
        # ------ Insert or delete ROWS ------
        if int_nbRows > 0:
            for i in range(0, int_nbRows):      xlWs.Rows(int_rowsWhere).EntireRow.Insert()
        elif int_nbRows < 0:
            for i in range(0, -int_nbRows):     xlWs.Rows(int_rowsWhere).EntireRow.Delete()                    
        # ------ Fill Cell by Cell  ------
        for i, row in enumerate(df_data.index):
            for j, col in enumerate(df_data.columns):	
                xlWs.Cells(i+1, j+1).Value = str(df_data.iat[i, j])
    except Exception as err:
        print('  ERROR in fl.fStr_fillXls_celByCel: Could not fill  Excel | {}'.format(str(err)))
        print('  - str_path : ', str_path)
        print('  - str_SheetName : ', str_SheetName)
        try:
            print('  - int_nbRows : ', int_nbRows, 'int_rowsWhere: ', int_rowsWhere)
            print('  - i : ', i, 'row: ', row)
            print('  - j : ', j, 'col: ', col)
            print('  - str(df_data.iat[i, j])', str(df_data.iat[i, j]))
            print('  - xlWs.Cells(i+1, j+1).Value', xlWs.Cells(i+1, j+1).Value)
        except:     pass
        return False
    # rustine depending where Function start
    if bl_CloseExcel:
        try:                        inst_xlApp.Visible = True
        except Exception as err:    print('  ERROR in fl.fStr_fillXls_celByCel: xlApp visible did not work | {}'.format(str(err)))
        try:                        inst_xlApp.CloseWorkbook(True)
        except Exception as err:    print('  ERROR in fl.fStr_fillXls_celByCel: Excel workbook could not be closed | {}'.format(str(err)))
        try:                        inst_xlApp.QuitXlApp(bl_force = False)
        except Exception as err:    print('  ERROR: Excel could not be closed | {}'.format(str(err)))
    return str_path


def fDf_convertToXlsx(str_path, str_SheetName = '', bl_header = None):
    str_pathNew = str_path.replace('.xls', '.xlsx').replace('.XLS', '.xlsx')
    # Test if file exist
    if not fBl_FileExist(str_pathNew):
        try:
            #time.sleep(2)
            inst_xlApp = c_win32_xlApp()
            str_WhereErr = 'Find App'
            inst_xlApp.FindXlApp(bl_gencache_EnsureDispatch = False, bl_visible = True)
            str_WhereErr = 'OpenWorkbook'
            inst_xlApp.OpenWorkbook(str_path)
            str_WhereErr = 'SaveAs'
            inst_xlApp.SaveAs(str_newPath = str_pathNew, int_fileFormat = 51)
            str_WhereErr = 'CloseWorkbook'
            inst_xlApp.CloseWorkbook(False)   
        except Exception as err:
            print('  ERROR fDf_convertToXlsx: {1} - {0} '.format(str(err), str_WhereErr))
            raise            
        print('  (*) Copying XLS file into XLSX: {}'.format(str_pathNew))
    try:
        if str_SheetName == '':     df_data = pd.read_excel(str_pathNew, header = bl_header)
        else:                       df_data = pd.read_excel(str_pathNew, header = bl_header, sheet_name = str_SheetName)
    except:
        print(' ERROR: fDf_convertToXlsx')
        print(' - str_path : ', str_path)
        print(' - str_SheetName : ', str_SheetName)
        print(' - bl_header : ', bl_header)
        raise
    return df_data




#-----------------------------------------------------------------
# FORMAT / STYLE
#-----------------------------------------------------------------

def fStr_StyleIntoExcel(str_path, str_SheetName = '', l_row = [1], str_styleName = 'Header_Perso',
                     bl_bold = True, str_fontColor = '', l_Fill = [], l_border = []):
    # Define EXCEL objects
    xlWb = openpyxl.load_workbook(filename = str_path)
    if str_SheetName == '':     xlWs = xlWb.active
    else:                       xlWs = xlWb.Sheets(str_SheetName)
    
    # Define the Style
    style_header = styl.NamedStyle(name = str_styleName)
    # FONT
    if str_fontColor == 'RED':      style_header.font = styl.Font(bold = bl_bold, color = styl.colors.RED)
    elif str_fontColor == 'BLUE':   style_header.font = styl.Font(bold = bl_bold, color = styl.colors.BLUE)
    elif str_fontColor == 'WHITE':  style_header.font = styl.Font(bold = bl_bold, color = styl.colors.WHITE)
    elif str_fontColor != '':       style_header.font = styl.Font(bold = bl_bold, color = str_fontColor)
    else:                           style_header.font = styl.Font(bold = bl_bold)
    # FILL
    if l_Fill:                      style_header.fill = styl.PatternFill(patternType = l_Fill[0],
                                                                         fill_type = l_Fill[1], 
                                                                         fgColor = l_Fill[2])
    # TO convert the color, please use: https://convertingcolors.com/rgb-color-91_155_213.html
    
    # BORDER
    if l_border: 
        o_border = styl.Side(border_style = l_border[0], color = l_border[1])
        style_header.border = styl.Border(top = o_border, right = o_border, bottom = o_border, left = o_border)
    
    # Save the Style in WK
    try:        xlWb.add_named_style(style_header)
    except:     print(' Information: The Style {} already exists in the workbook'.format(str_styleName))
    
    # Add Celle by Cell
    if 'header' in str_styleName.lower():
        for i_headerRow in l_row:
            header_row = xlWs[i_headerRow]
            for cell in header_row:
                if cell.value != '' and cell.value != None:
                    cell.style = str_styleName
    elif 'table' in str_styleName.lower():
        for i_row in l_row:
            ROW = xlWs[i_row]
            i_nbCol = 0
            for cell in ROW:
                if cell.value != '' and cell.value != None:
                    i_nbCol += 1
            for i_numRow in range(1, 1000):
                ROW = xlWs[i_row + i_numRow]
                str_firstCell = ROW[0].value
                if str_firstCell != '' and str_firstCell != None:
                    for cell in ROW[:i_nbCol]:
                        cell.style = str_styleName
                else:   break
    # SAVE
    xlWb.save(filename = str_path)
    return str_path
    





#-----------------------------------------------------------------
# ZIP
#-----------------------------------------------------------------
def ZipExtractFile(str_ZipPath, str_pathDest = '', str_FileName = '', bl_extractAll = False):
    try:
        with ZipFile(str_ZipPath, 'r') as zipObj:
            if bl_extractAll:
                # Extract all the file
                if str_pathDest == '':      zipObj.extractall()
                else:                       zipObj.extractall(str_pathDest)
                time.sleep(5)
            else:
                # Get a list of all archived file names from the zip
                l_fileInZip = zipObj.namelist()
                # Get The name of the list  matching
                l_fileInZip_file = fL_GetFileList_withinModel(l_fileInZip, str_FileName)
                # Extract the file
                for file in l_fileInZip_file:
                    zipObj.extract(file, str_pathDest)
    except Exception as err:
        print(' ERROR: ZipExtractFile || {}'.format(str(err)))
        if bl_extractAll:
            print(' - str_ZipPath : ', str_ZipPath)
            print(' - str_pathDest : ', str_pathDest)
            raise
        else:
            print(' - Failed to doanload the file : ', str_FileName)
            print(' - File List in the Zip : ', l_fileInZip)
            print(' (**) Trying to extract all files...')
            ZipExtractFile(str_ZipPath, str_pathDest, '', True)
    return True

#ZipExtractFile(r'C:\Users\laurent.tupin\Documents\5_Python\Py_Package\Brouillon\cccc.zip',
#               r'C:\Users\laurent.tupin\Documents\5_Python\Py_Package\Brouillon',
#               'HKGRFMHKSSET_ST-FM-TX-001-01_20191127_1_{XXXXXX}.XLS')
  
    

#------------------------------------------------------------------------------
# Files : renaming
#------------------------------------------------------------------------------   
def Act_Rename(str_folder, str_OriginalName, str_NewName, bl_message = True):    
    try:
        if str_NewName.upper() != str_OriginalName.upper():
            if bl_message:
                print(' RENAMING')
                print(' - str_OriginalName    : ', str_OriginalName)
                print(' - str_NewName: ', str_NewName)
            try:        os.rename(os.path.join(str_folder, str_OriginalName), os.path.join(str_folder, str_NewName))
            except:     shutil.move(os.path.join(str_folder, str_OriginalName), os.path.join(str_folder, str_NewName))
    except: 
        print(' ERROR in Act_Rename: Rename stuff')
        print(' - ', str_folder, str_OriginalName, str_NewName)
        raise
    return True


#------------------------------------------------------------------------------
#--------- To Archives / Prod --------------
#------------------------------------------------------------------------------   
def fL_GetListSubFolder_except(str_folder, str_folderExcept = ''):
   if str_folderExcept != '':       return [x[0] for x in os.walk(str_folder) if x[0][:9] != str_folderExcept]
   else:                            return [x[0] for x in os.walk(str_folder)]
   

def fL_GetListDirFileInFolders(l_subDir, l_typeFile = []):
    listTuple_PathFic = []
    if l_typeFile:
        for Dir in l_subDir:
            list_fic = [(Dir, fic) for fic in fList_FileInDir(Dir) if fic[-3:].lower() in l_typeFile or fic[-4:].lower() in l_typeFile]
            if list_fic: listTuple_PathFic += list_fic
    else:
        for Dir in l_subDir:
            list_fic = [(Dir, fic) for fic in fList_FileInDir(Dir)]
            if list_fic: listTuple_PathFic += list_fic
    #    for Dir in l_subDir:
    #        if l_typeFile:
    #            list_fic = [(Dir, fic) for fic in fList_FileInDir(Dir) if fic[-3:] in l_typeFile or fic[-4:] in l_typeFile]
    #        else: 
    #            list_fic = [(Dir, fic) for fic in fList_FileInDir(Dir)]
    #        if list_fic: listTuple_PathFic += list_fic
    return listTuple_PathFic


def Act_CopyUpdateFiles(l_PathFic_from, l_PathFic_dest, str_originFolder_replacedByDestFolder = '', str_removeInDestFolder = ''):
    if str_originFolder_replacedByDestFolder == '':
        print('Fill the 3rd argument on the function: Act_CopyUpdateFiles')
        return False
    # Loop on File to copy / update them
    for t_file in l_PathFic_from:
        str_path = t_file[0]
        str_file = t_file[1]
        str_path_Dest = str_path.replace('.', str_originFolder_replacedByDestFolder)
        str_path_Dest = str_path_Dest.replace(str_removeInDestFolder, '')
        
        # If file is new --> Copy
        if (str_path_Dest, str_file) not in l_PathFic_dest:
            print('COPY NEW...   ', 'Folder Origin:   ' + str_path, ' ||| Folder Dest:   ' + str_path_Dest, ' ||| File:   ' + str_file)
            fBl_createDir(str_path_Dest)
            shutil.copyfile(str_path + '\\' + str_file, str_path_Dest + '\\' + str_file)
        else:
            dte_lastmod = fDte_GetModificationDate(str_path + '\\' + str_file)
            dte_lastmod_dest = fDte_GetModificationDate(str_path_Dest + '\\' + str_file)
            # Compare Date
            if dte_lastmod > dte_lastmod_dest:
                print('COPY UPDATE...', 'Folder Origin:   ' + str_path, ' ||| Folder Dest:   ' + str_path_Dest, ' ||| File:   ' + str_file)
                if '.\\Archive' in str_originFolder_replacedByDestFolder:
                    str_dateTime =  str(dte_lastmod_dest.strftime('%Y%m%d'))
                    shutil.copyfile(str_path_Dest + '\\' + str_file, str_path_Dest + '\\' + str_dateTime + '_' + str_file)
                shutil.copyfile(str_path + '\\' + str_file, str_path_Dest + '\\' + str_file)
    return True


def Act_CopyUpdateFiles_specialBackUp(l_FolderFic_from, str_DestFolder, int_onlyFileMoreRecentThan = 7, str_removeInDestFolder = ''):
    # Loop on File to copy / update them
    for t_file in l_FolderFic_from:
        str_folder = t_file[0]
        str_file = t_file[1]
        str_pathOrigin = os.path.join(str_folder, str_file)
        
        str_folder_Dest = str_folder.replace('.', str_DestFolder)
        str_folder_Dest = str_folder_Dest.replace(str_removeInDestFolder, '')
        str_pathDest = os.path.join(str_folder_Dest, str_file)
        
        # Process Only if more recent for 7 days (7 for example)
        dte_lastmod = fDte_GetModificationDate(str_pathOrigin)
        dte_limit = dt.datetime.now() - dt.timedelta(int_onlyFileMoreRecentThan)
        
        if dte_lastmod > dte_limit:
            # If File DOES NOT Exists
            if not fBl_FileExist(str_pathDest):
                print('COPY NEW...   ', 'Folder Origin:   ' + str_folder, ' ||| Folder Dest:   ' + str_folder_Dest, ' ||| File:   ' + str_file)
                fBl_createDir(str_folder_Dest)
                shutil.copyfile(str_pathOrigin, str_pathDest)
            else:
                # Compare Date (Update only if CLoud is more recent)
                dte_lastmod_dest = fDte_GetModificationDate(str_pathDest)
                if dte_lastmod > dte_lastmod_dest:
                    print('COPY UPDATE...', 'Folder Origin:   ' + str_folder, ' ||| Folder Dest:   ' + str_folder_Dest, ' ||| File:   ' + str_file)
                    shutil.copyfile(str_pathOrigin, str_pathDest)
    return True












#------------------------------------------------------------------------------
# DEPRECATED
#------------------------------------------------------------------------------
    
