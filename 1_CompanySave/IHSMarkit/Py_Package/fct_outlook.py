try:
    import os
    import numpy as np
    import win32com.client as win32
    import exchangelib as xLib
    #from exchangelib import Credentials, Configuration, Account, DELEGATE, FileAttachment
except Exception as err:
    str_lib = str(err).replace("No module named ", "").replace("'", "")
    print(" ATTENTION,  Missing library: '{0}' \n * Please Open Anaconda prompt and type: 'pip install {0}'".format(str_lib))



#https://pypi.org/project/exchangelib/
    
    

#server = 'eumail.ihsmarkit.com'   #'https://10.199.15.14/owa/'
#mailAddress = 'sola@ihsmarkit.com'
#username = mailAddress #'markit\sola'
#password = 'D3lt@0n3'
#ews_auth_type = 'NTLM'
#
#credentials = Credentials(username = username, password = password)
#config = Configuration(server = server, credentials = credentials)
##config = Configuration(service_endpoint = server, credentials = credentials, auth_type = ews_auth_type)
##account = Account(primary_smtp_address = mailAddress, credentials = credentials, autodiscover = True)#, access_type = DELEGATE)
#account = Account(primary_smtp_address = mailAddress, config = config, autodiscover = True, access_type = DELEGATE)
##print(account.ad_response)
#print(account)
##print(account.inbox)
##print(account.sent)
#o_folder = account.inbox / 'PCF-Received'
#print(o_folder)
#o_submail = o_folder.filter(subject__icontains = 'blabla')
#
#
##for item in some_folder.all():
##    for attachment in item.attachments:
##        if isinstance(attachment, FileAttachment):
##            local_path = os.path.join(local_path, attachment.name)
##            with open(local_path, 'wb') as f:
##                f.write(attachment.content)
#
##account.protocol.close()



