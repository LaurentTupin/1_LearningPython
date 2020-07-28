import sys
sys.path.append('../')
import fct_Files as fl


def fstr_BackUp(dte_date, str_folderOrigin, str_folderTarget, dte_after):
    str_message = fl.fStr_CopPasteFolder(dte_date, str_folderOrigin, str_folderTarget, dte_after)
    return str_message





