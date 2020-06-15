import sys, os
import datetime as dt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog  #, QTableWidgetItem
from PyQt5.uic import loadUi
import NPA_Republished as rep
import NPA_BackUp as bck
import NPA_Log as log
import NPA_ArchiveMails as arch
import NPA_EasyForwardMail as easy
sys.path.append('../')
import fct_Files as fl
import fct_DB as db


str_Program = 'Spectre'
str_designFileName = 'NPA_design.ui'
str_windowTitle = 'Night Process App'

str_logFolder = r'\\uk-pdeqtfs01\E\Data\Lucerne\Data\SOLA PCF\Auto_Py\Log'

str_cloudPath = os.path.join(os.environ['USERPROFILE'], r'IHS Markit\HK PCF Services Team - General\Manual_py') #+ '\\'
str_cloudPath_Auto = str_cloudPath.replace('Manual_py', 'Auto_py')
str_networkPath = r'\\uk-pdeqtfs01\E\Data\Lucerne\Data\SOLA PCF' #+ '\\'
str_networkPath_Auto = str_networkPath + r'\Auto_py' #+ '\\'

str_sqlFileName = r'Re-Published ETF_Update Table.txt'


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
        dte_date = dt.datetime.now().date().strftime('%Y-%m-%d')
        self.lineEdit_Date.setText(dte_date)
        self.lineEdit_Origin.setText(str_cloudPath)
        self.lineEdit_Target.setText(str_networkPath)
        # Activate Button Event
        self.push_Clear.clicked.connect(self.onPush__Clear)
        self.Push_Republished.clicked.connect(self.OnPush__Republished)
        self.Push_BackUp.clicked.connect(self.OnPush__BackUp)
        self.Push_Log.clicked.connect(self.OnPush__Log)
        self.Push_Archive.clicked.connect(self.OnPush__ArchivesMails)
        self.Push_Easy.clicked.connect(self.OnPush__Easy)
        # checkBox
        self.checkBox_BackUpAuto.stateChanged.connect(self.onChange__BackUpAuto)
        #----------------------------------------------------------------------
        # LOAD Past Data
        # BACKUP
        self.label_backupOK.show()
        self.label_backupKO.hide()
        try:        str_return_Bck = fl.fStr_readFile(False, str_cloudPath_Auto + r'\file', str(dte_date) + '_' + 'BackUp.txt')
        except:
            str_return_Bck = ''
            self.label_backupOK.hide()
            self.label_backupKO.show()
        self.textEdit_BackUp.append(str_return_Bck)
        # REPUBLISHED
        self.label_repOK.show()
        self.label_repKO.hide()
        try:        str_return_Rep = fl.fStr_readFile(False, str_cloudPath_Auto + r'\file', str(dte_date) + '_' + 'Republished.txt')
        except: 
            str_return_Rep = ''
            self.label_repOK.hide()
            self.label_repKO.show()
        self.textEdit_Rep.append(str_return_Rep)
        # LOG
        self.label_logOK.show()
        self.label_logKO.hide()
        try:        str_return_Log = fl.fStr_readFile(False, str_cloudPath_Auto + r'\file', str(dte_date) + '_' + 'SaveLogExcel.txt')
        except:
            str_return_Log = ''
            self.label_logOK.hide()
            self.label_logKO.show()
        self.textEdit_Log.append(str_return_Log)
        # Archive Emails
        self.label_archOK.show()
        self.label_archKO.hide()
        try:        str_return_Arch = fl.fStr_readFile(False, str_cloudPath_Auto + r'\file', str(dte_date) + '_' + 'ArchiveOldEmail.txt')
        except:
            str_return_Arch = ''
            self.label_archOK.hide()
            self.label_archKO.show()
        self.textEdit_Archive.append(str_return_Arch)
        # Archive Emails
        self.label_easyOK.show()
        self.label_easyKO.hide()
        try:        str_return_easy = fl.fStr_readFile(False, str_cloudPath_Auto + r'\file', str(dte_date) + '_' + 'EasyForwardMail.txt')
        except:
            str_return_easy = ''
            self.label_easyOK.hide()
            self.label_easyKO.show()
        self.textEdit_Easy.append(str_return_easy)
        #----------------------------------------------------------------------
        
    @pyqtSlot()
    
    def onPush__Clear(self):
        self.textEdit_BackUp.clear()
        self.textEdit_Rep.clear()
        self.textEdit_Log.clear()
        self.textEdit_Archive.clear()
        self.textEdit_Easy.clear()
        self.textEdit_Error.clear()
        self.textEdit_Error.insertPlainText('Error Return: ')
        
    def onChange__BackUpAuto(self):
        bl_backUpAuto = self.checkBox_BackUpAuto.isChecked()
        if bl_backUpAuto:       
            self.lineEdit_Origin.setText(str_cloudPath_Auto)
            self.lineEdit_Target.setText(str_networkPath_Auto)
        else:               
            self.lineEdit_Origin.setText(str_cloudPath)
            self.lineEdit_Target.setText(str_networkPath)
     
    def OnPush__BackUp(self):
        # Param
        dte_date = self.lineEdit_Date.text()
        str_folderOrigin = self.lineEdit_Origin.text()
        str_folderTarget = self.lineEdit_Target.text()
        int_onlyFileMoreRecentThan = int(self.lineEdit_onlyFileMoreRecentThan.text())
        try:
            str_return = bck.fstr_BackUp(dte_date, str_folderOrigin, str_folderTarget, int_onlyFileMoreRecentThan)
            fl.act_createFile(False, str_cloudPath_Auto + r'\file', str(dte_date) + '_' + 'BackUp.txt', str_return)
        except:            
            str_ErrorComment = r'ERROR: fstr_BackUp did not work'
            self.textEdit_Error.append(str_ErrorComment)
            self.textEdit_BackUp.clear()
            Log_Python('BackUp', str_ErrorComment, 1)
            self.label_backupOK.hide()
            self.label_backupKO.show()
            return 0
        # LOG
        Log_Python('BackUp')
        self.label_backupOK.show()
        self.label_backupKO.hide()
        self.textEdit_BackUp.append(str_return)
    
    def OnPush__Republished(self):
        # Param
        dte_date = self.lineEdit_Date.text()
        try:
            str_return = rep.fstr_RePublished(str_sqlFileName, 'ETF', 60)
            fl.act_createFile(False, str_cloudPath_Auto + r'\file', str(dte_date) + '_' + 'Republished.txt', str_return)
        except:
            str_ErrorComment = r'ERROR: fstr_RePublished did not work'
            self.textEdit_Error.append(str_ErrorComment)
            self.textEdit_Rep.clear()
            Log_Python('Republished', str_ErrorComment, 1)
            self.label_repOK.hide()
            self.label_repKO.show()
            return 0
        # LOG
        Log_Python('Republished')
        self.label_repOK.show()
        self.label_repKO.hide()
        self.textEdit_Rep.append(str_return)
    
    def OnPush__Log(self):
        # Param
        dte_date = self.lineEdit_Date.text()
        try:
            str_return = log.fStr_SaveExcelLog(str_logFolder, 'log.txt')
            fl.act_createFile(False, str_cloudPath_Auto + r'\file', str(dte_date) + '_' + 'SaveLogExcel.txt', str_return)
        except:
            str_ErrorComment = r'ERROR: fStr_SaveExcelLog did not work'
            self.textEdit_Error.append(str_ErrorComment)
            self.textEdit_Log.clear()
            Log_Python('SaveLogExcel', str_ErrorComment, 1)
            self.label_logOK.hide()
            self.label_logKO.show()
            return 0
        # LOG
        Log_Python('SaveLogExcel')
        self.label_logOK.show()
        self.label_logKO.hide()
        self.textEdit_Log.append(str_return)
        
    def OnPush__ArchivesMails(self):
        # Param
        dte_date = self.lineEdit_Date.text()
        try:
            str_return = arch.ArchiveOldEmail()
            fl.act_createFile(False, str_cloudPath_Auto + r'\file', str(dte_date) + '_' + 'ArchiveOldEmail.txt', str_return)
        except:
            str_ErrorComment = r'ERROR: ArchiveOldEmail did not work'
            self.textEdit_Error.append(str_ErrorComment)
            self.textEdit_Archive.clear()
            Log_Python('ArchiveOldEmail', str_ErrorComment, 1)
            self.label_archOK.hide()
            self.label_archKO.show()
            return 0
        # LOG
        Log_Python('ArchiveOldEmail')
        self.label_archOK.show()
        self.label_archKO.hide()
        self.textEdit_Archive.append(str_return)
        
    def OnPush__Easy(self):
        # Param
        dte_date = self.lineEdit_Date.text()
        try:
            str_return = easy.EasyForwardMail()
            fl.act_createFile(False, str_cloudPath_Auto + r'\file', str(dte_date) + '_' + 'EasyForwardMail.txt', str_return)
        except:
            str_ErrorComment = r'ERROR: EasyForwardMail did not work'
            self.textEdit_Error.append(str_ErrorComment)
            self.textEdit_Easy.clear()
            Log_Python('EasyForwardMail', str_ErrorComment, 1)
            self.label_easyOK.hide()
            self.label_easyKO.show()
            return 0
        # LOG
        Log_Python('EasyForwardMail')
        self.label_easyOK.show()
        self.label_easyKO.hide()
        self.textEdit_Easy.append(str_return)
        
    
    
if __name__ == '__main__':
    if not QApplication.instance():     app = QApplication(sys.argv)
    else:                               app = QApplication.instance() 
    
    Log_Python('OPEN')
    widget = class_App()
    widget.show()
    
    if not QApplication.instance():     app = sys.exit(app.exec_())
    else:                               app = app.exec_()
    