##------------------------------------------------------------------------------
##------------- CLASS Email management -----------------------------------------
##------------------------------------------------------------------------------
#class c_WebMail():
#    """https://towardsdatascience.com/download-email-attachment-from-microsoft-exchange-web-services-automatically-9e20770f90ea
#    https://pypi.org/project/exchangelib/"""
#    def __init__(self):
#        self.o_config = None
#        self.o_account = None
#        self.o_folder = None
#        self.o_ArchiveFolder = None
#        self.o_mails = None
#        
#    #=== SEND MAILS ===========================================================
#    
#    
#    #=== LOOK INTO RECEIVED MAILS =============================================
#    def mail_DefineWebmail(self, str_MailAddr, str_pwd):
#        self.str_MailAddr = str_MailAddr
#        self.str_username = str_MailAddr
#        self.str_pwd = str_pwd
#        self.str_server = 'eumail.{}'.format(str_MailAddr.split('@')[-1])
#        self.ews_auth_type = 'NTLM'
#        try:
#            self.o_cred = Credentials(username = self.str_username, password = self.str_pwd)
#            self.o_config = Configuration(server = self.str_server, credentials = self.o_cred)
#            # o_config = Configuration(service_endpoint = server, credentials = credentials, auth_type = ews_auth_type)
#        except Exception as err:
#            print(' ERROR in mail_DefineWebmail: Cannot define Param')
#            print(' - ', str(err))
#            raise
#        return self.o_config
#    
#    def mail_getAccount(self):
#        try:    
#            if self.o_config is None:       raise
#        except:
#            print(' ERROR in mail_getAccount: o_config is not defined, cannot go further')
#            raise
#        try:
#            o_account = Account(primary_smtp_address = self.str_MailAddr, 
#                                credentials = self.o_cred,              # config = self.o_config
#                                autodiscover = True,
#                                access_type = DELEGATE)
#            #print(account.ad_response)
#            self.o_account = o_account
#        except Exception as err:
#            print(' ERROR in mail_getAccount: Cannot define o_account')
#            print(' - ', str(err))
#            raise
#        return self.o_account
#    
#    def mail_DefineFolder(self, str_Mailbox = 'Inbox', l_folders = []):
#        if self.o_account is None:      self.mail_getAccount()
#        self.str_Mailbox = str_Mailbox
#        self.l_folders = l_folders
#        # FIND FOLDERS
#        try:
#            # Define Inbox object (can be Send Items or else)
#            if self.str_Mailbox == 'Inbox':
#                o_folderBox = self.o_account.inbox
#                if l_folders:
#                    o_folder = o_folderBox / l_folders[0]
#                    for folder in l_folders[1:]:
#                        o_folder = o_folder / folder  #CHECK if its works
#                else:   o_folder = o_folderBox
#            else:       print(' INCOMPLETE in mail_DefineFolder. Please fill the condition : str_Mailbox = {}'.format(str_Mailbox))
#        except Exception as err:
#            print(' ERROR in mail_DefineFolder: Cannot find the folders')
#            print(' - ', str(err))
#            raise
#        # Put the info into Class
#        self.o_folderBox = o_folderBox
#        self.o_folder = o_folder
#        return self.o_folder
#    
#    def mail_DefineArchiveFolder(self, l_folders = []):
#        if self.o_folder is None:       self.mail_DefineFolder()
#        try:
#            if l_folders:
#                o_ArchiveFolder = self.o_folder / l_folders[0]  #CHECK if its works
#                for folder in l_folders[1:]:
#                    o_ArchiveFolder = o_ArchiveFolder / folder
#            else:   self.o_ArchiveFolder = None
#        except Exception as err:
#            print(' ERROR in mail_DefineArchiveFolder: Cannot find the folder Archive')
#            print(' - ', str(err))
#            raise
#        # Put the info into Class
#        self.o_ArchiveFolder = o_ArchiveFolder
#        return self.o_ArchiveFolder 
#    
#    def mail_GetAllMails(self):
#        '''Please Do not use'''
#        if self.o_folder is None:       self.outlk_DefineFolder()
#        try:
#            o_mails = self.o_folder.all()
#            if o_mails == []:           raise
#        except Exception as err:
#            print(' ERROR in mail_GetMails: Cannot get the mails')
#            print(' - ', str(err))
#            raise
#        self.o_mails = o_mails
#        return self.o_mails
#    
#    def mail_FilterMails(self, str_mailSubject, str_to = '', str_cc = '', str_File_startW = '', str_File_endW = ''):        
#        try:
#            self.str_mailSubject = str_mailSubject
#            # Filter on subject
#            if not str_mailSubject == '':
#                o_subMail = self.o_folder.filter(subject__icontains = str_mailSubject)
#            # Filter by name of attach 
#            if not str_File_startW == '':
#                o_subMail = [o_mail for o_mail in o_subMail if str_File_startW.lower() in 
#                             [str(o_attach.name).lower()[:len(str_File_startW)] for o_attach in o_mail.Attachments]]
#                if o_subMail == []:     print(' ... Empty on outlk_Filter with str_File_startW')
#            # Filter by name of attach if It is NOT Exact
#            if not str_File_endW == '':
#                o_subMail = [o_mail for o_mail in o_subMail if str_File_endW.lower() in 
#                             [str(o_attach.name).lower()[-len(str_File_endW):] for o_attach in o_mail.attachments]]
#                if o_subMail == []:     print(' ... Empty on outlk_Filter with str_File_endW')
#            # TEST END
#            if o_subMail == []:             raise   
#        except Exception as err:
#            print(' ERROR in mail_FilterMails: Cannot find the mails with Filter')
#            print(' - ', str(err))
#            raise
#        self.o_mails = o_subMail
#        return self.o_mails
#    
#    def mail_GetLatestMail(self):
#        try:    
#            if self.o_mails is None:       raise
#        except:
#            print(' ERROR in mail_GetLatestMail: o_mails is not defined, cannot go further')
#            raise
#        o_mails = self.o_mails
#        try:
#            # ----- TEST ---------
#            o_mail = o_mails.order_by('datetime_received')[0]
#            print(o_mail.subject, o_mail.sender, o_mail.datetime_received) 
#            o_mail = o_mails.order_by('-datetime_received')[0]
#            print(o_mail.subject, o_mail.sender, o_mail.datetime_received) 
#            #-----------------
#        except Exception as err:
#            print(' ERROR in mail_GetLatestMail: Cannot find the last mail')
#            print(' - ', str(err))
#            raise
#        self.o_latestMail = o_mail
#        return self.o_latestMail
#    
#    def mail_DownloadEmailsPJ(self, str_folder, str_File_startW = '', str_File_endW = ''):
#        if self.o_latestMail is None:    self.mail_GetLatestMail()
#        l_docDownloaded = []
#        o_mail = self.o_latestMail
#        try:
#            bl_download = False
#            for o_attach in o_mail.attachments:
#                if isinstance(o_attach, FileAttachment):
#                    str_attach = str(o_attach.name)
#                    str_lowerFileName = str_attach.lower()
#                    if (str_File_startW == '') or (str_File_startW.lower() == str_lowerFileName.lower()[:len(str_File_startW)]):
#                        if (str_File_endW == '') or (str_File_endW.lower() == str_lowerFileName.lower()[-len(str_File_endW):]):
#                            bl_download = True
#                    if bl_download:
#                        l_docDownloaded.append(str_attach)
#                        # DOWNLOAD
#                        str_path = os.path.join(str_folder, str_attach)
#                        with open(str_path, 'wb') as f:
#                            f.write(o_attach.content)
#        except Exception as err:
#            print(' ERROR in mail_DownloadEmailsPJ: Cannot dwld the mails')
#            print(' - ', str(err))
#            raise
#        #o_mail.Unread = False
#        if not l_docDownloaded:
#            print(' EMPTY in mail_DownloadEmailsPJ: download nothing from Mail')
#            print(' - Outlook Folder: ', str_folder)
#            print(' - Mail Subject: ', self.str_mailSubject)
#            print(' - fileName: ', str_File_startW, str_File_endW)
#        self.l_docDownloaded = l_docDownloaded
#        return self.l_docDownloaded
#    
#    def mail_ArchiveEmail(self):
#        if self.o_latestMail is None:    self.mail_GetLatestMail()
#        try:
#            self.o_latestMail.Move(self.o_ArchiveFolder)
#        except Exception as err:
#            print(' ERROR in mail_ArchiveEmail')
#            print(' - ', str(err))
#            raise
#        return True
#    
#    def __del__(self):
#        if not self.o_account is None:
#            self.o_account.protocol.close()
##____________________________________________________________________________                
    
    




