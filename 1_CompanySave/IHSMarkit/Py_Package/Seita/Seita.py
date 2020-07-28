'''
# Course:
#   https://www.youtube.com/watch?v=7SrD4l2o-uk
#   https://www.youtube.com/watch?v=Dmo8eZG5I2w
# Install:
#   Open command windows in the Dir of this file
#   pyuic -x pyqtdesigner.ui -o pyqtdesigner.py
#   C:/Python34/Lib/site-packages/PyQt4/pyuic4.bat -x pyqtdesigner.ui -o pyqtdesigner.py
#
# fbs to freeze into an App
#   https://build-system.fman.io/pyqt5-tutorial
#   https://www.learnpyqt.com/courses/packaging-and-distribution/packaging-pyqt5-apps-fbs
# PyInstaller
#   https://realpython.com/pyinstaller-python/
'''

import sys, os, datetime as dt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
#from PyQt5.QtGui import QIcon
#import win32com.client as win32
import PCF_creater as pcf
import PCF_download as dwl
import PCF_genericProcess as pp
sys.path.append('../')
import fct_Files as fl
import fct_DB as db


str_Program = 'Seita'
str_designFileName = 'pcfAutomate_design.ui'
str_windowTitle = 'PCF Production'

str_lucerneNetworkPath = r'\\uk-pdeqtfs01\E\Data\Lucerne\Data\SOLA PCF\Auto_Py' + '\\'
str_S3NetworkPath = r'\\PRDFIL001WI\DeltaOneShare\PCFDistribution\Auto_py' + '\\'
str_pathDesktop = os.environ['USERPROFILE']
str_pathLocal = os.path.join(str_pathDesktop, r'PCF\Auto_py') + '\\'
str_cloudPath = os.path.join(str_pathDesktop, r'IHS Markit\HK PCF Services Team - General\Auto_py') + '\\'


