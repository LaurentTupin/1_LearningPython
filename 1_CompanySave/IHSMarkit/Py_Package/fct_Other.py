try:
    import sys
except Exception as err:
    str_lib = str(err).replace("No module named ", "").replace("'", "")
    print(" ATTENTION,  Missing library: '{0}' \n * Please Open Anaconda prompt and type: 'pip install {0}'".format(str_lib))



#-----------------------------------------------------------------
# String
#-----------------------------------------------------------------
def fStr_RemoveDicoBracket(str_in):
    # Remove the 1st and last Char if its {}
    try:
        if str_in[0] == '{':    str_in = str_in[1:]
        if str_in[-1] == '}':   str_in = str_in[:-1]
    except Exception as err:
        print(' ERROR fStr_RemoveDicoBracket ||| '.format(err))
        print(' - str_in: {}'.format(str_in))
    return str_in

def fStr_CleanStringFromSymbol(str_in):
    str_in = str_in.replace("'", "").replace(" ", "")
    str_in = str_in.replace("[", "").replace("]", "")
    str_in = str_in.replace("{", "").replace("}", "")
    str_in = str_in.replace("\n", "")
    return str_in


#-----------------------------------------------------------------
# Dictionary
#-----------------------------------------------------------------
def fDic_GetDicFromString(str_in, str_valueType = 'list'):
    d_dico = eval(str_in)
    #    d_dico = {}
    #    d_dicoWithin = {}
    #    try:
    #        str_in = fStr_RemoveDicoBracket(str_in)
    #        if str_in == '':        return {}
    #        # Change into list (  , is actually set as ||  )
    #        l_coupleDico = str_in.split('||')
    #        # Fill the dictionary
    #        for str_couple in l_coupleDico:
    #            # KEY
    #            str_key = str_couple.split(':')[0]
    #            str_key = fStr_CleanStringFromSymbol(str_key)
    #            # Value
    #            if str_valueType == 'list':
    #                str_value = str_couple.split(':')[1]
    #                d_dico[str_key] = list(str_value.split(','))
    #            else:
    #                str_value = ':'.join(str_couple.split(':')[1:])
    #                str_value = fStr_RemoveDicoBracket(str_value)
    #                l_coupleDicoWithin = str_value.split(',')
    #                for str_coupleWithin in l_coupleDicoWithin:
    #                    str_coupleWithin = fStr_CleanStringFromSymbol(str_coupleWithin)
    #                    str_keyWithin = str_coupleWithin.split(':')[0]
    #                    str_valueWithin = str_coupleWithin.split(':')[1]
    #                    d_dicoWithin[str_keyWithin] = str_valueWithin
    #                d_dico[str_key] = d_dicoWithin
    #    except Exception as err:
    #        print(' ERROR fDic_GetDicFromString ||| '.format(err))
    #        print(' - str_in: {}'.format(str_in))
    #        print(' - l_coupleDico: {}'.format(l_coupleDico))
    #        print(' - d_dico: {}'.format(d_dico))
    #        return {}
    return d_dico



    