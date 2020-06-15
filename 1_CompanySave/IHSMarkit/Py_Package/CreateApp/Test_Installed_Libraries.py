

print('Welcome to the Installer helper !')
print(' You will have all the steps to know what you have to install')

bl_try_Importing = True


try:    
    import os
    import sys
    import datetime
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have one of the following library: os, sys, datetime')
    print('Please try to uninstall Anaconda and re-install it')
    print('Please contact Laurent Tupin for Help if needed')
    bl_try_Importing = False
## Add the folder
#try:
#    str_link = r'c:\programdata\anaconda3\lib\site-packages\ipython\extensions'
#    str_link = r'c:\programdata\anaconda3\Scripts'
#    str_link = r'c:\users\laurent.tupin\.ipython'
#    l_path = sys.path
#    l_path = [path.lower() for path in l_path]
#    l_path = list(dict.fromkeys(l_path))
#    if not str_link in l_path:
#        print('Adding Folder...    ')
#        sys.path.append(str_link)
#        #import Scripts
#    else:        print('No folder to ADD')
#except:
#    print('--------------------------------------------------------------------------------')
#    print('Error in import folder')
try:        import time
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have the library time. Please Open Anaconda prompt and type the following: ')
    print('pip install time --user')
    bl_try_Importing = False
try:        import pandas
except Exception as e: 
    print('--------------------------------------------------------------------------------')
    print(e)
    print('You do not have the library pandas. Please Open Anaconda prompt and type the following: ')
    print('pip install pandas --user')
    bl_try_Importing = False
try:        from pandas.tseries.offsets import BDay
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have !!! BDay !!! in the library pandas. ')
    bl_try_Importing = False
try:        import numpy
except Exception as e: 
    print('--------------------------------------------------------------------------------')
    print(e)
    print('You do not have the library numpy. ')
    bl_try_Importing = False
try:        import ftplib
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have the library ftplib. Please Open Anaconda prompt and type the following: ')
    print('pip install ftplib --user')
    bl_try_Importing = False
try:        import pyodbc
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have the library pyodbc. Please Open Anaconda prompt and type the following: ')
    print('pip install pyodbc --user')
    bl_try_Importing = False
try:        import requests
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have the library requests. Please Open Anaconda prompt and type the following: ')
    print('pip install requests --user')
    bl_try_Importing = False
try:        from bs4 import BeautifulSoup
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have the library beautifulsoup4. Please Open Anaconda prompt and type the following: ')
    print('pip install beautifulsoup4 --user')
    bl_try_Importing = False
try:        import xlsxwriter
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have the library xlsxwriter. Please Open Anaconda prompt and type the following: ')
    print('pip install xlsxwriter --user')
    bl_try_Importing = False
try:        import win32com.client as win32
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have the library win32com. Please Open Anaconda prompt and type the following: ')
    print('pip install pypiwin32  --user')
    bl_try_Importing = False
try:        import paramiko
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have the library paramiko. Please Open Anaconda prompt and type the following: ')
    print('pip install paramiko --user')
    bl_try_Importing = False
try:        from PyQt5.QtCore import pyqtSlot
except Exception as e: 
    print('--------------------------------------------------------------------------------')
    print(e)
    print('You do not have the library PyQt5. Please Open Anaconda prompt and type the following: ')
    print('pip install PyQt5==5.9.2 --user')
    print('pip install pyqt5-tools==5.9.2.1.3rc3 --user')
    bl_try_Importing = False
try:        from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
except Exception as e: 
    print('--------------------------------------------------------------------------------')
    print(e)
    print('You do not have the library PyQt5 tools. Please Open Anaconda prompt and type the following: ')
    print('pip install pyqt5-tools==5.9.2.1.3rc3 --user')
    bl_try_Importing = False
try:        from PyQt5.uic import loadUi
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have the library loadUi.')
    print('Please contact Laurent Tupin for Help if needed')
    bl_try_Importing = False
try:        from dateutil.relativedelta import relativedelta
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have the library dateutil. Please Open Anaconda prompt and type the following: ')
    print('pip install python-dateutil --user')
    bl_try_Importing = False
try:        import shutil
except:
    print('--------------------------------------------------------------------------------')
    print('You do not have the library shutil.')
    bl_try_Importing = False





if bl_try_Importing:
    print('+++++++++++++++++++++++++++++++++++')
    print('All libraries are installed successfully')
    print('+++++++++++++++++++++++++++++++++++')    


#time.sleep(20)
input("Press Enter to close the window: ")


#	Also, in case of old version, you can do:
# 	- python -m pip install --upgrade pip --user
# 	- pip install msgpackpip install msgpack --user
