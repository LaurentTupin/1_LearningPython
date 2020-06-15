import sys, os
import datetime as dt
import win32com.client as win32
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
sys.path.append('../')
import fct_DB as db
import DNS_1MainFct as m1
import DNS_3genericProcess as pp


str_Program = 'DNS'
str_designFileName = 'DNS_design.ui'
str_windowTitle = 'Download and Send'

str_networkPath = r'\\uk-pdeqtfs01\E\Data\Lucerne\Data\SOLA PCF' + '\\'
str_pathDesktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
str_localPath = os.path.join(str_pathDesktop, r'Python_App\PCF') + '\\'
str_paramFile = 'DNS_Param.csv'
str_paramPcfAddress = 'DNS_Param_PcfAdr.csv'
str_paramMailFile = 'DNS_Param_Mail.csv'

#str_networkFilePath = str_networkPath + 'file'
#str_localFilePath = str_localPath + 'file'
#str_folderNetwork = r'\\uk-pdeqtfs01\E\Data\Lucerne\Data\SOLA PCF\Python_Code\CodePackage\PCF\file'


#-----------------------------------------------------------------
# LOG
#-----------------------------------------------------------------
def Log_Python(str_action, str_comment = '', bl_error = 0):
    try:
        str_uid = os.getlogin()
        str_path = os.path.dirname(os.path.abspath(__file__))
        l_uid2 = str_uid.replace('.',' ').split(' ')
        str_uid2 = ' '.join([mot[:1].upper() + mot[1:] for mot in l_uid2])
        dte_Date = dt.datetime.now().date().strftime('%Y-%m-%d')
        str_query = "EXEC sp_log_add '" + str_uid + "','Python','" + str_action + "'," + str(bl_error) + ",'" \
                            + str_Program + "','" + str_path + "','" + str_uid2 + "','" + dte_Date  + "','" + str_comment + "'"
        db.db_EXEC(str_query,'','SolaQC')
    except: print('Log_Python did not work, please contact LAURENT TUPIN')
#-----------------------------------------------------------------
    