class c_outlookMail():
    def __init__(self):
        self.o_outlkAcct = None
        self.o_folderAcct = None
        self.o_folder = None
        self.o_mails = None
    
    def outlk_DefineOutlook(self, str_nameSpace = ''):
        try:        o_outlook = self.o_outlook
        except:
            try:
                if str_nameSpace == '':     o_outlook = win32.Dispatch('outlook.application')
                else:                       o_outlook = win32.Dispatch('Outlook.Application').GetNamespace('MAPI')
                self.o_outlook = o_outlook
            except Exception as err:
                print(' ERROR in outlk_DefineOutlook: Cannot define Outlook App in win32')
                print(' - ', str(err))
                raise
        return o_outlook
    
    #=== SEND MAILS ==================================================
    def outlk_SendMails(self, str_to, str_cc = '', str_bcc = '', str_subject = '', l_pathAttach = [], str_message = '', str_from='', bl_draft=True):
        o_outlook = self.outlk_DefineOutlook()
        self.str_to = str_to
        self.str_cc = str_cc
        self.str_bcc = str_bcc
        self.str_subject = str_subject
        self.l_pathAttach = l_pathAttach
        self.str_message = str_message
        self.str_from = str_from
        self.bl_draft = bl_draft
        try:
            o_mail = o_outlook.CreateItem(0)
            if self.str_from != '':     o_mail.SentOnBehalfOfName = self.str_from
            if self.str_to != '':       o_mail.To = self.str_to
            if self.str_cc != '':       o_mail.Cc = self.str_cc
            if self.str_bcc != '':      o_mail.Bcc = self.str_bcc
            if self.str_subject != '':  o_mail.Subject = self.str_subject
            if self.str_message != '':  o_mail.Body = self.str_message
            #o_mail.HTMLBody = '<h2>HTML Message body</h2>' 
        except Exception as err:
            print(' ERROR in outlk_SendMails: Cannot define the Email')
            print(' - ', str(err))
            raise
        try:
            for attach in self.l_pathAttach:
                o_mail.Attachments.Add(attach)
        except Exception as err:
            print(' ERROR in outlk_SendMails: Cannot attch file to the mail')
            print(' - ', str(err))
            raise
        try:
            if self.bl_draft:   o_mail.Display(True)
            else:               o_mail.Send()
        except Exception as err:
            print(' ERROR in outlk_SendMails: Cannot send / display the mail')
            print(' - ', str(err))
            raise
        return o_mail
    
    
    #=== LOOK INTO RECEIVED MAILS ==================================================
    def outlk_getAccount(self, str_outlkAcctName = 'sola@ihsmarkit.com'):
        o_outlook = self.outlk_DefineOutlook('MAPI')
        self.str_outlkAcctName = str_outlkAcctName
        try:
            o_outlkAcct = o_outlook.Session.Accounts(self.str_outlkAcctName)
            if o_outlkAcct is None:   raise
        except:
            str_ErrorMsg = ' WARNING in outlk_getAccount | Cannot find Account : {}{}'.format(str_outlkAcctName, '\n')
            for account in o_outlook.Session.Accounts:
                str_account = str(account)
                str_ErrorMsg += ' - Available Outlk Acct on this machine : {}{}'.format(str_account, '\n')
                if str_account.lower() == str_outlkAcctName.lower():        self.str_outlkAcctName = str_account
                elif str_account.upper() == str_outlkAcctName.upper():      self.str_outlkAcctName = str_account
                try:    o_outlkAcct = o_outlook.Session.Accounts(self.str_outlkAcctName)
                except Exception as err:
                    print(str_ErrorMsg)
                    print(' ERROR in outlk_getAccount: Cannot find the Outlk Account')
                    print(' - ', str(err))
                    raise
        self.o_outlkAcct = o_outlkAcct
        self.o_folderAcct = o_outlook.Folders(self.str_outlkAcctName)
        ## Re-Define the name of the account
        #self.str_outlkAcctName = o_outlkAcct.DeliveryStore.DisplayName
        return self.o_folderAcct
    
    def outlk_DefineFolder(self, str_outlkMailbox = 'Inbox', l_folders = []):
        if self.o_folderAcct is None:       self.outlk_getAccount()
        self.str_outlkMailbox = str_outlkMailbox
        self.l_folders = l_folders
        # FIND FOLDERS
        try:
            # Define Inbox object (can be Send Items or else)
            o_folderBox = self.o_folderAcct.Folders[str_outlkMailbox]
            # Go into Inbox Folders hierarchy
            if l_folders:
                o_folder = o_folderBox.Folders[l_folders[0]]
                for folder in l_folders[1:]:
                    o_folder = o_folder.Folders[folder]
            else:   o_folder = o_folderBox
        except Exception as err:
            print(' ERROR in outlk_DefineFolder: Cannot find the folders')
            print(' - ', str(err))
            raise
        # Put the info into Class
        self.o_folderBox = o_folderBox
        self.o_folder = o_folder
        return self.o_folder
    
    def outlk_DefineArchiveFolder(self, l_folders = []):
        if self.o_folder is None:       self.outlk_DefineFolder()
        try:
            if l_folders:
                o_ArchiveFolder = self.o_folder.Folders[l_folders[0]]
                for folder in l_folders[1:]:
                    o_ArchiveFolder = o_ArchiveFolder.Folders[folder]
            else:   self.o_ArchiveFolder = None
        except Exception as err:
            print(' ERROR in outlk_DefineArchiveFolder: Cannot find the folder Archive')
            print(' - ', str(err))
            raise
        # Put the info into Class
        self.o_ArchiveFolder = o_ArchiveFolder
        return self.o_ArchiveFolder 
    
    def outlk_GetMails(self):
        if self.o_folder is None:       self.outlk_DefineFolder()
        try:
            o_mails = self.o_folder.Items
            if o_mails == []:           raise
        except Exception as err:
            print(' ERROR in outlk_GetMails: Cannot get the mails')
            print(' - ', str(err))
            raise
        self.o_mails = o_mails
        return self.o_mails
    
    def outlk_GetLastMails(self, int_nbMails = 500):
        if self.o_folder is None:       self.outlk_DefineFolder()
        try:
            o_mails = self.o_folder.Items
            o_mails.Sort("[ReceivedTime]", True)
            o_mails = o_mails[:int_nbMails]
            if o_mails == []:           raise
        except Exception as err:
            print(' ERROR in outlk_GetLastMails: Cannot get the mails')
            print(' - ', str(err))
            raise
        self.o_mails = o_mails
        return self.o_mails
    
    def outlk_FilterMails(self, str_mailSubject, str_to = '', str_cc = '', str_File_startW = '', str_File_endW = ''):        
        if self.o_mails is None:        self.outlk_GetMails()
        try:
            self.str_mailSubject = str_mailSubject
            o_subMail = self.o_mails
            # Filter on subject
            if not str_mailSubject == '':
                o_subMail = [o_mail for o_mail in o_subMail if str_mailSubject in o_mail.Subject]
                if o_subMail == []:     print(' ... Empty on outlk_Filter with Subject: {}'.format(str_mailSubject))
            # Filter by To / Cc
            if not str_to == '':
                o_subMail = [o_mail for o_mail in o_subMail if str_to in o_mail.To]
                if o_subMail == []:     print(' ... Empty on outlk_Filter with To: {}'.format(str_to))
            if not str_cc == '':
                o_subMail = [o_mail for o_mail in o_subMail if str_cc in o_mail.Cc] 
                if o_subMail == []:     print(' ... Empty on outlk_Filter with CC: {}'.format(str_cc))
            # Filter by name of attach 
            if not str_File_startW == '':
                o_subMail = [o_mail for o_mail in o_subMail if str_File_startW.lower() in 
                             [str(o_attach).lower()[:len(str_File_startW)] for o_attach in o_mail.Attachments]]
                if o_subMail == []:     print(' ... Empty on outlk_Filter with str_File_startW: {}'.format(str_File_startW))
            # Filter by name of attach if It is NOT Exact
            if not str_File_endW == '':
                o_subMail = [o_mail for o_mail in o_subMail if str_File_endW.lower() in 
                             [str(o_attach).lower()[-len(str_File_endW):] for o_attach in o_mail.Attachments]]
                if o_subMail == []:     print(' ... Empty on outlk_Filter with str_File_endW: {}'.format(str_File_endW))
            # TEST END
            if o_subMail == []:             raise   
        except Exception as err:
            print(' ERROR in outlk_FilterMai: Cannot filter the mails')
            print(' - ', str(err))
            raise
        self.o_mails = o_subMail
        return self.o_mails
    
    def outlk_GetLatestMail(self):
        if self.o_mails is None:        self.outlk_GetMails()
        o_mails = self.o_mails
        o_mail = o_mails[np.argmax([o_mail.Senton for o_mail in o_mails])]
        # o_mails.Sort("[ReceivedTime]", True)
        self.o_latestMail = o_mail
        return self.o_latestMail
    
    def outlk_DownloadEmailsPJ(self, str_folder, str_File_startW = '', str_File_endW = ''):
        if self.o_latestMail is None:    self.outlk_GetLatestMail()
        l_docDownloaded = []
        o_mail = self.o_latestMail
        try:
            bl_download = False
            for o_attach in o_mail.Attachments:
                str_lowerFileName = str(o_attach).lower()
                if (str_File_startW == '') or (str_File_startW.lower() == str_lowerFileName.lower()[:len(str_File_startW)]):
                    if (str_File_endW == '') or (str_File_endW.lower() == str_lowerFileName.lower()[-len(str_File_endW):]):
                        bl_download = True
                if bl_download:
                    l_docDownloaded.append(o_attach)
                    # DOWNLOAD
                    o_attach.SaveAsFile(os.path.join(str_folder, str(o_attach)))
        except Exception as err:
            print(' ERROR in outlk_DownloadEmailsPJ: Cannot dwld the mails')
            print(' - ', str(err))
            raise
        #o_mail.Unread = False
        if not l_docDownloaded:
            print(' EMPTY in outlk_DownloadEmailsPJ: download nothing from Mail')
            print(' - Outlook Folder: ', str_folder)
            print(' - Mail Subject: ', self.str_mailSubject)
            print(' - fileName: ', str_File_startW, str_File_endW)
        self.l_docDownloaded = l_docDownloaded
        return self.l_docDownloaded
    
    def outlk_ArchiveEmail(self):
        if self.o_latestMail is None:    self.outlk_GetLatestMail()
        try:        self.o_latestMail.Move(self.o_ArchiveFolder)
        except Exception as err:
            print(' ERROR in outlk_ArchiveEmail')
            print(' - ', str(err))
            raise
