import os
import numpy as np
import win32com.client as win32


#____________________________________________________________________________
def fBl_SendMail_outlook(bl_draft = True, str_from = '', str_to='', str_cc='', str_bcc='', str_subject='', l_pathAttach=[], str_message=''):
    try:
        a_outlook = win32.Dispatch('outlook.application')
        o_mail = a_outlook.CreateItem(0)
        o_mail.SentOnBehalfOfName = str_from
        o_mail.To = str_to
        o_mail.Cc = str_cc
        o_mail.Bcc = str_bcc
        o_mail.Subject = str_subject
        o_mail.Body = str_message
        #o_mail.HTMLBody = '<h2>HTML Message body</h2>' 
    except:
        print("We cannot define the mail with win32.Dispatch('outlook.application')")
        print('bl_draft: ' + bl_draft, 'str_from: ' + str_from , 'str_to: ' + str_to, 'str_cc: ' + str_cc, 
              'str_bcc: ' + str_bcc, 'str_subject: ' + str_subject, 'l_pathAttach: ' + l_pathAttach,
              'str_message: ' + str_message)
        raise
    try:
        for attach in l_pathAttach:
            o_mail.Attachments.Add(attach)
    except:
        print('We cannot attch file to the mail ' )
        print('bl_draft: ' + bl_draft, 'str_from: ' + str_from , 'str_to: ' + str_to, 'str_cc: ' + str_cc, 
              'str_bcc: ' + str_bcc, 'str_subject: ' + str_subject, 'l_pathAttach: ' + l_pathAttach,
              'str_message: ' + str_message)
        raise
    try:
        if bl_draft:
            o_mail.Display(True)
        else:
            o_mail.Send()
    except:
        print('We cannot send / display the mail')
        print('bl_draft: ' + bl_draft, 'str_from: ' + str_from , 'str_to: ' + str_to, 'str_cc: ' + str_cc, 
              'str_bcc: ' + str_bcc, 'str_subject: ' + str_subject, 'l_pathAttach: ' + l_pathAttach,
              'str_message: ' + str_message)
        raise
    return True

#____________________________________________________________________________
def fStr_removeFwRe_subMail (str_subMail):
    return ':'.join(str_subMail.split(':')[1:]).lstrip()



#____________________________________________________________________________
def fObj_getOutlookAcct(o_outlook, str_outlookAcct):
    try:
        # Only action here (the rest is just error message)
        o_outAcct = o_outlook.Session.Accounts(str_outlookAcct)    
        # Case if its None
        if o_outAcct == None:
            # Special Process for MAJ
            for account in o_outlook.Session.Accounts:
                str_account = str(account)
                if str_account.lower() == str_outlookAcct.lower():
                    o_outAcct = fObj_getOutlookAcct(o_outlook, str_account)
                    return o_outAcct
            # Message of Empty
            print('  o_outAcct == None: Python could not connect to the Mail Account : ', str_outlookAcct)
            print('  - The available Mail Account are: ')
            for account in o_outlook.Session.Accounts:
                print('  - ' + str(account))
            return False
    # Case there is an error
    except:
        print(' ERROR: Python could not connect to the Mail Account : ', str_outlookAcct)
        print(' - The available Mail Account are: ')
        for account in o_outlook.Session.Accounts:
            print(' - ' + str(account))
        return False
    return o_outAcct


#____________________________________________________________________________
def fMail_getMails(str_outlookAcct, str_outlookMailbox, str_outlookFolderToLookFor, str_outFoldToArch):
    # 1. Outlook Object + Account
    try:    
        o_outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
        o_outAcct = fObj_getOutlookAcct(o_outlook, str_outlookAcct)
        str_outAcctName = o_outAcct.DeliveryStore.DisplayName
        if not o_outAcct: return False 
    except: raise
    # 2. Outlook Box + Folder + Mails
    try:
        if str_outlookFolderToLookFor == '':
            o_outFolder = o_outlook.Folders(str_outAcctName).Folders[str_outlookMailbox]
            o_folArchive = o_outlook.Folders(str_outAcctName).Folders[str_outlookMailbox].Folders[str_outFoldToArch]
        else:            
            o_outFolder = o_outlook.Folders(str_outAcctName).Folders[str_outlookMailbox].Folders[str_outlookFolderToLookFor]
            o_folArchive = o_outlook.Folders(str_outAcctName).Folders[str_outlookMailbox].Folders[str_outlookFolderToLookFor].Folders[str_outFoldToArch]
    except:
        print(' ERROR : Python could not connect to the Mailbox in the Mail Account')
        print(' - ',str_outlookAcct, str_outlookMailbox, str_outlookFolderToLookFor, str_outFoldToArch)
        raise
    # 3. Mails
    o_mails = o_outFolder.Items
    #o_mails.Sort("[ReceivedTime]", True)
    return o_mails, o_folArchive
    

#____________________________________________________________________________
def fMail_GetMailWithAttach(o_mails, str_mailSubject = '',str_to = '', str_cc = '', str_attachNameExact = '', 
                             str_attachNameDebut = '', str_attachNameFin = ''):
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
        if not str_attachNameDebut == '':
            o_subMail = [o_mail for o_mail in o_subMail if str_attachNameDebut.lower() in 
                         [str(o_attach).lower()[:len(str_attachNameDebut)] for o_attach in o_mail.Attachments]]
            if o_subMail == []: print(' ... Empty with str_attachNameDebut')
            
        # Filter by name of attach if It is NOT Exact
        if not str_attachNameFin == '':
            o_subMail = [o_mail for o_mail in o_subMail if str_attachNameFin.lower() in 
                         [str(o_attach).lower()[-len(str_attachNameFin):] for o_attach in o_mail.Attachments]]
            if o_subMail == []: print(' ... Empty with str_attachNameFin')
            
        # Take the most recent one
        o_mail = o_subMail[np.argmax([o_mail.Senton for o_mail in o_subMail])]
        o_subMail = [o_mail]
        
        if o_subMail == []: raise    
    except:
        print('   ERROR: No Mails to download with the Subjects: ', str_mailSubject)
        print('   - str_to :', str_to, 'str_cc :', str_cc)
        print('   - str_attachNameExact: ', str_attachNameExact)
        print('   - str_attachNameDebut: ', str_attachNameDebut)
        print('   - str_attachNameFin: ', str_attachNameFin)
        return False
    return o_subMail


#____________________________________________________________________________
def fMail_getmail_mostRecent(o_mails, l_Sub_stringToLookFor = [], str_to = '', str_cc = '', str_attachName = ''):
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
    o_mails.Sort("[ReceivedTime]", True)
    try:
        for o_mail in o_mails:
            o_mail.Move(o_folderToMove)
    except:
        print(' ERROR: We were not able to archive the mail !')
        print(' - ', o_mail.subject, o_mail.Senton, o_folderToMove)
        raise
    return True