class class_App(QDialog):
    def __init__(self):
        super(class_App, self).__init__()
        loadUi(str_designFileName, self)
        self.setWindowTitle(str_windowTitle)
        # Define Value
        self.lineEdit_Date.setText(dt.datetime.now().date().strftime('%Y-%m-%d'))
        self.lineEdit_folderRoot.setText(str_networkPath)
        # Activate Button Event
        self.checkBox_DevEnv.stateChanged.connect(self.onChange_DevEnv)
        self.push_downloadFiles.clicked.connect(self.onPush_downloadFiles)
        self.push_loadPcf.clicked.connect(self.onPush_loadPcf)
        self.push_Clear.clicked.connect(self.onPush_Clear)
        self.push_DisplayDoc.clicked.connect(self.onPush__DisplayDoc)
        self.push_sendPCF.clicked.connect(self.onPush_sendPCF)
        self.push_OpenParamCSV.clicked.connect(self.onPush_OpenParamCSV)
        self.push_OpenParamMailCSV.clicked.connect(self.onpush_OpenParamMailCSV)
        self.push_OpenPcfPath.clicked.connect(self.onPush_OpenPcfPath)
        
        
        
    @pyqtSlot()
      
        
    def onPush_Clear(self):
        self.textEdit_Result.clear()
        self.textEdit_Error.clear()
        self.textEdit_Result.insertPlainText('Main Figures: ')
        self.textEdit_Error.insertPlainText('Error Return: ')
    
    def onChange_DevEnv(self):
        bl_devEnv = self.checkBox_DevEnv.isChecked()
        if bl_devEnv:
            self.lineEdit_folderRoot.setText(str_localPath)
        else: self.lineEdit_folderRoot.setText(str_networkPath)
        
    def onPush_OpenParamCSV(self):
        try:
            xlApp = win32.Dispatch('Excel.Application')
            xlApp.Visible = True
            xlApp.Workbooks.Open(os.getcwd() + '\\' + str_paramFile)
        except: self.textEdit_Error.append(' ERROR: Could not Open the file')
        
    def onPush_OpenPcfPath(self):
        try:
            xlApp = win32.Dispatch('Excel.Application')
            xlApp.Visible = True
            xlApp.Workbooks.Open(os.getcwd() + '\\' + str_paramPcfAddress)
        except: self.textEdit_Error.append(' ERROR: Could not Open the file')
        
    def onpush_OpenParamMailCSV(self):
        try:
            xlApp = win32.Dispatch('Excel.Application')
            xlApp.Visible = True
            xlApp.Workbooks.Open(os.getcwd() + '\\' + str_paramMailFile)
        except: self.textEdit_Error.append(' ERROR: Could not Open the file')
        
    
    def onPush_downloadFiles(self):
        # Param
        dte_date = self.lineEdit_Date.text()
        str_floderRoot = self.lineEdit_folderRoot.text()
        bl_ArchiveMails = self.checkBox_ArchiveMails.isChecked()
        # Clear 
        self.listWidget_pathPcf.clear()
        try:
            str_perimeter = self.listWidget_Pcf.currentItem().text()
        except:
            self.textEdit_Error.append(" ERROR: You didn't choose any perimeter: " + str_perimeter)
            Log_Python('Download Files', 'No PCF chosen', 1)
            return 0
        # Choose PCF
        try:
            str_resultFigures, l_pathPcf = m1.DownloadFiles(str_perimeter, str_floderRoot, dte_date, bl_ArchiveMails)
            if 'ERROR' in str_resultFigures or l_pathPcf == []:
                self.textEdit_Error.append(str_resultFigures)
                Log_Python('Download Files', str_perimeter, 1)
                return 0
        except:
            self.textEdit_Error.append(" ERROR in onPush_downloadFiles: You didn't choose the right perimeter: " + str_perimeter)
            Log_Python('Download Files', str_perimeter, 1)
            return 0
        # Display the main figures        
        self.textEdit_Result.append(str_resultFigures)
        # Return the Path of PCF Produced        
        for path in l_pathPcf:
            self.listWidget_pathPcf.addItem(path)
        #LOG
        Log_Python('Download Files', str_perimeter)
        
    
    def onPush__DisplayDoc(self):
        try:
            self.tableWidget_comparison.clear()
            str_floderRoot = self.lineEdit_folderRoot.text()
            str_link = str_floderRoot + self.listWidget_pathPcf.currentItem().text()
            str_foler = '\\'.join(str_link.split('\\')[:-1]) + '\\'
            str_FileName = str_link.split('\\')[-1]
        except: 
            self.textEdit_Error.append('Please select a PCF path (DisplayDoc) !')
            return 0
        # Define the Table
        try:
            bl_header = None
            df = pp.fDf_getDfFromDownloaded(None, 0, str_foler, str_FileName, bl_header)
            df.fillna(value = '', inplace = True)
            if df is None: raise
        except: 
            self.textEdit_Error.append('Impossible to proceed. (DisplayDoc)')
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
        except: self.textEdit_Error.append('Display PCF - Could not process the display of array, (DisplayDoc)')
        
   
    def onPush_loadPcf(self):
        # Param
        str_floderRoot = self.lineEdit_folderRoot.text()
        dte_date = self.lineEdit_Date.text()
        str_perimeter = self.listWidget_Pcf.currentItem().text()
        self.listWidget_pathPcf.clear()
        try:
            str_perimeter = self.listWidget_Pcf.currentItem().text()
        except: str_perimeter = 'HK - AM'
        # Read File
        try: 
            str_resultFigures, l_pathPcf = m1.RetrievePcfPath(str_perimeter, str_floderRoot, dte_date)
            if 'ERROR' in str_resultFigures or l_pathPcf == []:
                self.textEdit_Error.append(str_resultFigures)
                Log_Python('GetPCF_path', str_perimeter, 1)
                return 0
        except: 
            self.textEdit_Error.append(" ERROR in onPush_loadPcf: You didn't choose the right perimeter: " + str_perimeter)
            Log_Python('GetPCF_path', str_perimeter, 1)
            return 0
        # Display the main figures        
        self.textEdit_Result.append(str_resultFigures)
        # Return the Path of PCF Produced
        for path in l_pathPcf:
            self.listWidget_pathPcf.addItem(path)
        # LOG
        Log_Python('GetPCF_path', str_perimeter)
        
    
    def onPush_sendPCF(self):
        try:    # Param
            dte_date = self.lineEdit_Date.text()
            str_folderRoot = self.lineEdit_folderRoot.text()        
            l_folder = self.listWidget_pathPcf.selectedItems()
            l_folder = [str_folderRoot + fold.text() for fold in l_folder]
            bl_displayMail = self.checkBox_DisplayMail.isChecked()
            # Force to TRUE
            bl_displayMail = True
            str_perimeter = self.listWidget_Pcf.currentItem().text()
        except:
            self.textEdit_Error.append("Please select a PCF path !")
            Log_Python('SendMail', l_folder[0], 1)
            return 0 
        try:
            m1.sendPCF(dte_date,l_folder, str_perimeter, bl_displayMail)
        except:             
            self.textEdit_Error.append('PCF Could not be sent. Please check if the file has been created !')
            Log_Python('SendMail', str_perimeter, 1)
        # LOG
        Log_Python('SendMail', str_perimeter)
        


if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    
    Log_Python('OPEN')
    widget = class_App()
    widget.show()
    
    if not QApplication.instance():
        app = sys.exit(app.exec_())
    else: app = app.exec_()
    