#____________________________________________________________________________    
    
    
    
#---------------------------------------------------------------
# ------ CONTINUITY: Function to launch Class ------------------
#---------------------------------------------------------------  
def fBl_SendMail_outlook(bl_draft = True, str_from = '', str_to='', str_cc='', str_bcc='', str_subject='', l_pathAttach=[], str_message=''):
    inst_outlookMail = c_outlookMail()
    inst_outlookMail.outlk_SendMails(str_to, str_cc, str_bcc, str_subject, l_pathAttach, str_message, str_from, bl_draft)

def fMail_getMails(str_outlkAcctName, str_outlkMailbox, str_folders, str_outFoldToArch):
    inst_outlookMail = c_outlookMail()
    #inst_outlookMail.outlk_DefineOutlook('MAPI')
    inst_outlookMail.outlk_getAccount(str_outlkAcctName)
    inst_outlookMail.outlk_DefineFolder(str_outlkMailbox, [str_folders])
    inst_outlookMail.outlk_GetMails()
    inst_outlookMail.outlk_DefineArchiveFolder([str_outFoldToArch])
    return inst_outlookMail.o_mails, inst_outlookMail.o_ArchiveFolder
 





###################################################################
#### Deprecated ###
###################################################################  

#____________________________________________________________________________
def fStr_removeFwRe_subMail (str_subMail):
    return ':'.join(str_subMail.split(':')[1:]).lstrip()




