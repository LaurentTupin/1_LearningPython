'''
# Course:
#   https://www.youtube.com/watch?v=7SrD4l2o-uk
#   https://www.youtube.com/watch?v=Dmo8eZG5I2w
# Install:
#   Open command windows in the Dir of this file
#   pyuic -x pyqtdesigner.ui -o pyqtdesigner.py
#   C:/Python34/Lib/site-packages/PyQt4/pyuic4.bat -x pyqtdesigner.ui -o pyqtdesigner.py
'''

import sys, os
import datetime as dt
import win32com.client as win32
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog   #, QTableWidgetItem
from PyQt5.uic import loadUi
#import PCF_creater as pcf
#import PCF_download as dwl
#import PCF_genericProcess as pp
import Process_Bruni as pp
sys.path.append('../')
#import fct_Files as fl
import fct_DB as db


str_Program = 'LaPerouse'
str_designFileName = 'LaPerouse.ui'
str_windowTitle = 'Upload FTP with LaPerouse'      


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
        self.lineEdit_folderRoot.setText(r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Auto_py' + '\\')
        # Activate Button Event
        self.push_Clear.clicked.connect(self.onPush_Clear)
        self.push_uploadFiles.clicked.connect(self.onPush_uploadFiles)
        self.push_downloadFiles.clicked.connect(self.onPush_downloadFiles)
        self.push_ListDirFTP.clicked.connect(self.onPush_ListDirFTP)
        self.push_OpenParamCSV.clicked.connect(self.onPush_OpenParamCSV)
        
        
    @pyqtSlot()
    
    
    def onPush_OpenParamCSV(self):
        try:
            xlApp = win32.Dispatch('Excel.Application')
            xlApp.Visible = True
            xlApp.Workbooks.Open(os.getcwd() + '\\LaPerouse_Param.csv')
        except: self.label_error.setText(self.label_error.text() + "\n ERROR: Could not Open the file")
    
    
    def onPush_ListDirFTP(self):
        # Param
        dte_date = self.lineEdit_Date.text()
        str_folderRoot = self.lineEdit_folderRoot.text()
        # Clear 
        self.listWidget_filePresentFolder.clear()
        self.listWidget_filePresentFTP.clear()
        # Choose Perimeter
        try:
            str_perimeter = self.listWidget_Pcf.currentItem().text()
        except: self.label_error.setText(self.label_error.text()  + "\n" + 'Perimeter is empty')
        # List on the server
        try:
            str_errorReport, l_ListFilesFolder, l_ListFilesFTP = pp.fL_ListFilesFTP(str_perimeter, str_folderRoot, dte_date)
            if str_errorReport: 
                Log_Python('FTP List Dir', str_perimeter+ ' ||| ' + str_errorReport, 1)
                self.label_error.setText(self.label_error.text()  + "\n" + str_errorReport)
        except:
            self.label_error.setText(self.label_error.text() + "\n ERROR: You didn't choose the right Perimeter: " + str_perimeter)
        # Fill it
        for str_File in l_ListFilesFolder:
            self.listWidget_filePresentFolder.addItem(str_File)
        for str_File in l_ListFilesFTP:
            self.listWidget_filePresentFTP.addItem(str_File)
        #LOG
        Log_Python('FTP List Dir', str_perimeter)
        print('Listing File is finish !')
        print('------------------------------------------------')
        
    
    def onPush_uploadFiles(self):
        # Param
        dte_date = self.lineEdit_Date.text()
        str_folderRoot = self.lineEdit_folderRoot.text()
        # Clear 
        self.listWidget_filePresentFolder.clear()
        self.listWidget_filePresentFTP.clear()
        # Choose Perimeter
        try:
            str_perimeter = self.listWidget_Pcf.currentItem().text()
        except: str_perimeter = ''
        # Upload
        try:
            str_return = pp.fStr_Upload_LaPerouse(str_perimeter, str_folderRoot, dte_date)
            if 'ERROR' in str_return or not str_return:
                Log_Python('FTP Upload', str_perimeter + ' ||| ' + str_return, 1)
                self.label_error.setText(self.label_error.text() + "\n" + str_return)
        except:
            self.label_error.setText(self.label_error.text() + "\n ERROR: You didn't choose the right Perimeter: " + str_perimeter)
        # Display the main figures
        #self.label_Result.setText(self.label_Result.text() + "\n" + str_return)
        #LOG
        Log_Python('FTP Upload', str_perimeter)
        print('Upload is finish !')
        print('------------------------------------------------')
        
        
    def onPush_downloadFiles(self):
        # Param
        dte_date = self.lineEdit_Date.text()
        str_folderRoot = self.lineEdit_folderRoot.text()
        bl_download = True
        # Clear 
        self.listWidget_filePresentFolder.clear()
        self.listWidget_filePresentFTP.clear()
        # Choose Perimeter
        try:
            str_perimeter = self.listWidget_Pcf.currentItem().text()
        except: str_perimeter = ''
        # Upload
        try:
            str_return = pp.fStr_Upload_LaPerouse(str_perimeter, str_folderRoot, dte_date, bl_download)
            if 'ERROR' in str_return or not str_return:
                Log_Python('FTP Download', str_perimeter + ' ||| ' + str_return, 1)
                self.label_error.setText(self.label_error.text() + "\n" + str_return)
        except:
            self.label_error.setText(self.label_error.text() + "\n ERROR: You didn't choose the right Perimeter: " + str_perimeter)
        # Display the main figures
        #self.label_Result.setText(self.label_Result.text() + "\n" + str_return)
        #LOG
        Log_Python('FTP Download', str_perimeter)
        print('Download is finish !')
        print('------------------------------------------------')
        
    
    def onPush_Clear(self):
        self.listWidget_filePresentFolder.clear()
        self.listWidget_filePresentFTP.clear()
        #self.label_Result.clear()
        self.label_error.clear()
        #self.label_Result.setText('Main Figures: ')
        self.label_error.setText('Error Return :')
        

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