class class_App(QDialog):
    def __init__(self):
        super(class_App, self).__init__()
        loadUi(str_designFileName, self)
        self.setWindowTitle(str_windowTitle)
        #self.setWindowIcon(QIcon('LaPerouse.ico'))  
        # Define Value
        self.lineEdit_Date.setText(dt.datetime.now().date().strftime('%Y-%m-%d'))
        self.lineEdit_folderRoot.setText(str_cloudPath)
        # Activate Button Event
        self.push_downloadFiles.clicked.connect(self.onPush_downloadFiles)
        self.push_producePcf.clicked.connect(self.onPush_producePcf)
        self.push_loadPcf.clicked.connect(self.onPush_loadPcf)
        self.push_Clear.clicked.connect(self.onPush_Clear)
        self.push_ComparePCF.clicked.connect(self.onPush_ComparePCF)
        self.push_DisplayDoc.clicked.connect(self.onPush__DisplayDoc)
        self.push_sendPCF.clicked.connect(self.onPush_sendPCF)
        self.push_OpenParamCSV.clicked.connect(self.onPush_OpenParamCSV)
        self.push_OpenParamMailCSV.clicked.connect(self.onpush_OpenParamMailCSV)
        self.push_KillExcel.clicked.connect(self.onPush_KillExcel)
        #        QDialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        #        QDialog.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.push_Minimize.clicked.connect(lambda: self.showMinimized())
        self.comboBox_DB.activated.connect(self.onChange__Database)
        self.push_sendFTP.clicked.connect(self.onPush__sendFTP)
        #self.comboBox_MailType.activated.connect(self.onChange__MailType)
        
        # change Check Box on OneDrive to a ComboBox with several choice        
        #self.checkBox_DevEnv.stateChanged.connect(self.onChange_DevEnv)
        self.comboBox_RootFolder.activated.connect(self.onChange__RootFolder)
        
        # Load Log
        db.Log_Python({'str_action':'OPEN', 'str_Program':'Seita', 'str_path':os.path.dirname(os.path.abspath(__file__))})
        
    @pyqtSlot()
    def onPush_OpenParamCSV(self):
        try:
            str_path = os.getcwd() + r'\Seita_Param.csv'
            inst_xlApp = fl.c_win32_xlApp()
            inst_xlApp.FindXlApp(bl_visible = True)
            inst_xlApp.OpenWorkbook(str_path)
            #            xlApp = win32.Dispatch('Excel.Application')
            #            xlApp.Visible = True
            #            xlApp.Workbooks.Open(str_path)
        except: self.textEdit_Error.append(' ERROR: Could not Open the file')
        
    def onpush_OpenParamMailCSV(self):
        try:
            str_path = os.getcwd() + r'\Seita_Param_Mail.csv'
            inst_xlApp = fl.c_win32_xlApp()
            inst_xlApp.FindXlApp(bl_visible = True)
            inst_xlApp.OpenWorkbook(str_path)
            #            xlApp = win32.Dispatch('Excel.Application')
            #            xlApp.Visible = True
            #            xlApp.Workbooks.Open(str_path)
        except: self.textEdit_Error.append(' ERROR: Could not Open the file')
        
    #    def onChange_DevEnv(self):
    #        bl_OneDrive = self.checkBox_DevEnv.isChecked()
    #        if bl_OneDrive:     self.lineEdit_folderRoot.setText(str_cloudPath)
    #        else:               self.lineEdit_folderRoot.setText(str_lucerneNetworkPath)
    
    def onChange__RootFolder(self):
        str_rootFolder = self.comboBox_RootFolder.currentText()
        if 'IHS_Drive' in str_rootFolder:
            self.lineEdit_folderRoot.setText(str_cloudPath)
        elif 'S3' in str_rootFolder:
            self.lineEdit_folderRoot.setText(str_S3NetworkPath)
        elif 'Local' in str_rootFolder:
            self.lineEdit_folderRoot.setText(str_pathLocal)
            fl.fBl_createDir(str_pathLocal)
            fl.Act_CopPasteFolder_severalTry(os.path.join(str_pathLocal, 'file'), 
                                             [os.path.join(str_cloudPath, 'file'), os.path.join(str_S3NetworkPath, 'file'), os.path.join(str_lucerneNetworkPath, 'file')],
                                             dte_after = 900, l_typeFile = ['.csv', '.xls', 'xlsx'])
        elif 'Lucerne' in str_rootFolder:
            self.lineEdit_folderRoot.setText(str_lucerneNetworkPath)
    
    @pyqtSlot()
    def onPush_KillExcel(self):
        try:    
            #            inst_xlApp = fl.c_win32_xlApp()
            #            inst_xlApp.QuitXlApp(bl_force = True, bl_killExcelProcess = True)
            fl.Act_KillExcel()
        except Exception as err: 
            print(' ERROR: {}'.format(str(err)))
            db.Log_Python({'str_action':'Kill Excel', 'bl_error':1, 'str_Program':'Seita'})
        
    @pyqtSlot()
    def onPush_downloadFiles(self):
        # Param
        dte_date = self.lineEdit_Date.text()
        str_folderRoot = self.lineEdit_folderRoot.text()
        bl_ArchiveMails = self.checkBox_ArchiveMails.isChecked()
        try:    str_pcf = self.listWidget_Pcf.currentItem().text()
        except: 
            str_ErrorComment = "You didnt choose a PCF to Produce"
            self.textEdit_Error.append(str_ErrorComment)
            db.Log_Python({'str_action':'DownloadFiles', 'bl_error':1, 'str_comment':str_ErrorComment, 'str_Program':'Seita'})
            return 0
        # Clear 
        self.listWidget_pathPcf.clear()
        # Choose PCF
        try:
            str_resultFigures, l_pathPcf = dwl.DownloadFiles(str_pcf, str_folderRoot, dte_date, bl_ArchiveMails)
            if 'ERROR' in str_resultFigures or l_pathPcf == []:
                self.textEdit_Error.append(str_resultFigures)
                db.Log_Python({'str_action':'DownloadFiles', 'bl_error':1, 'str_comment':str_pcf, 'str_Program':'Seita'})
                return 0
        except:
            self.textEdit_Error.append(" ERROR Download: You didnt choose the right PCF: " + str_pcf)
            db.Log_Python({'str_action':'DownloadFiles', 'bl_error':1, 'str_comment':str_pcf, 'str_Program':'Seita'})
            return 0
        # Display the main figures        
        self.textEdit_Result.append(str_resultFigures)
        # Return the Path of PCF Produced
        for path in l_pathPcf:
            self.listWidget_pathPcf.addItem(path)
            #        # Create a file to save the parameters of creation (Folder to take the PCF)
            #        str_fileName = str(dte_date) + '_fileDwl_' + str_pcf + ".txt"
            #        str_text = "\n".join(l_pathPcf)
            #        # Save file on loal and Network
            #        fl.act_createFile(False, str_localFilePath, str_fileName, str_text)
            #        fl.act_createFile(False, str_networkFilePath, str_fileName, str_text)
        #LOG
        db.Log_Python({'str_action':'DownloadFiles', 'str_comment':str_pcf, 'str_Program':'Seita'})
        
    @pyqtSlot()
    def onPush_producePcf(self):
        # Clear
        self.listWidget_pathPcf.clear()
        # Param
        dte_date = self.lineEdit_Date.text()
        str_folderRoot = self.lineEdit_folderRoot.text()
        bl_ArchiveMails = self.checkBox_ArchiveMails.isChecked()
        try:    str_pcf = self.listWidget_Pcf.currentItem().text()
        except Exception as err: 
            str_ErrorComment = "You didnt choose a PCF to Produce || {}".format(str(err))
            self.textEdit_Error.append(str_ErrorComment)
            db.Log_Python({'str_action':'ProducePCF', 'bl_error':1, 'str_comment':str_ErrorComment, 'str_Program':'Seita'})
            return 0
        
        # Choose PCF
        try:
            str_resultFigures, l_pathPcf =          pcf.producePCF(str_pcf, str_folderRoot, dte_date, bl_ArchiveMails)
            if 'ERROR' in str_resultFigures or l_pathPcf==[]:                
                self.textEdit_Error.append(str_resultFigures)
                db.Log_Python({'str_action':'ProducePCF', 'bl_error':1, 'str_comment':str_pcf, 'str_Program':'Seita'})
                return 0
        except Exception as err: 
            self.textEdit_Error.append(" ERROR Produce: You didnt choose the right PCF: {} ||| {}".format(str_pcf, str(err)))
            db.Log_Python({'str_action':'ProducePCF', 'bl_error':1, 'str_comment':str_pcf, 'str_Program':'Seita'})
            return 0
        # Display the main figures
        self.textEdit_Result.append(str_resultFigures)
        # Return the Path of PCF Produced        
        for path in l_pathPcf:
            self.listWidget_pathPcf.addItem(path)
        # Create a file to save the parameters of creation (Folder to take the PCF)
        str_fileName = str(dte_date) + '_' + str_pcf + ".txt"
        str_text = "\n".join(l_pathPcf)
        # Save file on Cloud or Network
        fl.act_createFile(False, str_folderRoot + 'file', str_fileName, str_text)
        #        # Save file on loal and Network
        #        fl.act_createFile(False, str_localFilePath , str_fileName, str_text)
        #        fl.act_createFile(False, str_networkFilePath , str_fileName, str_text)
        #LOG
        db.Log_Python({'str_action':'ProducePCF', 'str_comment':str_pcf, 'str_Program':'Seita'})
        
    @pyqtSlot()
    def onPush_loadPcf(self):
        # Param
        str_pathPcf = None
        dte_date = self.lineEdit_Date.text()
        str_folderRoot = self.lineEdit_folderRoot.text()
        self.listWidget_pathPcf.clear()
        try:    str_pcf = self.listWidget_Pcf.currentItem().text()
        except: 
            str_ErrorComment = "You didnt choose a PCF to load"
            self.textEdit_Error.append(str_ErrorComment)
            db.Log_Python({'str_action':'LoadPCF', 'bl_error':1, 'str_comment':str_ErrorComment, 'str_Program':'Seita'})
            return 0
        # Read File
        try:    str_pathPcf = fl.fStr_readFile(False, str_folderRoot + 'file' , str(dte_date) + '_' + str_pcf + ".txt")
        except: pass
        if not str_pathPcf:
            str_ErrorComment = "You didnt run # " + str_pcf + " # today. Please click on PRODUCE PCF first !"
            self.textEdit_Error.append(str_ErrorComment)
            db.Log_Python({'str_action':'LoadPCF', 'bl_error':1, 'str_comment':str_ErrorComment, 'str_Program':'Seita'})
            return 0
        # Fill the Path list
        l_pathPcf = str_pathPcf.split('\n')
        # Return the Path of PCF Produced
        for path in l_pathPcf:
            self.listWidget_pathPcf.addItem(path)
        #LOG
        db.Log_Python({'str_action':'LoadPCF', 'str_comment':str_pcf, 'str_Program':'Seita'})
        
    
    def onPush_Clear(self):
        self.textEdit_Result.clear()
        self.textEdit_Error.clear()
        self.textEdit_Result.insertPlainText('Main Figures: ')
        self.textEdit_Error.insertPlainText('Error Return: ')
        self.listWidget_pathPcf.clear()
        self.listWidget_filePresentFTP.clear()
        
    @pyqtSlot()
    def onPush_ComparePCF(self):
        try:
            self.tableWidget_comparison.clear()
            i_colToKeep = 1
            str_folderRoot = self.lineEdit_folderRoot.text()
            str_link1 = str_folderRoot + self.listWidget_pathPcf.currentItem().text()
            # PATH 2....
            if str_folderRoot in [str_cloudPath, str_S3NetworkPath, str_pathLocal]:
                str_link2 = str_folderRoot.replace('\\Auto_py','\\Manual_py') + self.listWidget_pathPcf.currentItem().text()
            elif str_folderRoot in [str_lucerneNetworkPath]:
                str_link2 = str_folderRoot.replace('\\Auto_Py','') + self.listWidget_pathPcf.currentItem().text()
            else:
                str_link2 = str_folderRoot.replace('\\Auto_Py','') + self.listWidget_pathPcf.currentItem().text()
                print('** Inconsistency: please check what folder you are using')
        except:
            self.textEdit_Error.append("Please select a PCF path !")
            return 0
        # Define the Table
        try:
            # Plusieurs ONGLET
            int_diffCount_Max = -1
            if '.XLSX' in str_link1.upper() or '.XLS' in str_link1.upper():
                o_Book = fl.fBk_OpenWk_xlrd(str_link1)
                l_sheetName = o_Book.sheet_names()
                for str_sheetName in l_sheetName:
                    df_onglet, int_diffCount =      pp.fdf_compare2files(str_link1, str_link2, i_colToKeep, str_sheetName)
                    if int_diffCount > int_diffCount_Max:
                        int_diffCount_Max = int_diffCount
                        df = df_onglet.copy()
                        str_sheetName_Final = str_sheetName
            else:   df, int_diffCount_Max =             pp.fdf_compare2files(str_link1, str_link2, i_colToKeep)
        except: 
            self.textEdit_Error.append("Impossible to proceed. Have you created the manual file ?")
            self.textEdit_Error.append(str_link2)
            return 0
        try:
            str_fileName = '_compare.csv'
            df.to_csv(str_link1[:-4] + str_fileName, index = False, header = False)
        except: 
            self.textEdit_Error.append('ERROR: Impossible to create the file of comparison')
            print('Path: ', str_link1[:-4] + str_fileName)
            print(df)
            return 0
        try:
            self.tableWidget_comparison.setColumnCount(len(df.columns))
            self.tableWidget_comparison.setRowCount(len(df.index))
            for i, row in enumerate(df.index):
                for j, col in enumerate(df.columns):
                    if df.iat[i, j] != '':
                        self.tableWidget_comparison.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))
            self.tableWidget_comparison.resizeColumnsToContents()
            self.tableWidget_comparison.resizeRowsToContents()
        except:     self.textEdit_Error.append('Compare PCF - Could not display the comparaison')
        try:
            if int_diffCount_Max > 0:
                if '.XLSX' in str_link1.upper() or '.XLS' in str_link1.upper():
                    if len(l_sheetName) > 1:
                        self.textEdit_Error.append('Sheet we compare with the most difference in Wk: ' + str_sheetName_Final)
        except:     self.textEdit_Error.append('Compare PCF - Could not display the Error message')
        
    @pyqtSlot()
    def onPush__DisplayDoc(self):
        try:
            self.tableWidget_comparison.clear()
            str_folderRoot = self.lineEdit_folderRoot.text()
            str_link = str_folderRoot + self.listWidget_pathPcf.currentItem().text()
            str_folder = '\\'.join(str_link.split('\\')[:-1]) + '\\'
            str_FileName = str_link.split('\\')[-1]
        except: 
            self.textEdit_Error.append('Please select a PCF path (onPush__DisplayDoc) !')
            return 0
        # Define the Table
        try:
            bl_header = None
            df = pp.fDf_getDfFromPCF(None, 0, str_folder, str_FileName, bl_header)
            df.fillna(value = '', inplace = True)
            if df is None: raise
        except:
            self.textEdit_Error.append('Impossible to proceed. onPush__DisplayDoc')
            return 0
        try:
            self.tableWidget_comparison.setColumnCount(len(df.columns))
            self.tableWidget_comparison.setRowCount(len(df.index))
            for i, row in enumerate(df.index):
                for j, col in enumerate(df.columns):
                    if df.iat[i, j] != '':
                        self.tableWidget_comparison.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))
            self.tableWidget_comparison.resizeColumnsToContents()
            self.tableWidget_comparison.resizeRowsToContents()
        except:     self.textEdit_Error.append('Display PCF - Could not process the display of array, onPush__DisplayDoc')
        
    @pyqtSlot()
    def onPush_sendPCF(self):
        # Param
        try:
            dte_date = self.lineEdit_Date.text()
            str_folderRoot = self.lineEdit_folderRoot.text()
            l_filesPath = self.listWidget_pathPcf.selectedItems()
            l_filesPath = [str_folderRoot + fold.text() for fold in l_filesPath]
            bl_displayMail = self.checkBox_DisplayMail.isChecked()
            bl_displayMail = True
            str_perimeter = self.listWidget_Pcf.currentItem().text()
            str_MailType = self.comboBox_MailType.currentText()
        except:
            self.textEdit_Error.append("Please select a PCF path !")
            db.Log_Python({'str_action':'SendMail', 'bl_error':1, 'str_comment':str_perimeter, 'str_Program':'Seita'})
            return 0 
        # Send
        try:
            #str_message = pcf.sendPCF(dte_date, l_filesPath, str_perimeter, bl_displayMail, False)
            str_message = pcf.sendPCF(dte_date, l_filesPath, str_perimeter, str_MailType, bl_displayMail)
            if not str_message == True: self.textEdit_Error.append(str_message)
        except:             
            self.textEdit_Error.append(' ** PCF Could not be sent')
            db.Log_Python({'str_action':'SendMail', 'bl_error':1, 'str_comment':str_perimeter, 'str_Program':'Seita'})
        db.Log_Python({'str_action':'SendMail', 'str_comment':str_perimeter, 'str_Program':'Seita'})
            
    @pyqtSlot()
    def onPush__sendFTP(self):
        # Param
        try:
            dte_date = self.lineEdit_Date.text()
            str_folderRoot = self.lineEdit_folderRoot.text()
            l_filesPath = self.listWidget_pathPcf.selectedItems()
            l_filesPath = [str_folderRoot + fold.text() for fold in l_filesPath]
            str_perimeter = self.listWidget_Pcf.currentItem().text()
            # Clear Windows
            self.listWidget_filePresentFTP.clear()
        except:
            self.textEdit_Error.append("Please select a PCF path !")
            db.Log_Python({'str_action':'SendFTP', 'bl_error':1, 'str_comment':str_perimeter, 'str_Program':'Seita'})
            return 0 
        # Send = UPLOAD
        try:
            str_message, l_ListFilesFTP = pcf.sendFTP(dte_date, l_filesPath, str_perimeter)
            #            str_return = pp.fStr_Upload_LaPerouse(str_perimeter, str_folderRoot, dte_date)
            if not str_message == True:
                self.textEdit_Error.append(str_message)
                db.Log_Python({'str_action':'SendFTP', 'str_comment': '{} ||| {}'.format(str_perimeter, str_message), 'str_Program':'Seita'})
            if not l_ListFilesFTP:
                str_message = 'l_ListFilesFTP is empty'
                self.textEdit_Error.append(str_message)
                db.Log_Python({'str_action':'SendFTP', 'bl_error':1, 'str_Program':'Seita', 
                                 'str_comment': '{} ||| {}'.format(str_perimeter, str_message)})
        except:
            self.textEdit_Error.append("\n ERROR: You didnt choose the right Perimeter: {}".format(str_perimeter))
            db.Log_Python({'str_action':'SendFTP', 'bl_error':1, 'str_Program':'Seita', 
                             'str_comment':'{} ||| You didnt choose the right Perimeter'.format(str_perimeter)})
        # Check if it is present on the FTP
        try:
            for str_File in l_ListFilesFTP:
                self.listWidget_filePresentFTP.addItem(str_File)
        except:
            self.textEdit_Error.append("\n ERROR: You could not fill the listWidget_filePresentFTP on Perimeter: {}".format(str_perimeter))
            db.Log_Python({'str_action':'SendFTP', 'bl_error':1, 'str_Program':'Seita', 
                             'str_comment':'{} ||| You could not fill the listWidget_filePresentFTP on Perimeter'.format(str_perimeter)})
        # LOG
        db.Log_Python({'str_action':'SendFTP', 'str_comment':str_perimeter, 'str_Program':'Seita'})
    
    @pyqtSlot()
    def onChange__Database(self):
        try:
            str_server = self.comboBox_DB.currentText()
            print('  (+++) Change of DB Server: ', str_server)
            inst_db = db.c_sqlDB()
            inst_db.server = str_server
        except: self.textEdit_Error.append(' ERROR: Could not Change the Database to the new value you input')
    
    def __del__(self):
        try:
            inst_db = db.c_sqlDB()
            inst_db.db_CloseConnexion()
        except: pass
    ## PUT THAT at The END of CREATE PCF or DOWNLOAD FILE with db as well
    #    # Kill Excel at the end to kill all ghost session
    #    try:
    #        inst_xlApp = fl.c_win32_xlApp()
    #        inst_xlApp.QuitXlApp()
    #    except Exception as err: print('ERROR: Kill Excel at the end to kill all ghost session - {0} | {1} '.format(str_PCF, str(err)))
    

if __name__ == '__main__':
    if not QApplication.instance():     app = QApplication(sys.argv)
    else:                               app = QApplication.instance() 
    
    widget = class_App()
    widget.show()
    
    if not QApplication.instance():     app = sys.exit(app.exec_())
    else:                               app = app.exec_()
    