##____________________________________________________________________________
#def fBl_SendMail_outlook(bl_draft = True, str_from = '', str_to='', str_cc='', str_bcc='', str_subject='', l_pathAttach=[], str_message=''):
#    try:
#        a_outlook = win32.Dispatch('outlook.application')
#        o_mail = a_outlook.CreateItem(0)
#        o_mail.SentOnBehalfOfName = str_from
#        o_mail.To = str_to
#        o_mail.Cc = str_cc
#        o_mail.Bcc = str_bcc
#        o_mail.Subject = str_subject
#        o_mail.Body = str_message
#    except:
#        print("We cannot define the mail with win32.Dispatch('outlook.application')")
#        print('bl_draft: ' + bl_draft, 'str_from: ' + str_from , 'str_to: ' + str_to, 'str_cc: ' + str_cc, 
#              'str_bcc: ' + str_bcc, 'str_subject: ' + str_subject, 'l_pathAttach: ' + l_pathAttach,
#              'str_message: ' + str_message)
#        raise
#    try:
#        for attach in l_pathAttach:
#            o_mail.Attachments.Add(attach)
#    except:
#        print('We cannot attch file to the mail ' )
#        print('bl_draft: ' + bl_draft, 'str_from: ' + str_from , 'str_to: ' + str_to, 'str_cc: ' + str_cc, 
#              'str_bcc: ' + str_bcc, 'str_subject: ' + str_subject, 'l_pathAttach: ' + l_pathAttach,
#              'str_message: ' + str_message)
#        raise
#    try:
#        if bl_draft:
#            o_mail.Display(True)
#        else:
#            o_mail.Send()
#    except:
#        print('We cannot send / display the mail')
#        print('bl_draft: ' + bl_draft, 'str_from: ' + str_from , 'str_to: ' + str_to, 'str_cc: ' + str_cc, 
#              'str_bcc: ' + str_bcc, 'str_subject: ' + str_subject, 'l_pathAttach: ' + l_pathAttach,
#              'str_message: ' + str_message)
#        raise
#    return True
    


##____________________________________________________________________________
#def fObj_getOutlookAcct(o_outlook, str_outlookAcct):
#    try:
#        # Only action here (the rest is just error message)
#        o_outAcct = o_outlook.Session.Accounts(str_outlookAcct)    
#        # Case if its None
#        if o_outAcct == None:
#            # Special Process for MAJ
#            for account in o_outlook.Session.Accounts:
#                str_account = str(account)
#                if str_account.lower() == str_outlookAcct.lower():
#                    o_outAcct = fObj_getOutlookAcct(o_outlook, str_account)
#                    return o_outAcct
#            # Message of Empty
#            print('  o_outAcct == None: Python could not connect to the Mail Account : ', str_outlookAcct)
#            print('  - The available Mail Account are: ')
#            for account in o_outlook.Session.Accounts:
#                print('  - ' + str(account))
#            return False
#    # Case there is an error
#    except:
#        print(' ERROR: Python could not connect to the Mail Account : ', str_outlookAcct)
#        print(' - The available Mail Account are: ')
#        for account in o_outlook.Session.Accounts:
#            print(' - ' + str(account))
#        return False
#    return o_outAcct
    


##____________________________________________________________________________
#def fMail_getMails(str_outlookAcct, str_outlookMailbox, str_outlookFolderToLookFor, str_outFoldToArch):
#    # 1. Outlook Object + Account
#    try:    
#        o_outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
#        o_outAcct = fObj_getOutlookAcct(o_outlook, str_outlookAcct)
#        str_outAcctName = o_outAcct.DeliveryStore.DisplayName
#        if not o_outAcct: return False 
#    except: raise
#    # 2. Outlook Box + Folder + Mails
#    try:
#        if str_outlookFolderToLookFor == '':
#            o_outFolder = o_outlook.Folders(str_outAcctName).Folders[str_outlookMailbox]
#            o_folArchive = o_outlook.Folders(str_outAcctName).Folders[str_outlookMailbox].Folders[str_outFoldToArch]
#        else:            
#            o_outFolder = o_outlook.Folders(str_outAcctName).Folders[str_outlookMailbox].Folders[str_outlookFolderToLookFor]
#            o_folArchive = o_outlook.Folders(str_outAcctName).Folders[str_outlookMailbox].Folders[str_outlookFolderToLookFor].Folders[str_outFoldToArch]
#    except:
#        print(' ERROR : Python could not connect to the Mailbox in the Mail Account')
#        print(' - ',str_outlookAcct, str_outlookMailbox, str_outlookFolderToLookFor, str_outFoldToArch)
#        raise
#    # 3. Mails
#    o_mails = o_outFolder.Items
#    #o_mails.Sort("[ReceivedTime]", True)
#    return o_mails, o_folArchive
    



#____________________________________________________________________________
def fMail_GetMailWithAttach(o_mails, str_mailSubject = '',str_to = '', str_cc = '', str_attachNameExact = '', 
                             str_File_startW = '', str_File_endW = ''):
    print('  INFORMATION DEV: replace fMail_GetMailWithAttach by outlk_FilterMails / outlk_GetLatestMail')
    #inst_outlookMail.outlk_FilterMails(str_mailSubject, str_to, str_cc, str_File_startW, str_File_endW)
    #inst_outlookMail.outlk_GetLatestMail()
    
    try:
        o_subMail = o_mails
        # Filter on subject
        if not str_mailSubject == '':
            o_subMail = [o_mail for o_mail in o_subMail if str_mailSubject in o_mail.Subject]
            if o_subMail == []: print(' ... Empty with Subject')
        
        # Filter by To / Cc
        if not str_to == '':
            print(' Filter by str_to: ', str_to)
            if str_to == 'empty':   o_subMail = [o_mail for o_mail in o_subMail if o_mail.To == '']
            else:                   o_subMail = [o_mail for o_mail in o_subMail if str_to in o_mail.To]  
        if not str_cc == '':
            print(' Filter by str_cc: ', str_cc)
            if str_cc == 'empty':   o_subMail = [o_mail for o_mail in o_subMail if o_mail.Cc == '']
            else:                   o_subMail = [o_mail for o_mail in o_subMail if str_cc in o_mail.Cc] 
        if o_subMail == []: print(' ... Empty with To / CC')
        
        # Filter by name of attach if It is Exact
        if not str_attachNameExact == '':
            #print(' ** OUTLOOK: We forced to search the exact document attach name: ', str_attachNameExact)
            o_subMail = [o_mail for o_mail in o_subMail if str_attachNameExact.lower() in
                         [str(o_attach).lower() for o_attach in o_mail.Attachments]]
            if o_subMail == []: print(' ... Empty with attachNameExact')
        
        # Filter by name of attach if It is NOT Exact
        if not str_File_startW == '':
            o_subMail = [o_mail for o_mail in o_subMail if str_File_startW.lower() in 
                         [str(o_attach).lower()[:len(str_File_startW)] for o_attach in o_mail.Attachments]]
            if o_subMail == []: print(' ... Empty with str_File_startW')
            
        # Filter by name of attach if It is NOT Exact
        if not str_File_endW == '':
            o_subMail = [o_mail for o_mail in o_subMail if str_File_endW.lower() in 
                         [str(o_attach).lower()[-len(str_File_endW):] for o_attach in o_mail.Attachments]]
            if o_subMail == []: print(' ... Empty with str_File_endW')
            
        # Take the most recent one
        o_mail = o_subMail[np.argmax([o_mail.Senton for o_mail in o_subMail])]
        o_subMail = [o_mail]
        
        if o_subMail == []: raise    
    except:
        print('   ERROR: No Mails to download with the Subjects: ', str_mailSubject)
        print('   - str_to :', str_to, 'str_cc :', str_cc)
        print('   - str_attachNameExact: ', str_attachNameExact)
        print('   - str_File_startW: ', str_File_startW)
        print('   - str_File_endW: ', str_File_endW)
        return False
    return o_subMail
    


#____________________________________________________________________________
def fMail_getmail_mostRecent(o_mails, l_Sub_stringToLookFor = [], str_to = '', str_cc = '', str_attachName = ''):
    print('  INFORMATION DEV: replace fMail_getmail_mostRecent by outlk_FilterMa / outlk_GetLatestMail')
    #inst_outlookMail.outlk_FilterMails(str_mailSubject, str_to, str_cc, str_File_startW, str_File_endW)
    #inst_outlookMail.outlk_GetLatestMail()
    
    l_mail = []
    for str_mailSub in l_Sub_stringToLookFor:
        try:
            # Filter on subject
            o_subMail = [o_mail for o_mail in o_mails if str_mailSub in o_mail.Subject]
            # Filter by To / Cc
            if not str_to == '':
                print(' Filter by str_to: ', str_to)
                if str_to == 'empty':   o_subMail = [o_mail for o_mail in o_subMail if o_mail.To == '']
                else:                   o_subMail = [o_mail for o_mail in o_subMail if str_to in o_mail.To]  
            if not str_cc == '':
                print(' Filter by str_cc: ', str_cc)
                if str_cc == 'empty':   o_subMail = [o_mail for o_mail in o_subMail if o_mail.Cc == '']
                else:                   o_subMail = [o_mail for o_mail in o_subMail if str_cc in o_mail.Cc] 
            # Filter by name of attach
            if str_attachName != '':
                #print(' ** OUTLOOK: We forced to search the exact document attach name: ', str_attachName)
                o_subMail = [o_mail for o_mail in o_subMail if str_attachName.lower() in 
                             [str(o_attach).lower() for o_attach in o_mail.Attachments]]
            # Sort for more recent
            o_mail = o_subMail[np.argmax([o_mail.Senton for o_mail in o_subMail])]
            l_mail.append(o_mail)
        except:
            print('  ERROR: No Mails to download with the Subjects: ', str_mailSub)
            print('  - l_Sub_stringToLookFor: ', l_Sub_stringToLookFor)
            print('  - str_attachName: ', str_attachName)
            print('  - str_to :', str_to, 'str_cc :', str_cc)
            return False
    if l_mail == []: 
        print(' EMPTY l_mail: No Mails to download in the Folder with the Subjects you define') 
        print(' - l_Sub_stringToLookFor', l_Sub_stringToLookFor)
        print([o_mail.Subject for o_mail in o_mails])
    return l_mail
    


#____________________________________________________________________________
def fBl_downMailAttch (str_folderRaw, l_mail, l_outlookAttach_fileType = []):
    print('  INFORMATION DEV: replace fBl_downMailAttch by  outlk_DownloadEmailsPJ')
    #inst_outlookMail.outlk_DownloadEmailsPJ(str_folderRaw, '', str_Attach_End[0])
    
    l_attach=[]
    try:
        for o_mail in l_mail:
            for o_attach in o_mail.Attachments:
                bl_download = False
                if l_outlookAttach_fileType == []:
                    bl_download = True
                else:
                    for str_fileType in l_outlookAttach_fileType:
                        if str_fileType.lower() in str(o_attach).lower():
                            bl_download = True
                if bl_download:
                    l_attach.append(o_attach)
                    o_attach.SaveAsFile(os.path.join(str_folderRaw, str(o_attach)))
            o_mail.Unread = False
    except:
        print(' ERROR: We were not able to DWL the Attachement from the mail !')
        print(' - Number Mail : ', len(l_mail))
        print(' - list Mail : ', set([o_mail.subject for o_mail in l_mail]))
        print(' - list File Type to look for  : ', l_outlookAttach_fileType)
        print(' - Folder: ', str_folderRaw)
        raise
    return l_attach

#____________________________________________________________________________
def fBl_downMailAttch2 (str_folderRaw, l_mail, str_Attach_Debut = '', str_Attach_End = ''):
    print('  INFORMATION DEV: replace by outlk_DownloadEmailsPJ')
    #inst_outlookMail.outlk_DownloadEmailsPJ(str_folderRaw, str_Attach_Debut, str_Attach_End)
     
    l_attach=[]
    str_realAttachName= ''
    try:
        for o_mail in l_mail:
            for o_attach in o_mail.Attachments:
                str_realAttachName = str(o_attach).lower()
                bl_download = False
                if (str_Attach_Debut == '') or (str_Attach_Debut.lower() == str_realAttachName.lower()[:len(str_Attach_Debut)]):
                    if (str_Attach_End == '') or (str_Attach_End.lower() == str_realAttachName.lower()[-len(str_Attach_End):]):
                        bl_download = True
                if bl_download:
                    l_attach.append(o_attach)
                    o_attach.SaveAsFile(os.path.join(str_folderRaw, str(o_attach)))
            o_mail.Unread = False
    except:
        print(' ERROR: We were not able to download the Attachement from the mail !')
        print(' - Number Mail : ', len(l_mail))
        print(' - list Mail Subject : ', set([o_mail.subject for o_mail in l_mail]))
        print(' - Attach file we look for || START  : ', str_Attach_Debut, '  || END : ', str_Attach_End)
        print(' - str_realAttachName  : ', str_realAttachName)
        print(' - Folder: ', str_folderRaw)
        raise
    return l_attach


#____________________________________________________________________________
def fBl_archiveMail (o_mails, o_folderToMove):
    print('  INFORMATION DEV: replace by outlk_ArchiveEmail')
    #inst_outlookMail.outlk_ArchiveEmail()
    
    o_mails.Sort("[ReceivedTime]", True)
    try:
        for o_mail in o_mails:
            o_mail.Move(o_folderToMove)
    except:
        print(' ERROR: We were not able to archive the mail !')
        print(' - ', o_mail.subject, o_mail.Senton, o_folderToMove)
        raise
    return True

